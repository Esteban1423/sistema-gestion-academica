"""
Modelos del Sistema de Gestión Académica - Universidad de Manizales.

Contiene todas las clases del dominio:
    - Persona (clase base)
        - Estudiante
        - Docente
        - Administrativo
    - ProgramaAcademico
    - Asignatura

Los atributos están encapsulados (prefijo "_") y se acceden mediante
propiedades (@property), que actúan como getters y setters con validación.
"""


# ---------------------------------------------------------------------------
# Funciones auxiliares de validación
# ---------------------------------------------------------------------------

def _validar_texto(valor, campo):
    """Verifica que un valor sea un texto no vacío y lo devuelve sin espacios extra."""
    if valor is None or str(valor).strip() == "":
        raise ValueError(f"El campo '{campo}' no puede estar vacío.")
    return str(valor).strip()


def _validar_entero_positivo(valor, campo):
    """Verifica que un valor sea un número entero mayor que cero."""
    if type(valor) is not int or valor <= 0:
        raise ValueError(f"El campo '{campo}' debe ser un número entero mayor que 0 (recibido: {valor!r}).")
    return valor


# ---------------------------------------------------------------------------
# Programa académico y asignatura
# ---------------------------------------------------------------------------

class ProgramaAcademico:
    """Representa un programa académico (carrera) de la universidad."""

    def __init__(self, codigo, nombre, facultad, numero_semestres):
        self.codigo = codigo
        self.nombre = nombre
        self.facultad = facultad
        self.numero_semestres = numero_semestres

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = _validar_texto(valor, "código del programa")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = _validar_texto(valor, "nombre del programa")

    @property
    def facultad(self):
        return self._facultad

    @facultad.setter
    def facultad(self, valor):
        self._facultad = _validar_texto(valor, "facultad")

    @property
    def numero_semestres(self):
        return self._numero_semestres

    @numero_semestres.setter
    def numero_semestres(self, valor):
        self._numero_semestres = _validar_entero_positivo(valor, "número de semestres")

    def mostrar_informacion(self):
        print(f"  Programa: [{self._codigo}] {self._nombre}")
        print(f"    Facultad: {self._facultad} | Semestres: {self._numero_semestres}")

    def __str__(self):
        return f"{self._nombre} ({self._codigo})"


class Asignatura:
    """Representa una asignatura que pertenece a un programa académico."""

    def __init__(self, codigo, nombre, creditos, programa):
        self.codigo = codigo
        self.nombre = nombre
        self.creditos = creditos
        self.programa = programa

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = _validar_texto(valor, "código de la asignatura")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = _validar_texto(valor, "nombre de la asignatura")

    @property
    def creditos(self):
        return self._creditos

    @creditos.setter
    def creditos(self, valor):
        self._creditos = _validar_entero_positivo(valor, "créditos")

    @property
    def programa(self):
        return self._programa

    @programa.setter
    def programa(self, valor):
        if valor is None:
            raise ValueError("La asignatura debe pertenecer a un programa académico.")
        self._programa = valor

    def mostrar_informacion(self):
        print(f"  Asignatura: [{self._codigo}] {self._nombre}")
        print(f"    Créditos: {self._creditos} | Programa: {self._programa}")

    def __str__(self):
        return f"{self._nombre} ({self._creditos} créditos)"


# ---------------------------------------------------------------------------
# Jerarquía de personas
# ---------------------------------------------------------------------------

class Persona:
    """Clase base con los datos comunes a todas las personas de la universidad."""

    def __init__(self, identificacion, nombre, correo):
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    @property
    def identificacion(self):
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor):
        self._identificacion = _validar_texto(valor, "identificación")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = _validar_texto(valor, "nombre")

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        correo = _validar_texto(valor, "correo")
        if "@" not in correo:
            raise ValueError(f"El correo '{correo}' no tiene un formato válido (falta '@').")
        self._correo = correo

    def mostrar_informacion(self):
        print(f"  Identificación: {self._identificacion}")
        print(f"  Nombre: {self._nombre}")
        print(f"  Correo: {self._correo}")

    def realizar_actividad_principal(self):
        """Cada subclase debe definir su propia actividad principal."""
        raise NotImplementedError("Las subclases deben implementar realizar_actividad_principal().")


class Estudiante(Persona):
    """Estudiante matriculado en un programa académico."""

    PROMEDIO_MINIMO = 0.0
    PROMEDIO_MAXIMO = 5.0

    def __init__(self, identificacion, nombre, correo, codigo_estudiantil, programa, semestre, promedio):
        super().__init__(identificacion, nombre, correo)
        self.codigo_estudiantil = codigo_estudiantil
        self.programa = programa
        self.semestre = semestre
        self.promedio = promedio
        self._asignaturas_inscritas = []

    @property
    def codigo_estudiantil(self):
        return self._codigo_estudiantil

    @codigo_estudiantil.setter
    def codigo_estudiantil(self, valor):
        self._codigo_estudiantil = _validar_texto(valor, "código estudiantil")

    @property
    def programa(self):
        return self._programa

    @programa.setter
    def programa(self, valor):
        if valor is None:
            raise ValueError("El estudiante debe pertenecer a un programa académico.")
        self._programa = valor

    @property
    def semestre(self):
        return self._semestre

    @semestre.setter
    def semestre(self, valor):
        _validar_entero_positivo(valor, "semestre")
        if valor > self._programa.numero_semestres:
            raise ValueError(
                f"El semestre {valor} supera los {self._programa.numero_semestres} "
                f"semestres del programa {self._programa.nombre}."
            )
        self._semestre = valor

    @property
    def promedio(self):
        return self._promedio

    @promedio.setter
    def promedio(self, valor):
        if not (self.PROMEDIO_MINIMO <= valor <= self.PROMEDIO_MAXIMO):
            raise ValueError(
                f"El promedio debe estar entre {self.PROMEDIO_MINIMO} y {self.PROMEDIO_MAXIMO} (recibido: {valor})."
            )
        self._promedio = float(valor)

    @property
    def asignaturas_inscritas(self):
        # Se devuelve una copia para que la lista interna no se modifique desde fuera.
        return list(self._asignaturas_inscritas)

    def inscribir_asignatura(self, asignatura):
        self._asignaturas_inscritas.append(asignatura)

    def total_creditos(self):
        return sum(a.creditos for a in self._asignaturas_inscritas)

    def mostrar_informacion(self):
        print("[ESTUDIANTE]")
        super().mostrar_informacion()
        print(f"  Código estudiantil: {self._codigo_estudiantil}")
        print(f"  Programa: {self._programa}")
        print(f"  Semestre: {self._semestre}")
        print(f"  Promedio: {self._promedio:.2f}")
        nombres = ", ".join(a.nombre for a in self._asignaturas_inscritas) or "Ninguna"
        print(f"  Asignaturas inscritas: {nombres} ({self.total_creditos()} créditos)")

    def realizar_actividad_principal(self):
        print(f"  >> {self._nombre} está estudiando para sus asignaturas de "
              f"semestre {self._semestre} en {self._programa.nombre}.")


class Docente(Persona):
    """Docente vinculado a una facultad."""

    def __init__(self, identificacion, nombre, correo, numero_empleado, facultad, tipo_contratacion, horas_semanales):
        super().__init__(identificacion, nombre, correo)
        self.numero_empleado = numero_empleado
        self.facultad = facultad
        self.tipo_contratacion = tipo_contratacion
        self.horas_semanales = horas_semanales
        self._asignaturas_a_cargo = []

    @property
    def numero_empleado(self):
        return self._numero_empleado

    @numero_empleado.setter
    def numero_empleado(self, valor):
        self._numero_empleado = _validar_texto(valor, "número de empleado")

    @property
    def facultad(self):
        return self._facultad

    @facultad.setter
    def facultad(self, valor):
        self._facultad = _validar_texto(valor, "facultad")

    @property
    def tipo_contratacion(self):
        return self._tipo_contratacion

    @tipo_contratacion.setter
    def tipo_contratacion(self, valor):
        self._tipo_contratacion = _validar_texto(valor, "tipo de contratación")

    @property
    def horas_semanales(self):
        return self._horas_semanales

    @horas_semanales.setter
    def horas_semanales(self, valor):
        self._horas_semanales = _validar_entero_positivo(valor, "horas semanales")

    @property
    def asignaturas_a_cargo(self):
        return list(self._asignaturas_a_cargo)

    def asignar_asignatura(self, asignatura):
        self._asignaturas_a_cargo.append(asignatura)

    def mostrar_informacion(self):
        print("[DOCENTE]")
        super().mostrar_informacion()
        print(f"  Número de empleado: {self._numero_empleado}")
        print(f"  Facultad: {self._facultad}")
        print(f"  Tipo de contratación: {self._tipo_contratacion}")
        print(f"  Horas semanales: {self._horas_semanales}")
        nombres = ", ".join(a.nombre for a in self._asignaturas_a_cargo) or "Ninguna"
        print(f"  Asignaturas a cargo: {nombres}")

    def realizar_actividad_principal(self):
        nombres = ", ".join(a.nombre for a in self._asignaturas_a_cargo) or "sus cursos"
        print(f"  >> {self._nombre} está dictando clase de {nombres} "
              f"({self._horas_semanales} horas semanales).")


class Administrativo(Persona):
    """Funcionario administrativo de una dependencia de la universidad."""

    def __init__(self, identificacion, nombre, correo, numero_empleado, dependencia, cargo, jornada):
        super().__init__(identificacion, nombre, correo)
        self.numero_empleado = numero_empleado
        self.dependencia = dependencia
        self.cargo = cargo
        self.jornada = jornada

    @property
    def numero_empleado(self):
        return self._numero_empleado

    @numero_empleado.setter
    def numero_empleado(self, valor):
        self._numero_empleado = _validar_texto(valor, "número de empleado")

    @property
    def dependencia(self):
        return self._dependencia

    @dependencia.setter
    def dependencia(self, valor):
        self._dependencia = _validar_texto(valor, "dependencia")

    @property
    def cargo(self):
        return self._cargo

    @cargo.setter
    def cargo(self, valor):
        self._cargo = _validar_texto(valor, "cargo")

    @property
    def jornada(self):
        return self._jornada

    @jornada.setter
    def jornada(self, valor):
        self._jornada = _validar_texto(valor, "jornada")

    def mostrar_informacion(self):
        print("[ADMINISTRATIVO]")
        super().mostrar_informacion()
        print(f"  Número de empleado: {self._numero_empleado}")
        print(f"  Dependencia: {self._dependencia}")
        print(f"  Cargo: {self._cargo}")
        print(f"  Jornada: {self._jornada}")

    def realizar_actividad_principal(self):
        print(f"  >> {self._nombre} está gestionando trámites como {self._cargo} "
              f"en {self._dependencia} (jornada {self._jornada.lower()}).")
