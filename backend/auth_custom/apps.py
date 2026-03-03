from django.apps import AppConfig


class AuthCustomConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auth_custom"
    verbose_name = "Autenticacion"
    
    def ready(self):
        """
        Método ready() - Se ejecuta cuando Django inicializa la aplicación        
        Se encarga de:
          1. Importar los signals para que se registren
          2. Garantizar que se ejecuten para CUALQUIER creación de usuario
        """
        import auth_custom.signals 
