import streamlit
import pandas 
import streamlit.web.cli as stcli
import os, sys
import psycopg2
import sqlalchemy
import numpy
import plotly.express
import plotly.graph_objs


def resolve_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path


if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("main.py"),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())