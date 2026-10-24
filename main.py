import re
from datetime import datetime
from pathlib import Path


# ============================================================
# DECISIONES DEL ESTUDIANTE
# ============================================================
# 1. Una línea válida debe comenzar con un nivel reconocido:
#    [INFO], [WARNING] o [ERROR].
#
# 2. La fecha es opcional, pero si aparece debe tener el formato
#    YYYY-MM-DD y además representar una fecha real.
#
# 3. Una línea se considera mal formada cuando:
#    - Está vacía.
#    - No contiene un nivel de severidad válido.
#    - No contiene mensaje después del nivel/fecha.
#    - Contiene una fecha con forma YYYY-MM-DD pero la fecha no existe.
#
# 4. Las líneas mal formadas se cuentan en el total de eventos
#    porque forman parte del archivo analizado, pero también se
#    registran por separado como inconsistencias.
#
# 5. Si una línea tiene nivel válido y mensaje, pero no tiene fecha,
#    se acepta como evento válido "sin fecha".
# ============================================================


NIVELES_VALIDOS = ("INFO", "WARNING", "ERROR")

# La expresión regular ayuda a separar:
# [NIVEL] + fecha opcional + mensaje.
PATRON_LINEA = re.compile(
    r"^\[(INFO|WARNING|ERROR)\]\s+"
    r"(?:(\d{4}-\d{2}-\d{2})\s+)?"
    r"(.+?)\s*$"
)


def fecha_es_valida(fecha_texto):
    """Devuelve True si la fecha existe y usa el formato YYYY-MM-DD."""
    if not fecha_texto:
        return True

    try:
        datetime.strptime(fecha_texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def analizar_linea(linea):
    """
    Analiza una línea individual.

    Retorna un diccionario para mantener clara la información
    encontrada y evitar mezclar validación con presentación.
    """
    contenido = linea.strip()

    if not contenido:
        return {
            "valida": False,
            "nivel": None,
            "tiene_fecha": False,
            "motivo": "Línea vacía"
        }

    coincidencia = PATRON_LINEA.match(contenido)

    if not coincidencia:
        return {
            "valida": False,
            "nivel": None,
            "tiene_fecha": False,
            "motivo": "Formato incompleto o nivel de severidad inválido"
        }

    nivel, fecha, mensaje = coincidencia.groups()

    if not mensaje.strip():
        return {
            "valida": False,
            "nivel": nivel,
            "tiene_fecha": bool(fecha),
            "motivo": "Falta el mensaje del evento"
        }

    if fecha and not fecha_es_valida(fecha):
        return {
            "valida": False,
            "nivel": nivel,
            "tiene_fecha": True,
            "motivo": f"Fecha inválida: {fecha}"
        }

    return {
        "valida": True,
        "nivel": nivel,
        "tiene_fecha": bool(fecha),
        "motivo": None
    }


def analizar_archivo(ruta_archivo):
    """Lee el archivo completo y genera las estadísticas solicitadas."""
    resumen = {
        "total_eventos": 0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "lineas_mal_formadas": 0,
        "eventos_con_fecha": 0,
        "eventos_sin_fecha": 0,
        "detalles_errores": []
    }

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):
            resumen["total_eventos"] += 1
            resultado = analizar_linea(linea)

            if resultado["valida"]:
                resumen[resultado["nivel"]] += 1

                if resultado["tiene_fecha"]:
                    resumen["eventos_con_fecha"] += 1
                else:
                    resumen["eventos_sin_fecha"] += 1
            else:
                resumen["lineas_mal_formadas"] += 1
                resumen["detalles_errores"].append(
                    f"Línea {numero_linea}: {resultado['motivo']}"
                )

    return resumen


def mostrar_resumen(resumen, nombre_archivo):
    """Muestra en consola un resultado fácil de leer."""
    print("\n" + "=" * 55)
    print("           RESUMEN DEL ANÁLISIS DE LOGS")
    print("=" * 55)
    print(f"Archivo analizado       : {nombre_archivo}")
    print(f"Total de líneas/eventos : {resumen['total_eventos']}")
    print("-" * 55)
    print(f"INFO                    : {resumen['INFO']}")
    print(f"WARNING                 : {resumen['WARNING']}")
    print(f"ERROR                   : {resumen['ERROR']}")
    print("-" * 55)
    print(f"Eventos con fecha válida: {resumen['eventos_con_fecha']}")
    print(f"Eventos sin fecha       : {resumen['eventos_sin_fecha']}")
    print(f"Líneas mal formadas     : {resumen['lineas_mal_formadas']}")

    if resumen["detalles_errores"]:
        print("\nDetalle de inconsistencias:")
        for detalle in resumen["detalles_errores"]:
            print(f"  - {detalle}")

    print("=" * 55)


def solicitar_archivo():
    """
    Solicita al usuario la ruta del archivo.
    Se usa entrada por consola para mantener el proyecto simple,
    portable y sin dependencias adicionales.
    """
    while True:
        ruta_texto = input(
            "\nIngrese la ruta del archivo .txt a analizar "
            "(o escriba 'salir'): "
        ).strip().strip('"')

        if ruta_texto.lower() == "salir":
            return None

        ruta = Path(ruta_texto)

        if not ruta.exists():
            print("Advertencia: el archivo no existe. Intente nuevamente.")
            continue

        if not ruta.is_file():
            print("Advertencia: la ruta indicada no corresponde a un archivo.")
            continue

        if ruta.suffix.lower() != ".txt":
            print("Advertencia: para esta actividad se requiere un archivo .txt.")
            continue

        return ruta


def main():
    print("=" * 55)
    print("        ANALIZADOR DE LOGS EN PYTHON")
    print("=" * 55)

    ruta = solicitar_archivo()

    if ruta is None:
        print("Programa finalizado por el usuario.")
        return

    try:
        resumen = analizar_archivo(ruta)
        mostrar_resumen(resumen, ruta.name)
    except UnicodeDecodeError:
        print(
            "Error: no fue posible leer el archivo con codificación UTF-8."
        )
    except OSError as error:
        print(f"Error al leer el archivo: {error}")


if __name__ == "__main__":
    main()
