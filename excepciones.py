"""
Excepciones personalizadas del Sistema de Gestión Académica.

Todas heredan de ErrorGestionAcademica, de modo que el programa principal
puede capturarlas de forma individual o todas a la vez.
"""


class ErrorGestionAcademica(Exception):
    """Excepción base de todos los errores propios del sistema."""


class EstudianteYaMatriculadoError(ErrorGestionAcademica):
    """El estudiante ya está matriculado en el grupo."""

    def __init__(self, codigo_estudiantil, codigo_grupo):
        self.codigo_estudiantil = codigo_estudiantil
        self.codigo_grupo = codigo_grupo
        super().__init__(
            f"El estudiante '{codigo_estudiantil}' ya está matriculado en el grupo '{codigo_grupo}'."
        )


class GrupoLlenoError(ErrorGestionAcademica):
    """El grupo alcanzó su capacidad máxima."""

    def __init__(self, codigo_grupo, capacidad):
        self.codigo_grupo = codigo_grupo
        self.capacidad = capacidad
        super().__init__(
            f"El grupo '{codigo_grupo}' alcanzó su capacidad máxima de {capacidad} estudiantes."
        )


class EstudianteNoMatriculadoError(ErrorGestionAcademica):
    """El estudiante que se desea retirar no está matriculado en el grupo."""

    def __init__(self, codigo_estudiantil, codigo_grupo):
        self.codigo_estudiantil = codigo_estudiantil
        self.codigo_grupo = codigo_grupo
        super().__init__(
            f"El estudiante '{codigo_estudiantil}' no está matriculado en el grupo '{codigo_grupo}'."
        )


class AsignaturaNoEncontradaError(ErrorGestionAcademica):
    """La asignatura buscada no existe."""

    def __init__(self, codigo):
        self.codigo = codigo
        super().__init__(f"No existe una asignatura con el código '{codigo}'.")


class ProgramaNoEncontradoError(ErrorGestionAcademica):
    """El programa académico buscado no existe."""

    def __init__(self, codigo):
        self.codigo = codigo
        super().__init__(f"No existe un programa académico con el código '{codigo}'.")
