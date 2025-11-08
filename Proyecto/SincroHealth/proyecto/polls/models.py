from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

class Paciente(models.Model):
    idpaciente = models.IntegerField(primary_key=True)
    contrasena = models.IntegerField()
    nombre = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    correo_electronico = models.CharField(max_length=45)
    telefono = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class Medico(models.Model):
    idmedico = models.IntegerField(primary_key=True)
    contrasena = models.IntegerField()
    nombre = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    especialidad = models.CharField(max_length=45)
    correo_electronico = models.EmailField(max_length=45)
    telefono = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} {self.apellidos} | Especialidad: {self.especialidad}"

class Administrador(models.Model):
    idadministradores = models.OneToOneField(User, on_delete=models.CASCADE)
    contraseña = models.IntegerField()
    nombre = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    correo_electronico = models.CharField(max_length=45)
    telefono = models.IntegerField()

    def __str__(self):
        return f"{self.idadministradores.username} | Nombre: {self.nombre}{self.apellidos}"

class CitaMedica(models.Model):
    idcitas_medicas = models.AutoField(primary_key=True)
    idpaciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    idmedico = models.ForeignKey('Medico', on_delete=models.CASCADE, null=True, blank=True)
    especialidad = models.CharField(max_length=45)
    fecha = models.DateField()
    hora = models.CharField(max_length=45)
    estado_cita = models.CharField(max_length=45, default="Pendiente")

    def __str__(self):
        return (
            f"{self.idcitas_medicas} | Especialidad: {self.especialidad} | "
            f"Médico: {self.idmedico.nombre} {self.idmedico.apellidos} | "
            f"Paciente: {self.idpaciente.nombre} {self.idpaciente.apellidos} | "
            f"Fecha: {self.fecha} | Hora: {self.hora}"
        )

class RecetaMedica(models.Model):
    idrecetas_medicas = models.AutoField(primary_key=True)
    idpaciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    idmedico = models.ForeignKey('Medico', on_delete=models.CASCADE, null=True, blank=True)
    idcitas_medicas = models.ForeignKey('CitaMedica', on_delete=models.CASCADE)
    diagnostico = models.CharField(max_length=300)
    medicamentos = models.CharField(max_length=45)
    indicaciones = models.CharField(max_length=45)

    def __str__(self):
        return (
            f"{self.idrecetas_medicas} | "
            f"Paciente: {self.idpaciente.nombre} {self.idpaciente.apellidos} | "
            f"Médico: {self.idmedico.nombre} {self.idmedico.apellidos} | "
            f"Cita: {self.idcitas_medicas.idcitas_medicas}"
        )

class HistorialMedico(models.Model):
    idhistorial = models.AutoField(primary_key=True)
    idpaciente = models.OneToOneField('Paciente', on_delete=models.CASCADE)
    recetas_json = models.JSONField(blank=True, default=list)
    fecha = models.DateField(auto_now=True)

    def actualizar_recetas(self):
        recetas = self.idpaciente.recetamedica_set.all().values(
            'idrecetas_medicas',
            'diagnostico',
            'medicamentos',
            'indicaciones',
            'idcitas_medicas'
        )
        self.recetas_json = list(recetas)
        self.save()

    def __str__(self):
        recetas_texto = "; ".join(
            [f"(ID {r['idrecetas_medicas']}) {r['diagnostico']} - {r['medicamentos']} ({r['indicaciones']})"
             for r in self.recetas_json]
        ) if self.recetas_json else "Sin recetas registradas"
        return f"Historial del paciente {self.idpaciente.nombre} {self.idpaciente.apellidos} - {self.fecha} | Recetas: {recetas_texto}"

@receiver(post_save, sender='polls.RecetaMedica')
def actualizar_historial_al_guardar(sender, instance, **kwargs):
    paciente = instance.idpaciente
    historial, creado = HistorialMedico.objects.get_or_create(idpaciente=paciente)
    historial.actualizar_recetas()


@receiver(post_delete, sender='polls.RecetaMedica')
def actualizar_historial_al_eliminar(sender, instance, **kwargs):
    paciente = instance.idpaciente
    historial = HistorialMedico.objects.filter(idpaciente=paciente).first()
    if historial:
        historial.actualizar_recetas()

class Auditoria(models.Model):
    idauditoria = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    fecha = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.idauditoria} - {self.descripcion}"