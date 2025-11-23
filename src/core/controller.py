"""
Controlador Central do Sistema FarmTech
Integra todos os módulos das Fases 1-6
"""

from alerts.aws_alert import send_alert
from typing import Optional, Dict, Any, List
import os
from datetime import datetime


class FarmTechController:
    """
    Controlador central que integra todas as fases do projeto
    
    Responsável por:
    - Inicializar todos os serviços
    - Coordenar comunicação entre módulos
    - Fornecer interface unificada para o dashboard
    """
    
    def __init__(self):
        """Inicializa o controlador e todos os serviços"""
        self.calculo_plantio = None
        self.clima_service = None
        self.ml_model = None
        self.database = None
        self.sensor_handler = None
        self.yolo_detector = None
        
        self._inicializar_servicos()
    
    def _inicializar_servicos(self):
        """Inicializa todos os serviços necessários"""
        print("🚀 Inicializando FarmTech Controller...")
        
        try:
            # Fase 1: Cálculos e Clima
            from src.fase1.calculo_plantio import CalculoPlantio
            from src.fase1.clima_service import ClimaService
            from src.core.config import Config
            
            self.calculo_plantio = CalculoPlantio()
            self.clima_service = ClimaService(Config.OPENWEATHER_API_KEY)
            print("  ✅ Fase 1: Cálculos e Clima inicializados")
            
            # Fase 2: Database
            from src.fase2.database import DatabaseHandler
            from src.fase2.models import Base
            
            self.database = DatabaseHandler(db_type="sqlite")
            self.database.create_tables(Base)
            print("  ✅ Fase 2: Banco de dados inicializado")
            
            # Fase 3: Sensores IoT
            from src.fase3.sensor_handler import SensorHandler
            
            self.sensor_handler = SensorHandler()
            print("  ✅ Fase 3: Handler de sensores inicializado")
            
            # Fase 4: Machine Learning
            from src.fase4.ml_model import MLModel
            
            self.ml_model = MLModel()
            print("  ✅ Fase 4: Modelo ML inicializado")
            
            # Fase 6: YOLO (placeholder)
            from src.fase6.yolo_detector import YOLODetector
            
            self.yolo_detector = YOLODetector()
            print("  ✅ Fase 6: YOLO detector inicializado (placeholder)")
            
            print("✅ Todos os serviços inicializados com sucesso!\n")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar serviços: {e}")
            raise
    
    # ========================================
    # MÉTODOS PARA FASE 1: Cálculos e Clima
    # ========================================
    
    def calcular_plantio_milho(self, comprimento: float, largura: float) -> Dict:
        """
        Calcula área e insumos para plantio de milho
        
        Args:
            comprimento: Comprimento do terreno em metros
            largura: Largura do terreno em metros
            
        Returns:
            Dicionário com informações do plantio
        """
        area = self.calculo_plantio.calcular_area_retangular(comprimento, largura)
        return self.calculo_plantio.adicionar_plantio("milho", area)
    
    def calcular_plantio_soja(self, raio: float) -> Dict:
        """
        Calcula área e insumos para plantio de soja
        
        Args:
            raio: Raio do terreno circular em metros
            
        Returns:
            Dicionário com informações do plantio
        """
        area = self.calculo_plantio.calcular_area_circular(raio)
        return self.calculo_plantio.adicionar_plantio("soja", area)
    
    def obter_previsao_clima(self, cidade: str, pais: str = "BR") -> Optional[Dict]:
        """
        Obtém previsão do tempo para uma cidade
        
        Args:
            cidade: Nome da cidade
            pais: Código do país (padrão: BR)
            
        Returns:
            Dicionário com previsão ou None se falhar
        """
        dados = self.clima_service.buscar_previsao(cidade, pais)
        if dados:
            chuva, previsoes = self.clima_service.analisar_chuva(dados)
            cidade_info = self.clima_service.obter_info_cidade(dados)
            
            return {
                'dados_api': dados,
                'ha_chuva': chuva,
                'previsoes': previsoes,
                'cidade_info': cidade_info
            }
        return None
    
    def obter_dados_plantio(self) -> List[Dict]:
        """Retorna todos os dados de plantio armazenados"""
        return self.calculo_plantio.obter_dados()
    
    def obter_resumo_plantio(self) -> Dict:
        """Retorna resumo estatístico dos plantios"""
        return self.calculo_plantio.obter_resumo()
    
    # ========================================
    # MÉTODOS PARA FASE 2: Banco de Dados
    # ========================================
    
    def obter_sessao_db(self):
        """Retorna sessão do banco de dados para operações CRUD"""
        return self.database.get_session()
    
    def testar_conexao_db(self) -> bool:
        """Testa conexão com o banco de dados"""
        return self.database.test_connection()
    
    # ========================================
    # MÉTODOS PARA FASE 3: Sensores IoT
    # ========================================
    
    def gerar_dados_sensores_simulados(self, n_leituras: int = 20) -> List:
        """
        Gera dados simulados de sensores para demonstração
        
        Args:
            n_leituras: Número de leituras a gerar
            
        Returns:
            Lista de SensorData
        """
        return self.sensor_handler.gerar_dados_simulados(n_leituras)
    
    def adicionar_leitura_sensor(self, umidade: float, ph: float,
                                 fosforo: bool, potassio: bool,
                                 temperatura: Optional[float] = None):
        """
        Adiciona nova leitura de sensor
        
        Args:
            umidade: Umidade do solo (%)
            ph: pH do solo
            fosforo: Presença de fósforo
            potassio: Presença de potássio
            temperatura: Temperatura (opcional)
            
        Returns:
            SensorData criado
        """
        return self.sensor_handler.adicionar_leitura(
            umidade, ph, fosforo, potassio, temperatura
        )

         # NOVO — verifica alertas e envia para AWS se tiver crítico
        self.sensor_handler.verificar_alertas()

        return dado
    
    def obter_ultima_leitura_sensor(self):
        """Retorna última leitura de sensor"""
        return self.sensor_handler.obter_ultima_leitura()
    
    def obter_estatisticas_sensores(self) -> Dict:
        """Retorna estatísticas do histórico de sensores"""
        return self.sensor_handler.obter_estatisticas()
    
    def obter_alertas_sensores(self) -> List[str]:
    """Verifica alertas e também dispara AWS se houver crítico"""

    alertas = self.sensor_handler.verificar_alertas()

    # Se houver alertas, envia para AWS (segurança extra)
    if alertas:
        mensagem = " | ".join(alertas)
        send_alert(f"ALERTA DO CONTROLLER: {mensagem}")

    return alertas
    
    # ========================================
    # MÉTODOS PARA FASE 4: Machine Learning
    # ========================================
    
    def prever_irrigacao(self, umidade: float, temperatura: float, 
                        nutrientes: float) -> Dict:
        """
        Faz previsão de necessidade de irrigação usando ML
        
        Args:
            umidade: Umidade do solo (%)
            temperatura: Temperatura (°C)
            nutrientes: Nível de nutrientes N (ppm)
            
        Returns:
            Dicionário com previsão
        """
        dados = {
            'umidade_solo': umidade,
            'temperatura': temperatura,
            'nutrientes_N': nutrientes
        }
        return self.ml_model.prever(dados)
    
    def obter_info_modelo_ml(self) -> Dict:
        """Retorna informações sobre o modelo ML"""
        return self.ml_model.info()
    
    # ========================================
    # MÉTODOS PARA FASE 6: Visão Computacional
    # ========================================
    
    def detectar_pragas(self, imagem_path: str) -> Dict:
        """
        Detecta pragas em uma imagem (placeholder)
        
        Args:
            imagem_path: Caminho para a imagem
            
        Returns:
            Resultado da detecção
        """
        return self.yolo_detector.detectar(imagem_path)
    
    def analisar_saude_planta(self, imagem_path: str) -> Dict:
        """
        Analisa saúde da planta (placeholder)
        
        Args:
            imagem_path: Caminho para a imagem
            
        Returns:
            Análise de saúde
        """
        return self.yolo_detector.analisar_saude_planta(imagem_path)
    
    # ========================================
    # MÉTODOS INTEGRADOS (Múltiplas Fases)
    # ========================================
    
    def analisar_necessidade_irrigacao_completa(
        self, 
        cidade: str,
        umidade_solo: float, 
        temperatura: float, 
        nutrientes: float
    ) -> Dict:
        """
        Análise completa integrando clima (Fase 1) + ML (Fase 4)
        
        Args:
            cidade: Cidade para previsão do tempo
            umidade_solo: Umidade atual do solo (%)
            temperatura: Temperatura atual (°C)
            nutrientes: Nível de nutrientes N (ppm)
            
        Returns:
            Decisão final sobre irrigação
        """
        print(f"🔍 Analisando necessidade de irrigação para {cidade}...")
        
        # 1. Verificar clima
        clima_info = self.obter_previsao_clima(cidade)
        
        # 2. Previsão ML
        ml_resultado = self.prever_irrigacao(umidade_solo, temperatura, nutrientes)
        
        # 3. Decisão final integrada
        decisao_final = {
            'timestamp': datetime.now().isoformat(),
            'deve_irrigar': False,
            'motivo': '',
            'prioridade': 'baixa',
            'clima': clima_info,
            'ml_previsao': ml_resultado,
            'dados_entrada': {
                'cidade': cidade,
                'umidade_solo': umidade_solo,
                'temperatura': temperatura,
                'nutrientes_N': nutrientes
            }
        }
        
        # Lógica de decisão
        # Regra 1: Se há previsão de chuva, NÃO irrigar
        if clima_info and clima_info['ha_chuva']:
            decisao_final['deve_irrigar'] = False
            decisao_final['motivo'] = (
                "❌ Não irrigar: Previsão de chuva detectada nas próximas horas"
            )
            decisao_final['prioridade'] = 'baixa'
        
        # Regra 2: Se não há chuva, seguir recomendação do ML
        elif ml_resultado.get('deve_irrigar'):
            decisao_final['deve_irrigar'] = True
            decisao_final['motivo'] = (
                f"✅ Irrigar: Modelo ML recomenda irrigação "
                f"(Confiança: {ml_resultado.get('confianca', 'N/A')})"
            )
            
            # Definir prioridade baseada na umidade
            if umidade_solo < 30:
                decisao_final['prioridade'] = 'alta'
            elif umidade_solo < 45:
                decisao_final['prioridade'] = 'media'
            else:
                decisao_final['prioridade'] = 'baixa'
        
        # Regra 3: Sem chuva e sem necessidade de irrigação
        else:
            decisao_final['deve_irrigar'] = False
            decisao_final['motivo'] = (
                "✅ Não irrigar: Umidade do solo adequada "
                f"({umidade_solo}%)"
            )
            decisao_final['prioridade'] = 'baixa'
        
        return decisao_final
    
    def obter_dashboard_resumo(self) -> Dict:
        """
        Retorna resumo geral para dashboard principal
        
        Returns:
            Dicionário com informações de todas as fases
        """

        
        alertas = self.sensor_handler.verificar_alertas()
        
        if alertas:
            mensagem = " | ".join(alertas)
            send_alert(f"ALERTA DO DASHBOARD: {mensagem}")
        
        resumo = {
            'fase1': {
                'total_plantios': len(self.calculo_plantio.dados),
                'resumo': self.calculo_plantio.obter_resumo()
            },
            'fase2': {
                'db_status': self.database.test_connection()
            },
            'fase3': {
                'estatisticas_sensores': self.sensor_handler.obter_estatisticas(),
                'alertas': alertas

            },
            'fase4': {
                'modelo_info': self.ml_model.info()
            }
        }
        
        return resumo
    
    def status_sistema(self) -> Dict:
        """
        Verifica status de todos os componentes do sistema
        
        Returns:
            Dicionário com status de cada fase
        """
        from src.core.config import Config
        
        status = {
            'fase1_calculo': self.calculo_plantio is not None,
            'fase1_clima': self.clima_service is not None,
            'fase2_database': self.database is not None and self.database.test_connection(),
            'fase3_sensores': self.sensor_handler is not None,
            'fase4_ml': self.ml_model is not None and self.ml_model.model_info['carregado'],
            'fase6_yolo': self.yolo_detector is not None,
            'configuracao': Config.validate_config()
        }
        
        return status
