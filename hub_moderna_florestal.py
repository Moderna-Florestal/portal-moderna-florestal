import streamlit as st
import streamlit.components.v1 as components
import os
import subprocess

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Hub Moderna Florestal",
    layout="wide",
    page_icon="🌲"
)

# 🎨 CSS PERSONALIZADO
st.markdown("""
<style>
    /* Fundo geral */
    .main { background-color: #f5f7fa; }

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

    /* Títulos principais no corpo da página */
    h1, h2 { color: #002b5c; }

    /* Cards Estilizados */
    .card {
        background-color: white;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
        transition: 0.3s;
        color: #333333;
        margin-bottom: 20px;
    }
    .card h1, .card h2, .card h3 { color: #002b5c !important; margin-top: 0; }
    .card:hover { transform: translateY(-6px); }

    /* Botão customizado para o Power BI */
    .btn-pbi {
        display: inline-block;
        padding: 12px 24px;
        background-color: #228B22;
        color: white !important;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        transition: 0.3s;
    }
    .btn-pbi:hover { background-color: #1a6b1a; transform: scale(1.05); }

    html { translate: no; }
</style>
""", unsafe_allow_html=True)

# 📌 SIDEBAR
st.sidebar.markdown("### 🌲 Moderna Florestal")

# ✅ LOGO
diretorio_root = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(diretorio_root, "assets", "LOGO MODERNA FLORESTAL.png")

if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=160)
else:
    st.sidebar.warning("⚠️ Logo não encontrado.")

st.sidebar.markdown("---")
st.sidebar.markdown("### Navegação")

aba = st.sidebar.radio(
    "Ir para:",
    ["Home", "Produção", "Financeiro"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Hub Inteligência Operacional")

# --- LINKS EXTERNOS ---
link_bdt_form = "https://bdt-flow-pro.base44.app"
link_pbi_dash = "https://app.powerbi.com/groups/me/reports/b2dc9200-b8e0-4278-a2cb-7d7b2f1c17ef/ee8cfd8b801656bc0123?experience=power-bi"

# 🏠 HOME
if aba == "Home":
    st.markdown(f"""
    <div class="card">
        <h1>🌲 Bem-vindo(a)!</h1>
        <p>Centro de comando para gestão de dados, formulários operacionais e dashboards estratégicos da <b>Moderna Florestal</b>.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="card">
            <h3>📝 Formulários</h3>
            <p>Acesse o portal do Base44 para lançamento de boletins diários.</p>
            <a href="{link_bdt_form}" target="_blank" style="color: #004a99; font-weight: bold;">Acessar Portal ➔</a>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <h3>📊 Dashboards</h3>
            <p>Indicadores de produtividade, metas e bônus em tempo real.</p>
            <a href="{link_pbi_dash}" target="_blank" style="color: #228B22; font-weight: bold;">Ver Dashboards ➔</a>
        </div>
        """, unsafe_allow_html=True)

# 🚜 PRODUÇÃO
elif aba == "Produção":
    st.markdown(f"""
    <div class="card">
        <h2>📊 Portal de Dados - Produção de Campo</h2>
    </div>
    """, unsafe_allow_html=True)

    tab_form, tab_dash = st.tabs(["📋 Formulários (Base44)", "📈 Relatórios (Power BI)"])

    with tab_form:
        st.markdown("### Boletim Diário de Trabalho (BDT)")
        st.info("Preencha ou visualize os envios dos operadores abaixo.")
        
        # Exibe o Base44 embutido
        components.iframe(link_bdt_form, height=700, scrolling=True)
        st.link_button("🔗 Abrir app em tela cheia", link_bdt_form)

    with tab_dash:
        st.markdown("### Dashboard Estratégico")
        
        # Botão de Processamento
        if st.button("🔄 1. Processar Novos Dados (Python)"):
            with st.spinner('Lendo arquivos e calculando metas...'):
                try:
                    # Executa o script de automação
                    script_path = r"C:\Users\carol\OneDrive\Área de Trabalho\Dandara\Projetos Python\PRODUÇÃO\BDT\automacao_bdt.py"
                    subprocess.run(["python", script_path], check=True)
                    st.success("✅ Dados processados com sucesso!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Erro ao processar: {e}")

        st.divider()

        # Seção do Power BI
        st.markdown("""
        <div class="card">
            <h3>Visualização dos Indicadores</h3>
            <p>Utilize o botão abaixo para abrir o relatório em uma nova aba segura.</p>
            <br>
        </div>
        """, unsafe_allow_html=True)
        
        # Botão estilizado para o Power BI
        st.markdown(f'<a href="{link_pbi_dash}" target="_blank" class="btn-pbi">🚀 Abrir Dashboard no Power BI Service</a>', unsafe_allow_html=True)
        
        st.warning("⚠️ Nota: É necessário estar logado com sua conta institucional para visualizar.")

# 📂 FINANCEIRO
elif aba == "Financeiro":
    st.markdown('<div class="card"><h2>📊 Portal de Dados - Financeiro</h2></div>', unsafe_allow_html=True)
    st.info("Área em desenvolvimento...")
