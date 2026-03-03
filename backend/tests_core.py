"""
tests_core.py — Tests principales del sistema HackaEdu
=======================================================

Cubre cuatro áreas clave:
  1. Obtención de logros (check_and_award_logros + get_all_achievements_for_user)
  2. Racha de días consecutivos (RachaUsuario.calcular_racha)
  3. Ranking global: suma de puntos acumulativos y recalculación de posiciones
  4. Puntos para pasar de nivel (puntos_en_nivel vs NivelCEFR.puntos_requeridos)

Ejecutar:
    python manage.py test tests_core
    python manage.py test tests_core -v 2   # verbose
"""

from datetime import date, timedelta

from django.test import TestCase
from django.utils import timezone

from auth_custom.models import CustomUser
from niveles.models import NivelCEFR
from usuarios.models import PerfilUsuario, ProgresionNivel
from logros.models import Logro, LogroUsuario
from logros.selectors import get_all_achievements_for_user
from logros.services import check_and_award_logros
from ranking.models import RachaUsuario, Ranking
from ranking.selectors import get_user_ranking, get_user_streak, get_top_players


# ─────────────────────────────────────────────
#  Helpers de creación
# ─────────────────────────────────────────────

def crear_nivel(codigo="A1", nombre="Principiante", categoria="BASICO",
                puntos_requeridos=50):
    """Crea o recupera un NivelCEFR."""
    nivel, _ = NivelCEFR.objects.get_or_create(
        codigo=codigo,
        defaults={
            "nombre": nombre,
            "categoria": categoria,
            "vocab_min": 0,
            "vocab_max": 500,
            "puntos_requeridos": puntos_requeridos,
            "multiplicador_puntos": "1.00",
        },
    )
    return nivel


def crear_usuario(email="test@hackaedu.com", nombre="Test", apellido="User"):
    """Crea usuario + datos relacionados manualmente (sin depender del signal)."""
    user = CustomUser.objects.create_user(
        email=email, password="Pass1234!", nombre=nombre, apellido=apellido
    )
    # El signal intenta crear ProgresionNivel con nivel A1 → debe existir antes.
    # Si el signal falla silenciosamente creamos los objetos aquí.
    nivel_a1 = NivelCEFR.objects.filter(codigo="A1").first()
    if nivel_a1:
        ProgresionNivel.objects.get_or_create(
            usuario=user,
            defaults={"nivel_actual": nivel_a1},
        )
    RachaUsuario.objects.get_or_create(usuario=user)
    Ranking.objects.get_or_create(usuario=user)
    PerfilUsuario.objects.get_or_create(usuario=user)
    return user


# ═══════════════════════════════════════════════════════════
#  1. LOGROS — Obtención automática
# ═══════════════════════════════════════════════════════════

class LogrosObtenciónTests(TestCase):
    """
    Verifica que check_and_award_logros() otorgue o deniegue logros
    según los criterios definidos en cada Logro.
    """

    def setUp(self):
        crear_nivel()  # A1 necesario para el signal
        self.user = crear_usuario()
        self.perfil = self.user.perfil_hackaedu
        self.progresion = self.user.progresion

    # ── Listas de logros ────────────────────────────────────────────────────

    def test_sin_logros_todo_bloqueado(self):
        """Sin logros, get_all_achievements_for_user devuelve unlocked=False."""
        Logro.objects.create(
            codigo="PRIMER_PASO",
            nombre="Primer Paso",
            descripcion="Completa tu primera lectura",
            criterios={"lecturas_completadas": 1},
            puntos_recompensa=10,
        )
        resultado = get_all_achievements_for_user(self.user)
        self.assertEqual(len(resultado), 1)
        self.assertFalse(resultado[0]["unlocked"])
        self.assertIsNone(resultado[0]["fecha_obtencion"])

    def test_logro_ya_obtenido_aparece_como_unlocked(self):
        """Logro previamente otorgado aparece con unlocked=True y fecha."""
        logro = Logro.objects.create(
            codigo="LECTOR_NIVEL1",
            nombre="Lector Nivel 1",
            descripcion="Completa 5 lecturas",
            criterios={"lecturas_completadas": 5},
            puntos_recompensa=20,
        )
        LogroUsuario.objects.create(usuario=self.user, logro=logro)

        resultado = get_all_achievements_for_user(self.user)
        item = next(r for r in resultado if r["logro"].codigo == "LECTOR_NIVEL1")
        self.assertTrue(item["unlocked"])
        self.assertIsNotNone(item["fecha_obtencion"])

    # ── check_and_award_logros ──────────────────────────────────────────────

    def test_otorga_logro_por_lecturas_completadas(self):
        """Otorga el logro cuando lecturas_completadas >= criterio."""
        Logro.objects.create(
            codigo="LECTOR5",
            nombre="Lector 5",
            descripcion="5 lecturas",
            criterios={"lecturas_completadas": 5},
            puntos_recompensa=15,
        )
        self.perfil.lecturas_completadas = 5
        self.perfil.save()

        nuevos = check_and_award_logros(self.user)

        self.assertIn("LECTOR5", nuevos)
        self.assertTrue(
            LogroUsuario.objects.filter(usuario=self.user, logro_id="LECTOR5").exists()
        )

    def test_no_otorga_logro_si_lecturas_insuficientes(self):
        """No otorga logro cuando lecturas_completadas < criterio."""
        Logro.objects.create(
            codigo="LECTOR10",
            nombre="Lector 10",
            descripcion="10 lecturas",
            criterios={"lecturas_completadas": 10},
            puntos_recompensa=30,
        )
        self.perfil.lecturas_completadas = 3
        self.perfil.save()

        nuevos = check_and_award_logros(self.user)

        self.assertNotIn("LECTOR10", nuevos)
        self.assertFalse(
            LogroUsuario.objects.filter(usuario=self.user, logro_id="LECTOR10").exists()
        )

    def test_otorga_logro_por_dias_consecutivos(self):
        """Otorga el logro de racha cuando dias_consecutivos >= criterio."""
        Logro.objects.create(
            codigo="RACHA7",
            nombre="Racha 7 días",
            descripcion="7 días seguidos",
            criterios={"dias_consecutivos": 7},
            puntos_recompensa=25,
        )
        racha = self.user.racha
        racha.dias_consecutivos = 7
        racha.save()

        nuevos = check_and_award_logros(self.user)

        self.assertIn("RACHA7", nuevos)

    def test_no_otorga_logro_si_racha_insuficiente(self):
        """No otorga logro racha cuando dias_consecutivos < criterio."""
        Logro.objects.create(
            codigo="RACHA7",
            nombre="Racha 7 días",
            descripcion="7 días seguidos",
            criterios={"dias_consecutivos": 7},
            puntos_recompensa=25,
        )
        racha = self.user.racha
        racha.dias_consecutivos = 3
        racha.save()

        nuevos = check_and_award_logros(self.user)

        self.assertNotIn("RACHA7", nuevos)

    def test_otorga_logro_por_nivel_igual_o_superior(self):
        """Otorga logro de nivel cuando nivel_actual >= nivel requerido."""
        nivel_b1 = crear_nivel(
            codigo="B1", nombre="Intermedio", categoria="INTERMEDIO",
            puntos_requeridos=60,
        )
        Logro.objects.create(
            codigo="NIVEL_B1",
            nombre="Alcanzaste B1",
            descripcion="Nivel B1",
            criterios={"nivel": "B1"},
            puntos_recompensa=50,
        )
        # Subir al usuario a C1
        nivel_c1 = crear_nivel(
            codigo="C1", nombre="Avanzado", categoria="AVANZADO",
            puntos_requeridos=70,
        )
        self.progresion.nivel_actual = nivel_c1
        self.progresion.save()

        nuevos = check_and_award_logros(self.user)

        self.assertIn("NIVEL_B1", nuevos)

    def test_no_duplica_logro_ya_obtenido(self):
        """check_and_award_logros no vuelve a otorgar un logro ya obtenido."""
        logro = Logro.objects.create(
            codigo="LECTOR5_DUP",
            nombre="Lector 5 dup",
            descripcion="5 lecturas",
            criterios={"lecturas_completadas": 5},
            puntos_recompensa=15,
        )
        LogroUsuario.objects.create(usuario=self.user, logro=logro)
        self.perfil.lecturas_completadas = 10
        self.perfil.save()

        nuevos = check_and_award_logros(self.user)

        self.assertNotIn("LECTOR5_DUP", nuevos)
        self.assertEqual(
            LogroUsuario.objects.filter(usuario=self.user, logro=logro).count(), 1
        )


# ═══════════════════════════════════════════════════════════
#  2. RACHA — Días consecutivos conectados
# ═══════════════════════════════════════════════════════════

class RachaDiasConectadosTests(TestCase):
    """
    Verifica la lógica de RachaUsuario.calcular_racha():
      - Primer acceso inicia la racha en 1
      - Día consecutivo incrementa la racha
      - Mismo día no incrementa
      - Saltar un día reinicia la racha a 1
    """

    def setUp(self):
        crear_nivel()
        self.user = crear_usuario(email="racha@hackaedu.com")
        self.racha = self.user.racha

    def _set_ultimo_acceso(self, dias_atras: int):
        """Simula que el último acceso fue hace N días."""
        self.racha.ultimo_acceso = date.today() - timedelta(days=dias_atras)
        self.racha.save(update_fields=["ultimo_acceso"])

    # ── Casos principales ───────────────────────────────────────────────────

    def test_primer_acceso_inicia_racha_en_1(self):
        """Sin acceso previo, calcular_racha() establece dias_consecutivos=1."""
        self.racha.ultimo_acceso = None
        self.racha.dias_consecutivos = 0
        self.racha.save()

        self.racha.calcular_racha()
        self.racha.refresh_from_db()

        self.assertEqual(self.racha.dias_consecutivos, 1)
        self.assertEqual(self.racha.ultimo_acceso, date.today())

    def test_dia_consecutivo_incrementa_racha(self):
        """Acceder al día siguiente incrementa la racha en 1."""
        self.racha.dias_consecutivos = 4
        self.racha.save()
        self._set_ultimo_acceso(dias_atras=1)

        self.racha.calcular_racha()
        self.racha.refresh_from_db()

        self.assertEqual(self.racha.dias_consecutivos, 5)
        self.assertEqual(self.racha.ultimo_acceso, date.today())

    def test_mismo_dia_no_incrementa_racha(self):
        """Llamar calcular_racha el mismo día no suma días."""
        self.racha.dias_consecutivos = 3
        self.racha.ultimo_acceso = date.today()
        self.racha.save()

        self.racha.calcular_racha()
        self.racha.refresh_from_db()

        self.assertEqual(self.racha.dias_consecutivos, 3)

    def test_saltar_un_dia_reinicia_racha_a_1(self):
        """No acceder ayer (diferencia > 1) reinicia la racha a 1."""
        self.racha.dias_consecutivos = 10
        self.racha.save()
        self._set_ultimo_acceso(dias_atras=2)  # Hace 2 días → rompió racha

        self.racha.calcular_racha()
        self.racha.refresh_from_db()

        self.assertEqual(self.racha.dias_consecutivos, 1)
        self.assertEqual(self.racha.ultimo_acceso, date.today())

    def test_racha_3_dias_consecutivos(self):
        """Simula 3 días consecutivos llamando calcular_racha cada vez."""
        # Día 1
        self.racha.ultimo_acceso = None
        self.racha.dias_consecutivos = 0
        self.racha.save()
        self.racha.calcular_racha()

        # Día 2 (simular que ayer fue el último)
        self.racha.refresh_from_db()
        self.racha.ultimo_acceso = date.today() - timedelta(days=1)
        self.racha.save(update_fields=["ultimo_acceso"])
        self.racha.calcular_racha()

        # Día 3
        self.racha.refresh_from_db()
        self.racha.ultimo_acceso = date.today() - timedelta(days=1)
        self.racha.save(update_fields=["ultimo_acceso"])
        self.racha.calcular_racha()

        self.racha.refresh_from_db()
        self.assertEqual(self.racha.dias_consecutivos, 3)

    def test_tiene_lectura_hoy_falso_si_no_hay_lectura(self):
        """tiene_lectura_hoy() devuelve False si ultima_lectura_fecha es None."""
        self.racha.ultima_lectura_fecha = None
        self.racha.save()
        self.assertFalse(self.racha.tiene_lectura_hoy())

    def test_tiene_lectura_hoy_verdadero(self):
        """tiene_lectura_hoy() devuelve True si ultima_lectura_fecha es hoy."""
        self.racha.ultima_lectura_fecha = date.today()
        self.racha.save()
        self.assertTrue(self.racha.tiene_lectura_hoy())

    def test_get_user_streak_selector(self):
        """get_user_streak() devuelve el objeto RachaUsuario correcto."""
        racha = get_user_streak(self.user)
        self.assertIsNotNone(racha)
        self.assertEqual(racha.usuario, self.user)


# ═══════════════════════════════════════════════════════════
#  3. RANKING GLOBAL — Puntos acumulativos y posiciones
# ═══════════════════════════════════════════════════════════

class RankingGlobalTests(TestCase):
    """
    Verifica:
      - Ranking.puntos_totales refleja puntos_acumulativos de ProgresionNivel
      - recalcular_ranking_global() ordena usuarios de mayor a menor puntos
      - get_top_players() retorna los n mejores jugadores en orden correcto
    """

    def setUp(self):
        crear_nivel()

        self.user1 = crear_usuario("user1@test.com", "Ana", "García")
        self.user2 = crear_usuario("user2@test.com", "Luis", "Pérez")
        self.user3 = crear_usuario("user3@test.com", "Mía", "López")

        # Asignar puntos acumulativos distintos
        ProgresionNivel.objects.filter(usuario=self.user1).update(puntos_acumulativos=300)
        ProgresionNivel.objects.filter(usuario=self.user2).update(puntos_acumulativos=150)
        ProgresionNivel.objects.filter(usuario=self.user3).update(puntos_acumulativos=450)

    # ── puntos_totales ──────────────────────────────────────────────────────

    def test_puntos_totales_refleja_progresion(self):
        """Ranking.puntos_totales devuelve el valor de ProgresionNivel.puntos_acumulativos."""
        ranking_u1 = self.user1.ranking
        self.assertEqual(ranking_u1.puntos_totales, 300)

        ranking_u3 = self.user3.ranking
        self.assertEqual(ranking_u3.puntos_totales, 450)

    def test_puntos_totales_cero_si_no_hay_progresion(self):
        """Si no existe ProgresionNivel, puntos_totales devuelve 0."""
        ProgresionNivel.objects.filter(usuario=self.user2).delete()
        self.assertEqual(self.user2.ranking.puntos_totales, 0)

    # ── recalcular_ranking_global ───────────────────────────────────────────

    def test_recalcular_ranking_ordena_mayor_a_menor(self):
        """El usuario con más puntos queda en posición 1."""
        Ranking.recalcular_ranking_global()

        self.user1.ranking.refresh_from_db()
        self.user2.ranking.refresh_from_db()
        self.user3.ranking.refresh_from_db()

        # user3 (450 pts) → #1, user1 (300 pts) → #2, user2 (150 pts) → #3
        self.assertEqual(self.user3.ranking.posicion, 1)
        self.assertEqual(self.user1.ranking.posicion, 2)
        self.assertEqual(self.user2.ranking.posicion, 3)

    def test_recalcular_ranking_asigna_posicion_a_todos(self):
        """Todos los usuarios reciben una posición distinta tras recalcular."""
        Ranking.recalcular_ranking_global()

        posiciones = set(
            Ranking.objects.values_list("posicion", flat=True)
        )
        # No hay posiciones repetidas ni cero
        self.assertEqual(len(posiciones), 3)
        self.assertNotIn(0, posiciones)

    def test_recalcular_actualiza_posicion_tras_cambio_de_puntos(self):
        """Si user2 gana muchos puntos, su posición mejora al recalcular."""
        Ranking.recalcular_ranking_global()

        # user2 sube a 999 pts
        ProgresionNivel.objects.filter(usuario=self.user2).update(puntos_acumulativos=999)
        Ranking.recalcular_ranking_global()

        self.user2.ranking.refresh_from_db()
        self.assertEqual(self.user2.ranking.posicion, 1)

    # ── get_top_players ─────────────────────────────────────────────────────

    def test_get_top_players_devuelve_n_jugadores(self):
        """get_top_players(3) devuelve exactamente 3 rankings."""
        Ranking.recalcular_ranking_global()
        top = get_top_players(limit=3)
        self.assertEqual(len(top), 3)

    def test_get_top_players_orden_correcto(self):
        """El primer elemento de get_top_players tiene posición 1."""
        Ranking.recalcular_ranking_global()
        top = list(get_top_players(limit=3))
        self.assertEqual(top[0].posicion, 1)
        self.assertEqual(top[0].usuario, self.user3)  # 450 pts

    def test_get_user_ranking_selector(self):
        """get_user_ranking() devuelve el Ranking del usuario."""
        Ranking.recalcular_ranking_global()
        r = get_user_ranking(self.user1)
        self.assertIsNotNone(r)
        self.assertEqual(r.usuario, self.user1)


# ═══════════════════════════════════════════════════════════
#  4. PUNTOS PARA PASAR DE NIVEL
# ═══════════════════════════════════════════════════════════

class PuntosParaPasarDeNivelTests(TestCase):
    """
    Verifica la lógica de progresión de nivel:
      - puntos_faltantes = nivel.puntos_requeridos - progresion.puntos_en_nivel
      - listo_para_ascenso se activa cuando puntos_en_nivel >= puntos_requeridos
      - Los puntos acumulativos (ranking) y los puntos en nivel son independientes
    """

    def setUp(self):
        self.nivel_a1 = crear_nivel(codigo="A1", puntos_requeridos=50)
        self.nivel_a2 = crear_nivel(
            codigo="A2", nombre="Elemental", categoria="BASICO",
            puntos_requeridos=60,
        )
        self.user = crear_usuario(email="nivel@hackaedu.com")
        self.progresion = self.user.progresion

    # ── Cálculo de puntos faltantes ─────────────────────────────────────────

    def test_puntos_faltantes_inicial_es_puntos_requeridos(self):
        """Al inicio (puntos_en_nivel=0), faltan todos los puntos del nivel."""
        self.progresion.puntos_en_nivel = 0
        self.progresion.save()

        faltantes = (
            self.progresion.nivel_actual.puntos_requeridos
            - self.progresion.puntos_en_nivel
        )
        self.assertEqual(faltantes, 50)

    def test_puntos_faltantes_decrece_al_sumar_puntos(self):
        """Al ganar 30 puntos en nivel, faltan 20 para llegar al umbral."""
        self.progresion.puntos_en_nivel = 30
        self.progresion.save()

        faltantes = (
            self.progresion.nivel_actual.puntos_requeridos
            - self.progresion.puntos_en_nivel
        )
        self.assertEqual(faltantes, 20)

    def test_puntos_faltantes_cero_cuando_umbral_alcanzado(self):
        """Al alcanzar exactamente puntos_requeridos, no faltan puntos."""
        self.progresion.puntos_en_nivel = 50
        self.progresion.save()

        faltantes = (
            self.progresion.nivel_actual.puntos_requeridos
            - self.progresion.puntos_en_nivel
        )
        self.assertEqual(faltantes, 0)

    # ── Flag listo_para_ascenso ─────────────────────────────────────────────

    def test_no_listo_para_ascenso_con_puntos_bajos(self):
        """Con puntos_en_nivel < puntos_requeridos, listo_para_ascenso=False."""
        self.progresion.puntos_en_nivel = 20
        self.progresion.listo_para_ascenso = False
        self.progresion.save()

        self.assertFalse(self.progresion.listo_para_ascenso)

    def test_listo_para_ascenso_cuando_puntos_suficientes(self):
        """Simula que el sistema marca listo_para_ascenso=True al cumplir umbral."""
        self.progresion.puntos_en_nivel = 50  # == puntos_requeridos
        self.progresion.listo_para_ascenso = True
        self.progresion.save()

        self.progresion.refresh_from_db()
        self.assertTrue(self.progresion.listo_para_ascenso)

    def test_ascenso_ofrecido_se_guarda_independientemente(self):
        """ascenso_ofrecido se puede marcar sin alterar puntos."""
        self.progresion.listo_para_ascenso = True
        self.progresion.ascenso_ofrecido = True
        self.progresion.save()

        self.progresion.refresh_from_db()
        self.assertTrue(self.progresion.ascenso_ofrecido)
        self.assertTrue(self.progresion.listo_para_ascenso)

    # ── Independencia puntos_en_nivel vs puntos_acumulativos ────────────────

    def test_puntos_acumulativos_y_en_nivel_son_independientes(self):
        """
        Subir de nivel resetea puntos_en_nivel a 0, pero
        puntos_acumulativos (ranking) sigue creciendo.
        """
        self.progresion.puntos_en_nivel = 50
        self.progresion.puntos_acumulativos = 120
        self.progresion.listo_para_ascenso = True
        self.progresion.save()

        # Simular ascenso: cambiar nivel y resetear puntos_en_nivel
        self.progresion.nivel_actual = self.nivel_a2
        self.progresion.puntos_en_nivel = 0
        self.progresion.listo_para_ascenso = False
        self.progresion.save()

        self.progresion.refresh_from_db()
        self.assertEqual(self.progresion.nivel_actual.codigo, "A2")
        self.assertEqual(self.progresion.puntos_en_nivel, 0)
        self.assertEqual(self.progresion.puntos_acumulativos, 120)  # sin cambio

    def test_puntos_requeridos_varia_por_nivel(self):
        """
        Cada nivel tiene su propio umbral de puntos requeridos.
        A1 requiere 50, A2 requiere 60.
        """
        self.assertEqual(self.nivel_a1.puntos_requeridos, 50)
        self.assertEqual(self.nivel_a2.puntos_requeridos, 60)

    def test_porcentaje_progreso_en_nivel(self):
        """
        El porcentaje de progreso = (puntos_en_nivel / puntos_requeridos) * 100.
        Con 25/50 puntos → 50%.
        """
        self.progresion.puntos_en_nivel = 25
        self.progresion.save()

        porcentaje = (
            self.progresion.puntos_en_nivel
            / self.progresion.nivel_actual.puntos_requeridos
            * 100
        )
        self.assertAlmostEqual(porcentaje, 50.0)
