import streamlit as st
import pandas as pd
import pdfplumber
import re
import folium
from streamlit_folium import folium_static  # Pour intégrer la carte

st.set_page_config(page_title="Crime Report Extraction", layout="wide")

# ✅ Initialisation du stockage des données dans Session State
if "crime_data" not in st.session_state:
    st.session_state.crime_data = pd.DataFrame()

# ✅ Stocker les fichiers déjà traités
if "uploaded_files" not in st.session_state:
    # Stocke les noms des fichiers déjà uploadés
    st.session_state.uploaded_files = set()

# ✅ Fonction pour extraire les informations d'un rapport


def extract_info(text):
    def find(pattern):
        match = re.search(pattern, text)
        return match.group(1) if match else "Not specified"

    def find_float(pattern):
        match = re.search(pattern, text)
        return float(match.group(1)) if match else None

    return {
        "Report Number": find(r'Report Number:\s*(\d{4}-\d+)'),
        "Date & Time": find(r'Date & Time:\s*([\d-]+\s[\d:]+)'),
        "Reporting Officer": find(r'Reporting Officer:\s*(.+)'),
        "Incident Location": find(r'Incident Location:\s*(.+)'),
        "Latitude": find_float(r'Coordinates:\s*\(([-\d.]+),'),
        "Longitude": find_float(r'Coordinates:\s*\([-\d.]+,\s*([-\d.]+)\)'),
        "Detailed Description": find(r'Detailed Description:\s*(.+)'),
        "Police District": find(r'Police District:\s*(.+)'),
        "Resolution": find(r'Resolution:\s*(.+)'),
        "Suspect Description": find(r'Suspect Description:\s*(.+)'),
        "Victim Information": find(r'Victim Information:\s*(.+)'),
    }


# ✅ Interface Streamlit
st.title("📄 Crime Report Extraction")
st.write("Upload PDF police reports to extract and analyze crime details.")

uploaded_files = st.file_uploader(
    "Upload PDF reports", type="pdf", accept_multiple_files=True)

if uploaded_files:
    new_reports = []

    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state.uploaded_files:  # Vérifie si déjà traité
            with pdfplumber.open(uploaded_file) as pdf:
                text = "\n".join([page.extract_text()
                                 for page in pdf.pages if page.extract_text()])
                extracted_data = extract_info(text)
                new_reports.append(extracted_data)

            # ✅ Marquer le fichier comme traité
            st.session_state.uploaded_files.add(uploaded_file.name)

    # ✅ Ajouter uniquement les nouvelles données
    if new_reports:
        new_df = pd.DataFrame(new_reports)
        st.session_state.crime_data = pd.concat(
            [st.session_state.crime_data, new_df], ignore_index=True)

# ✅ Afficher la table mise à jour
st.subheader("Extracted Crime Reports")
st.dataframe(st.session_state.crime_data)

# ✅ Bouton pour réinitialiser la table
if st.button("🗑️ Clear Table"):
    st.session_state.crime_data = pd.DataFrame()
    st.session_state.uploaded_files.clear()  # Nettoyer la liste des fichiers
    st.success("Table cleared!")

# ✅ Ajouter une carte interactive avec Folium
if not st.session_state.crime_data.empty:
    # Initialiser la carte centré sur une position approximative
    crime_map = folium.Map(location=[st.session_state.crime_data["Latitude"].mean(
    ), st.session_state.crime_data["Longitude"].mean()], zoom_start=12)

    # Ajouter des marqueurs pour chaque incident sur la carte
    for _, row in st.session_state.crime_data.iterrows():
        if pd.notna(row["Latitude"]) and pd.notna(row["Longitude"]):
            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=f"""
                    <b>Crime Report</b><br>
                    <b>Report Number:</b> {row['Report Number']}<br>
                    <b>Date:</b> {row['Date & Time']}<br>
                    <b>Location:</b> {row['Incident Location']}<br>
                    <b>Description:</b> {row['Detailed Description']}
                """,
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(crime_map)

    # Afficher la carte dans Streamlit
    folium_static(crime_map)


# ✅ Option : Télécharger les données en CSV
if not st.session_state.crime_data.empty:
    csv = st.session_state.crime_data.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "crime_reports.csv", "text/csv")
