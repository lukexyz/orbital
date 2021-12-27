import streamlit as st
from datetime import timedelta, datetime

from astropy.time import Time
from astropy import units as u
from poliastro.bodies import Earth, Mars, Sun
from poliastro.twobody import Orbit


st.set_page_config(page_title="Orbital", layout="wide", page_icon="💫")
st.header("💫 Orbital Mechanics with `rocketpy`")

# ------------------------------------------------------------------------ #
# matplotlib

import pandas as pd
import streamlit as st

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.title("Netlix shows analysis")

shows = pd.read_csv("media/db.csv")
gb = GridOptionsBuilder.from_dataframe(shows)

gb.configure_pagination()
gb.configure_side_bar()
gb.configure_default_column(
    groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True
)
gridOptions = gb.build()

AgGrid(shows, gridOptions=gridOptions, enable_enterprise_modules=True)
