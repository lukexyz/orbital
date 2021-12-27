import streamlit as st
from datetime import timedelta, datetime

from astropy.time import Time
from astropy import units as u
from poliastro.bodies import Earth, Mars, Sun
from poliastro.ephem import Ephem
from poliastro.frames import Planes
from poliastro.plotting import OrbitPlotter3D
from poliastro.util import time_range
from poliastro.plotting.misc import plot_solar_system

from poliastro.earth.plotting import GroundtrackPlotter
from poliastro.earth import EarthSatellite



st.set_page_config(page_title = "Orbital", layout = "centered", page_icon = "💫")

EPOCH = Time("2018-02-18 12:00:00", scale="tdb")

st.header('💫 Orbital Mechanics with `poliastro`')


roadster = Ephem.from_horizons(
    "SpaceX Roadster",
    epochs=time_range(EPOCH, end=EPOCH + 360 * u.day),
    attractor=Sun,
    plane=Planes.EARTH_ECLIPTIC
)

# ------------------------------------------------------------------------ # 
# plotly
f = GroundtrackPlotter()

# Map element colors
_LAND_COLOR = "white"
_WATER_COLOR = "rgb(140, 181, 245)"
_COUNTRY_COLOR = "lightgray"

f.fig.update_geos(
    projection_type = "orthographic",
    bgcolor = "rgba(0, 0, 0, 0)",
    showframe = False,
    lataxis = {"showgrid" : False},
    lonaxis = {"showgrid" : False},
    showlakes = True,
    showcountries = True,
    showrivers = True,
    oceancolor = _WATER_COLOR,
    landcolor = _LAND_COLOR,
    lakecolor = _WATER_COLOR,
    rivercolor = _WATER_COLOR,
    countrycolor = _COUNTRY_COLOR,
)

f.fig.update_layout(
    showlegend = False,
    margin = {"l" : 0, "r" : 0, "b" : 0, "t" : 0}
)
st.plotly_chart(f.fig)


# ------------------------------------------------------------------------ # 
# matplotlib
fig = plot_solar_system(outer=False, epoch=EPOCH)
fig = fig.plot_ephem(roadster, EPOCH, label="SpaceX Roadster", color="black")
st.pyplot(fig[1].figure)


# ------------------------------------------------------------------------ # 
# matplotlib
from poliastro.twobody import Orbit
r_p = Earth.R + 165 * u.km
r_a = Earth.R + 215 * u.km

a_parking = (r_p + r_a) / 2
ecc_parking = 1 - r_p / a_parking

parking = Orbit.from_classical(
    Earth,
    a_parking,
    ecc_parking,
    0 * u.deg,
    0 * u.deg,
    0 * u.deg,
    0 * u.deg,  # We don't mind
    Time("2006-01-19", scale="utc"),
)
p = parking.plot()

st.write(parking.v)


st.pyplot(p[0].figure)