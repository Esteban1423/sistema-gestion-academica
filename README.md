# Universidad de Manizales
## Facultad de Ciencias e Ingeniería · Programación I

### Taller: Sistema de Gestión Académica con Programación Orientada a Objetos (POO) en Python

---

## Integrantes

| # | Nombre completo | Código |
|---|-----------------|--------|
| 1 | Juan Esteban Romero Mosquera| 82202524107 |


**Docente:** Natalia Marcela Castellano Gomez
**Fecha de entrega:** 18/10/2026

---

## 1. Descripción general

Esta es la primera versión de un **Sistema de Gestión Académica**. Todas las clases forman un único sistema: cada parte se conecta con las demás.

- Un **Programa Académico** (por ejemplo, Ingeniería de Sistemas y Telecomunicaciones) pertenece a una facultad y tiene un número de semestres.
- Cada **Asignatura** pertenece a un programa académico y tiene un número de créditos.
- Las **Personas** de la universidad se dividen en tres roles:
  - **Estudiante**: está matriculado en un programa, cursa un semestre, tiene un promedio e inscribe asignaturas.
  - **Docente**: pertenece a una facultad, tiene un tipo de contratación y unas horas semanales, y dicta asignaturas.
  - **Administrativo**: trabaja en una dependencia con un cargo y una jornada.

El sistema valida los datos en el momento en que se asignan. Si un valor es inválido, se lanza un `ValueError` con un mensaje claro y el objeto conserva su valor anterior.

---

## 2. Estructura de archivos

```
programacion_1/
├── modelos.py   # Clases del sistema: Persona, Estudiante, Docente, Administrativo,
│                #   ProgramaAcademico y Asignatura (con sus validaciones)
├── main.py      # Programa principal con todas las pruebas del sistema
├── README.md    # Este documento
└── .gitignore   # Archivos que Git debe ignorar (__pycache__, etc.)
```

### Diagrama de clases (simplificado)

```
                 ┌───────────────────────────┐
                 │          Persona          │
                 │---------------------------│
                 │ _identificacion           │
                 │ _nombre                   │
                 │ _correo                   │
                 │---------------------------│
                 │ mostrar_informacion()     │
                 │ realizar_actividad_       │
                 │   principal()             │
                 └─────────────┬─────────────┘
           ┌───────────────────┼────────────────────┐
┌──────────┴─────────┐ ┌───────┴────────────┐ ┌─────┴──────────────┐
│     Estudiante     │ │      Docente       │ │   Administrativo   │
│--------------------│ │--------------------│ │--------------------│
│ _codigo_estudiantil│ │ _numero_empleado   │ │ _numero_empleado   │
│ _programa ─────────┼┐│ _facultad          │ │ _dependencia       │
│ _semestre          │││ _tipo_contratacion │ │ _cargo             │
│ _promedio          │││ _horas_semanales   │ │ _jornada           │
└────────────────────┘│└────────────────────┘ └────────────────────┘
                      │
   ┌──────────────────┴───┐        ┌──────────────────────┐
   │  ProgramaAcademico   │◄───────│      Asignatura      │
   │----------------------│        │----------------------│
   │ _codigo, _nombre     │        │ _codigo, _nombre     │
   │ _facultad            │        │ _creditos            │
   │ _numero_semestres    │        │ _programa            │
   └──────────────────────┘        └──────────────────────┘
```

---

## 3. Cómo ejecutar el proyecto

**Requisito:** Python 3.8 o superior. No se necesitan librerías externas.

1. Abra una terminal en la carpeta del proyecto.
2. Ejecute:

   ```bash
   python main.py
   ```

   (En algunos sistemas el comando es `python3 main.py`.)

El programa muestra cinco secciones de pruebas:

1. Creación de programas académicos y asignaturas.
2. Creación de 6 personas (2 estudiantes, 2 docentes y 2 administrativos).
3. Modificaciones válidas mediante *setters*.
4. Intentos de asignar valores inválidos (correo vacío, semestres ≤ 0, créditos ≤ 0 y promedio fuera de rango), mostrando el mensaje de validación de cada uno.
5. Recorrido polimórfico de la lista de personas con un único ciclo `for`.

---

## 4. Conceptos de POO aplicados

### 4.1 Encapsulamiento

Los atributos de todas las clases usan el prefijo `_` (por ejemplo, `_correo` o `_creditos`). Por convención en Python, ese prefijo indica que el atributo es **protegido**: no debe modificarse directamente desde fuera de la clase.

El acceso se hace con **propiedades** (`@property`), que cumplen el papel de *getters* y *setters*:

```python
@property
def correo(self):              # getter
    return self._correo

@correo.setter
def correo(self, valor):       # setter con validación
    correo = _validar_texto(valor, "correo")
    if "@" not in correo:
        raise ValueError(...)
    self._correo = correo
```

El constructor (`__init__`) también asigna los valores a través de los setters. Por eso es imposible crear un objeto con datos inválidos. Algunas validaciones del sistema:

| Clase | Validación |
|-------|-----------|
| `Persona` | Identificación y nombre no vacíos. El correo no puede estar vacío y debe contener `@`. |
| `ProgramaAcademico` | `numero_semestres` debe ser un entero mayor que 0. |
| `Asignatura` | `creditos` debe ser un entero mayor que 0. |
| `Estudiante` | El semestre debe estar entre 1 y el número de semestres del programa. El promedio debe estar entre 0.0 y 5.0. |
| `Docente` | `horas_semanales` debe ser un entero mayor que 0. |

Las listas internas (asignaturas inscritas o a cargo) se exponen como **copias**. Así, quien las lea no puede alterar el estado interno del objeto.

### 4.2 Herencia

`Estudiante`, `Docente` y `Administrativo` **heredan** de `Persona`:

```python
class Estudiante(Persona):
    def __init__(self, identificacion, nombre, correo, codigo_estudiantil, programa, semestre, promedio):
        super().__init__(identificacion, nombre, correo)   # reutiliza la clase base
        self.codigo_estudiantil = codigo_estudiantil
        ...
```

Gracias a la herencia, los atributos comunes (identificación, nombre y correo), sus validaciones y sus propiedades se escriben **una sola vez** en `Persona`. Cada subclase solo agrega lo que la hace diferente.

### 4.3 Sobreescritura (*override*)

Cada subclase **redefine** `mostrar_informacion()`. Primero llama a la versión de la clase padre con `super()` para imprimir los datos generales y luego agrega sus datos propios:

```python
def mostrar_informacion(self):
    print("[DOCENTE]")
    super().mostrar_informacion()          # datos generales (Persona)
    print(f"  Facultad: {self._facultad}")  # datos específicos
    ...
```

`realizar_actividad_principal()` también se sobreescribe. En `Persona` se define pero lanza `NotImplementedError`, porque cada rol debe implementar su propia actividad:

- **Estudiante** → estudia para sus asignaturas.
- **Docente** → dicta clase de sus asignaturas.
- **Administrativo** → gestiona trámites en su dependencia.

### 4.4 Polimorfismo

En `main.py` se crea **una única lista heterogénea** con objetos de los tres tipos. Se recorre con **un solo ciclo `for`**:

```python
personas = [est1, doc1, adm1, est2, doc2, adm2]

for persona in personas:
    persona.mostrar_informacion()
    persona.realizar_actividad_principal()
```

No se usa `isinstance()`, ni condicionales por tipo, ni ciclos separados. Todos los objetos responden a los mismos mensajes (`mostrar_informacion()` y `realizar_actividad_principal()`), y Python ejecuta automáticamente la versión del método que corresponde a la clase real de cada objeto. Esto es el **polimorfismo**: una misma instrucción produce comportamientos distintos según el objeto que la recibe.

---

## 5. Declaración del uso de herramientas de Inteligencia Artificial

En cumplimiento de los lineamientos institucionales de la Universidad de Manizales sobre el uso ético y transparente de la Inteligencia Artificial en las actividades académicas, los integrantes del grupo declaran lo siguiente:

| Aspecto | Detalle |
|--------|---------|
| **Herramienta utilizada** | Claude (Anthropic), mediante Claude Code |
| **Fecha de uso** | ____ / ____ / ________ |
| **Propósito** | Apoyo en la generación de la estructura inicial del código (`modelos.py`, `main.py`) y en la redacción de este documento `README.md`. |
| **Instrucción (prompt) principal** | Se solicitó construir un sistema de gestión académica en Python que aplicara encapsulamiento, herencia, sobreescritura y polimorfismo, según los requerimientos del taller. |
| **Revisión humana** | Los integrantes revisaron, ejecutaron y comprendieron el código generado, y verificaron que cumpliera cada requerimiento del enunciado. *(Describan aquí las modificaciones que hicieron por cuenta propia.)* |

Los integrantes declaran que:

1. Comprenden el funcionamiento de todo el código entregado y pueden explicarlo y sustentarlo.
2. La herramienta de IA se usó como **apoyo al aprendizaje** y no como sustituto del trabajo académico propio.
3. Asumen la responsabilidad total por el contenido de esta entrega.

> **Nota para los integrantes:** antes de entregar, consulten los lineamientos vigentes de la Universidad y del docente del curso sobre el uso de IA, y ajusten esta sección si exigen un formato específico.

**Firmas de los integrantes:**

- _______________________
- _______________________
- _______________________
