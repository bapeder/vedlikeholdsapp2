
import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from openpyxl import load_workbook

# Filsti til Excel-filen
excel_file = "vedlikeholdsplan_ver22.xlsx"

# Koordinater for værdata
latitude = 70.1112
longitude = 29.3532

# Hent dagens dato
today = datetime.today().strftime("%Y-%m-%d")

# Hent værdata fra Open-Meteo API
def hent_vaerdata(lat, lon):
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current=temperature_2m,weathercode,windspeed_10m"
            f"&timezone=auto"
        )
        response = requests.get(url)
        data = response.json()
        temp = data["current"]["temperature_2m"]
        wind = data["current"]["windspeed_10m"]
        weather_code = data["current"]["weathercode"]

        # Enkle beskrivelser basert på weathercode
        weather_map = {
            0: "Klar himmel",
            1: "Hovedsakelig klar",
            2: "Delvis skyet",
            3: "Overskyet",
            45: "Tåke",
            48: "Tåke med rim",
            51: "Lett yr",
            53: "Moderat yr",
            55: "Kraftig yr",
            61: "Lett regn",
            63: "Moderat regn",
            65: "Kraftig regn",
            71: "Lett snø",
            73: "Moderat snø",
            75: "Kraftig snø",
        }
        weather = weather_map.get(weather_code, "Ukjent vær")
        return weather, temp, f"{wind} m/s"
    except:
        return "Ukjent", "Ukjent", "Ukjent"

# Hent værdata
vaer, temperatur, vind = hent_vaerdata(latitude, longitude)

# Last inn tiltak fra vedlikeholdsplanen
df_plan = pd.read_excel(excel_file, sheet_name="Vedlikeholdsplan", engine="openpyxl")
tiltak_liste = df_plan["Tiltak"].dropna().unique().tolist()

# Streamlit-app
st.title("Registrer tiltak og erfaring")

with st.form("erfaringsskjema"):
    st.write("📅 Automatisk dato:", today)
    st.write("🌤️ Automatisk vær:", vaer)
    st.write("🌡️ Temperatur:", temperatur)
    st.write("💨 Vind:", vind)

    tiltak = st.selectbox("Tiltak", tiltak_liste)
    utført_av = st.text_input("Utført av")
    timer = st.number_input("Timer brukt", min_value=0.0, step=0.5)
    erfaring = st.text_area("Erfaring")
    forbedringer = st.text_area("Forslag til forbedringer")

    send = st.form_submit_button("Lagre")

    if send:
        # Last inn arbeidsbok og ark
        wb = load_workbook(excel_file)
        sheet = wb["Erfaringslogg"]

        # Finn første tomme rad
        row = 2
        while sheet.cell(row=row, column=1).value not in [None, ""]:
            row += 1

        # Skriv data til raden
        sheet.cell(row=row, column=1).value = today
        sheet.cell(row=row, column=2).value = vaer
        sheet.cell(row=row, column=3).value = temperatur
        sheet.cell(row=row, column=4).value = vind
        sheet.cell(row=row, column=5).value = tiltak
        sheet.cell(row=row, column=6).value = utført_av
        sheet.cell(row=row, column=7).value = timer
        sheet.cell(row=row, column=8).value = erfaring
        sheet.cell(row=row, column=9).value = forbedringer

        # Lagre filen
        wb.save(excel_file)

        st.success("Registreringen er lagret i Excel-filen.")
