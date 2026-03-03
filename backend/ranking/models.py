from django.db import models
from django.utils import timezone
from datetime import timedelta


class RachaUsuario(models.Model):
    """Seguimiento de racha (días consecutivos con al menos 1 lectura)"""
    
    usuario = models.OneToOneField('auth_custom.CustomUser', on_delete=models.CASCADE, related_name='racha', verbose_name='usuario')
    dias_consecutivos = models.IntegerField('días consecutivos', default=0)
    ultimo_acceso = models.DateField('último acceso', null=True, blank=True)
    ultima_lectura_fecha = models.DateField('última lectura', null=True, blank=True)
    fecha_ultima_actualizacion = models.DateTimeField('fecha última actualización', auto_now=True)
    
    class Meta:
        db_table = 'racha_usuario'
        verbose_name = 'Racha del Usuario'
        verbose_name_plural = 'Rachas de Usuarios'
    
    def __str__(self):
        return f'{self.usuario.username} - {self.dias_consecutivos} días 🔥'
    
    def calcular_racha(self):
        """Actualiza la racha según la actividad de lectura del usuario."""
        hoy = timezone.now().date()

        if not self.ultimo_acceso:
            # Primer acceso registrado
            self.ultimo_acceso = hoy
            self.dias_consecutivos = 1
            self.save()
            return

        diferencia_dias = (hoy - self.ultimo_acceso).days

        if diferencia_dias == 0:
            # Ya se contó hoy, solo guardar ultima_lectura_fecha si cambió
            self.save(update_fields=['ultima_lectura_fecha'])
            return

        if diferencia_dias == 1:
            # Día consecutivo → incrementar racha
            self.dias_consecutivos += 1
        else:
            # Rompió la racha → reiniciar
            self.dias_consecutivos = 1

        self.ultimo_acceso = hoy
        self.save()
    
    def tiene_lectura_hoy(self):
        """Verifica si hay al menos 1 lectura registrada hoy"""
        hoy = timezone.now().date()
        return self.ultima_lectura_fecha == hoy
    
    def actualizar_bonus_racha(self):
        """Incrementa días consecutivos si cumple con lectura + acceso"""
        from usuarios.models import ProgresionNivel
        
        if self.tiene_lectura_hoy():
            self.dias_consecutivos += 1
            self.save()
            
            # Bonus de puntos cada 7 días (reset domingo)
            if self.dias_consecutivos in [3, 4, 5, 6, 7]:
                puntos_bonus = self.dias_consecutivos - 2  # 3 dias = 1 extra, 7 dias = 5 extra
                progresion = ProgresionNivel.objects.get(usuario=self.usuario)
                progresion.puntos_totales += puntos_bonus
                progresion.save()
                return puntos_bonus
        return 0


class Ranking(models.Model):
    """Ranking global acumulativo de usuarios"""
    
    usuario = models.OneToOneField('auth_custom.CustomUser', on_delete=models.CASCADE, related_name='ranking', verbose_name='usuario')
    posicion = models.IntegerField('posición', default=0)
    fecha_actualizacion = models.DateTimeField('fecha de actualización', auto_now=True)
    
    class Meta:
        db_table = 'ranking'
        verbose_name = 'Ranking'
        verbose_name_plural = 'Rankings'
        ordering = ['posicion']
        indexes = [
            models.Index(fields=['posicion']),
        ]
    
    def __str__(self):
        return f'#{self.posicion} {self.usuario.username} - {self.puntos_totales}pts'
    
    @property
    def puntos_totales(self):
        """Obtiene los puntos totales acumulativos del usuario desde ProgresionNivel"""
        from usuarios.models import ProgresionNivel
        try:
            progresion = ProgresionNivel.objects.get(usuario=self.usuario)
            return progresion.puntos_acumulativos
        except ProgresionNivel.DoesNotExist:
            return 0
    
    @staticmethod
    def recalcular_ranking_global():
        """Recalcula las posiciones del ranking global basado en puntos totales"""
        from usuarios.models import ProgresionNivel
        
        # Obtener todos los usuarios ordenados por puntos totales
        progresiones = ProgresionNivel.objects.select_related('usuario').order_by('-puntos_acumulativos', 'fecha_actualizacion')
        
        for idx, progresion in enumerate(progresiones, 1):
            ranking, created = Ranking.objects.get_or_create(usuario=progresion.usuario)
            ranking.posicion = idx
            ranking.save(update_fields=['posicion', 'fecha_actualizacion'])
