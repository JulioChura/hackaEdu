from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        
        # crea una instancia del modelo (CustomUser)
        user = self.model(email=email, **extra_fields)
        
        # hashea la cosntraseña
        user.set_password(password) 
        
        # guarda el usuario en la base de datos
        user.save(using=self._db)
        
        return user

# 2. LUEGO crea el modelo
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Autenticación
    email = models.EmailField('correo electrónico', unique=True)
    username = models.CharField('nombre de usuario', max_length=150, unique=True, null=True, blank=True)
    nombre = models.CharField('nombre', max_length=30)
    apellido = models.CharField('apellido', max_length=30)
    
    # Campos opcionales
    telefono = models.CharField('teléfono', max_length=20, blank=True)
    fecha_nacimiento = models.DateField('fecha de nacimiento', null=True, blank=True)
    avatar = models.ImageField('avatar', upload_to='avatars/', null=True, blank=True)
    email_verificado = models.BooleanField('email verificado', default=False)
    acepto_terminos = models.BooleanField('aceptó términos', default=False)
    
    # Campos requeridos por Django
    is_active = models.BooleanField('activo', default=True)
    is_staff = models.BooleanField('es staff', default=False)
    date_joined = models.DateTimeField('fecha de registro', auto_now_add=True)
    last_login = models.DateTimeField('último login', auto_now=True)
    
    # CONFIGURACIÓN CRÍTICA
    USERNAME_FIELD = 'email'  # Login con email (como el manager espera)
    REQUIRED_FIELDS = ['nombre', 'apellido']  # Para createsuperuser
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        db_table = 'auth_user'  # Para mantener compatibilidad
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.nombre} {self.apellido}"
    
    def get_short_name(self):
        return self.nombre
    
    # Helper methods para acceder a datos de Google
    @property
    def google_account(self):
        """Obtener cuenta de Google si existe"""
        from allauth.socialaccount.models import SocialAccount
        try:
            return SocialAccount.objects.get(user=self, provider='google')
        except SocialAccount.DoesNotExist:
            return None
    
    @property
    def google_id(self):
        """Obtener Google ID del usuario"""
        account = self.google_account
        return account.uid if account else None
    
    @property
    def google_picture(self):
        """Obtener foto de perfil de Google"""
        account = self.google_account
        return account.extra_data.get('picture') if account else None
    
    def has_google_account(self):
        """Verificar si el usuario tiene Google vinculado"""
        return self.google_account is not None