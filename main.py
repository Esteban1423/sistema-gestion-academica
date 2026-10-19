"""
Pruebas del Sistema de Gestión Académica - Universidad de Manizales.

Ejecutar con:
    python main.py
"""

from modelos import (
    ProgramaAcademico,
    Asignatura,
    Estudiante,
    Docente,
    Administrativo,
)


def titulo(texto):
    print("\n" + "=" * 70)
    print(f" {texto}")
    print("=" * 70)


def intentar(descripcion, accion):
    """Ejecuta una acción que debería fallar y muestra el mensaje de validación."""
    print(f"\n- Intento: {descripcion}")
    try:
        accion()
        print("  (!) No se produjo error: la validación no funcionó.")
    except ValueError as error:
        print(f"  Validación correcta -> {error}")


def main():
    # ------------------------------------------------------------------
    # 1. Programas académicos y asignaturas
    # ------------------------------------------------------------------
    titulo("1. CREACIÓN DE PROGRAMAS ACADÉMICOS Y ASIGNATURAS")

    ing_sistemas = ProgramaAcademico("ISC", "Ingeniería de Sistemas y Telecomunicaciones", "Ciencias e Ingeniería", 10)
    contaduria = ProgramaAcademico("CP", "Contaduría Pública", "Ciencias Contables, Económicas y Administrativas", 9)

    programacion = Asignatura("PRG1", "Programación I", 4, ing_sistemas)
    estructuras = Asignatura("EDD", "Estructuras de Datos", 3, ing_sistemas)
    contabilidad = Asignatura("CTB1", "Contabilidad General", 3, contaduria)

    for elemento in (ing_sistemas, contaduria, programacion, estructuras, contabilidad):
        elemento.mostrar_informacion()

    # ------------------------------------------------------------------
    # 2. Creación de personas (2 estudiantes, 2 docentes, 2 administrativos)
    # ------------------------------------------------------------------
    titulo("2. CREACIÓN DE PERSONAS")

    est1 = Estudiante("1053000001", "Laura Gómez", "laura.gomez@umanizales.edu.co",
                      "EST-2024-001", ing_sistemas, 3, 4.2)
    est2 = Estudiante("1053000002", "Andrés Ríos", "andres.rios@umanizales.edu.co",
                      "EST-2023-045", contaduria, 5, 3.8)

    doc1 = Docente("75000001", "Carlos Martínez", "carlos.martinez@umanizales.edu.co",
                   "EMP-101", "Ciencias e Ingeniería", "Tiempo completo", 40)
    doc2 = Docente("75000002", "Diana López", "diana.lopez@umanizales.edu.co",
                   "EMP-102", "Ciencias Contables, Económicas y Administrativas", "Cátedra", 12)

    adm1 = Administrativo("30000001", "Marta Salazar", "marta.salazar@umanizales.edu.co",
                          "EMP-201", "Registro Académico", "Coordinadora", "Diurna")
    adm2 = Administrativo("30000002", "Jorge Henao", "jorge.henao@umanizales.edu.co",
                          "EMP-202", "Bienestar Universitario", "Auxiliar administrativo", "Mixta")

    # Integración del sistema: inscripción y asignación de asignaturas
    est1.inscribir_asignatura(programacion)
    est1.inscribir_asignatura(estructuras)
    est2.inscribir_asignatura(contabilidad)
    doc1.asignar_asignatura(programacion)
    doc1.asignar_asignatura(estructuras)
    doc2.asignar_asignatura(contabilidad)

    print("Se crearon 6 personas: 2 estudiantes, 2 docentes y 2 administrativos.")

    # ------------------------------------------------------------------
    # 3. Modificaciones válidas mediante setters
    # ------------------------------------------------------------------
    titulo("3. MODIFICACIONES VÁLIDAS MEDIANTE SETTERS")

    print(f"Correo de {est1.nombre} antes: {est1.correo}")
    est1.correo = "laura.gomez.nuevo@umanizales.edu.co"
    print(f"Correo de {est1.nombre} después: {est1.correo}")

    print(f"\nSemestre de {est2.nombre} antes: {est2.semestre}")
    est2.semestre = 6
    est2.promedio = 4.0
    print(f"Semestre de {est2.nombre} después: {est2.semestre} | Nuevo promedio: {est2.promedio}")

    print(f"\nHoras semanales de {doc2.nombre} antes: {doc2.horas_semanales}")
    doc2.horas_semanales = 20
    doc2.tipo_contratacion = "Medio tiempo"
    print(f"Horas semanales de {doc2.nombre} después: {doc2.horas_semanales} ({doc2.tipo_contratacion})")

    print(f"\nCargo de {adm2.nombre} antes: {adm2.cargo}")
    adm2.cargo = "Profesional de Bienestar"
    print(f"Cargo de {adm2.nombre} después: {adm2.cargo}")

    print(f"\nCréditos de '{estructuras.nombre}' antes: {estructuras.creditos}")
    estructuras.creditos = 4
    print(f"Créditos de '{estructuras.nombre}' después: {estructuras.creditos}")

    # ------------------------------------------------------------------
    # 4. Intentos deliberados de asignar valores inválidos
    # ------------------------------------------------------------------
    titulo("4. VALIDACIONES: INTENTOS CON VALORES INVÁLIDOS")

    def correo_vacio():
        doc1.correo = ""

    def semestres_cero():
        ing_sistemas.numero_semestres = 0

    def semestres_negativos():
        ProgramaAcademico("MED", "Medicina", "Ciencias de la Salud", -2)

    def creditos_cero():
        programacion.creditos = 0

    def creditos_negativos():
        Asignatura("X01", "Asignatura inválida", -3, contaduria)

    def promedio_fuera_de_rango():
        est1.promedio = 6.5

    intentar("asignar un correo vacío a un docente", correo_vacio)
    intentar("asignar 0 semestres a un programa existente", semestres_cero)
    intentar("crear un programa con -2 semestres", semestres_negativos)
    intentar("asignar 0 créditos a una asignatura", creditos_cero)
    intentar("crear una asignatura con -3 créditos", creditos_negativos)
    intentar("asignar un promedio de 6.5 a un estudiante", promedio_fuera_de_rango)

    print("\nLos valores originales se conservan tras los intentos fallidos:")
    print(f"  Correo de {doc1.nombre}: {doc1.correo}")
    print(f"  Semestres de {ing_sistemas.nombre}: {ing_sistemas.numero_semestres}")
    print(f"  Créditos de {programacion.nombre}: {programacion.creditos}")

    # ------------------------------------------------------------------
    # 5. Polimorfismo: una única lista heterogénea y un solo ciclo for
    # ------------------------------------------------------------------
    titulo("5. RECORRIDO POLIMÓRFICO DE LA LISTA DE PERSONAS")

    personas = [est1, doc1, adm1, est2, doc2, adm2]

    for persona in personas:
        print()
        persona.mostrar_informacion()
        persona.realizar_actividad_principal()

    titulo("FIN DE LAS PRUEBAS")


if __name__ == "__main__":
    main()
