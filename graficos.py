from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.ticker import FuncFormatter

app = Flask(__name__)

# Leer datos
df = pd.read_excel("base_predios.xlsx", engine="openpyxl")

# Crear carpeta para imágenes si no existe
os.makedirs("static/img", exist_ok=True)

# Generar gráficos y guardarlos
def generar_graficos():
    sns.set(style="whitegrid")

    # 1. Histograma del Valor del Avalúo (en millones)
    plt.figure(figsize=(10,6))
    sns.histplot(df["VALOR_AVALUO"] / 1e6, bins=30, kde=True, color='skyblue')
    plt.title("Distribución del Valor del Avalúo")
    plt.xlabel("Valor del Avalúo (Millones de COP)")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig("static/img/grafico_valor_avaluo.png")
    plt.close()

    # 2. Área construida
    plt.figure(figsize=(10,6))
    sns.histplot(df["AREA_CONSTRUIDA"], bins=30, kde=True, color='salmon')
    plt.title("Distribución del Área Construida")
    plt.xlabel("Área Construida (m²)")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig("static/img/grafico_area_construida.png")
    plt.close()

    # 3. Boxplot por estrato
    plt.figure(figsize=(10,6))
    sns.boxplot(x="ESTRATO_PREDIO", y="VALOR_AVALUO", data=df, palette="Set3")
    plt.title("Valor del Avalúo por Estrato")
    plt.xlabel("Estrato")
    plt.ylabel("Valor Avalúo (COP)")
    plt.tight_layout()
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x/1_000_000):,.0f}'))
    plt.savefig("static/img/boxplot_avaluo_estrato.png")
    plt.close()

    # 4. Dispersión área vs avalúo (en millones)
    plt.figure(figsize=(10,6))
    sns.scatterplot(x="AREA_CONSTRUIDA", y=df["VALOR_AVALUO"] / 1e6, hue="ESTRATO_PREDIO", data=df, palette="viridis")
    plt.title("Área Construida vs Valor Avalúo")
    plt.xlabel("Área Construida (m²)")
    plt.ylabel("Valor Avalúo (Millones de COP)")
    plt.tight_layout()
    plt.savefig("static/img/scatter_area_avaluo.png")
    plt.close()

    # 5. Dispersión edad vs avalúo (en millones)
    plt.figure(figsize=(10,6))
    sns.scatterplot(x="EDAD_PREDIO", y=df["VALOR_AVALUO"] / 1e6, hue="ESTRATO_PREDIO", data=df, palette="plasma")
    plt.title("Edad del Predio vs Valor Avalúo")
    plt.xlabel("Edad del Predio (años)")
    plt.ylabel("Valor Avalúo (Millones de COP)")
    plt.tight_layout()
    plt.savefig("static/img/scatter_edad_avaluo.png")
    plt.close()



@app.route('/')
def index():
    generar_graficos()
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
