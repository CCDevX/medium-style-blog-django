from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"

    def ready(self):
        # Importer ici pour éviter les imports trop tôt
        from .models import Post
        from cloudinary_storage.storage import MediaCloudinaryStorage

        # Réaffecte le backend Cloudinary au champ image APRÈS l'init de Django
        Post._meta.get_field("image").storage = MediaCloudinaryStorage()
