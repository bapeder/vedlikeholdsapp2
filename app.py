import streamlit as st
import pandas as pd
from openpyxl import load_workbook

EXCEL_FILE = "vedlikeholdsplan_ver22.xlsx"

def append_to_erfaringslogg(data):
    df = pd.read_excel(EXCEL_FILE, sheet_name="Erfaringslogg", engine="openpyxl")
    for i in range(len(df)):
        if pd.isna(df.loc[i, "Dato"]):
            for key in data:
                df.loc[i, key] = data[key]
            break
    df.to_excel(EXCEL_FILE, sheet_name="Erfaringslogg", index=False, engine="openpyxl")

st.title("Vedlikeholdslogg")

with st.form("logg_form"):
    st.subheader("Registrer nytt tiltak")
    dato = st.date_input("Dato")
    vaer = st.selectbox("Vær", ["Sol", "Skyet", "Regn", "Ukjent"])
    temp = st.number_input("Temperatur (°C)", min_value=-20, max_value=40, step=1)
    vind = st.text_input("Vind")
    tiltak = st.text_input("Tiltak")
    utfort_av = st.text_input("Utført av")
    timer = st.number_input("Timer brukt", min_value=0.0, step=0.5)
    erfaring = st.text_area("Erfaring")
    forbedringer = st.text_area("Forslag til forbedringer")
    submitted = st.form_submit_button("Lagre")

    if submitted:
        new_entry = {
            "Dato": dato,
            "Vær": vaer,
            "Temp": temp,
            "Vind": vind,
            "Tiltak": tiltak,
            "Utført av": utfort_av,
            "Timer": timer,
            "Erfaring": erfaring,
            "Forbedringer": forbedringer
        }
        append_to_erfaringslogg(new_entry)
        st.success("Tiltak lagret i vedlikeholdsplanen.")
