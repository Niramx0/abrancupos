from datetime import date
from polls.models import Paciente, Medico, CitaMedica, RecetaMedica, HistorialMedico

print("=== Iniciando carga de datos (SEED) ===")

pacientes = []
medicos = []
citas = []

# ==============================================================
# 1. PACIENTES (10 iniciales + 20 nuevos = 30 pacientes)
# ==============================================================

pacientes_data = [
    # === 10 YA CREADOS PREVIAMENTE ===
    (10001, 12345, "Carlos", "Ramírez", "Calle 10 #12-34", "carlos.ramirez@example.com", 3104567890),
    (10002, 54321, "Ana", "Gómez", "Carrera 45 #67-89", "ana.gomez@example.com", 3209876543),
    (10003, 67890, "María", "Fernández", "Calle 23 #4-56", "maria.fernandez@example.com", 3001234567),
    (10004, 11223, "Pedro", "López", "Avenida 5 #33-12", "pedro.lopez@example.com", 3112223333),
    (10005, 44556, "Sofía", "Martínez", "Cra 7 #45-90", "sofia.martinez@example.com", 3124445555),
    # === 5 extra anteriores ===
    (10006, 77889, "Jorge", "Castro", "Transv 2 #15-18", "jorge.castro@example.com", 3105556666),
    (10007, 99001, "Natalia", "Ruiz", "Cll 30 #14-70", "natalia.ruiz@example.com", 3105557777),
    (10008, 10101, "Andrés", "Ortiz", "Cra 99 #40-12", "andres.ortiz@example.com", 3105558888),
    (10009, 20202, "Liliana", "Vargas", "Cll 12 #8-55", "liliana.vargas@example.com", 3105559999),
    (10010, 30303, "Felipe", "Mejía", "Cra 70 #66-09", "felipe.mejia@example.com", 3105550000),

    # === 20 pacientes nuevos ===
    (10011, 40404, "Daniela", "Cárdenas", "Cll 80 #45-12", "daniela.cardenas@example.com", 3001112222),
    (10012, 50505, "Hernán", "Pérez", "Cra 28 #19-90", "hernan.perez@example.com", 3002223333),
    (10013, 60606, "Julieta", "García", "Cll 94 #12-34", "julieta.garcia@example.com", 3003334444),
    (10014, 70707, "Camilo", "Rojas", "Cra 50 #9-10", "camilo.rojas@example.com", 3004445555),
    (10015, 80808, "Lucía", "Santos", "Cll 14 #23-50", "lucia.santos@example.com", 3005556666),
    (10016, 90909, "Mateo", "Delgado", "Cra 87 #44-80", "mateo.delgado@example.com", 3006667777),
    (10017, 11112, "Paula", "Rivera", "Cll 33 #55-10", "paula.rivera@example.com", 3007778888),
    (10018, 13141, "Tomás", "Gil", "Cra 51 #95-22", "tomas.gil@example.com", 3008889999),
    (10019, 15161, "Elena", "Prieto", "Cll 65 #14-92", "elena.prieto@example.com", 3009990000),
    (10020, 17181, "Juan", "Guevara", "Cra 10 #22-18", "juan.guevara@example.com", 3011112222),
    (10021, 19191, "Manuela", "Suárez", "Cll 98 #16-77", "manuela.suarez@example.com", 3012223333),
    (10022, 21212, "Esteban", "Moreno", "Cra 15 #70-05", "esteban.moreno@example.com", 3013334444),
    (10023, 23232, "Sara", "Luna", "Cll 42 #58-30", "sara.luna@example.com", 3014445555),
    (10024, 25252, "Ricardo", "Peña", "Cra 100 #30-88", "ricardo.pena@example.com", 3015556666),
    (10025, 27272, "Carla", "Benítez", "Cll 20 #9-22", "carla.benitez@example.com", 3016667777),
    (10026, 29292, "Gabriel", "Acosta", "Cra 55 #88-12", "gabriel.acosta@example.com", 3017778888),
    (10027, 31313, "Valeria", "Mendoza", "Cll 4 #19-11", "valeria.mendoza@example.com", 3018889999),
    (10028, 33334, "Miguel", "Salazar", "Cra 61 #25-50", "miguel.salazar@example.com", 3019990000),
    (10029, 35354, "Adriana", "Cortes", "Cll 18 #67-12", "adriana.cortes@example.com", 3021112222),
    (10030, 37374, "Roberto", "Fajardo", "Cra 72 #33-77", "roberto.fajardo@example.com", 3022223333),
]

for p in pacientes_data:
    paciente, _ = Paciente.objects.get_or_create(
        idpaciente=p[0],
        defaults={
            "contrasena": p[1],
            "nombre": p[2],
            "apellidos": p[3],
            "direccion": p[4],
            "correo_electronico": p[5],
            "telefono": p[6],
        }
    )
    pacientes.append(paciente)

print("✔ 30 Pacientes insertados.")

# ==============================================================
# 2. MÉDICOS (10 previos + 20 nuevos = 30 médicos)
# ==============================================================

medicos_data = [
    # 10 previos
    (20001, 12345, "Laura", "Molina", "Pediatría", "laura.molina@example.com", 3201112222),
    (20002, 54321, "Héctor", "Jiménez", "Cardiología", "hector.jimenez@example.com", 3202223333),
    (20003, 67890, "Sandra", "León", "Dermatología", "sandra.leon@example.com", 3203334444),
    (20004, 11223, "Julián", "Arango", "Neurología", "julian.arango@example.com", 3204445555),
    (20005, 44556, "Paola", "Nieto", "Medicina General", "paola.nieto@example.com", 3205556666),
    # 5 extra previos
    (20006, 66778, "Luis", "Patiño", "Medicina Interna", "luis.patino@example.com", 3205556666),
    (20007, 77889, "Carolina", "Vélez", "Gastroenterología", "carolina.velez@example.com", 3205557777),
    (20008, 88990, "Esteban", "Córdoba", "Ortopedia", "esteban.cordoba@example.com", 3205558888),
    (20009, 99001, "Daniel", "Herrera", "Oftalmología", "daniel.herrera@example.com", 3205559999),
    (20010, 11122, "Valentina", "Soto", "Psiquiatría", "valentina.soto@example.com", 3205550000),

    # 20 nuevos
    (20011, 22233, "Sebastián", "Durán", "Oncología", "sebastian.duran@example.com", 3201113333),
    (20012, 33344, "Isabela", "Rivas", "Ginecología", "isabela.rivas@example.com", 3204447777),
    (20013, 44455, "David", "Torres", "Endocrinología", "david.torres@example.com", 3205551111),
    (20014, 55566, "Lorena", "Céspedes", "Reumatología", "lorena.cespedes@example.com", 3201115555),
    (20015, 66677, "Mauricio", "Pardo", "Urología", "mauricio.pardo@example.com", 3202225555),
    (20016, 77788, "Daniela", "Reyes", "Odontología", "daniela.reyes@example.com", 3203336666),
    (20017, 88899, "Óscar", "Silva", "Otorrinolaringología", "oscar.silva@example.com", 3204447777),
    (20018, 99900, "Adriana", "Peralta", "Alergología", "adriana.peralta@example.com", 3206669999),
    (20019, 12121, "Sergio", "Roldán", "Hematología", "sergio.roldan@example.com", 3207771111),
    (20020, 23232, "Catalina", "Hoyos", "Nefrología", "catalina.hoyos@example.com", 3208882222),
    (20021, 34343, "Kevin", "Villa", "Medicina General", "kevin.villa@example.com", 3201237890),
    (20022, 45454, "Tatiana", "Castillo", "Psicología", "tatiana.castillo@example.com", 3204561234),
    (20023, 56565, "Camilo", "Salinas", "Geriatría", "camilo.salinas@example.com", 3207896541),
    (20024, 67676, "Mariana", "Osorio", "Nutrición", "mariana.osorio@example.com", 3209517532),
    (20025, 78787, "Guillermo", "Gómez", "Medicina Deportiva", "guillermo.gomez@example.com", 3201593574),
    (20026, 89898, "Luisa", "Zapata", "Traumatología", "luisa.zapata@example.com", 3202584567),
    (20027, 90909, "Jairo", "Sierra", "Radiología", "jairo.sierra@example.com", 3203691478),
    (20028, 10101, "Silvia", "Montoya", "Anestesiología", "silvia.montoya@example.com", 3201473698),
    (20029, 20202, "Pablo", "Berrío", "Patología", "pablo.berrio@example.com", 3207539514),
    (20030, 30303, "Karla", "Del Valle", "Psiquiatría", "karla.delvalle@example.com", 3208524569),
]

for m in medicos_data:
    medico, _ = Medico.objects.get_or_create(
        idmedico=m[0],
        defaults={
            "contrasena": m[1],
            "nombre": m[2],
            "apellidos": m[3],
            "especialidad": m[4],
            "correo_electronico": m[5],
            "telefono": m[6],
        }
    )
    medicos.append(medico)

print("✔ 30 Médicos insertados.")

# ==============================================================
# 3. CITAS (10 previas + 20 nuevas = 30)
# ==============================================================

citas_data = []

# 10 citas previas ya mostradas antes:
citas_data.extend([
    (10001, 20001, "Pediatría", date(2025, 1, 10), "08:00"),
    (10002, 20002, "Cardiología", date(2025, 1, 12), "09:30"),
    (10003, 20003, "Dermatología", date(2025, 1, 14), "11:00"),
    (10004, 20004, "Neurología", date(2025, 1, 17), "14:30"),
    (10005, 20005, "Medicina General", date(2025, 1, 19), "16:00"),
    (10006, 20006, "Medicina Interna", date(2025, 2, 2), "09:00"),
    (10007, 20007, "Gastroenterología", date(2025, 2, 5), "10:30"),
    (10008, 20008, "Ortopedia", date(2025, 2, 7), "15:00"),
    (10009, 20009, "Oftalmología", date(2025, 2, 10), "13:15"),
    (10010, 20010, "Psiquiatría", date(2025, 2, 12), "16:00"),
])

# +20 nuevas citas con especialidades coherentes
horas = ["08:00", "09:00", "10:00", "11:00", "13:00", "15:00", "16:00"]

for i in range(20):
    paciente = pacientes[10 + i]  # pacientes[10..29]
    medico = medicos[10 + i]      # medicos[10..29]
    citas_data.append((
        paciente.idpaciente,
        medico.idmedico,
        medico.especialidad,
        date(2025, 3, 1 + i),
        horas[i % len(horas)]
    ))

# Insertar en DB
for cid in citas_data:
    p = Paciente.objects.get(idpaciente=cid[0])
    m = Medico.objects.get(idmedico=cid[1])
    nueva = CitaMedica.objects.create(
        idpaciente=p,
        idmedico=m,
        especialidad=cid[2],
        fecha=cid[3],
        hora=cid[4],
        estado_cita="Confirmada"
    )
    citas.append(nueva)

print("✔ 30 Citas insertadas.")

# ==============================================================
# 4. RECETAS (10 previas + 20 nuevas = 30)
# ==============================================================

diagnosticos_genericos = [
    ("Hipertensión leve", "Losartán 50mg", "1 tableta diaria por la mañana"),
    ("Asma controlada", "Salbutamol inhalador", "2 inhalaciones cada 6 horas si hay dificultad"),
    ("Alergia estacional", "Loratadina 10mg", "1 tableta diaria"),
    ("Dolor lumbar", "Naproxeno 500mg", "Tomar cada 12 horas por 5 días"),
    ("Migraña", "Sumatriptán 50mg", "Tomar al inicio del dolor"),
    ("Colitis leve", "Butilbromuro 10mg", "3 veces al día por 7 días"),
    ("Infección urinaria", "Nitrofurantoína 100mg", "Cada 6 horas por 5 días"),
    ("Artritis leve", "Meloxicam 7.5mg", "1 tableta diaria"),
    ("Dermatitis alérgica", "Hidrocortisona crema", "Aplicar 2 veces al día"),
    ("Ansiedad moderada", "Sertralina 50mg", "1 tableta diaria"),
]

# 10 recetas previas + 20 nuevas (=30)
recetas_total = 30

for i in range(recetas_total):
    p = citas[i].idpaciente
    m = citas[i].idmedico

    diag, med, ind = diagnosticos_genericos[i % len(diagnosticos_genericos)]

    RecetaMedica.objects.create(
        idpaciente=p,
        idmedico=m,
        idcitas_medicas=citas[i],
        diagnostico=diag,
        medicamentos=med,
        indicaciones=ind,
    )

print("✔ 30 Recetas insertadas.")

# ==============================================================
# 5. HISTORIALES MÉDICOS
# ==============================================================

for p in pacientes:
    HistorialMedico.objects.get_or_create(idpaciente=p)

print("✔ Historiales médicos generados.")

print("=== SEED COMPLETADO EXITOSAMENTE ===")
