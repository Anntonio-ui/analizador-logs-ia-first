# Reflexión técnica — Uso de IA como herramienta de apoyo

## 1. Uso de Inteligencia Artificial durante el desarrollo

Durante el desarrollo del analizador de logs utilicé Inteligencia Artificial como una herramienta de apoyo, principalmente para consultar posibles formas de organizar el código, comprender el funcionamiento de algunos bloques y revisar alternativas de validación.

La IA fue útil para sugerir una expresión regular capaz de separar el nivel de severidad, una fecha opcional y el mensaje de cada evento. También se utilizó para revisar la estructura general del programa y recomendar la separación del código en funciones pequeñas, por ejemplo una función para analizar cada línea, otra para validar fechas, otra para procesar el archivo completo y otra para mostrar los resultados.

Sin embargo, no se delegó a la IA la decisión de qué debía considerarse correcto o incorrecto. Esas reglas fueron definidas como parte del criterio técnico del desarrollador.

## 2. Decisiones tomadas por el estudiante

Decidí que solamente se reconocerían como niveles válidos `INFO`, `WARNING` y `ERROR`, porque son los únicos requeridos por la actividad.

También decidí que la fecha sería opcional. Esto se debe a que uno de los ejemplos proporcionados en la actividad muestra un evento `WARNING` sin fecha, por lo que consideré incorrecto rechazar automáticamente toda línea que no tuviera marca de tiempo.

Cuando una fecha sí aparece, decidí exigir dos condiciones: que tenga la estructura `YYYY-MM-DD` y que además corresponda a una fecha real. Por ejemplo, `2025-02-30` tiene una apariencia correcta, pero representa una fecha inexistente.

Otra decisión fue contar las líneas mal formadas dentro del total de eventos analizados, porque físicamente forman parte del archivo recibido. Sin embargo, esas líneas no se suman a los contadores de `INFO`, `WARNING` o `ERROR` válidos.

También decidí que una línea vacía, una línea con nivel desconocido y una línea sin mensaje se consideran inconsistencias.

## 3. Ejemplo de una sugerencia de IA que fue mejorada

Una primera alternativa sugerida con apoyo de IA fue validar la fecha únicamente mediante una expresión regular similar a:

```text
\d{4}-\d{2}-\d{2}
```

La expresión permite comprobar que existe una estructura parecida a `2025-01-10`, pero detecté que era insuficiente porque también aceptaría valores como `2025-02-30` o `2025-13-01`.

Para corregirlo decidí conservar la expresión regular únicamente para identificar el texto que parece una fecha y posteriormente utilizar:

```python
datetime.strptime(fecha_texto, "%Y-%m-%d")
```

De esta manera el programa verifica no solamente el formato, sino también que la fecha realmente exista.

Este cambio demuestra que una sugerencia de IA puede ser técnicamente útil, pero todavía debe ser evaluada antes de incorporarla al código final.

## 4. Casos borde considerados

El programa contempla los siguientes casos:

- Archivo inexistente.
- Ruta que no corresponde a un archivo.
- Archivo que no tiene extensión `.txt`.
- Línea vacía.
- Nivel de severidad desconocido.
- Ausencia de fecha.
- Fecha con estructura correcta pero valor imposible.
- Ausencia de mensaje.
- Error de lectura por codificación.
- Error del sistema operativo durante la lectura.

No se implementaron formatos de fecha diferentes a `YYYY-MM-DD`, niveles adicionales como `DEBUG` o `CRITICAL`, ni análisis de archivos binarios, porque están fuera del alcance definido para esta actividad.

## 5. Aprendizaje obtenido

La principal conclusión es que la Inteligencia Artificial puede acelerar el desarrollo y ayudar a encontrar soluciones, pero no debe reemplazar el criterio del programador.

En este ejercicio resultó especialmente útil para proponer estructuras, expresiones regulares y explicaciones. Sin embargo, fue necesario revisar cada propuesta y compararla con los requisitos de la actividad.

Aprendí que utilizar IA correctamente no significa aceptar automáticamente el código generado. El desarrollador debe comprender para qué sirve cada bloque, probar el comportamiento, detectar casos no contemplados y decidir conscientemente qué reglas forman parte de la solución.

Por lo tanto, la responsabilidad final sobre el comportamiento, las validaciones y la calidad del programa continúa siendo humana.
