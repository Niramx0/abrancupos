from django.db.models.signals import post_save
from django.dispatch import receiver
from polls.models import CitaMedica
from polls.tasks import enviar_notificaciones

@receiver(post_save, sender=CitaMedica)
def notificar_cita_creada(sender, instance, created, **kwargs):
    """
    Se ejecuta automáticamente cada vez que un usuario crea una nueva cita
    desde la web, admin, shell o cualquier parte.
    """
    if created:
        print("⚡ Nueva cita creada — enviando notificaciones inmediatas…")
        
        # Llamamos a enviar_notificaciones SOLO para esta cita
        enviar_notificaciones(fecha_forzada=instance.fecha)