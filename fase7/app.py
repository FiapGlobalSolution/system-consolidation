"""
Dashboard Principal - FarmTech Solutions Fase 7
Sistema Consolidado de Gestão para Agronegócio

Criado pela Pessoa 1 (Arquiteto de Integração)
Será expandido pela Pessoa 4 (Frontend Lead & Documentador)
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adicionar src ao path para imports
sys.path.insert(0, str(Path(__file__).parent))

from src.core.controller import FarmTechController
from src.core.config import Config

# ========================================
# CONFIGURAÇÃO DA PÁGINA
# ========================================

st.set_page_config(
    page_title="FarmTech Solutions - Sistema Integrado",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# INICIALIZAÇÃO DO CONTROLADOR
# ========================================

@st.cache_resource
def inicializar_controller():
    """Inicializa o controlador (cache para não recriar a cada interação)"""
    return FarmTechController()

# Inicializar controlador
try:
    controller = inicializar_controller()
except Exception as e:
    st.error(f"❌ Erro ao inicializar sistema: {e}")
    st.stop()

# ========================================
# SIDEBAR - MENU DE NAVEGAÇÃO
# ========================================

st.sidebar.title("🌾 FarmTech Solutions")
st.sidebar.markdown("### Sistema Integrado - Fase 7")
st.sidebar.markdown("---")

menu_option = st.sidebar.radio(
    "📋 Navegação",
    [
        "🏠 Home",
        "📊 Fase 1: Cálculos e Clima",
        "🗄️ Fase 2: Gestão de Dados",
        "🌡️ Fase 3: Monitoramento IoT",
        "🤖 Fase 4: Machine Learning",
        "👁️ Fase 6: Visão Computacional",
        "🔔 Análise Integrada",
        "⚙️ Status do Sistema"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    """
    **📚 Sobre o Projeto:**
    
    Sistema que integra todas as fases do projeto FarmTech Solutions FIAP.
    
    - Fase 1: Cálculos e API Meteorológica
    - Fase 2: Banco de Dados Estruturado
    - Fase 3: IoT e Sensores
    - Fase 4: Machine Learning
    - Fase 5: Cloud Computing (AWS)
    - Fase 6: Visão Computacional
    """
)

# ========================================
# PÁGINA: HOME
# ========================================

if menu_option == "🏠 Home":
    st.title("🌾 FarmTech Solutions - Fase 7")
    st.markdown("## Sistema Consolidado de Gestão para Agronegócio")
    
    st.markdown("""
    ### 👋 Bem-vindo ao Sistema Integrado!
    
    Este dashboard consolida todas as funcionalidades desenvolvidas nas Fases 1 a 6 do projeto FarmTech Solutions.
    
    #### 🎯 Funcionalidades Principais:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📊 Fase 1: Cálculos e Clima**
        - Cálculo de área de plantio
        - Gestão de insumos
        - Previsão do tempo
        - Análise de chuva
        """)
        
        st.markdown("""
        **🗄️ Fase 2: Gestão de Dados**
        - Sistema CRUD completo
        - Gestão de funcionários
        - Controle de insumos
        - Gestão financeira
        """)
    
    with col2:
        st.markdown("""
        **🌡️ Fase 3: IoT**
        - Monitoramento de sensores
        - Umidade e pH do solo
        - Detecção de nutrientes
        - Controle de irrigação
        """)
        
        st.markdown("""
        **🤖 Fase 4: Machine Learning**
        - Previsão de irrigação
        - Análise preditiva
        - Recomendações inteligentes
        """)
    
    with col3:
        st.markdown("""
        **☁️ Fase 5: Cloud & AWS**
        - Infraestrutura na nuvem
        - Sistema de alertas
        - Mensageria (SNS/SMS)
        """)
        
        st.markdown("""
        **👁️ Fase 6: Visão Computacional**
        - Detecção de pragas
        - Análise de saúde das plantas
        - YOLO para monitoramento
        """)
    
    st.markdown("---")
    
    # Resumo do sistema
    st.subheader("📈 Resumo do Sistema")
    
    try:
        resumo = controller.obter_dashboard_resumo()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_plantios = resumo['fase1']['total_plantios']
            st.metric("Plantios Registrados", total_plantios)
        
        with col2:
            db_status = "✅ Online" if resumo['fase2']['db_status'] else "❌ Offline"
            st.metric("Banco de Dados", db_status)
        
        with col3:
            total_leituras = resumo['fase3']['estatisticas_sensores']['total_leituras']
            st.metric("Leituras de Sensores", total_leituras)
        
        with col4:
            modelo_status = "✅ Carregado" if resumo['fase4']['modelo_info']['carregado'] else "❌ N/D"
            st.metric("Modelo ML", modelo_status)
        
        # Alertas
        if resumo['fase3']['alertas']:
            st.warning("**⚠️ Alertas Ativos:**")
            for alerta in resumo['fase3']['alertas']:
                st.warning(alerta)
    
    except Exception as e:
        st.error(f"Erro ao carregar resumo: {e}")

# ========================================
# PÁGINA: FASE 1 - CÁLCULOS E CLIMA
# ========================================

elif menu_option == "📊 Fase 1: Cálculos e Clima":
    st.title("📊 Fase 1: Cálculos de Plantio e Previsão do Tempo")
    
    tab1, tab2 = st.tabs(["🌱 Cálculo de Plantio", "🌦️ Previsão do Tempo"])
    
    # TAB: Cálculo de Plantio
    with tab1:
        st.header("Cálculo de Área e Insumos")
        
        cultura = st.selectbox("Selecione a cultura:", ["Milho", "Soja"])
        
        if cultura == "Milho":
            st.subheader("🌽 Plantio de Milho (Área Retangular)")
            
            col1, col2 = st.columns(2)
            with col1:
                comprimento = st.number_input("Comprimento (m):", min_value=0.1, value=100.0, step=1.0)
            with col2:
                largura = st.number_input("Largura (m):", min_value=0.1, value=50.0, step=1.0)
            
            if st.button("📐 Calcular Milho", type="primary"):
                try:
                    resultado = controller.calcular_plantio_milho(comprimento, largura)
                    
                    st.success("✅ Cálculo realizado com sucesso!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Área Total", f"{resultado['area']:.2f} m²")
                    with col2:
                        st.metric("Tipo de Insumo", resultado['tipo_insumo'])
                    with col3:
                        st.metric("Quantidade", f"{resultado['qnt_insumo']:.2f} L")
                    
                    with st.expander("📄 Detalhes Completos"):
                        st.json(resultado)
                
                except Exception as e:
                    st.error(f"❌ Erro: {e}")
        
        else:  # Soja
            st.subheader("🌿 Plantio de Soja (Área Circular)")
            
            raio = st.number_input("Raio (m):", min_value=0.1, value=50.0, step=1.0)
            
            if st.button("📐 Calcular Soja", type="primary"):
                try:
                    resultado = controller.calcular_plantio_soja(raio)
                    
                    st.success("✅ Cálculo realizado com sucesso!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Área Total", f"{resultado['area']:.2f} m²")
                    with col2:
                        st.metric("Tipo de Insumo", resultado['tipo_insumo'])
                    with col3:
                        st.metric("Quantidade", f"{resultado['qnt_insumo']:.2f} L")
                    
                    with st.expander("📄 Detalhes Completos"):
                        st.json(resultado)
                
                except Exception as e:
                    st.error(f"❌ Erro: {e}")
        
        # Exibir dados armazenados
        st.markdown("---")
        st.subheader("📋 Histórico de Plantios")
        
        dados = controller.obter_dados_plantio()
        if dados:
            df = pd.DataFrame(dados)
            st.dataframe(df, use_container_width=True)
            
            # Resumo
            resumo = controller.obter_resumo_plantio()
            st.markdown("**📊 Resumo:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Plantios", resumo['total_registros'])
            with col2:
                st.metric("Área Total", f"{resumo['area_total']:.2f} m²")
            with col3:
                st.metric("Insumo Total", f"{resumo['insumo_total']:.2f} L")
        else:
            st.info("Nenhum plantio registrado ainda.")
    
    # TAB: Previsão do Tempo
    with tab2:
        st.header("🌦️ Previsão do Tempo")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            cidade = st.text_input("Digite a cidade:", value="São Paulo")
        with col2:
            pais = st.text_input("País:", value="BR", max_chars=2)
        
        if st.button("🌍 Buscar Previsão", type="primary"):
            with st.spinner("Consultando API meteorológica..."):
                clima_info = controller.obter_previsao_clima(cidade, pais)
            
            if clima_info:
                st.success("✅ Dados obtidos com sucesso!")
                
                # Status de chuva
                if clima_info['ha_chuva']:
                    st.warning("⚠️ **ALERTA:** Previsão de chuva significativa nas próximas horas!")
                else:
                    st.info("✅ Sem previsão de chuva significativa")
                
                # Informações da cidade
                if clima_info['cidade_info']:
                    st.markdown(f"**📍 Localização:** {clima_info['cidade_info']['nome']}, {clima_info['cidade_info']['pais']}")
                
                # Tabela de previsões
                st.subheader("📊 Previsões Detalhadas")
                
                if clima_info['previsoes']:
                    df_previsoes = pd.DataFrame(clima_info['previsoes'])
                    st.dataframe(df_previsoes, use_container_width=True)
                    
                    # Gráfico de temperatura
                    st.line_chart(df_previsoes.set_index('timestamp')['temp'])
            else:
                st.error("❌ Erro ao buscar dados climáticos. Verifique o nome da cidade e a API key.")

# ========================================
# PÁGINA: FASE 2 - GESTÃO DE DADOS
# ========================================

elif menu_option == "🗄️ Fase 2: Gestão de Dados":
    st.title("🗄️ Fase 2: Sistema de Gestão (CRUD)")
    
    st.info("""
    🚧 **Esta seção será expandida pela Pessoa 4 (Frontend Lead & Documentador)**
    
    Funcionalidades planejadas:
    - Gestão de Funcionários
    - Gestão de Insumos
    - Gestão de Talhões
    - Controle Financeiro
    - Relatórios
    - Checklist de Tarefas
    """)
    
    # Status do banco de dados
    st.subheader("💾 Status do Banco de Dados")
    if controller.testar_conexao_db():
        st.success("✅ Conexão com banco de dados OK")
    else:
        st.error("❌ Erro na conexão com banco de dados")

# ========================================
# PÁGINA: FASE 3 - MONITORAMENTO IoT
# ========================================

elif menu_option == "🌡️ Fase 3: Monitoramento IoT":
    st.title("🌡️ Fase 3: Monitoramento de Sensores IoT")
    
    st.markdown("### 📡 Dados dos Sensores ESP32")
    
    # Botão para gerar dados simulados
    col1, col2 = st.columns([3, 1])
    with col1:
        n_leituras = st.slider("Número de leituras a gerar:", 5, 50, 20)
    with col2:
        if st.button("🔄 Gerar Dados Simulados"):
            controller.gerar_dados_sensores_simulados(n_leituras)
            st.success(f"✅ {n_leituras} leituras geradas!")
    
    # Última leitura
    ultima_leitura = controller.obter_ultima_leitura_sensor()
    
    if ultima_leitura:
        st.subheader("📊 Última Leitura")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Umidade", f"{ultima_leitura.umidade:.1f}%")
        with col2:
            st.metric("pH do Solo", f"{ultima_leitura.ph:.2f}")
        with col3:
            status_p = "✅ Presente" if ultima_leitura.fosforo_presente else "❌ Ausente"
            st.metric("Fósforo (P)", status_p)
        with col4:
            status_k = "✅ Presente" if ultima_leitura.potassio_presente else "❌ Ausente"
            st.metric("Potássio (K)", status_k)
        with col5:
            status_bomba = "🟢 Ligada" if ultima_leitura.bomba_ligada else "🔴 Desligada"
            st.metric("Bomba", status_bomba)
        
        # Alertas
        alertas = controller.obter_alertas_sensores()
        if alertas:
            st.warning("**⚠️ Alertas Ativos:**")
            for alerta in alertas:
                st.warning(alerta)
        
        # Estatísticas
        st.markdown("---")
        st.subheader("📈 Estatísticas do Histórico")
        
        stats = controller.obter_estatisticas_sensores()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Leituras", stats['total_leituras'])
        with col2:
            st.metric("Umidade Média", f"{stats['umidade_media']:.1f}%")
        with col3:
            st.metric("pH Médio", f"{stats['ph_medio']:.2f}")
        with col4:
            st.metric("% Irrigação", f"{stats['percentual_irrigacao']:.1f}%")
        
        # Histórico em tabela
        st.markdown("---")
        st.subheader("📋 Histórico de Leituras")
        
        historico = controller.sensor_handler.exportar_para_dict()
        if historico:
            df_historico = pd.DataFrame(historico)
            st.dataframe(df_historico, use_container_width=True)
    
    else:
        st.info("Nenhuma leitura disponível. Gere dados simulados para começar.")

# ========================================
# PÁGINA: FASE 4 - MACHINE LEARNING
# ========================================

elif menu_option == "🤖 Fase 4: Machine Learning":
    st.title("🤖 Fase 4: Previsão de Irrigação com Machine Learning")
    
    # Info do modelo
    modelo_info = controller.obter_info_modelo_ml()
    
    if modelo_info['carregado']:
        st.success(f"✅ Modelo carregado: {modelo_info.get('tipo_modelo', 'N/A')}")
    else:
        st.warning("""
        ⚠️ **Modelo ML não encontrado!**
        
        Para usar esta funcionalidade, copie o arquivo `modelo_irrigacao.pkl` 
        da Fase 4 para a pasta `models/` do projeto.
        """)
    
    st.markdown("---")
    st.header("📊 Entrada de Dados dos Sensores")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        umidade = st.slider("Umidade do Solo (%)", 0.0, 100.0, 50.0, 1.0)
    with col2:
        temperatura = st.slider("Temperatura (°C)", 0.0, 50.0, 25.0, 0.5)
    with col3:
        nutrientes = st.slider("Nutrientes N (ppm)", 0.0, 300.0, 150.0, 5.0)
    
    if st.button("🔮 Prever Necessidade de Irrigação", type="primary"):
        resultado = controller.prever_irrigacao(umidade, temperatura, nutrientes)
        
        if 'erro' in resultado:
            st.error(f"❌ {resultado['erro']}")
        else:
            st.markdown("---")
            st.subheader("📊 Resultado da Previsão")
            
            if resultado['deve_irrigar']:
                st.error(f"### 💧 **{resultado['status']}**")
            else:
                st.success(f"### ✅ **{resultado['status']}**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Decisão", resultado['status'])
            with col2:
                st.metric("Confiança", resultado['confianca'].capitalize())
            
            # Probabilidades (se disponível)
            if resultado.get('probabilidade'):
                st.markdown("**Probabilidades:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Não Irrigar", f"{resultado['probabilidade']['nao_irrigar']:.1%}")
                with col2:
                    st.metric("Irrigar", f"{resultado['probabilidade']['irrigar']:.1%}")
            
            with st.expander("📄 Detalhes Completos"):
                st.json(resultado)

# ========================================
# PÁGINA: FASE 6 - VISÃO COMPUTACIONAL
# ========================================

elif menu_option == "👁️ Fase 6: Visão Computacional":
    st.title("👁️ Fase 6: Visão Computacional com YOLO")
    
    st.warning("""
    🚧 **Esta seção será implementada pela Pessoa 3 (Especialista em IA & IoT)**
    
    Funcionalidades planejadas:
    - Upload de imagens de plantas
    - Detecção automática de pragas usando YOLO
    - Análise de saúde das plantas
    - Geração de relatórios visuais
    - Sistema de alertas para problemas detectados
    """)
    
    st.info("""
    **Como usar (quando implementado):**
    
    1. Faça upload de uma imagem da plantação
    2. O sistema processará usando YOLOv5/v8
    3. Receberá análise automática de:
       - Presença de pragas
       - Doenças visíveis
       - Saúde geral da planta
       - Recomendações de ação
    """)

# ========================================
# PÁGINA: ANÁLISE INTEGRADA
# ========================================

elif menu_option == "🔔 Análise Integrada":
    st.title("🔔 Análise Integrada: Decisão Inteligente de Irrigação")
    st.markdown("### Combina Clima (Fase 1) + Machine Learning (Fase 4)")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📍 Localização")
        cidade = st.text_input("Cidade:", value="São Paulo", key="cidade_integrada")
    
    with col2:
        st.subheader("🌡️ Dados dos Sensores")
        umidade_int = st.number_input("Umidade do Solo (%):", 0.0, 100.0, 35.0, 1.0, key="umidade_int")
    
    col1, col2 = st.columns(2)
    with col1:
        temperatura_int = st.number_input("Temperatura (°C):", 0.0, 50.0, 28.0, 0.5, key="temp_int")
    with col2:
        nutrientes_int = st.number_input("Nutrientes N (ppm):", 0.0, 300.0, 150.0, 5.0, key="nutr_int")
    
    if st.button("🚀 Executar Análise Completa", type="primary"):
        with st.spinner("🔍 Processando análise integrada..."):
            resultado = controller.analisar_necessidade_irrigacao_completa(
                cidade, umidade_int, temperatura_int, nutrientes_int
            )
        
        st.markdown("---")
        st.subheader("📊 Resultado da Análise")
        
        # Decisão principal
        if resultado['deve_irrigar']:
            st.error(f"### 💧 RECOMENDAÇÃO: IRRIGAR")
            cor_prioridade = "🔴" if resultado['prioridade'] == 'alta' else "🟡" if resultado['prioridade'] == 'media' else "🟢"
            st.warning(f"**Prioridade:** {cor_prioridade} {resultado['prioridade'].upper()}")
        else:
            st.success(f"### ✅ RECOMENDAÇÃO: NÃO IRRIGAR")
        
        st.info(f"**💡 Motivo:** {resultado['motivo']}")
        
        # Detalhes das análises
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🌦️ Análise Climática:**")
            if resultado['clima']:
                if resultado['clima']['ha_chuva']:
                    st.warning("⚠️ Previsão de chuva detectada")
                else:
                    st.success("✅ Sem previsão de chuva")
            else:
                st.error("❌ Dados climáticos indisponíveis")
        
        with col2:
            st.markdown("**🤖 Análise ML:**")
            if resultado['ml_previsao'].get('deve_irrigar'):
                st.warning("💧 ML recomenda irrigar")
            else:
                st.success("✅ ML: umidade adequada")
            st.info(f"Confiança: {resultado['ml_previsao'].get('confianca', 'N/A')}")
        
        # Detalhes completos
        with st.expander("📄 Ver Análise Completa"):
            st.json(resultado)

# ========================================
# PÁGINA: STATUS DO SISTEMA
# ========================================

elif menu_option == "⚙️ Status do Sistema":
    st.title("⚙️ Status do Sistema FarmTech")
    
    st.markdown("### 🔍 Verificação de Componentes")
    
    status = controller.status_sistema()
    
    # Status dos módulos
    st.subheader("📦 Módulos do Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Fase 1: Cálculos e Clima**")
        st.write(f"{'✅' if status['fase1_calculo'] else '❌'} Calculadora de Plantio")
        st.write(f"{'✅' if status['fase1_clima'] else '❌'} Serviço de Clima")
        
        st.markdown("**Fase 2: Banco de Dados**")
        st.write(f"{'✅' if status['fase2_database'] else '❌'} Conexão com Database")
        
        st.markdown("**Fase 3: IoT**")
        st.write(f"{'✅' if status['fase3_sensores'] else '❌'} Handler de Sensores")
    
    with col2:
        st.markdown("**Fase 4: Machine Learning**")
        st.write(f"{'✅' if status['fase4_ml'] else '❌'} Modelo ML Carregado")
        
        st.markdown("**Fase 6: Visão Computacional**")
        st.write(f"{'✅' if status['fase6_yolo'] else '⚠️'} YOLO Detector (placeholder)")
    
    # Configurações
    st.markdown("---")
    st.subheader("⚙️ Configurações")
    
    config_status = status['configuracao']
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"{'✅' if config_status['api_weather'] else '❌'} API Meteorológica")
        st.write(f"{'✅' if config_status['db_sqlite'] else '❌'} SQLite Database")
    with col2:
        st.write(f"{'✅' if config_status['db_oracle'] else '⚠️'} Oracle Database (opcional)")
        st.write(f"{'✅' if config_status['aws'] else '⚠️'} AWS (Fase 5 - Pessoa 2)")
    
    # Informações adicionais
    st.markdown("---")
    st.subheader("ℹ️ Informações do Sistema")
    
    st.code(f"""
Diretório Base: {Config.BASE_DIR}
Diretório de Dados: {Config.DATA_DIR}
Diretório de Modelos: {Config.MODELS_DIR}
Banco SQLite: {Config.SQLITE_DB_PATH}
Ambiente: {Config.ENVIRONMENT}
    """)

# ========================================
# FOOTER
# ========================================

st.sidebar.markdown("---")
st.sidebar.markdown("""
<small>
**FarmTech Solutions v7.0**<br>
Desenvolvido para FIAP<br>
Equipe: Pessoas 1-4
</small>
""", unsafe_allow_html=True)

