"""
MODELS - Módulo de Autenticación
=================================
REUTILIZABLE EN OTROS PROYECTOS: Sí

Este módulo contiene:
  - CustomUserManager: Gestor de usuarios con email como identificador
  - CustomUser: Modelo de usuario personalizado (AbstractBaseUser)

  Características:
  1. Autenticación por EMAIL (no username)
  2. Campos opcionales: teléfono, fecha_nacimiento, avatar
  3. Integración con Google OAuth (via django-allauth)
  4. Compatible con Django permissions system
  
  IMPORTANTE: Los signals en signals.py se encargan de crear
             datos iniciales cuando se crea un nuevo usuario
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    """
    Reutilizable
    Gestor personalizado para CustomUser.
    Reemplaza el UserManager por defecto de Django para permitir
    autenticación con EMAIL en lugar de username.
    """
    def create_user(self, email, password=None, **extra_fields):
        """Crear usuario regular"""
        if not email:
            raise ValueError('El campo Email es obligatorio')
        email = self.normalize_email(email)
        
        # Crear instancia del modelo
        user = self.model(email=email, **extra_fields)
        
        # Hashear la contraseña
        user.set_password(password) 
        
        # Guardar en base de datos
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Crear usuario admin/superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if not extra_fields.get('is_staff'):
            raise ValueError('El superuser debe tener is_staff=True')
        if not extra_fields.get('is_superuser'):
            raise ValueError('El superuser debe tener is_superuser=True')
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Reutilizable: Sí
    
    Modelo personalizado de usuario basado en AbstractBaseUser.
    Características:
      - Autenticación por EMAIL (USERNAME_FIELD = 'email')
      - Campos adicionales: teléfono, fecha_nacimiento, avatar
      - Integración con Google OAuth
      - Compatible con sistema de permisos de Django
    
    Al crear un usuario, el signal post_save en signals.py
       crea automáticamente: ProgresionNivel, RachaUsuario, Ranking
    """
    
    # ========== AUTENTICACIÓN ==========
    email = models.EmailField('correo electrónico', unique=True)
    username = models.CharField('nombre de usuario', max_length=150, unique=True, null=True, blank=True)
    password = models.CharField('contraseña', max_length=128)
    
    # ========== INFORMACIÓN PERSONAL ==========
    nombre = models.CharField('nombre', max_length=30)
    apellido = models.CharField('apellido', max_length=30)
    
    # ========== CAMPOS OPCIONALES ==========
    telefono = models.CharField('teléfono', max_length=20, blank=True)
    fecha_nacimiento = models.DateField('fecha de nacimiento', null=True, blank=True)
    avatar = models.ImageField('avatar', upload_to='avatars/', null=True, blank=True)
    
    # ========== VERIFICACIÓN Y TÉRMINOS ==========
    email_verificado = models.BooleanField('email verificado', default=False)
    acepto_terminos = models.BooleanField('aceptó términos', default=False)
    
    # ========== METADATOS DE DJANGO ==========
    is_active = models.BooleanField('activo', default=True)
    is_staff = models.BooleanField('es staff', default=False)
    date_joined = models.DateTimeField('fecha de registro', auto_now_add=True)
    last_login = models.DateTimeField('último login', auto_now=True)
    
    # ========== CONFIGURACIÓN CRÍTICA ==========
    USERNAME_FIELD = 'email'  # Campo para autenticación
    REQUIRED_FIELDS = ['nombre', 'apellido']  # Para createsuperuser por CLI
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Retorna nombre completo del usuario"""
        return f"{self.nombre} {self.apellido}"
    
    def get_short_name(self):
        """Retorna primer nombre del usuario"""
        return self.nombre
    
    # ========== INTEGRACIÓN GOOGLE OAUTH ==========
    
    @property
    def google_account(self):
        """
        Reutilizable: Sí
        
        Obtener la cuenta de Google OAuth si existe.
        Requiere django-allauth instalado.
        """
        from allauth.socialaccount.models import SocialAccount
        try:
            return SocialAccount.objects.get(user=self, provider='google')
        except SocialAccount.DoesNotExist:
            return None
    
    @property
    def google_id(self):
        """Obtener Google UID del usuario"""
        account = self.google_account
        return account.uid if account else None
    
    @property
    def google_picture(self):
        """Obtener foto de perfil de Google"""
        account = self.google_account
        return account.extra_data.get('picture') if account else None
    
    def has_google_account(self):
        """Verificar si el usuario tiene Google OAuth vinculado"""
        return self.google_account is not None