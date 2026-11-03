# Estación 1. Comprender el problema y modelar el flujo

Fecha: 3 de noviembre de 2026. Proyecto: **BibliotecaReservas**. Paquete previsto en la guía: `biblioteca`.

Esta estación documenta el análisis antes de programar. Su alcance es el diagrama de flujo, la separación de responsabilidades y la explicación de cohesión y mantenimiento. Las clases se mencionan como responsabilidades previstas por la guía; todavía no se implementan en esta estación.

## Referencia original

Se contrastó el texto con estas dos capturas proporcionadas por el usuario:

- [Captura de pantalla 2026-11-03 103519.png](<fuentes/Captura de pantalla 2026-11-03 103519.png>): comienzo de la estación 1, decisión y pasos 1 a 5; también contiene las reglas funcionales y la estructura prevista del proyecto.
- [Captura de pantalla 2026-11-03 103535.png](<fuentes/Captura de pantalla 2026-11-03 103535.png>): continuación de la estación 1, pasos 6 a 8, actividad y comprobación.

No se detectó una incompatibilidad entre los requisitos de la estación 1. Los pasos, nombres de patrones y decisión se conservan como aparecen en las capturas. Las explicaciones que siguen son el desarrollo de la actividad, no una transcripción de código.

## Transcripción de la estación

**Estación 1. Comprender el problema y modelar el flujo**

Tiempo estimado: 15 minutos.

> Antes de programar, represente el proceso en un diagrama de flujo. Incluya la decisión «¿hay una sala adecuada?».
> Si la respuesta es no, el proceso termina sin crear una reserva confirmada.

1. El estudiante registra los datos de la solicitud.
2. El sistema consulta las salas disponibles.
3. Una estrategia selecciona la sala.
4. Builder construye la reserva y valida los datos.
5. Facade registra y coordina la confirmación.
6. State valida el cambio de estado.
7. Observer comunica el cambio a los suscriptores.
8. El estudiante puede cancelar o finalizar la reserva según su estado.

> Actividad individual: dibuje el flujo y escriba al menos cinco responsabilidades distintas que no deberían quedar concentradas en Main.

> Comprobación: explique por qué una clase Main que consulta salas, valida datos, construye reservas, notifica y controla estados tendría baja cohesión y sería difícil de mantener.

## Diagrama de flujo

- [Fuente editable del diagrama](flujo.mmd).
- [Diagrama en SVG](flujo.svg).
- [Documento PDF para revisión y capturas](../../output/pdf/estacion-01.pdf).

El flujo debe conservar el orden de los ocho pasos. La decisión «¿hay una sala adecuada?» se evalúa después de que la estrategia intenta seleccionar la sala y antes de construir la reserva. La salida **No** termina sin crear una reserva confirmada. La salida **Sí** permite continuar con Builder, Facade, State y Observer.

El paso 8 queda sujeto al estado actual de la reserva. Las reglas generales de la guía permiten Pendiente → Confirmada, Pendiente → Cancelada, Confirmada → Cancelada y Confirmada → Finalizada. Una transición no contemplada se rechaza y no genera notificación. El diagrama representa el proceso; no incorpora una agenda real, persistencia o interfaz gráfica.

## Responsabilidades que deben separarse de Main

Los nombres siguientes corresponden al esquema de archivos de la guía. Esta asignación explica el diseño previsto y no adelanta su implementación.

| Responsabilidad | Clases o interfaces previstas por la guía | Motivo para separarla de Main |
| --- | --- | --- |
| Representar los datos del estudiante y de la sala | `Estudiante`, `Sala` | Los datos y sus invariantes pertenecen a los conceptos del dominio. |
| Consultar las salas disponibles | `RepositorioSalas`, `RepositorioSalasMemoria` | Permite cambiar la fuente de consulta sin reescribir el punto de entrada. |
| Seleccionar una sala según el criterio solicitado | `EstrategiaSeleccionSala`, `SeleccionPorCapacidad`, `SeleccionSalaPreferida` | Cada algoritmo concentra sus reglas de selección y puede intercambiarse mediante el contrato común. |
| Construir la reserva y validar sus datos | `ReservaBuilder` | Centraliza la construcción y las validaciones para evitar repetirlas en Main. |
| Registrar las reservas | `RepositorioReservas`, `RepositorioReservasMemoria` | Aísla el registro de reservas del flujo de presentación. |
| Coordinar consulta, selección, construcción, registro y confirmación | `ReservaFacade` | Ofrece al punto de entrada una operación del caso de uso y oculta el orden de los pasos internos. |
| Controlar las transiciones de estado | `EstadoReserva`, `Pendiente`, `Confirmada`, `Cancelada`, `Finalizada` | Cada estado conserva las operaciones permitidas y rechaza las transiciones inválidas. |
| Comunicar cambios y ejecutar las respuestas de los suscriptores | `ObservadorReserva`, `NotificadorEstudiante`, `RegistroEventos`, `Reserva` | La reserva publica el cambio a través del contrato de observadores y cada suscriptor decide cómo responder. |

`Main` tendrá la responsabilidad de configurar las dependencias y presentar el flujo de la aplicación. No necesita concentrar los algoritmos, la construcción, el almacenamiento, las transiciones y las notificaciones.

## Respuesta a la comprobación

Una clase Main que consulta salas, valida datos, construye reservas, notifica y controla estados reúne tareas que cambian por razones diferentes. Su cohesión sería baja porque sus métodos y decisiones no se concentrarían en una sola responsabilidad: mezclarían el punto de entrada con reglas del dominio, acceso a datos y comunicación de eventos.

Modificar un criterio de selección, una validación o un mensaje de notificación obligaría a editar la misma clase. Esto incrementaría el riesgo de alterar otras partes del flujo, dificultaría localizar las reglas y haría más difícil comprobar cada comportamiento de forma aislada. También favorecería la repetición de validaciones y la acumulación de condicionales.

Separar estas responsabilidades permite mantener cada regla en el componente que le corresponde. Main configura y presenta; los repositorios consultan y registran; Strategy selecciona; Builder construye y valida; Facade coordina; State controla las transiciones; Observer comunica los cambios. Esta división aplica el principio de responsabilidad única y facilita comprender, comprobar y mantener el sistema.

## Comparación con la guía original

| Requisito de la captura | Desarrollo de la estación 1 | Criterio para la revisión |
| --- | --- | --- |
| Representar el proceso antes de programar | Fuente `flujo.mmd`, representación `flujo.svg` y PDF | Revisar un diagrama legible con inicio, proceso, decisión y fin. |
| Incluir «¿hay una sala adecuada?» | Decisión posterior a la selección | Verificar el texto de la decisión y las salidas Sí y No. |
| Si la respuesta es no, terminar sin crear una reserva confirmada | Salida No hacia el fin correspondiente | Verificar que esta salida no pase por construcción, registro o confirmación. |
| Conservar los pasos 1 a 8 | Transcripción anterior y etiquetas del diagrama | Comparar los ocho pasos con las capturas, sin cambiar nombres de patrones. |
| Escribir al menos cinco responsabilidades distintas fuera de Main | Ocho responsabilidades explicadas en la tabla | Revisar que cada responsabilidad tenga un propósito concreto. |
| Explicar baja cohesión y dificultad de mantenimiento | Respuesta a la comprobación | Verificar razones de cambio, efectos sobre mantenimiento y separación propuesta. |
| Trabajar de forma acumulativa y por estación | La estación 1 contiene análisis y documentación | No implementar todavía el dominio ni las estaciones posteriores. |

## Controles y límites de esta estación

- **Comparación textual realizada:** se inspeccionaron visualmente las dos capturas y se transcribieron los ocho pasos, la decisión, la actividad y la comprobación.
- **Revisión de responsabilidades realizada:** la tabla contiene ocho responsabilidades distintas y conserva los nombres del esquema de la guía.
- **Compilación Java:** no aplica a la estación 1; esta estación pide modelar el flujo antes de programar. No se afirma una compilación ni una ejecución de Main.
- **Pruebas de ejecución:** no aplican a este alcance. Las pruebas funcionales P01 a P11 corresponden al desarrollo posterior; todavía no se declaran aprobadas.
- **Revisión visual del PDF y del diagrama:** los resultados reales se documentan por separado al generar y revisar los artefactos.
- **Git y publicación remota:** se verificó la publicación de `estacion-01` en `Alejoms09/Diana-trabajo` y el seguimiento `origin/estacion-01`. Los comandos, hashes y resultados constan en [el registro de verificación](verificacion.txt) y en [la bitácora](../../BITACORA.md).

La [rama publicada para revisión](https://github.com/Alejoms09/Diana-trabajo/tree/estacion-01) contiene esta estación y sus doce archivos, enumerados de forma exacta en la bitácora.

## Capturas que debe tomar el estudiante

1. Abrir el PDF o el SVG en un visor y capturar el diagrama completo: deben leerse los ocho pasos, la decisión, las salidas Sí y No y el fin sin reserva confirmada.
2. Abrir este documento en un visor Markdown y capturar la tabla de responsabilidades.
3. Capturar la respuesta a la comprobación y la tabla de comparación con la guía.
4. Mostrar la carpeta `docs/estacion-01` en el explorador o editor, con sus fuentes y archivos de documentación; mostrar también `output/pdf/estacion-01.pdf`.
5. En una terminal del repositorio, capturar los resultados reales de `git status -sb`, `git branch -vv` y `git log -1 --format=fuller` para identificar la rama, su seguimiento y su commit.
6. Abrir la rama `estacion-01` en `Alejoms09/Diana-trabajo` en GitHub y capturar el nombre de la rama, el commit descriptivo y los archivos publicados.
7. Capturar la bitácora de modificaciones y el registro de comprobaciones de la estación una vez completados con los resultados reales.

No corresponde preparar una captura de ejecución Java en esta estación.

## Punto de revisión obligatorio

Al terminar esta estación se debe detener el trabajo para que el usuario revise las capturas, la documentación, el diagrama y la publicación de su rama. **No se debe pasar a la estación 2 hasta recibir autorización del usuario.** Tampoco se deben integrar las estaciones en `main` antes de la revisión del trabajo final.
