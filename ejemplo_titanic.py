import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE PÁGINA (Opcional: hace que se vea más ancho) ---
st.set_page_config(page_title="Titanic Dashboard", layout="wide")

# 1. Carga de datos
df = pd.read_csv("database_titanic.csv")

# --- LIMPIEZA ---
df['Age'] = df['Age'].fillna(df['Age'].mean())

st.write("""
# 🚢 Dashboard del Titanic
## Análisis interactivo de sobrevivientes y demografía
""")

# ----------------------------------------------------------
# 2. BARRA LATERAL (SIDEBAR) - FILTROS
# ----------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Filtros de Datos")
    
    # A. Filtro por Estado (Sobreviviente o No)
    tipo_visualizacion = st.radio(
        "Mostrar datos de:",
        ("Todos los pasajeros", "Solo Sobrevivientes", "Solo Fallecidos")
    )
    
    # B. Filtro por Rango de Edad (Slider Doble)
    # value=(0, 80) define los puntos iniciales de los dos selectores
    rango_edad = st.slider(
        "Selecciona el rango de edad:",
        min_value=0, 
        max_value=80, 
        value=(0, 80)
    )
    
    st.markdown("---") # Separador visual
    
    # C. Configuración del Gráfico
    st.write("🎨 Configuración de Gráficos")
    div = st.slider('Número de bins (barras del histograma):', 5, 50, 15)


# ----------------------------------------------------------
# 3. LÓGICA DE FILTRADO (EL MOTOR)
# ----------------------------------------------------------

# Paso 1: Filtrar por Sobrevivencia
if tipo_visualizacion == "Solo Sobrevivientes":
    df_temp = df[df['Survived'] == 1]
    color_main = "#4CAF50" # Verde
elif tipo_visualizacion == "Solo Fallecidos":
    df_temp = df[df['Survived'] == 0]
    color_main = "#FF5252" # Rojo
else:
    df_temp = df
    color_main = "#2196F3" # Azul

# Paso 2: Filtrar por Rango de Edad (Usando el resultado del paso 1)
# rango_edad es una tupla, ej: (20, 40). rango_edad[0] es 20, rango_edad[1] es 40
df_filtrado = df_temp[(df_temp['Age'] >= rango_edad[0]) & (df_temp['Age'] <= rango_edad[1])]


# ----------------------------------------------------------
# 4. VISUALIZACIÓN (KPIs y GRÁFICOS)
# ----------------------------------------------------------

# --- KPIs (Indicadores Clave) ---
# Usamos columnas para mostrar números grandes arriba
col1, col2, col3 = st.columns(3)
col1.metric("Total Pasajeros Mostrados", len(df_filtrado))
col2.metric("Edad Promedio", f"{df_filtrado['Age'].mean():.1f} años")
col3.metric("Rango Edad Seleccionado", f"{rango_edad[0]} - {rango_edad[1]} años")

# --- GRÁFICOS ---
st.subheader("📊 Visualización de Datos")

# Creamos el espacio para gráficos
fig, ax = plt.subplots(1, 2, figsize=(12, 5)) # Un poco más ancho

# Gráfico 1: Histograma
ax[0].hist(df_filtrado["Age"], bins=div, color=color_main, edgecolor='white', alpha=0.8)
ax[0].set_xlabel("Edad")
ax[0].set_ylabel("Frecuencia")
ax[0].set_title(f"Distribución de Edades ({tipo_visualizacion})")
ax[0].grid(axis='y', linestyle='--', alpha=0.5) # Rejilla suave de fondo

# Gráfico 2: Barras por Sexo
cant_male = len(df_filtrado[df_filtrado["Sex"] == "male"])
cant_female = len(df_filtrado[df_filtrado["Sex"] == "female"])

barras = ax[1].bar(["Masculino", "Femenino"], [cant_male, cant_female], color=["#3F51B5", "#E91E63"])
ax[1].set_ylabel("Cantidad")
ax[1].set_title('Distribución por Género')
ax[1].bar_label(barras) # Pone el número exacto encima de la barra

st.pyplot(fig)

# ----------------------------------------------------------
# 5. DISPLAY DE DATOS (ESTÉTICO)
# ----------------------------------------------------------
st.subheader("📋 Detalle de Pasajeros")
st.caption("Usa las flechas en los encabezados para ordenar la tabla.")

# st.dataframe es mucho más poderoso que st.table
st.dataframe(
    df_filtrado,
    use_container_width=True, # Se estira al ancho de la pantalla
    height=300, # Altura fija con scroll
    hide_index=True # Ocultamos el índice numérico (0,1,2...) que a veces molesta
)
