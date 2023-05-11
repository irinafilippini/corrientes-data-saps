import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import json

import streamlit as st

import streamlit as st

# Agregar imagen
image = Image.open('..\\corrientes-data\logo-mcc.png')
st.image()
# Agregar título
st.title("S.A.P.S. Corrientes Capital")

# Agregar texto
st.write("En este reporte se intenta...")

# Leer el archivo shapefile de barrios y crear un GeoDataFrame de GeoPandas
barrios = gpd.read_file("..\\corrientes-data\barrios_de_la-ciudad.csv")

for i, row in barrios.iterrows():
    try:
        json.loads(row["st_asgeojson"])
    except json.JSONDecodeError:
        print("Error en el índice", i, row["st_asgeojson"])

barrios = barrios.drop([115, 116, 133, 134, 135, 136, 138])

# Leer el archivo CSV y crear un GeoDataFrame de GeoPandas
saps = gpd.read_file('..\\corrientes-data\vw_saps.csv')

# Crear objetos geométricos a partir de la columna "st_asgeojson"
saps.geometry = saps["st_asgeojson"].apply(json.loads).apply(shape)

# Definir la función para plotear el mapa
def plot_map(column_name):
    # Filtrar los saps que tienen el valor "si" en la columna
    saps = df_saps[df_saps[column_name] == 'si']

    # Crear una lista de coordenadas de los saps
    coords_saps = [[json.loads(x)['coordinates'][1], json.loads(x)['coordinates'][0]] for x in saps['geo_saps']]
    nombres_saps = saps['descripcion'].tolist()

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_aspect('equal')

    # Agregar capa de barrios
    barrios.plot(ax=ax, facecolor='none', edgecolor='black', lw=0.5)

    # Agregar capa de saps y nombres
    for i, coord in enumerate(coords_saps):
        ax.scatter(coord[1], coord[0], s=100, alpha=0.7, c='green', marker='s')
        ax.annotate(nombres_saps[i], xy=(coord[1], coord[0]), xytext=(coord[1]+0.001, coord[0]+0.001), fontsize=10, fontweight='bold')

    # Agregar título al gráfico
    ax.set_title('S.A.P.S. CON TURNOS WEB')

    # Mostrar el gráfico
    st.pyplot(fig)

# Llamar a la función
plot_map('turnos_web')


import streamlit as st
import pandas as pd
import geopandas as gpd
import json
import matplotlib.pyplot as plt

@st.cache
def load_data():
    df_saps = pd.read_csv('..\\corrientes-data\vw_saps.csv')
    return df_saps

@st.cache
def load_map():
    barrios = gpd.read_file('..\\corrientes-data\barrios_de_la-ciudad.csv')
    return barrios

def plot_comparison(column1, column2):
    df_saps = load_data()

    # Filtrar los saps que tienen el valor "si" en las columnas
    saps1 = df_saps[df_saps[column1] == 'si']
    saps2 = df_saps[df_saps[column2] == 'si']

    # Crear listas de coordenadas de los saps
    coords_saps1 = [[json.loads(x)['coordinates'][1], json.loads(x)['coordinates'][0]] for x in saps1['geo_saps']]
    coords_saps2 = [[json.loads(x)['coordinates'][1], json.loads(x)['coordinates'][0]] for x in saps2['geo_saps']]

    # Crear el gráfico principal y los dos sub-gráficos
    fig = plt.figure(figsize=(15, 7))
    ax1 = plt.subplot(121)
    ax2 = plt.subplot(122)
    ax1.set_aspect('equal')
    ax2.set_aspect('equal')

    # Agregar capa de barrios en los tres gráficos
    barrios = load_map()
    barrios.plot(ax=ax1, facecolor='none', edgecolor='black', lw=0.5)
    barrios.plot(ax=ax2, facecolor='none', edgecolor='black', lw=0.5)

    # Agregar capa de saps en los tres gráficos
    ax1.scatter([x[1] for x in coords_saps1], [x[0] for x in coords_saps1], s=100, alpha=0.7, c='green', marker='s', label=column1)
    ax2.scatter([x[1] for x in coords_saps2], [x[0] for x in coords_saps2], s=100, alpha=0.7, c='blue', marker='s', label=column2)

    # Eliminar leyendas en los tres gráficos
    ax1.legend().set_visible(False)
    ax2.legend().set_visible(False)

    # Agregar título al gráfico principal y a los sub-gráficos
    fig.suptitle('Comparación de S.A.P.S. con Turnos Web y Turnos Presenciales')
    ax1.set_title('Turnos Web')
    ax2.set_title('Turnos Presenciales')

    # Mostrar los gráficos
    st.pyplot(fig)

# Mostrar la interfaz de usuario
def main():
    st.title("Comparación de S.A.P.S. con Turnos Web y Turnos Presenciales")
    columnas = ['turnos_web', 'turnos_presenciales']
    columna1 = st.selectbox('Seleccione la primera columna:', columnas)
    columna2 = st.selectbox('Seleccione la segunda columna:', columnas)
    plot_comparison(columna1, columna2)

if __name__ == '__main__':
    main()


# Obtener la cantidad de SAPS y atención por columna
total_saps = len(df_saps)
atencion_turnos_web = len(df_saps[df_saps['turnos_web'] == 'si'])
atencion_turnos_pre = len(df_saps[df_saps['turnos_pre'] == 'si'])

# Crear la tarjeta
card = st.container()
with card:
    st.header(f"Cantidad total de S.A.P.S.: {total_saps}")
    st.subheader("S.A.P.S.:")
    st.write(f"CON TURNOS WEB: {atencion_turnos_web}")
    st.write(f"CON TURNOS PRESENCIALES: {atencion_turnos_pre}")


import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import json

# Lectura de los datos
df_saps = pd.read_csv('datos_saps.csv')
barrios = gpd.read_file('barrios.csv')

def plot_map(column_name):
    # Filtrar los saps que tienen el valor "si" en la columna
    saps = df_saps[df_saps[column_name] == 'si']

    # Crear una lista de coordenadas de los saps
    coords_saps = [[json.loads(x)['coordinates'][1], json.loads(x)['coordinates'][0]] for x in saps['geo_saps']]
    nombres_saps = saps['descripcion'].tolist()

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_aspect('equal')

    # Agregar capa de barrios
    barrios.plot(ax=ax, facecolor='none', edgecolor='black', lw=0.5)

    # Agregar capa de saps y nombres
    for i, coord in enumerate(coords_saps):
        ax.scatter(coord[1], coord[0], s=100, alpha=0.7, c='green', marker='s')
        ax.annotate(nombres_saps[i], xy=(coord[1], coord[0]), xytext=(coord[1]+0.001, coord[0]+0.001), fontsize=10, fontweight='bold')

    # Agregar título al gráfico
    ax.set_title('S.A.P.S. QUE CUENTAN CON ATENCIÓN PSICOLÓGICA')

    # Mostrar el gráfico
    st.pyplot(fig)

st.title('Anexo: Especialidades')
plot_map('psicología')

