"""Funciones de apoyo reutilizables para el análisis exploratorio (EDA).

Son funciones genéricas: no dependen de los nombres de las columnas de este
proyecto, así que se pueden usar con cualquier DataFrame.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def resumen_nulos(datos):
    """Devuelve el número y el porcentaje de nulos de las columnas que tienen alguno."""
    nulos = datos.isnull().sum()
    nulos = nulos[nulos > 0]
    tabla = pd.DataFrame({
        "nulos": nulos,
        "porcentaje": (nulos / len(datos) * 100).round(2),
    })
    return tabla.sort_values("porcentaje", ascending=False)


def explorar_dataframe(datos, nombre="DataFrame"):
    """Primer vistazo a un DataFrame: tamaño, duplicados, tipos y nulos."""
    print(f"========== {nombre} ==========")
    print("Filas y columnas:", datos.shape)
    print("Filas duplicadas:", datos.duplicated().sum())
    print("\nTipos de dato:")
    print(datos.dtypes)
    print("\nNulos:")
    nulos = resumen_nulos(datos)
    if nulos.empty:
        print("No hay nulos")
    else:
        print(nulos)
    print()


def mostrar_recuentos(datos, columnas):
    """Muestra el recuento de valores (incluidos los nulos) de cada columna."""
    for col in columnas:
        print(datos[col].value_counts(dropna=False))
        print("-" * 40)


def tasa_exito(datos, columna, objetivo="y"):
    """Devuelve el número de registros y la tasa de éxito (%) de cada categoría.

    La columna objetivo debe valer 1 (éxito) o 0 (fracaso).
    """
    tabla = datos.groupby(columna, observed=True)[objetivo].agg(["count", "mean"])
    tabla["mean"] = (tabla["mean"] * 100).round(1)
    tabla = tabla.rename(columns={"count": "registros", "mean": "tasa_exito_%"})
    return tabla.sort_values("tasa_exito_%", ascending=False)


def grafico_tasa(datos, columna, titulo, ruta_archivo, objetivo="y",
                 min_registros=100, orden_natural=False):
    """Barras horizontales con la tasa de éxito de cada categoría y la media global.

    Se excluyen las categorías con menos de min_registros (no son representativas).
    Con orden_natural=True se respeta el orden de las categorías en lugar de ordenar por tasa.
    """
    tabla = tasa_exito(datos, columna, objetivo)
    tabla = tabla[tabla["registros"] >= min_registros]
    if orden_natural:
        tabla = tabla.sort_index()

    media_global = datos[objetivo].mean() * 100

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=tabla["tasa_exito_%"], y=tabla.index.astype(str), color="steelblue", ax=ax)
    ax.axvline(media_global, color="red", linestyle="--",
               label=f"Media global ({media_global:.1f} %)")

    ax.set_title(titulo)
    ax.set_xlabel("Tasa de éxito (%)")
    ax.set_ylabel("")
    ax.legend(loc="best")

    plt.tight_layout()
    plt.savefig(ruta_archivo, dpi=100)
    plt.show()