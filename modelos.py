"""
Modelos del Sistema de Gestión Académica - Universidad de Manizales.

Contiene todas las clases del dominio:
    - Persona (clase abstracta)
        - Estudiante
        - Docente
        - Administrativo
    - ProgramaAcademico
    - Asignatura
    - Horario
    - GrupoAcademico (contiene un Horario: composición)

Los atributos están encapsulados (prefijo "_") y se acceden mediante
propiedades (@property), que actúan como getters y setters con validación.
"""

from abc import ABC, abstractmethod
from datetime import datetime

from excepciones import (
    EstudianteYaMatriculadoError,
    GrupoLlenoError,
    EstudianteNoMatriculadoError,
    AsignaturaNoEncontradaError,
    ProgramaNoEncontradoError,
)


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

class Persona(ABC):
    """Clase abstracta con los datos comunes a todas las personas de la universidad.

    No se puede instanciar directamente: toda persona debe ser un Estudiante,
    un Docente o un Administrativo.
    """

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

    @abstractmethod
    def realizar_actividad_principal(self):
        """Cada subclase debe definir su propia actividad principal."""


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


# ---------------------------------------------------------------------------
# Oferta académica: horarios, grupos y catálogo
# ---------------------------------------------------------------------------

class Horario:
    """Describe cuándo y dónde se dicta un grupo académico.

    Un Horario no existe por sí solo: lo crea y lo posee un GrupoAcademico
    (relación de composición).
    """

    DIAS_VALIDOS = ("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado")
    FORMATO_HORA = "%H:%M"

    def __init__(self, dia, hora_inicio, hora_fin, salon):
        self.dia = dia
        self._hora_inicio = self._validar_hora(hora_inicio, "hora de inicio")
        self.hora_fin = hora_fin
        self.salon = salon

    @classmethod
    def _validar_hora(cls, valor, campo):
        texto = _validar_texto(valor, campo)
        try:
            datetime.strptime(texto, cls.FORMATO_HORA)
        except ValueError:
            raise ValueError(f"La {campo} '{texto}' no tiene el formato HH:MM (ej. 08:00).")
        return texto

    @property
    def dia(self):
        return self._dia

    @dia.setter
    def dia(self, valor):
        dia = _validar_texto(valor, "día").capitalize()
        if dia not in self.DIAS_VALIDOS:
            raise ValueError(f"El día '{dia}' no es válido. Opciones: {', '.join(self.DIAS_VALIDOS)}.")
        self._dia = dia

    @property
    def hora_inicio(self):
        return self._hora_inicio

    @hora_inicio.setter
    def hora_inicio(self, valor):
        hora = self._validar_hora(valor, "hora de inicio")
        if hasattr(self, "_hora_fin") and hora >= self._hora_fin:
            raise ValueError("La hora de inicio debe ser anterior a la hora de finalización.")
        self._hora_inicio = hora

    @property
    def hora_fin(self):
        return self._hora_fin

    @hora_fin.setter
    def hora_fin(self, valor):
        hora = self._validar_hora(valor, "hora de finalización")
        if hora <= self._hora_inicio:
            raise ValueError("La hora de finalización debe ser posterior a la hora de inicio.")
        self._hora_fin = hora

    @property
    def salon(self):
        return self._salon

    @salon.setter
    def salon(self, valor):
        self._salon = _validar_texto(valor, "salón")

    def __str__(self):
        return f"{self._dia} {self._hora_inicio}-{self._hora_fin} (Salón {self._salon})"


class GrupoAcademico:
    """Grupo en el que se ofrece una asignatura, con su docente, cupo y horario.

    Recibe objetos ya creados de Asignatura y Docente (asociación) y crea
    internamente su Horario (composición): si el grupo desaparece, su horario
    también.
    """

    def __init__(self, codigo, asignatura, docente, capacidad_maxima, dia, hora_inicio, hora_fin, salon):
        self.codigo = codigo
        self.asignatura = asignatura
        self.docente = docente
        self.capacidad_maxima = capacidad_maxima
        self._horario = Horario(dia, hora_inicio, hora_fin, salon)
        self._estudiantes = []

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = _validar_texto(valor, "código del grupo")

    @property
    def asignatura(self):
        return self._asignatura

    @asignatura.setter
    def asignatura(self, valor):
        if not isinstance(valor, Asignatura):
            raise ValueError("El grupo debe recibir un objeto Asignatura.")
        self._asignatura = valor

    @property
    def docente(self):
        return self._docente

    @docente.setter
    def docente(self, valor):
        if not isinstance(valor, Docente):
            raise ValueError("El grupo debe recibir un objeto Docente.")
        self._docente = valor

    @property
    def capacidad_maxima(self):
        return self._capacidad_maxima

    @capacidad_maxima.setter
    def capacidad_maxima(self, valor):
        valor = _validar_entero_positivo(valor, "capacidad máxima")
        if hasattr(self, "_estudiantes") and valor < len(self._estudiantes):
            raise ValueError("La capacidad no puede ser menor que el número de estudiantes matriculados.")
        self._capacidad_maxima = valor

    @property
    def horario(self):
        return self._horario

    @property
    def estudiantes(self):
        # Copia, para que la lista interna no se modifique desde fuera.
        return list(self._estudiantes)

    @property
    def cupos_disponibles(self):
        return self._capacidad_maxima - len(self._estudiantes)

    def _buscar_estudiante(self, codigo_estudiantil):
        for estudiante in self._estudiantes:
            if estudiante.codigo_estudiantil == codigo_estudiantil:
                return estudiante
        return None

    def matricular_estudiante(self, estudiante):
        """Matricula un estudiante. Lanza EstudianteYaMatriculadoError o GrupoLlenoError."""
        if not isinstance(estudiante, Estudiante):
            raise ValueError("Solo se pueden matricular objetos de tipo Estudiante.")
        if self._buscar_estudiante(estudiante.codigo_estudiantil) is not None:
            raise EstudianteYaMatriculadoError(estudiante.codigo_estudiantil, self._codigo)
        if len(self._estudiantes) >= self._capacidad_maxima:
            raise GrupoLlenoError(self._codigo, self._capacidad_maxima)
        self._estudiantes.append(estudiante)

    def retirar_estudiante(self, codigo_estudiantil):
        """Retira un estudiante por su código. Lanza EstudianteNoMatriculadoError."""
        estudiante = self._buscar_estudiante(codigo_estudiantil)
        if estudiante is None:
            raise EstudianteNoMatriculadoError(codigo_estudiantil, self._codigo)
        self._estudiantes.remove(estudiante)
        return estudiante

    def mostrar_informacion_grupo(self):
        print(f"  Grupo: [{self._codigo}] {self._asignatura.nombre}")
        print(f"    Docente: {self._docente.nombre}")
        print(f"    Horario: {self._horario}")
        print(f"    Cupos: {len(self._estudiantes)}/{self._capacidad_maxima} "
              f"({self.cupos_disponibles} disponibles)")

    def mostrar_estudiantes(self):
        print(f"  Estudiantes del grupo {self._codigo}:")
        if not self._estudiantes:
            print("    (sin estudiantes matriculados)")
        for i, estudiante in enumerate(self._estudiantes, start=1):
            print(f"    {i}. {estudiante.nombre} ({estudiante.codigo_estudiantil})")


class CatalogoAcademico:
    """Registro de programas y asignaturas con búsqueda por código."""

    def __init__(self):
        self._programas = {}
        self._asignaturas = {}

    def registrar_programa(self, programa):
        self._programas[programa.codigo] = programa

    def registrar_asignatura(self, asignatura):
        self._asignaturas[asignatura.codigo] = asignatura

    def buscar_programa(self, codigo):
        """Devuelve el programa o lanza ProgramaNoEncontradoError."""
        if codigo not in self._programas:
            raise ProgramaNoEncontradoError(codigo)
        return self._programas[codigo]

    def buscar_asignatura(self, codigo):
        """Devuelve la asignatura o lanza AsignaturaNoEncontradaError."""
        if codigo not in self._asignaturas:
            raise AsignaturaNoEncontradaError(codigo)
        return self._asignaturas[codigo]
