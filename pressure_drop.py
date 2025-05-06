import streamlit as st
import numpy as np
import pandas as pd
from functions import friction_factor, pressure_loss, reynolds

st.title('Calculadora de caída de presión')

# Inicializar la tabla
if 'tabla' not in st.session_state:
    columnas = {
        'Flujo\n[m³/s]': [],
        'Velocidad\n[m/s]': [],
        'Densidad\n[kg/m³]': [],
        'Viscosidad\n[Pa·s]': [],
        'Factor de fricción\n[-]': [],
        'Caída de presión\n[Pa]': []
    }
    st.session_state.tabla = pd.DataFrame(columnas)

# Formulario para agregar registro
st.subheader("Agregar registro")
with st.form("formulario"):
    # Entradas
    flujo = float(st.text_input('Flujo en m³/s:', value='0.121'))
    diametro = float(st.text_input('Diámetro en mm:', value='243'))
    densidad = float(st.text_input('Densidad del fluido (kg/m³):', value='1000'))
    viscosidad = float(st.text_input('Viscosidad del fluido (Pa·s):', value='0.00047'))
    rugosidad = float(st.text_input('Rugosidad de la tubería (mm):', value='0.046'))
    longitud = float(st.text_input('Longitud de la tubería (m):', value='100'))

    # Cálculos
    area = np.pi * ((diametro / 2000) ** 2)  # diámetro a metros y dividido por 2
    velocidad = flujo / area
    Re = reynolds(densidad, velocidad, diametro, viscosidad)
    friccion = friction_factor(diametro, Re, rugosidad)
    pressure_drop_m = pressure_loss(friccion, diametro, longitud, velocidad)
    pressure_drop_Pa = pressure_drop_m * densidad * 9.81  # Conversión a pascales

    # Resultados
    st.write(f'🔹 Velocidad: {velocidad:.3f} m/s')
    st.write(f'🔹 Número de Reynolds: {Re:.0f}')
    st.write(f'🔹 Factor de fricción: {friccion:.5f}')
    st.write(f'🔹 Caída de presión: {pressure_drop_m:.2f} m  |  {pressure_drop_Pa:.2f} Pa')
    agregar = st.form_submit_button("Agregar")

if agregar:
    nuevo = {
        'Flujo\n[m³/s]': flujo,
        'Velocidad\n[m/s]': velocidad,
        'Densidad\n[kg/m³]': densidad,
        'Viscosidad\n[Pa·s]': viscosidad,
        'Factor de fricción\n[-]': friccion,
        'Caída de presión\n[Pa]': pressure_drop_Pa
    }
    st.session_state.tabla.loc[len(st.session_state.tabla)] = nuevo
    st.success("✅ Registro agregado.")

# Mostrar la tabla
st.subheader("Registros")
st.dataframe(st.session_state.tabla)

# Selección para eliminar
st.subheader("Eliminar registros")
indices_a_eliminar = []
for i, row in st.session_state.tabla.iterrows():
    if st.checkbox(f"Eliminar fila {i}", key=f"del_{i}"):
        indices_a_eliminar.append(i)

if st.button("Eliminar seleccionados"):
    st.session_state.tabla.drop(indices_a_eliminar, inplace=True)
    st.session_state.tabla.reset_index(drop=True, inplace=True)
    st.success("🧹 Registros eliminados.")

st.markdown(f"** Suma total de la caída de presión: {st.session_state.tabla['Caída de presión\n[Pa]'].sum():,.2f} Pa**")