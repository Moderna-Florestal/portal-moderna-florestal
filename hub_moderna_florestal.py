import streamlit as st
import streamlit.components.v1 as components
import os

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Hub Moderna Florestal",
    layout="wide",
    page_icon="🌲"
)

# 🎨 CSS
st.markdown("""
<style>

/* Fundo geral */
.main {
    background-color: #f5f7fa;
}

/* Sidebar fundo */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #002b5c, #004a99);
}

/* TEXTO BRANCO SIDEBAR */
section[data-testid="stSidebar"] .stText, 
section[data-testid="stSidebar"] .stMarkdown, 
section[data-testid="stSidebar"] p, 
section[data-testid="stSidebar"] h1, 
section[data-testid="stSidebar"] h2, 
section[data-testid="stSidebar"] h3, 
section[data-testid="stSidebar"] span, 
section[data-testid="stSidebar"] label {
    color: white !important;
}

/* Cores dos botões e ícones sidebar */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: white !important;
    font-weight: bold;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label div p {
    color: white !important;
}

/* Cor dos itens selecionados e setas do Selectbox */
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    color: white !important;
    background-color: rgba(255, 255, 255, 0.1) !important;
}

/* Títulos principais no corpo da página */
h1, h2 {
    color: #002b5c;
}

/* Texto padrão no corpo */
.main p, .main span, .main div {
    color: #333333;
}

/* Botões */
.stButton > button {
    background-color: #004a99;
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #0066cc;
    transform: scale(1.03);
}

/* Cards */
.card {
    background-color: white;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
    transition: 0.3s;
    color: #333333;
}

.card h1, .card h2, .card h3 {
    color: #002b5c !important;
}

.card:hover {
    transform: translateY(-6px);
}

html {
    translate: no;
}

</style>
""", unsafe_allow_html=True)

# 📌 SIDEBAR
st.sidebar.markdown("### 🌲 Moderna Florestal")

# ✅ LOGO (Caminho dinâmico e seguro)
# Descobre a pasta onde o script atual está guardado
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(diretorio_atual, "assets", "LOGO MODERNA FLORESTAL.png")

if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=160)
else:
    st.sidebar.error("Logo não encontrado em: assets/")
    # Debug para você ver onde ele está procurando se der erro:
    # st.sidebar.write(logo_path)

st.sidebar.markdown("---")
st.sidebar.markdown("### Navegação")

aba = st.sidebar.radio(
    "Ir para:",
    ["Home", "Setores"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Hub Inteligência Operacional")

# 🏠 HOME
if aba == "Home":

    st.markdown("""
    <div class="card">
        <h1>🌲 Hub de Inteligência Operacional</h1>
        <h3>Moderna Florestal</h3>
        <p>Centro de comando para gestão de dados, formulários operacionais e dashboards estratégicos.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <h3>📝 Produção</h3>
            <p>Acesso aos formulários.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3>📊 Dashboards</h3>
            <p>Visualização estratégica dos dados.</p>
        </div>
        """, unsafe_allow_html=True)

# 📂 SETORES
elif aba == "Setores":

    setor = st.sidebar.selectbox(
        "Selecione a área:",
        ["Produção", "Financeiro"]
    )

    st.markdown(f"""
    <div class="card">
        <h2>📊 Portal de Dados - {setor}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if setor == "Produção":

        st.markdown("## 🚜 Produção de Campo")

        tab_form, tab_dash = st.tabs([
            "📋 Formulários",
            "📈 Relatórios Estratégicos"
        ])

        with tab_form:

            st.markdown("""
            <div class="card">
                <h3>Boletim Diário de Trabalho (BDT)</h3>
                <p>Preenchimento diário das operações.</p>
            </div>
            """, unsafe_allow_html=True)

            link_bdt = "https://bdt-flow-pro.base44.app"

            st.markdown("<br>", unsafe_allow_html=True)

            components.iframe(link_bdt, height=700, scrolling=True)

            st.link_button("🔗 Abrir em tela cheia", link_bdt)

        with tab_dash:

            st.markdown("""
            <div class="card">
                <h3>Dashboard BDT</h3>
                <p>Análise estratégica dos dados.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🔄 Atualizar Dados (Processar BDTs)"):
                import subprocess

                with st.spinner('Processando arquivos...'):
                    try:
                        subprocess.run(["python", "automacao_bdt.py"], check=True)

                        st.success("✅ Dados atualizados com sucesso!")
                        st.info("Agora atualize seu Power BI Desktop.")

                    except Exception:
                        st.error("❌ Erro ao processar.")

            st.divider()

            st.info("📊 Aguardando publicação do Power BI...")

    elif setor == "Financeiro":
        st.warning("⚠️ Área em desenvolvimento.")