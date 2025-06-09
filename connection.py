import streamlit as st
import pandas as pd
import numpy as np
import sqlalchemy as sa
import psycopg2
from sqlalchemy.engine import URL

@st.cache_data(ttl=600)
def cargarDatos(queryDatos):
    conString=st.secrets["conString"]    
    engine = sa.create_engine(conString)
    dfDatos = pd.read_sql_query(queryDatos, engine)    
    return dfDatos

def ejecutarComandos(query,  params):
    conString = st.secrets["conString"]    
    engine = sa.create_engine(conString)
    
    with engine.connect() as conn:
        if params:
            conn.execute(sa.text(query), params)
        else:
            conn.execute(sa.text(query))
        conn.commit()


# fig= px.bar(dfDatos.sort_values(by='EPI Score',ascending=False).head(10),x='EPI Score',y='Country', color='Country')

# st.plotly_chart(fig,use_container_width=True)