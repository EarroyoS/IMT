import streamlit as st

informe_page = st.Page("informe.py",  icon=":material/add_circle:")
factura_page = st.Page("factura.py",  icon=":material/delete:")

#
pg = st.navigation([informe_page, factura_page])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()