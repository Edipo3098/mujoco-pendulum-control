# Entorno de desarrollo en Windows

Estado documentado el 16 de noviembre de 2026 a partir de las salidas de terminal y las comprobaciones compartidas por el autor.

## Arquitectura del proyecto

- Simulación y controladores en C++ con MuJoCo.
- MuJoCo Studio para inspeccionar y probar modelos.
- Python para gráficas y análisis de resultados.
- El modelo del carro-péndulo será creado por el autor en `models/`.

## Herramientas comprobadas

| Componente | Versión / estado |
| --- | --- |
| Sistema | Windows 11; versión de sistema mostrada: 10.0.26200.9911 |
| Arquitectura de destino | x64 (AMD64) |
| MuJoCo / Studio | Distribución mujoco-4.0.1-windows-x86_64 |
| Archivos de desarrollo MuJoCo | Cabeceras en include/mujoco, mujoco.lib y mujoco.dll confirmados por el autor |
| Visual Studio Build Tools | 2026, Developer Command Prompt v18.12.0 |
| Compilador elegido | MSVC 19.52.37029 para x64 |
| CMake de Visual Studio | 4.3.1-msvc1 |
| Ninja | 1.13.2, comprobado en C:\Program Files\CMake\bin\ninja.exe |
| Python | CPython 3.14.10, AMD64, 64 bits, variante convencional (free-threaded: False) |
| pip | 26.2.2, asociado a Python 3.14 |
| venv | Módulo disponible; no se ha confirmado la creación de un entorno para este proyecto |
| Git | 2.45.1.windows.1 |

Windows SDK se seleccionó durante la preparación de Build Tools; su instalación efectiva y versión deben confirmarse con una compilación. No se ha confirmado la instalación de clang-tidy.

## Selección de herramientas

Para compilar se utilizará la terminal **x64 Native Tools Command Prompt for VS**. La salida compartida confirma que el entorno se inicializa para x64 y que `cl` está disponible.

Existen varias instalaciones de CMake. El comando simple `cmake --version` estaba seleccionando CMake 3.28.1 de STM32CubeCLT. Para este proyecto se ha identificado explícitamente el CMake de Visual Studio; no debe asumirse que el primero del PATH sea el elegido.

Comprobaciones de consulta en CMD:

```bat
cl
where cmake
"C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe" --version
"C:\Program Files\CMake\bin\ninja.exe" --version
```

Las rutas anteriores corresponden al equipo revisado y pueden variar en otros equipos. La futura configuración CMake deberá seleccionar de forma coherente compilador, generador y herramienta de construcción.

El antiguo MinGW GCC 6.3.0 de `C:\MinGW\bin`, cuyo destino es `mingw32`, no es el compilador elegido. No se ha confirmado su retirada. La herramienta Arm GNU Toolchain utilizada para microcontroladores es independiente y debe conservarse si otros proyectos la necesitan.

## Python

El intérprete comprobado está en:

```text
C:\Users\fporras\AppData\Local\Programs\Python\Python314\python.exe
```

Cuando existan scripts de análisis, se utilizará pip dentro de un venv propio, sin `--system-site-packages`. Todavía no hay dependencias Python fijadas ni una instalación de paquetes validada para este proyecto.

La arquitectura elegida no requiere pybind11 ni los bindings Python de MuJoCo para ejecutar la simulación C++.

## Alcance de la validación

Las versiones y la presencia de archivos están comprobadas; esto no equivale a una compilación o simulación validada.

Pendiente:

- Crear el modelo MJCF del carro-péndulo y documentar parámetros, unidades y coordenadas.
- Preparar CMake y el primer ejecutable C++.
- Comprobar compilación, enlace con MuJoCo y carga de la DLL.
- Ejecutar movimiento pasivo y registrar estados.
- Implementar las pruebas físicas descritas en tests/README.md.

La versión mínima de CMake, el estándar C++, las opciones de enlace y las instrucciones de ejecución se fijarán al incorporar la primera implementación. No hay resultados de compilación ni pruebas del proyecto que declarar todavía.
