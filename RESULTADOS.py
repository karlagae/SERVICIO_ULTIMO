import streamlit as st
import pandas as pd

st.set_page_config(page_title="Resultados", layout="wide")

# =========================
# Estado para notas
# =========================
if "notas_guardadas" not in st.session_state:
    st.session_state.notas_guardadas = []

# =========================
# CSS
# =========================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f4f1fb 0%, #eef3ff 100%);
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
        max-width: 1400px;
    }

    /* Top bar */
    .topbar {
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 18px;
        padding: 16px 22px;
        box-shadow: 0 8px 28px rgba(31, 41, 55, 0.08);
        margin-bottom: 14px;
    }

    .topbar-title {
        font-size: 2rem;
        font-weight: 800;
        color: #1f2a44;
        margin: 0;
    }

    .topbar-sub {
        font-size: 0.96rem;
        color: #6b7280;
        margin-top: 4px;
    }

    /* Tabs fake */
    .tabs-wrap {
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 16px;
        padding: 10px 18px;
        box-shadow: 0 6px 20px rgba(31, 41, 55, 0.06);
        margin-bottom: 20px;
    }

    .tabs-row {
        display: flex;
        gap: 28px;
        align-items: center;
        font-size: 1rem;
        flex-wrap: wrap;
    }

    .tab-item {
        color: #6b7280;
        font-weight: 600;
        padding-bottom: 8px;
    }

    .tab-active {
        color: #1f4e79;
        border-bottom: 3px solid #5aa9ff;
    }

    /* Cards */
    .soft-card {
        background: rgba(255,255,255,0.94);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 18px;
        padding: 18px 20px;
        box-shadow: 0 8px 24px rgba(31, 41, 55, 0.06);
        margin-bottom: 18px;
    }

    .patient-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1f2a44;
        margin-bottom: 2px;
    }

    .patient-id {
        font-size: 1rem;
        color: #7b8190;
        margin-bottom: 18px;
    }

    .section-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #26324b;
        margin-bottom: 14px;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    .vitals-box {
        background: #f7f8fc;
        border-radius: 14px;
        padding: 14px 16px;
        border: 1px solid #edf0f6;
        margin-top: 8px;
    }

    .vital-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid #edf0f6;
        padding: 12px 0;
        gap: 14px;
    }

    .vital-row:first-child {
        border-top: none;
        padding-top: 0;
    }

    .vital-label {
        font-size: 1rem;
        font-weight: 700;
    }

    .vital-value {
        font-size: 1.05rem;
        font-weight: 800;
        color: #1f2a44;
        text-align: right;
    }

    .muted {
        color: #7b8190;
    }

    /* KPI cards */
    .kpi-card {
        background: rgba(255,255,255,0.94);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 18px;
        padding: 18px 18px 14px 18px;
        box-shadow: 0 8px 24px rgba(31, 41, 55, 0.06);
        min-height: 138px;
        margin-bottom: 10px;
    }

    .kpi-label {
        font-size: 0.95rem;
        color: #5e6576;
        font-weight: 700;
        text-transform: uppercase;
        line-height: 1.2;
        margin-top: 8px;
    }

    .kpi-value {
        font-size: 2.3rem;
        font-weight: 800;
        color: #24314f;
        margin-top: 14px;
    }

    .kpi-icon {
        font-size: 2rem;
    }

    .kpi-blue { background: linear-gradient(180deg, #ffffff 0%, #f4f7ff 100%); }
    .kpi-purple { background: linear-gradient(180deg, #ffffff 0%, #faf3ff 100%); }
    .kpi-green { background: linear-gradient(180deg, #ffffff 0%, #f1fff7 100%); }

    /* Notes box */
    .note-box {
        background: rgba(255,255,255,0.94);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 18px;
        padding: 18px 20px;
        box-shadow: 0 8px 24px rgba(31, 41, 55, 0.06);
        margin-bottom: 12px;
    }

    .file-card {
        background: rgba(255,255,255,0.94);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 18px;
        padding: 16px 18px;
        box-shadow: 0 8px 24px rgba(31, 41, 55, 0.06);
        margin-bottom: 12px;
    }

    .small-note {
        font-size: 0.92rem;
        color: #7b8190;
    }

    .saved-note {
        background: #f8fafc;
        border: 1px solid #e8edf5;
        border-radius: 12px;
        padding: 10px 12px;
        margin-bottom: 8px;
        color: #334155;
    }

    div[data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.94);
        border-radius: 16px;
        padding: 6px;
        box-shadow: 0 8px 24px rgba(31, 41, 55, 0.06);
        border: 1px solid rgba(0,0,0,0.06);
    }

    .footer-space {
        margin-top: 14px;
        padding-top: 14px;
        border-top: 1px solid #edf0f6;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Datos demo
# =========================
paciente = {
    "nombre": "Paciente #1",
    "id": "AEMCT-45CV",
    "fecha_pdf": "24/04/2024",
    "vitales": [
        ("ALTURA", "1.78 m", "#7c61b5"),
        ("PESO", "74 kg", "#4d89c7"),
        ("IMC", "23.4 kg/m²", "#6ca84f"),
        ("TEMPERATURA", "36.5 °C", "#3aa99f"),
        ("FREC. RESPIRATORIA", "17 r/min", "#2f9fa0"),
        ("PRESIÓN ARTERIAL", "120/80 mmHg", "#c74d73"),
        ("FREC. CARDIACA", "62 lpm", "#be4d72"),
    ]
}

archivos = pd.DataFrame([
    {"Archivo": "Informe_C1_DEO5FI_F8XOA2F.pdf", "Tamaño": "2.1 MB", "Tiempo": "1m 42s"},
    {"Archivo": "Reporte_C2_2BQ9XH_03MD2V.pdf", "Tamaño": "1.8 MB", "Tiempo": "1m 55s"},
    {"Archivo": "Sesion_C3_AJYG2K_H1DNES.pdf", "Tamaño": "1.7 MB", "Tiempo": "1m 33s"},
])

# =========================
# Función guardar nota
# =========================
def guardar_nota():
    texto = st.session_state.get("nota_input", "").strip()
    if texto:
        st.session_state.notas_guardadas.append(texto)
        st.session_state.nota_input = ""

# =========================
# Header
# =========================
st.markdown("""
<div class="topbar">
    <div class="topbar-title">🩺 Automatización de Hojas Clínicas</div>
    <div class="topbar-sub">Panel de resultados y seguimiento de documentos procesados</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="tabs-wrap">
    <div class="tabs-row">
        <div class="tab-item">☰ Carga</div>
        <div class="tab-item tab-active">Resultados</div>
        <div class="tab-item">Configuración</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# Layout principal
# =========================
left, right = st.columns([1.05, 1.95], gap="large")

with left:
    vitals_html = ""
    for label, value, color in paciente["vitales"]:
        vitals_html += f"""
        <div class="vital-row">
            <div class="vital-label" style="color:{color};">{label}</div>
            <div class="vital-value">{value}</div>
        </div>
        """

    patient_card_html = f"""
    <div class="soft-card">
        <div class="patient-title">{paciente["nombre"]}</div>
        <div class="patient-id">ID: {paciente["id"]}</div>

        <div class="section-title">Signos vitales</div>

        <div class="vitals-box">
            {vitals_html}
        </div>

        <div class="footer-space small-note">
            Fecha del PDF: <strong>{paciente["fecha_pdf"]}</strong>
        </div>
    </div>
    """
    st.markdown(patient_card_html, unsafe_allow_html=True)

    st.markdown("""
    <div class="file-card">
        <h4 style="margin-top:0; margin-bottom:0; color:#26324b;">Archivos analizados</h4>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(archivos, use_container_width=True, hide_index=True)

with right:
    k1, k2, k3 = st.columns(3, gap="medium")

    with k1:
        st.markdown("""
        <div class="kpi-card kpi-blue">
            <div class="kpi-icon">📄</div>
            <div class="kpi-label">Archivos<br>procesados</div>
            <div class="kpi-value">5</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown("""
        <div class="kpi-card kpi-purple">
            <div class="kpi-icon">👥</div>
            <div class="kpi-label">Registros<br>extraídos</div>
            <div class="kpi-value">112</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown("""
        <div class="kpi-card kpi-green">
            <div class="kpi-icon">📋</div>
            <div class="kpi-label">Sesiones<br>pendientes</div>
            <div class="kpi-value">4</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="note-box">
        <h3 style="margin-top:0; margin-bottom:0; color:#26324b;">Notas</h3>
    </div>
    """, unsafe_allow_html=True)

    st.text_input(
        "Escribe una nota",
        key="nota_input",
        placeholder="Agregar una nota importante sobre el paciente...",
        label_visibility="collapsed"
    )

    col_btn1, col_btn2 = st.columns([5, 1])
    with col_btn2:
        st.button("Guardar", use_container_width=True, on_click=guardar_nota)

    if st.session_state.notas_guardadas:
        st.markdown("""
        <div class="file-card">
            <h4 style="margin-top:0; color:#26324b;">Notas guardadas</h4>
        </div>
        """, unsafe_allow_html=True)

        for nota in reversed(st.session_state.notas_guardadas):
            st.markdown(f'<div class="saved-note">{nota}</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="file-card">
        <h3 style="margin-top:0; margin-bottom:0; color:#26324b;">Archivos analizados</h3>
    </div>
    """, unsafe_allow_html=True)

    df_show = archivos.copy()
    df_show["Ver"] = "👁️"

    st.dataframe(df_show, use_container_width=True, hide_index=True)

# =========================
# Resumen adicional
# =========================
st.markdown("###")
st.markdown("""
<div class="file-card">
    <h3 style="margin-top:0; color:#26324b;">Resumen adicional</h3>
    <div class="small-note">
        Aquí después puedes conectar los resultados reales de tu OCR.
    </div>
</div>
""", unsafe_allow_html=True)
