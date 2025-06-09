import streamlit as st
from connection import ejecutarComandos

st.title("Agregar Factura")

# Inicializar valores en session_state si no existen
if "nombre" not in st.session_state:
    st.session_state.nombre = ""
if "servicio" not in st.session_state:
    st.session_state.servicio = ""
if "total" not in st.session_state:
    st.session_state.total = None
if "estado" not in st.session_state:
    st.session_state.estado = ""
if "fecha_factura" not in st.session_state:
    st.session_state.fecha_factura = None
if "fecha_pago" not in st.session_state:
    st.session_state.fecha_pago = None

@st.dialog("Confirma los datos")
def check(item):
    st.subheader(f"Nombre: {item['nombre']}")
    st.subheader(f"Servicio: {item['servicio']}")
    st.subheader(f"Total: {item['total']}")
    st.subheader(f"Estado: {item['estado']}")
    st.subheader(f"Fecha de la factura: {item['fecha_factura']}")
    st.subheader(f"Fecha de pago: {item['fecha_pago']}")
    col1, col2 = st.columns(2)
    if col1.button("Confirmar"):
        query = """
        INSERT INTO factura (nombre, servicio, total_costo, estado_transaccion, fecha_factura, fecha_pago)
        VALUES (:nombre, :servicio, :total, :estado, :fecha_factura, :fecha_pago)
        """
        ejecutarComandos(query, item)
        # Restablecer los valores del formulario
        st.session_state.nombre = ""
        st.session_state.servicio = ""
        st.session_state.total = None
        st.session_state.estado = ""
        st.session_state.fecha_factura = None
        st.session_state.fecha_pago = None
        st.rerun()
    if col2.button("Cancelar"):
        st.rerun()

with st.form('add'):
    nombre = st.text_input('Nombre:', value=st.session_state.nombre, key="nombre")
    servicio = st.text_input('Servicio:', value=st.session_state.servicio, key="servicio")
    total = st.number_input('Total:', value=st.session_state.total, key="total")
    estado = st.selectbox('Estado:', ['', 'Pendiente', 'Pagado'], index=0 if st.session_state.estado == "" else (1 if st.session_state.estado == "Pendiente" else 2), key="estado")
    fecha_factura = st.date_input('Fecha de la factura:', value=st.session_state.fecha_factura, key="fecha_factura")
    fecha_pago = st.date_input('Fecha de pago:', value=st.session_state.fecha_pago, key="fecha_pago")
    
    if st.form_submit_button("Confirmar"):
        if nombre and total is not None and estado and fecha_factura:
            check({'nombre': nombre, 'servicio': servicio,'total': total, 'estado': estado, 'fecha_factura': fecha_factura, 'fecha_pago': fecha_pago})
        else:
            st.error("Por favor complete todos los campos")