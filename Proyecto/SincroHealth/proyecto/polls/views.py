from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse
from .models import *
from datetime import date, timedelta
from django.template import loader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.db.models import Max

def crear_cita(request):
    if request.method == "POST":
        pass

    return render(request, "citas/crear_cita.html")

def home(request):
    return render(request, 'Home.html')

def recetas_paciente(request, idpaciente):
    try:
        paciente = Paciente.objects.get(idpaciente=idpaciente)
    except Paciente.DoesNotExist:
        return redirect("homepacientes")

    recetas = RecetaMedica.objects.filter(idpaciente=paciente)

    return render(request, "RecetasPaciente.html", {
        "paciente": paciente,
        "recetas": recetas
    })

def recetas_medico(request):
    medico_id = request.session.get("medico_id")
    if not medico_id:
        return redirect("loginmedicos")

    medico = Medico.objects.get(idmedico=medico_id)
    recetas = RecetaMedica.objects.filter(idmedico=medico).order_by('-idcitas_medicas__fecha')

    return render(request, "RecetasMedico.html", {
        "medico": medico,
        "recetas": recetas
    })
    
def pacientes_medico(request):
    medico_id = request.session.get("medico_id")
    if not medico_id:
        return redirect("loginmedicos")

    medico = Medico.objects.get(idmedico=medico_id)
    pacientes = Paciente.objects.filter(citamedica__idmedico=medico).distinct()

    return render(request, "PacientesMedico.html", {
        "medico": medico,
        "pacientes": pacientes
    })

def historial_paciente_medico(request, idpaciente):
    paciente = get_object_or_404(Paciente, idpaciente=idpaciente)
    historial, creado = HistorialMedico.objects.get_or_create(idpaciente=paciente)
    medico_id = request.session.get("medico_id")
    if not medico_id:
        return redirect("loginmedicos")
    medico = Medico.objects.get(idmedico=medico_id)

    volver_url = request.GET.get("volver", "/homemedicos/")  
    return render(request, "HistorialPacienteMedico.html", {
        "paciente": paciente,
        "historial": historial,
        "medico": medico,
        "volver_url": volver_url
    })    

def ver_receta_paciente(request, idreceta):
    receta = get_object_or_404(RecetaMedica, idrecetas_medicas=idreceta)
    paciente = receta.idpaciente
    medico = receta.idmedico
    volver_url = request.GET.get("volver", "/")

    return render(request, "VerReceta.html", {
        "receta": receta,
        "paciente": paciente,   # Para HomePacientes.html
        "medico": medico,       # Para mostrar datos del médico en la receta
        "volver_url": volver_url
    })

def ver_receta_medico(request, idreceta):
    receta = get_object_or_404(RecetaMedica, idrecetas_medicas=idreceta)
    paciente = receta.idpaciente
    medico = receta.idmedico
    volver_url = request.GET.get("volver", "/")

    return render(request, "VerRecetaMedico.html", {
        "receta": receta,
        "paciente": paciente,   # Para mostrar datos del paciente en la receta
        "medico": medico,       # Para HomeMedicos.html
        "volver_url": volver_url
    })

    
def descargar_receta(request, idreceta):
    receta = get_object_or_404(RecetaMedica, idrecetas_medicas=idreceta)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="receta_{idreceta}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "Receta Médica")

    p.setFont("Helvetica", 12)
    p.drawString(50, 720, f"Paciente: {receta.idpaciente.nombre} {receta.idpaciente.apellidos}")
    p.drawString(50, 700, f"Médico: {receta.idmedico.nombre} {receta.idmedico.apellidos}")
    p.drawString(50, 680, f"Diagnóstico: {receta.diagnostico}")
    p.drawString(50, 660, f"Medicamentos: {receta.medicamentos}")
    p.drawString(50, 640, f"Indicaciones: {receta.indicaciones}")
    p.drawString(50, 620, f"Fecha cita: {receta.idcitas_medicas.fecha} {receta.idcitas_medicas.hora}")

    p.showPage()
    p.save()

    return response

def loginpacientes(request):

    error_general = None

    if request.method == "POST":
        usuario = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        if not usuario or not password:
            error_general = "Por favor ingresa tu usuario y contraseña."
        else:
            try:
                paciente = Paciente.objects.get(idpaciente=usuario)

                if str(paciente.contrasena) == str(password):
                    request.session["paciente_id"] = paciente.idpaciente
                    return redirect("homepacientes")
                else:
                    error_general = "Usuario o contraseña incorrecta, por favor intente nuevamente."

            except Paciente.DoesNotExist:
                error_general = "Usuario o contraseña incorrecta, por favor intente nuevamente."
            except Exception as e:
                error_general = "Ocurrió un error inesperado. Por favor intenta de nuevo."

    return render(request, "LoginPacientes.html", {
        "error_general": error_general
    })

def loginmedicos(request):

    error_general = None

    if request.method == "POST":
        usuario = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        if not usuario or not password:
            error_general = "Por favor ingresa tu usuario y contraseña."
        else:
            try:
                medico = Medico.objects.get(idmedico=usuario)

                if str(medico.contrasena) == str(password):
                    request.session["medico_id"] = medico.idmedico
                    return redirect("homemedicos") 
                else:
                    error_general = "Usuario o contraseña incorrecta, por favor intente nuevamente."

            except Medico.DoesNotExist:
                error_general = "Usuario o contraseña incorrecta, por favor intente nuevamente."
            except Exception as e:
                error_general = "Ocurrió un error inesperado. Por favor intenta de nuevo."

    return render(request, "LoginMedicos.html", {
        "error_general": error_general
    })

def homepacientes(request):
    paciente_id = request.session.get("paciente_id")

    if not paciente_id:
        return redirect("loginpacientes")

    paciente = Paciente.objects.get(idpaciente=paciente_id)

    return render(request, "HomePacientes.html", {
        "paciente": paciente
    })


@require_http_methods(["GET"])
def citas_pendientes(request):
    """Lista de citas pendientes del paciente actualmente en sesión."""
    paciente_id = request.session.get("paciente_id")
    if not paciente_id:
        return redirect("loginpacientes")

    paciente = get_object_or_404(Paciente, idpaciente=paciente_id)

    citas = CitaMedica.objects.filter(
        idpaciente=paciente,
        estado_cita="Pendiente"
    ).order_by("fecha", "hora")

    return render(request, "CitasPendientes.html", {
        "paciente": paciente,
        "citas": citas
    })

def homemedicos(request):
    medico_id = request.session.get("medico_id")

    if not medico_id:
        return redirect("loginmedicos")

    medico = Medico.objects.get(idmedico=medico_id)

    return render(request, "HomeMedicos.html", {
        "medico": medico
    })

def agendarcitas(request):
    paciente_id = request.session.get("paciente_id")

    if not paciente_id:
        return redirect("loginpacientes")

    paciente = Paciente.objects.get(idpaciente=paciente_id)
    especialidades = Medico.objects.values_list("especialidad", flat=True).distinct()

    # HORAS DISPONIBLES
    horas_base = ["08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00"]
    horas = [(h, True) for h in horas_base]
    medicos = Medico.objects.all()

    # --- POST: GUARDAR CITA ---
    if request.method == "POST":
        especialidad = request.POST.get("especialidad")
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")
        medico_id = request.POST.get("medico")

        if fecha <= str(date.today()):
            return render(request, "AgendarCitas.html", {
                "paciente": paciente,
                "especialidades": especialidades,
                "horas": horas,
                "hoy": date.today(),
                "medicos": medicos,
                "error": " No puedes agendar una cita para hoy ni para una fecha pasada."
            })

        # Validación de conflicto
        conflicto = CitaMedica.objects.filter(
            fecha=fecha,
            hora=hora,
            idmedico_id=medico_id
        ).exists()

        if conflicto:
            return render(request, "AgendarCitas.html", {
                "paciente": paciente,
                "especialidades": especialidades,
                "horas": [(h, True) for h in horas_base],
                "hoy": date.today(),
                "medicos": Medico.objects.all(),
                "error": "El médico ya tiene una cita en ese horario."
            })

        # Si no hay conflicto, guardar la cita
        CitaMedica.objects.create(
            idpaciente=paciente,
            idmedico_id=medico_id,
            especialidad=especialidad,
            fecha=fecha,
            hora=hora,
            estado_cita="Pendiente"
        )

        return render(request, "AgendarCitas.html", {
            "paciente": paciente,
            "especialidades": especialidades,
            "horas": [(h, True) for h in horas_base],
            "hoy": date.today(),
            "medicos": Medico.objects.all(),
            "exito": "La cita fue agendada correctamente."
        })

    # --- GET: CARGAR HORAS DISPONIBLES ---
    fecha_sel = request.GET.get("fecha")
    esp_sel = request.GET.get("especialidad")

    horas = []
    if fecha_sel and esp_sel:
        ocupadas = CitaMedica.objects.filter(
            fecha=fecha_sel,
            especialidad=esp_sel
        ).values_list("hora", flat=True)

        for h in horas_base:
            horas.append((h, h not in ocupadas))
    else:
        horas = [(h, True) for h in horas_base]

    return render(request, "AgendarCitas.html", {
        "paciente": paciente,
        "especialidades": especialidades,
        "horas": horas,
        "hoy": date.today(),
        "medicos": Medico.objects.all(),
    })

def filtrar_medicos(request):
    esp = request.GET.get("especialidad")
    medicos = Medico.objects.filter(especialidad=esp)

    data = {
        "medicos": [
            {"id": m.idmedico, "nombre": f"{m.nombre} {m.apellido}"}
            for m in medicos
        ]
    }
    return JsonResponse(data)

def cancelar_aplazar_citas(request):
    paciente_id = request.session.get("paciente_id")

    if not paciente_id:
        return redirect("loginpacientes")

    paciente = Paciente.objects.get(idpaciente=paciente_id)
    
    # Citas pendientes del paciente
    citas = CitaMedica.objects.filter(
        idpaciente=paciente,
        estado_cita="Pendiente"
    )

    horas_base = [
        "08:00", "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00", "15:00", "16:00"
    ]

    mensaje_exito = None
    mensaje_error = None

    if request.method == "POST":
        accion = request.POST.get("accion")
        cita_id = request.POST.get("cita")

        if not cita_id:
            mensaje_error = "Debe seleccionar una cita."
        else:
            cita = CitaMedica.objects.get(idcitas_medicas=cita_id)

            # --- CANCELAR ---
            if accion == "confirmar_cancelar":
                cita.estado_cita = "Cancelada"
                cita.save()
                mensaje_exito = "Cita cancelada exitosamente."

            # --- APLAZAR ---
            elif accion == "confirmar_aplazar":
                nueva_fecha = request.POST.get("nueva_fecha")
                nueva_hora = request.POST.get("nueva_hora")

                if not nueva_fecha or not nueva_hora:
                    mensaje_error = "Debe seleccionar nueva fecha y hora."
                else:
                    if nueva_fecha <= str(date.today()):
                        mensaje_error = "No puede aplazar la cita a una fecha pasada o el día de hoy."
                    else:
                        # Verificar disponibilidad
                        ocupado = CitaMedica.objects.filter(
                            idmedico=cita.idmedico,
                            fecha=nueva_fecha,
                            hora=nueva_hora,
                            estado_cita="Pendiente"
                        ).exists()

                        if ocupado:
                            mensaje_error = "El médico ya tiene una cita en esa fecha y hora."
                        else:
                            cita.fecha = nueva_fecha
                            cita.hora = nueva_hora
                            cita.save()
                            mensaje_exito = "Cita aplazada exitosamente."

    context = {
        "paciente": paciente,
        "citas": citas,
        "hoy": date.today(),
        "horas": horas_base,
        "mensaje_exito": mensaje_exito,
        "mensaje_error": mensaje_error,
    }

    return render(request, "CanAplaCitas.html", context)

def info(request):
    return render(request, 'Info.html')

def horario_medico(request,idmedico):
    medico = Medico.objects.get(idmedico=idmedico)
    hoy = date.today()
    lunes = hoy - timedelta(days=hoy.weekday())        
    domingo = lunes + timedelta(days=6)  
    citas_semana = CitaMedica.objects.filter(
        idmedico=medico,
        fecha__range=[lunes, domingo]
    ).order_by("fecha", "hora")
    dias = {}
    for i in range(7):
        dia = lunes + timedelta(days=i)
        dias[dia] = []
    for cita in citas_semana:
        dias[cita.fecha].append(cita)
    return render(request, "horario_medico.html", {
        "medico": medico,
        "dias":dias,
        "lunes":lunes,
        "domingo":domingo
    })

def vista_historial(request, idpaciente):
    paciente = get_object_or_404(Paciente, idpaciente=idpaciente)
    historial = get_object_or_404(HistorialMedico, idpaciente=paciente)
    return render(request, "historial.html", {
        "paciente": paciente,
        "historial": historial,
    })

def historial_pdf(request, idpaciente):
    paciente = Paciente.objects.get(pk=idpaciente)
    historial, creado = HistorialMedico.objects.get_or_create(idpaciente=paciente)

    response = HttpResponse(content_type="application/pdf")
    response["X-Frame-Options"] = "ALLOWALL"
    response["X-Content-Type-Options"] = "nosniff"
    if request.GET.get("preview") == "1":
        response["Content-Disposition"] = "inline; filename=historial.pdf"
    else:
        response["Content-Disposition"] = f'attachment; filename="historial_{paciente.idpaciente}.pdf"'
        
    p = canvas.Canvas(response, pagesize=letter)
    y = 750
    p.setTitle(f"{paciente.nombre} {paciente.apellidos}")
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Historial Médico")
    y -= 30

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Paciente: {paciente.nombre} {paciente.apellidos}")
    y -= 20

    p.drawString(50, y, f"Fecha: {historial.fecha}")
    y -= 40

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Recetas registradas:")
    y -= 25

    p.setFont("Helvetica", 12)
    if not historial.recetas_json:
        p.drawString(50, y, "No hay recetas registradas.")
    else:
        for receta in historial.recetas_json:
            text = (
                f"- ({receta['idrecetas_medicas']}) "
                f"{receta['diagnostico']} | "
                f"{receta['medicamentos']} ({receta['indicaciones']})"
            )
            p.drawString(50, y, text)
            y -= 20
            if y < 50:
                p.showPage()
                y = 750

    p.showPage()
    p.save()

    return response
@require_http_methods(["GET"])
def seleccionar_paciente_receta(request):
    """
    Mostrar lista de pacientes (con sus próximas/últimas citas) para que el médico
    seleccione la cita a partir de la cual crear una receta.
    """
    medico_id = request.session.get("medico_id")
    if not medico_id:
        return redirect("loginmedicos")
    medico = get_object_or_404(Medico, idmedico=medico_id)

    # Pacientes distintos con al menos una cita con este médico
    pacientes = Paciente.objects.filter(citamedica__idmedico=medico).distinct()

    # Para cada paciente traemos la última cita con este médico (fecha más reciente)
    pacientes_info = []
    for p in pacientes:
        ultima_cita = CitaMedica.objects.filter(idpaciente=p, idmedico=medico).order_by("-fecha", "-hora").first()
        pacientes_info.append({
            "paciente": p,
            "ultima_cita": ultima_cita
        })

    return render(request, "SeleccionarPacienteReceta.html", {
        "medico": medico,
        "pacientes_info": pacientes_info
    })


@require_http_methods(["GET", "POST"])
def crear_receta(request, cita_id=None):
    """
    Formulario para crear una RecetaMedica asociada a una cita.
    - Si llega cita_id (URL), prefill.
    - En GET muestra el form.
    - En POST valida y crea.
    """
    medico_id_sesion = request.session.get("medico_id")
    if not medico_id_sesion:
        return redirect("loginmedicos")
    medico = get_object_or_404(Medico, idmedico=medico_id_sesion)

    cita_prefill = None
    if cita_id:
        cita_prefill = get_object_or_404(CitaMedica, idcitas_medicas=cita_id)

    # Traer sólo las citas de este médico (recientes) para selección alternativa
    citas_medico = CitaMedica.objects.filter(idmedico=medico).order_by("-fecha", "-hora")

    if request.method == "POST":
        # Preferimos la cita enviada vía POST (si existe), sino usar cita_prefill
        cita_post = request.POST.get("cita")
        try:
            if cita_post:
                cita_obj = CitaMedica.objects.get(idcitas_medicas=cita_post)
            elif cita_prefill:
                cita_obj = cita_prefill
            else:
                cita_obj = None
        except CitaMedica.DoesNotExist:
            cita_obj = None

        diagnostico = request.POST.get("diagnostico", "").strip()
        medicamentos = request.POST.get("medicamentos", "").strip()
        indicaciones = request.POST.get("indicaciones", "").strip()

        errores = []
        if not cita_obj:
            errores.append("Debe seleccionar una cita válida para asociar la receta.")
        if not diagnostico or len(diagnostico) < 2:
            errores.append("Diagnóstico está vacío o demasiado corto.")

        if errores:
            return render(request, "CrearRecetaMedico.html", {
                "medico": medico,
                "citas": citas_medico,
                "cita_prefill": cita_prefill,
                "errores": errores,
                "form": {
                    "diagnostico": diagnostico,
                    "medicamentos": medicamentos,
                    "indicaciones": indicaciones,
                    "cita": cita_post
                }
            })

        # Crear la receta usando la cita (y su paciente)
        receta = RecetaMedica.objects.create(
            idpaciente=cita_obj.idpaciente,
            idmedico=medico,
            idcitas_medicas=cita_obj,
            diagnostico=diagnostico,
            medicamentos=medicamentos or "No especificado",
            indicaciones=indicaciones or "No especificado"
        )

        messages.success(request, "Receta creada correctamente.")
        return redirect('seleccionar_paciente_receta')
    # GET
    return render(request, "CrearRecetaMedico.html", {
        "medico": medico,
        "citas": citas_medico,
        "cita_prefill": cita_prefill
    })



@require_http_methods(["GET", "POST"])
def editar_perfil_paciente(request):
    """
    Vista para que un paciente edite su perfil (correo, dirección, teléfono, contraseña)
    """
    paciente_id = request.session.get("paciente_id")
    if not paciente_id:
        return redirect("loginpacientes")
    
    paciente = get_object_or_404(Paciente, idpaciente=paciente_id)
    
    if request.method == "POST":
        correo = request.POST.get("correo", "").strip()
        direccion = request.POST.get("direccion", "").strip()
        telefono = request.POST.get("telefono", "").strip()
        password = request.POST.get("password", "").strip()
        
        errores = []

        if correo and "@" not in correo:
            errores.append("El correo no es válido.")
        
        if telefono and not telefono.isdigit():
            errores.append("El teléfono debe contener solo números.")

        if password:
            if len(password) < 5 or len(password) > 25:
                errores.append("La contraseña debe tener entre 5 y 25 caracteres.")
        
        if errores:
            return render(request, "editar_perfil_pac.html", {
                "paciente": paciente,
                "nombre_paciente": paciente.nombre,
                "apellido_paciente": paciente.apellidos,
                "errores": errores,
                "form": {
                    "correo": correo,
                    "direccion": direccion,
                    "telefono": telefono
                }
            })
        # Actualizar datos (con el paciente que le metamos)
        if correo:
            paciente.correo_electronico = correo
        if direccion:
            paciente.direccion = direccion
        if telefono:
            paciente.telefono = int(telefono)
        if password:
            paciente.contrasena = password
        
        paciente.save()
        messages.success(request, "Perfil actualizado correctamente.")
        return redirect("homepacientes")
    
    return render(request, "editar_perfil_pac.html", {
        "paciente": paciente,
        "nombre_paciente": paciente.nombre,
        "apellido_paciente": paciente.apellidos,
        "correo": paciente.correo_electronico,
        "direccion": paciente.direccion,
        "telefono": paciente.telefono
    })


@require_http_methods(["GET", "POST"])
def editar_perfil_medico(request):
    """
    Vista para que un médico edite su perfil (correo, teléfono, contraseña)
    """
    medico_id = request.session.get("medico_id")
    if not medico_id:
        return redirect("loginmedicos")
    
    medico = get_object_or_404(Medico, idmedico=medico_id)
    
    if request.method == "POST":
        correo = request.POST.get("correo", "").strip()
        telefono = request.POST.get("telefono", "").strip()
        password = request.POST.get("password", "").strip()
        
        errores = []

        if correo and "@" not in correo:
            errores.append("El correo no es válido.")

        if telefono and not telefono.isdigit():
            errores.append("El teléfono debe contener solo números.")

        if password:
            if len(password) < 5 or len(password) > 25:
                errores.append("La contraseña debe tener entre 5 y 25 caracteres.")
        
        if errores:
            return render(request, "editar_perfil_med.html", {
                "medico": medico,
                "nombre_medico": medico.nombre,
                "apellido_medico": medico.apellidos,
                "especialidad": medico.especialidad,
                "errores": errores,
                "form": {
                    "correo": correo,
                    "telefono": telefono
                }
            })

        if correo:
            medico.correo_electronico = correo
        if telefono:
            medico.telefono = int(telefono)
        if password:
            medico.contrasena = password
        
        medico.save()
        messages.success(request, "Perfil actualizado correctamente.")
        return redirect("homemedicos")
    
    # GET
    return render(request, "editar_perfil_med.html", {
        "medico": medico,
        "nombre_medico": medico.nombre,
        "apellido_medico": medico.apellidos,
        "especialidad": medico.especialidad,
        "correo": medico.correo_electronico,
        "telefono": medico.telefono
    })