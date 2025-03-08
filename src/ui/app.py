"""
Interface Streamlit para interação com o modelo de previsão de renda.
"""

import streamlit as st
import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Previsão de Renda",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': """
        # Sobre esta Ferramenta
        
        Esta calculadora utiliza um modelo de Machine Learning treinado com dados do Census Income Dataset para estimar sua faixa de renda.
        
        **Informações importantes sobre o modelo:**
        - **Dataset**: UCI Adult Census Income (1994)
        - **Origem**: Censo dos Estados Unidos
        - **Objetivo**: Prever renda anual > R$ 250.000,00 (≈ $50.000,00 em 1994)
        
        **Limitações conhecidas:**
        - Dados históricos (1994) podem não refletir a realidade atual
        - Baseado no mercado de trabalho americano
        - Pode conter vieses históricos (ex: estado civil, gênero)
        
        **Como interpretar os resultados:**
        - A previsão é uma estimativa baseada em padrões históricos
        - Considere o contexto atual do mercado de trabalho
        - Use como uma referência, não como verdade absoluta
        """
    }
)

st.markdown("""
<style>
    .main {
        padding: 0.25rem !important;
    }
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        margin-top: -2rem;
        max-width: 100% !important;
    }
    .stButton>button {
        padding: 0.25rem;
        font-size: 0.9rem;
        width: 100%;
    }
    .stSelectbox {
        margin-bottom: 0.25rem;
    }
    .stNumberInput {
        margin-bottom: 0.25rem;
    }
    h1 {
        font-size: 1.5rem !important;
        margin-bottom: 0.5rem !important;
        padding-bottom: 0 !important;
    }
    h3 {
        font-size: 1.1rem !important;
        margin: 0.25rem 0 !important;
    }
    div[data-testid="column"] {
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    div[data-testid="column"]:nth-of-type(2) {
        border-left: 2px solid rgba(128, 128, 128, 0.3);
        padding-left: 2rem !important;
    }
    div[data-testid="column"]:nth-of-type(1) {
        padding-right: 2rem !important;
    }
    .form-container {
        padding: 0.75rem;
        margin-top: -1rem;
        max-width: 100%;
        overflow: hidden;
    }
    .results-container {
        padding: 0.75rem;
        margin-top: -1rem;
        height: 100%;
    }
    .stAlert {
        padding: 0.25rem;
    }
    div[data-testid="stVerticalBlock"] > div:has(div.stAlert) {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    div[data-testid="stForm"] {
        padding-top: 0.25rem;
        padding-bottom: 0.25rem;
        max-width: 100%;
    }
    .row-widget.stSelectbox {
        padding-bottom: 0.25rem;
        max-width: 100%;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0.25rem !important;
        width: 100% !important;
    }
    .element-container {
        margin: 0.25rem 0 !important;
    }
    div.stMarkdown p {
        margin: 0 0 0.25rem;
        font-size: 0.9rem;
    }
    div.stSpinner {
        margin-top: 0.25rem;
        margin-bottom: 0.25rem;
    }
    [data-testid="column"] [data-testid="stVerticalBlock"] {
        height: 100%;
        width: 100% !important;
    }
    .stApp {
        max-width: 100vw;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 💰 Calculadora de Renda")

API_URL = "http://localhost:8000"

def check_api_status():
    """Verifica se a API está online."""
    try:
        response = requests.get(f"{API_URL}/health")
        logger.debug(f"Status da API: {response.status_code}")
        logger.debug(f"Resposta da API: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Erro ao verificar status da API: {str(e)}")
        return False

tipo_trabalho_map = {
    "Empresa Privada": 4,
    "Autônomo (sem empresa)": 6,
    "Prefeitura": 2,
    "Governo Estadual": 7,
    "Empresário": 5,
    "Governo Federal": 1,
    "Trabalho Voluntário": 8
}

escolaridade_map = {
    "Ensino Médio Completo": 11,
    "Superior Incompleto": 14,
    "Superior Completo": 2,
    "Mestrado": 12,
    "Curso Técnico": 1,
    "Ensino Médio Incompleto": 0,
    "Curso Tecnólogo": 0,
    "Fundamental Completo": 0,
    "Fundamental Incompleto": 0,
    "Pós-graduação": 13,
    "Doutorado": 8
}

estado_civil_map = {
    "Casado(a)": 2,
    "Solteiro(a)": 4,
    "Divorciado(a)": 0,
    "Separado(a)": 5,
    "Viúvo(a)": 6,
    "União Estável": 3,
    "Casado(a) - Cônjuge Militar": 1
}

ocupacao_map = {
    "Profissional Especializado": 10,
    "Técnico/Artesão": 3,
    "Gerente/Diretor": 4,
    "Administrativo": 1,
    "Vendas": 11,
    "Prestador de Serviços": 8,
    "Operador de Máquinas": 7,
    "Transportes": 13,
    "Serviços Gerais": 6,
    "Agricultura/Pesca": 5,
    "Suporte Técnico": 12,
    "Segurança": 9,
    "Forças Armadas": 2,
    "Empregado Doméstico": 0
}

situacao_familiar_map = {
    "Chefe de Família": 0,
    "Mora Sozinho(a)": 3,
    "Filho(a)": 4,
    "Solteiro(a) com Dependentes": 5,
    "Cônjuge": 6,
    "Outros Parentes": 2
}

etnia_map = {
    "Branca": 4,
    "Preta": 2,
    "Asiática": 1,
    "Indígena": 0,
    "Outra": 3
}

sexo_map = {
    "Masculino": 1,
    "Feminino": 0
}

col_form, col_results = st.columns([5, 4], gap="medium")

with col_form:
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        with st.form("prediction_form"):
            st.markdown("### 📋 Seus Dados", help=None)
            
            col1, col2 = st.columns(2)
            
            with col1:
                age = st.number_input("Idade", min_value=17, max_value=90, value=30)
                workclass = st.selectbox("Tipo de Trabalho", options=list(tipo_trabalho_map.keys()), index=0)
                education = st.selectbox("Escolaridade", options=list(escolaridade_map.keys()), index=0)
                marital_status = st.selectbox("Estado Civil", options=list(estado_civil_map.keys()), index=0)
                occupation = st.selectbox("Área de Atuação", options=list(ocupacao_map.keys()), index=0)
                relationship = st.selectbox("Situação Familiar", options=list(situacao_familiar_map.keys()), index=0)
            
            with col2:
                race = st.selectbox("Como você se identifica", options=list(etnia_map.keys()), index=0)
                sex = st.selectbox("Sexo", options=list(sexo_map.keys()), index=0)
                capital_gain = st.number_input("Rendimentos Extras (Anual)", min_value=0, max_value=1000000, value=0)
                capital_loss = st.number_input("Perdas Financeiras (Anual)", min_value=0, max_value=1000000, value=0)
                hours_per_week = st.number_input("Horas por Semana", min_value=1, max_value=100, value=40)
                native_country = st.selectbox("País de Origem", options=["Brasil", "Outro País"], index=0)
            
            submit_button = st.form_submit_button("🎯 Calcular Minha Renda")
        st.markdown('</div>', unsafe_allow_html=True)

with col_results:
    with st.container():
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        if not submit_button:
            st.markdown("""
            ### 👋 Bem-vindo!
            Preencha o formulário para receber sua análise de potencial de renda e dicas personalizadas.
            """)
        else:
            api_status = check_api_status()
            if not api_status:
                st.error("❌ Sistema temporariamente indisponível. Por favor, tente novamente em alguns instantes.")
                logger.error("API está offline ou inacessível")
            else:
                input_data = {
                    "age": age,
                    "workclass": tipo_trabalho_map[workclass],
                    "education": escolaridade_map[education],
                    "marital-status": estado_civil_map[marital_status],
                    "occupation": ocupacao_map[occupation],
                    "relationship": situacao_familiar_map[relationship],
                    "race": etnia_map[race],
                    "sex": sexo_map[sex],
                    "capital_gain": capital_gain,
                    "capital_loss": capital_loss,
                    "hours_per_week": hours_per_week,
                    "native-country": 39 if native_country == "Brasil" else 0
                }
                
                try:
                    with st.spinner("Analisando seus dados..."):
                        response = requests.post(f"{API_URL}/predict", json=input_data, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        prob_high = result["probability_>50K"] * 100
                        
                        if prob_high >= 70:
                            potential = "Alto"
                            emoji = "🌟"
                            color = "#28a745"
                        elif prob_high >= 40:
                            potential = "Moderado"
                            emoji = "⭐"
                            color = "#ffc107"
                        else:
                            potential = "Em Desenvolvimento"
                            emoji = "💫"
                            color = "#6c757d"
                        
                        st.markdown(f"""
                        ### 📊 Resultado
                        
                        <div style='background-color: {color}1a; padding: 0.75rem; border-radius: 0.5rem; border: 1px solid {color}'>
                            <h3 style='color: {color}; margin: 0;'>{emoji} Potencial de Renda {potential}</h3>
                            <p style='font-size: 2rem; margin: 0.5rem 0;'>{prob_high:.1f}%</p>
                            <p style='font-size: 0.8rem; margin: 0;'>Chance de renda > R$ 250.000,00/ano</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("### 💡 Dicas")
                        st.markdown("Para melhorar ainda mais:")
                        
                        if prob_high < 40:
                            dicas = [
                                "Invista em educação continuada",
                                "Busque certificações profissionais",
                                "Desenvolva habilidades técnicas específicas",
                                "Explore oportunidades de networking"
                            ]
                        elif prob_high < 70:
                            dicas = [
                                "Busque certificações profissionais",
                                "Desenvolva habilidades de liderança",
                                "Considere empreender na sua área",
                                "Amplie sua rede de contatos profissionais"
                            ]
                        else:
                            dicas = [
                                "Mantenha-se atualizado com tendências do mercado",
                                "Desenvolva sua rede de contatos",
                                "Considere mentorar outros profissionais",
                                "Explore oportunidades de investimento"
                            ]
                        
                        for dica in dicas:
                            st.markdown(f"- {dica}")
                        
                        st.markdown("""
                        <div class='disclaimer'>
                            <p><strong>Nota:</strong> Esta é uma estimativa baseada em dados históricos e não deve ser considerada como garantia de resultados futuros.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("❌ Não foi possível realizar a análise. Erro: " + str(response.json()))
                        
                except requests.exceptions.Timeout:
                    st.error("❌ O servidor demorou muito para responder. Por favor, tente novamente.")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Não foi possível conectar ao servidor. Por favor, verifique sua conexão.")
                except Exception as e:
                    st.error("❌ Ocorreu um erro inesperado. Por favor, tente novamente.")
                    logger.error(f"Erro inesperado: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)