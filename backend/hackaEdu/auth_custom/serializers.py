"""
REUTILIZABLE EN OTROS PROYECTOS: Sí (parcialmente)

Los serializers están diseñados para:
  - UserSerializer & UserDetailSerializer: Generales, reutilizables
  - RegisterSerializer: Específico del registro, reutilizable con CustomUser
  - ChangePasswordSerializer: Reutilizable en cualquier sistema de auth

IMPORTANTE: Los signals now manejan la creación de datos iniciales
             (ProgresionNivel, RachaUsuario, Ranking)
"""

from rest_framework import serializers
from .models import CustomUser
from django.apps import apps


class UserSerializer(serializers.ModelSerializer):
    """
    Reutilizable: Sí
    
    Serializador básico del usuario. Expone solo los campos esenciales.
    Úsalo para listar usuarios, perfiles públicos, etc.
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'nombre', 'apellido', 'telefono', 'avatar', 'fecha_nacimiento')
        read_only_fields = ('id',)


class UserDetailSerializer(UserSerializer):
    """
    Reutilizable: Sí
    
    Serializador detallado del usuario con información extra.
    Incluye datos de Google si tiene cuenta vinculada.
    Úsalo para: perfil del usuario logueado, endpoints /me/
    """
    google_profile = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('date_joined', 'is_active', 'email_verificado', 'google_profile')
        read_only_fields = UserSerializer.Meta.read_only_fields + ('date_joined', 'is_active', 'email_verificado')
    
    def get_google_profile(self, obj):
        """Incluir datos de Google si el usuario tiene cuenta vinculada"""
        if obj.has_google_account():
            return {
                'google_id': obj.google_id,
                'picture': obj.google_picture,
                'has_google': True
            }
        return {'has_google': False}


class RegisterSerializer(serializers.ModelSerializer):
    """
    Reutilizable: Sí
    
    Serializador para registro de usuarios por formulario.
    
    CAMPOS ADICIONALES (v2):
      - categorias_preferidas: Lista de IDs de categorías de interés
      - dificultad_inicial: Dificultad inicial (BASIC, INTERMEDIATE, ADVANCED, EXPERT)
    
    IMPORTANTE: La creación de ProgresionNivel, RachaUsuario y Ranking
                   ahora se maneja automáticamente mediante signals
                   (ver: auth_custom/signals.py)
    
    Flujo:
      1. Valida email no duplicado
      2. Valida contraseñas coincidan
      3. Crea CustomUser
      4. Signal post_save se dispara → crea datos iniciales
      5. Crea PreferenciasUsuario con categorías y dificultad
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    # Preferencias adicionales
    categorias_preferidas = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text='Lista de códigos de categorías de interés (ej: ["ciencia", "tecnologia"])'
    )
    dificultad_inicial = serializers.ChoiceField(
        choices=['BASIC', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'],
        default='BASIC',
        required=False,
        help_text='Dificultad inicial: BASIC, INTERMEDIATE, ADVANCED, EXPERT'
    )

    class Meta:
        model = CustomUser
        fields = (
            'email', 'nombre', 'apellido', 'password', 'password_confirm', 'telefono',
            'categorias_preferidas', 'dificultad_inicial'
        )

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError({'password': 'Las contraseñas no coinciden'})
        return data

    def create(self, validated_data):
        """
        Crea el usuario y sus preferencias.
        
        El signal 'crear_datos_iniciales_usuario' en signals.py
        crea automáticamente:
          - ProgresionNivel (comienza en A1)
          - RachaUsuario
          - Ranking
          - PreferenciasUsuario (inicialmente vacío)
        
        Luego aquí actualizamos PreferenciasUsuario con las preferencias
        capturadas en el registro.
        """
        # Extraer preferencias antes de crear el usuario
        categorias_codigos = validated_data.pop('categorias_preferidas', [])
        dificultad_inicial = validated_data.pop('dificultad_inicial', 'BASIC')
        
        # Crear el usuario
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            nombre=validated_data['nombre'],
            apellido=validated_data['apellido'],
            telefono=validated_data.get('telefono', ''),
        )
        
        # El signal ya creó PreferenciasUsuario, ahora lo actualizamos
        try:
            from usuarios.models import PreferenciasUsuario
            from contenido.models import Categoria
            
            preferencias = PreferenciasUsuario.objects.get(usuario=user)
            preferencias.dificultad_inicial = dificultad_inicial
            preferencias.save()
            
            # Agregar categorías
            if categorias_codigos:
                categorias = Categoria.objects.filter(codigo__in=categorias_codigos)
                preferencias.categorias_preferidas.set(categorias)
        except Exception as e:
            print(f"⚠️ Error al actualizar preferencias: {e}")
        
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    Reutilizable: Sí
    
    Serializador para cambiar contraseña de usuario logueado.
    Requiere autenticación (JWT, sesión, etc.)
    
    Validaciones:
      1. Contraseña actual debe ser correcta
      2. Nueva contraseña tiene min 8 caracteres
      3. Confirmación de nueva contraseña debe coincidir
    """
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['new_password'] != data.pop('new_password_confirm'):
            raise serializers.ValidationError({'new_password': 'Las contraseñas no coinciden'})
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Contraseña actual incorrecta')
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
