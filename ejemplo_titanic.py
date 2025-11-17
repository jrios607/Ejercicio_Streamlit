import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Carga de datos
df = pd.read_csv("database_titanic.csv")

# --- LIMPIEZA: Rellenamos edades vacías con el promedio ---
df['Age'] = df['Age'].fillna(df['Age'].mean())

st.write("""
# Mi primera aplicación interactiva
## Gráficos usando la base de datos del Titanic
""")

# 2. Barra Lateral (Sidebar) con CONTROLES
with st.sidebar:
    st.write("# Opciones")
    
    # --- NUEVO CONTROL: Radio Button para filtrar datos ---
    tipo_visualizacion = st.radio(
        "¿Qué grupo deseas analizar?",
        ("Todos los pasajeros", "Solo Sobrevivientes")
    )
    
    # --- CORRECCIÓN SLIDER: Mínimo en 5 para evitar error de división por 0 ---
    div = st.slider('Número de bins (barras):', 5, 50, 10)
    st.write("Bins seleccionados:", div)

# --- LÓGICA DE FILTRADO ---
# Aquí ocurre la "magia". Definimos qué datos usar según el Radio Button.
if tipo_visualizacion == "Solo Sobrevivientes":
    # Filtramos solo los que sobrevivieron (1)
    df_filtrado = df[df['Survived'] == 1]
    titulo_grafico_sexo = "Sobrevivientes por Género (Tarea)"
    color_barra = "green" # Cambiamos color para que se note el cambio
else:
    # Usamos todos los datos
    df_filtrado = df
    titulo_grafico_sexo = "Distribución Total de Pasajeros"
    color_barra = "blue"

# 3. Generación de Gráficos (Usando df_filtrado)
fig, ax = plt.subplots(1, 2, figsize=(10, 4))

# --- Gráfico 1: Histograma de Edades ---
# Nota que usamos df_filtrado, así el histograma también cambia dinámicamente
ax[0].hist(df_filtrado["Age"], bins=div, color='#4CAF50', edgecolor='black')
ax[0].set_xlabel("Edad")
ax[0].set_ylabel("Frecuencia")
ax[0].set_title(f"Edades ({tipo_visualizacion})")

# --- Gráfico 2: Barras por Sexo ---
# Calculamos los conteos basándonos en los datos FILTRADOS
cant_male = len(df_filtrado[df_filtrado["Sex"] == "male"])
cant_female = len(df_filtrado[df_filtrado["Sex"] == "female"])

# Dibujamos
ax[1].bar(["Masculino", "Femenino"], [cant_male, cant_female], color=color_barra)
ax[1].set_xlabel("Sexo")
ax[1].set_ylabel("Cantidad")
ax[1].set_title(titulo_grafico_sexo)

# Desplegamos el gráfico combinado
st.pyplot(fig)

# Tabla de datos
st.write(f"## Muestra de datos: {tipo_visualizacion}")
st.table(df_filtrado.head())
