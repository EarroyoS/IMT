import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import sqlalchemy as sa
from sqlalchemy.engine import URL
from connection import cargarDatos

st.title('Informe de Ganancias')
    
# Load initial data
query = "SELECT * FROM factura"
dfFacturas = cargarDatos(query)
    
# Basic Data Preprocessing
dfFacturas['fecha_factura'] = pd.to_datetime(dfFacturas['fecha_factura'])
dfFacturas['mes'] = dfFacturas['fecha_factura'].dt.to_period('M').astype(str)
    
# Sidebar for Filters
st.sidebar.header('Filtros de Análisis')
    
# Date Range Selection
min_date = dfFacturas['fecha_factura'].min()
max_date = dfFacturas['fecha_factura'].max()
date_range = st.sidebar.date_input(
    'Seleccionar Rango de Fechas',
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)
    
# Filter DataFrame based on date range
start_date, end_date = date_range
dfFiltered = dfFacturas[
    (dfFacturas['fecha_factura'].dt.date >= start_date) & 
    (dfFacturas['fecha_factura'].dt.date <= end_date)
]
    
# Métricas Generales
st.header('Métricas Generales')
col1, col2, col3 = st.columns(3)
    
with col1:
    st.metric('Ingresos Totales', f'${dfFiltered["total_costo"].sum():,.2f}')
    
with col2:
    st.metric('Número de Facturas', len(dfFiltered))
    
with col3:
    avg_invoice = dfFiltered['total_costo'].mean()
    st.metric('Promedio por Factura', f'${avg_invoice:,.2f}')
    
# Gráficos y Análisis
st.header('Análisis de Ganancias')
    
# 1. Ingresos Mensuales
ingresos_mensuales = dfFiltered.groupby('mes')['total_costo'].sum().reset_index()
    
fig_ingresos = px.bar(
    ingresos_mensuales, 
    x='mes', 
    y='total_costo', 
    title='Ingresos Mensuales',
    labels={'total_costo': 'Ingresos', 'mes': 'Mes'}
)
st.plotly_chart(fig_ingresos, use_container_width=True)
    
# 2. Distribución de Servicios
servicios_distribucion = dfFiltered.groupby('servicio')['total_costo'].sum()
    
fig_servicios = px.pie(
    values=servicios_distribucion.values, 
    names=servicios_distribucion.index, 
    title='Distribución de Ingresos por Servicio'
)
st.plotly_chart(fig_servicios, use_container_width=True)
    
# 3. Estado de Transacciones
estado_transacciones = dfFiltered['estado_transaccion'].value_counts()
    
fig_estado = px.bar(
    x=estado_transacciones.index, 
    y=estado_transacciones.values, 
    title='Estado de Transacciones',
    labels={'x': 'Estado', 'y': 'Número de Facturas'}
)
st.plotly_chart(fig_estado, use_container_width=True)