from numpy import zeros
import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path
import time
from rocketpy import Environment, SolidMotor, Rocket, Flight
from orbital.launch import prepare_and_launch

st.set_page_config(page_title="Orbital", layout="centered", page_icon="💫")
st.header("💫 Orbital Mechanics with `rocketpy`")

# ------------------------------------------------------------------------ #

TestFlight = prepare_and_launch(datapath="nbs/")

df = pd.DataFrame(TestFlight.z[:, :], columns=["time", "elevation"])
df["velocity_z"] = TestFlight.vz[:, 1]
df["x"] = TestFlight.x[:, 1]
df["y"] = TestFlight.y[:, 1]

width, height = 400, 100
z = (
    alt.Chart(df)
    .mark_line()
    .encode(x="time", y="elevation")
    .properties(width=width, height=height)
)

vz = (
    alt.Chart(df)
    .mark_line()
    .encode(x="time", y="velocity_z")
    .properties(width=width, height=height)
)

fig = st.altair_chart(z & vz, use_container_width=True)
wait_period = 0.05

step = st.number_input("step", value=20)
if st.button("🔴 Run"):

    x_max = df.time.max()
    y_max = df.elevation.max() * 1.1
    vz_min = df.velocity_z.min() * 1.1
    vz_max = df.velocity_z.max() * 1.1
    for i in range(0, df.shape[0], step):
        dx = df.iloc[:i, :]
        z = (
            alt.Chart(dx)
            .mark_line()
            .encode(
                x=alt.X("time", scale=alt.Scale(domain=[0, x_max], clamp=True)),
                y=alt.Y("elevation", scale=alt.Scale(domain=[0, y_max], clamp=True)),
            )
            .properties(width=width, height=height)
        )

        vz = (
            alt.Chart(dx)
            .mark_line()
            .encode(
                x=alt.X("time", scale=alt.Scale(domain=[0, x_max], clamp=True)),
                y=alt.Y(
                    "velocity_z", scale=alt.Scale(domain=[vz_min, vz_max], clamp=True)
                ),
            )
            .properties(width=width, height=height)
        )
        time.sleep(wait_period)
        fig.altair_chart(z & vz, use_container_width=True)
