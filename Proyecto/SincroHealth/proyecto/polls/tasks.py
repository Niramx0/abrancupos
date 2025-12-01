from datetime import date, timedelta
from polls.models import CitaMedica
from polls.sms import enviar_sms
from polls.email_utils import enviar_correo


def enviar_notificaciones(fecha_forzada=None):
    """
    Envía recordatorios de citas:
    ✔ 7 días antes
    ✔ 3 días antes
    ✔ 1 día antes
    ✔ el mismo día

    Y si llega fecha_forzada (desde signals), SOLO envía recordatorios
    para la cita recién creada.
    """

    hoy = date.today()

    # Si se está llamando desde una señal post_save
    if fecha_forzada:
        fechas_objetivo = [fecha_forzada]
        tipos = {fecha_forzada: "asignada"}
    else:
        # Notificaciones programadas por cron o manuales
        fechas_objetivo = [
            hoy + timedelta(days=7),
            hoy + timedelta(days=3),
            hoy + timedelta(days=1),
            hoy
        ]
        tipos = {
            hoy + timedelta(days=7): "dentro de 1 semana",
            hoy + timedelta(days=3): "dentro de 3 días",
            hoy + timedelta(days=1): "el dia de mañana",
            hoy: "el dia de hoy"
        }

    # Recorrer fechas objetivo
    for fecha in fechas_objetivo:
        tipo = tipos[fecha]

        print(f"\n🔍 Buscando citas programadas para {tipo} ({fecha})…")

        citas = CitaMedica.objects.filter(fecha=fecha)

        if not citas.exists():
            print("   → No hay citas para esta fecha.")
            continue

        for cita in citas:
            paciente = cita.idpaciente
            telefono = f"+57{paciente.telefono}"
            # -----------------------
            # Construcción del email
            # -----------------------
            mensaje_email = (
                f"Hola {paciente.nombre},\n\n"
                f"Este es un recordatorio: tienes una nueva cita médica {tipo}.\n\n"
                f"📅 Fecha: {cita.fecha}\n"
                f"⏰ Hora: {cita.hora}\n"
                f"👨‍⚕️ Médico: {cita.idmedico.nombre} {cita.idmedico.apellidos}\n\n"
                "SincroHealth"
            )
            # Enviar correo
            try:
                enviar_correo(
                    destinatario=paciente.correo_electronico,
                    asunto="Recordatorio de cita médica",
                    mensaje=mensaje_email
                )
            except Exception as e:
                print(f"⚠ Error al enviar correo a {paciente.correo_electronico}: {e}")

            # ---------------------
            # Construcción del SMS
            # ---------------------
            mensaje_sms = (
                f"SincroHealth: Tienes una cita {tipo}. "
                f"{cita.fecha} a las {cita.hora}."
            )

            try:
                enviar_sms(
                    numero_destino=telefono,
                    mensaje=mensaje_sms
                )
            except Exception as e:
                print(f"⚠ Error al enviar SMS a {telefono}: {e}")

            print(f"✔ Notificaciones enviadas a {paciente.nombre} ({tipo})")
