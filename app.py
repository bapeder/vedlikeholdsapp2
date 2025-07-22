import streamlit as st
import pandas as pd

# Load Excel file
EXCEL_FILE = 'vedlikeholdsplan_ver22.xlsx'

@st.cache_data
def load_data(sheet_name):
    return pd.read_excel(EXCEL_FILE, sheet_name=sheet_name, engine='openpyxl')

def append_row(sheet_name, new_row):
    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name, engine='openpyxl')
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

st.title("Vedlikeholdsplan og Erfaringslogg")

tab1, tab2 = st.tabs(["📅 Vedlikeholdsplan", "📝 Erfaringslogg"])

with tab1:
    st.header("Vedlikeholdsplan")
    df_plan = load_data("Vedlikeholdsplan")
    st.dataframe(df_plan)

    with st.expander("➕ Legg til nytt tiltak"):
        uke = st.text_input("Uke")
        tiltak = st.text_area("Tiltak")
        utført = st.selectbox("Utført (Ja/Nei)", ["Ja", "Nei", ""])
        områder = st.text_input("Berørte områder")
        dato = st.date_input("Utført dato", format="YYYY-MM-DD")
        ansvarlig = st.text_input("Ansvarlig")
        status = st.selectbox("Status", ["Utført", "Delvis", "Ikke utført", ""])
        prioritet = st.selectbox("Prioritet", ["Høy", "Middels", "Lav", ""])
        ukeoversikt = st.text_input("Ukeoversikt")
        kommentar = st.text_input("Kommentarer")

        if st.button("Legg til tiltak"):
            new_row = {
                "Uke": uke,
                "Tiltak": tiltak,
                "Utført (Ja/Nei)": utført,
                "Berørte områder": områder,
                "Utført dato": dato,
                "Ansvarlig": ansvarlig,
                "Status": status,
                "Prioritet": prioritet,
                "Ukeoversikt": ukeoversikt,
                "Kommentarer": kommentar
            }
            append_row("Vedlikeholdsplan", new_row)
            st.success("Tiltak lagt til!")

with tab2:
    st.header("Erfaringslogg")
    df_logg = load_data("Erfaringslogg")
    st.dataframe(df_logg)

    with st.expander("➕ Legg til ny erfaring"):
        dato = st.date_input("Dato", format="YYYY-MM-DD")
        vær = st.text_input("Vær")
        temp = st.text_input("Temp")
        vind = st.text_input("Vind")
        tiltak = st.text_input("Tiltak")
        utført_av = st.text_input("Utført av")
        timer = st.number_input("Timer", min_value=0.0, step=0.5)
        erfaring = st.text_area("Erfaring")
        forbedringer = st.text_area("Forbedringer")

        if st.button("Legg til erfaring"):
            new_row = {
                "Dato": dato,
                "Vær": vær,
                "Temp": temp,
                "Vind": vind,
                "Tiltak": tiltak,
                "Utført av": utført_av,
                "Timer": timer,
                "Erfaring": erfaring,
                "Forbedringer": forbedringer
            }
            append_row("Erfaringslogg", new_row)
            st.success("Erfaring lagt til!")
