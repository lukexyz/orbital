import streamlit as st
from datetime import timedelta, datetime

from astropy.time import Time
from astropy import units as u
from poliastro.bodies import Earth, Mars, Sun
from poliastro.twobody import Orbit


st.set_page_config(page_title="Orbital", layout="centered", page_icon="💫")
st.header("💫 Orbital Mechanics with `poliastro`")

# ------------------------------------------------------------------------ #
# matplotlib

r_p = Earth.R + 165 * u.km
r_a = 1.5 * Earth.R + 215 * u.km

a_parking = (r_p + r_a) / 2
ecc_parking = 1 - r_p / a_parking


def plot_orbit(i):
    parking = Orbit.from_classical(
        Earth,
        a_parking,
        ecc_parking,
        0 * u.deg,
        0 * u.deg,
        0 * u.deg,
        i * u.deg,  # We don't mind
        Time("2006-01-19", scale="utc"),
    )
    print(parking.v)
    return parking.plot()[0].figure


world_plot = st.pyplot(plot_orbit(0), use_container_width=True)

if st.button("🔴 Run"):
    for i in range(0, 100, 5):
        p = plot_orbit(i)
        world_plot.pyplot(p)
