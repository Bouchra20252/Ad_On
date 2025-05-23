from django.apps import AppConfig


class PetitesAnnoncesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'petites_annonces'
    
    def ready(self):
        import petites_annonces.signals
