# Bitácora de modificaciones

## 03/11/2026 - Estación 1

**Rama de trabajo:** `estacion-01`. **Remoto autorizado:** `https://github.com/Alejoms09/Diana-trabajo.git`.

### Preparación

Se detectó que la carpeta original heredaba un repositorio del Escritorio cuyo remoto era `AlejoFx`. Se creó un clon independiente del remoto solicitado en `BibliotecaReservas/`. El remoto estaba vacío. Se conservó el repositorio heredado y los cinco archivos Java vacíos preexistentes fuera del clon, sin modificarlos. No se creó ni integró trabajo en `main`.

### Desarrollo frente a la guía

Se inspeccionaron las capturas originales `103519.png` y `103535.png` antes de desarrollar la estación. Se copiaron sin modificaciones para permitir la comparación. La estación 1 solicita análisis antes de programar: se elaboraron el diagrama con ocho pasos, la decisión «¿hay una sala adecuada?», la salida No sin reserva confirmada, la separación de responsabilidades y la explicación de cohesión de Main.

El Markdown contiene ocho responsabilidades; el PDF desarrolla siete, ambas cantidades superan las cinco exigidas. Las explicaciones son desarrollo de la actividad. Los ocho pasos y la decisión se transcriben literalmente. No hay código explícito de estación 1 que deba transcribirse ni discrepancias que requieran corregirlo. Las notas del flujo conservan las transiciones y la ausencia de notificaciones ante un rechazo indicadas por las reglas generales.

### Archivos creados (lista exacta)

1. `.gitattributes`
2. `.gitignore`
3. `BITACORA.md`
4. `README.md`
5. `docs/estacion-01/estacion-01.md`
6. `docs/estacion-01/flujo.mmd`
7. `docs/estacion-01/flujo.svg`
8. `docs/estacion-01/fuentes/Captura de pantalla 2026-11-03 103519.png`
9. `docs/estacion-01/fuentes/Captura de pantalla 2026-11-03 103535.png`
10. `docs/estacion-01/verificacion.txt`
11. `output/pdf/estacion-01.pdf`
12. `scripts/generar_documentacion_estacion_01.py`

No se modificaron archivos anteriores del proyecto, porque el repositorio remoto estaba vacío. Los archivos temporales de renderizado y comprobación están en `tmp/`, excluidos de Git. El generador es una herramienta documental, separada del futuro proyecto Java sin dependencias externas.

### Comprobaciones realizadas

- Se generaron el SVG y un PDF de dos páginas con ReportLab 5.1.0.
- Se renderizaron las dos páginas con PyMuPDF, porque Poppler no está disponible en PATH; se inspeccionaron ambas visualmente y en una revisión independiente. No se detectaron cortes ni solapamientos.
- Se contrastaron los ocho pasos y la decisión en Markdown, Mermaid, SVG y texto del PDF. Se comprobó la salida No terminal antes de Builder.
- Se revisaron las responsabilidades, la explicación de cohesión y los enlaces relativos. El primer control de enlaces detectó que aún faltaba crear el registro de verificación; se completó y se repitió el control antes del commit.
- Se verificó la identidad de las dos copias de las capturas mediante SHA-256. Los resultados exactos están en `docs/estacion-01/verificacion.txt`.
- Se comprobó la ausencia de archivos Java dentro del clon. Se detectaron JDK y javac 17.0.18; no se ejecutó una compilación Java ni las pruebas P01-P11, porque no aplican a esta estación documental.
- Se ejecuta `git diff --cached --check` antes de crear el commit. La publicación y el seguimiento se registran tras realizarse, sin afirmar anticipadamente su resultado.

### Control de avance

La estación 1 se entrega para revisión del diagrama, documentación y evidencias. Las estaciones `estacion-02` a `estacion-08` están pendientes de autorización y se desarrollarán acumulativamente, con commit propio, publicación y verificación del seguimiento en cada estación. No se ha desarrollado ninguna de ellas. No avanzar a estación 2 sin autorización ni integrar en `main` antes de revisar el trabajo final.
