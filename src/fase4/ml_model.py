"""
Módulo para modelo de Machine Learning de previsão de irrigação
Adaptado da Fase 4 (modelagem_ml.py)
"""

import joblib
import pandas as pd
import numpy as np
from typing import Dict, Optional, List
import os
from pathlib import Path


class MLModel:
    """Classe para carregar e usar modelo de ML para previsão de irrigação"""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Inicializa o modelo de ML
        
        Args:
            model_path: Caminho para o arquivo .pkl do modelo treinado
        """
        if model_path is None:
            from src.core.config import Config
            model_path = Config.ML_MODEL_PATH
        
        self.model_path = model_path
        self.model = None
        self.model_info = {
            'carregado': False,
            'features': ['umidade_solo', 'temperatura', 'nutrientes_N'],
            'target': 'acao_irrigacao'
        }
        
        self._carregar_modelo()
    
    def _carregar_modelo(self):
        """Carrega modelo treinado do disco"""
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                self.model_info['carregado'] = True
                print(f"✅ Modelo ML carregado: {self.model_path}")
            except Exception as e:
                print(f"❌ Erro ao carregar modelo: {e}")
                self.model_info['carregado'] = False
        else:
            print(f"⚠️ Modelo não encontrado em: {self.model_path}")
            print("   Execute o treinamento primeiro ou copie o modelo da Fase 4")
            self.model_info['carregado'] = False
    
    def prever(self, dados: Dict) -> Dict:
        """
        Faz previsão baseado nos dados de sensores
        
        Args:
            dados: Dicionário com 'umidade_solo', 'temperatura', 'nutrientes_N'
            
        Returns:
            Dicionário com resultado da previsão
        """
        if not self.model_info['carregado']:
            return {
                'erro': 'Modelo não carregado',
                'deve_irrigar': None,
                'status': 'ERRO',
                'dados_entrada': dados
            }
        
        try:
            # Preparar dados para o modelo
            df = pd.DataFrame([dados])
            
            # Garantir que as colunas estão na ordem correta
            df = df[self.model_info['features']]
            
            # Fazer previsão
            previsao = self.model.predict(df)[0]
            
            # Tentar obter probabilidade (se o modelo suportar)
            probabilidade = None
            if hasattr(self.model, 'predict_proba'):
                prob = self.model.predict_proba(df)[0]
                probabilidade = {
                    'nao_irrigar': round(float(prob[0]), 3),
                    'irrigar': round(float(prob[1]), 3)
                }
            
            resultado = {
                'deve_irrigar': bool(previsao == 1),
                'codigo_previsao': int(previsao),
                'status': "IRRIGAR" if previsao == 1 else "NÃO IRRIGAR",
                'probabilidade': probabilidade,
                'dados_entrada': dados,
                'confianca': self._calcular_confianca(dados, previsao)
            }
            
            return resultado
            
        except Exception as e:
            return {
                'erro': f'Erro na previsão: {str(e)}',
                'deve_irrigar': None,
                'status': 'ERRO',
                'dados_entrada': dados
            }
    
    def _calcular_confianca(self, dados: Dict, previsao: int) -> str:
        """
        Calcula nível de confiança baseado nos dados de entrada
        
        Args:
            dados: Dados de entrada
            previsao: Resultado da previsão
            
        Returns:
            'alta', 'media' ou 'baixa'
        """
        umidade = dados.get('umidade_solo', 50)
        
        # Lógica simples de confiança
        if previsao == 1:  # Irrigar
            if umidade < 30:
                return 'alta'
            elif umidade < 45:
                return 'media'
            else:
                return 'baixa'
        else:  # Não irrigar
            if umidade > 60:
                return 'alta'
            elif umidade > 45:
                return 'media'
            else:
                return 'baixa'
    
    def prever_lote(self, lista_dados: List[Dict]) -> List[Dict]:
        """
        Faz previsões para múltiplas entradas
        
        Args:
            lista_dados: Lista de dicionários com dados de sensores
            
        Returns:
            Lista de dicionários com resultados
        """
        return [self.prever(dados) for dados in lista_dados]
    
    def obter_importancia_features(self) -> Optional[Dict]:
        """
        Retorna importância das features (se o modelo suportar)
        
        Returns:
            Dicionário com importância das features ou None
        """
        if not self.model_info['carregado']:
            return None
        
        if hasattr(self.model, 'feature_importances_'):
            importancias = self.model.feature_importances_
            return dict(zip(self.model_info['features'], importancias))
        
        return None
    
    def validar_entrada(self, dados: Dict) -> tuple[bool, str]:
        """
        Valida dados de entrada antes da previsão
        
        Args:
            dados: Dicionário com dados de sensores
            
        Returns:
            Tupla (é_válido, mensagem)
        """
        # Verificar se todas as features necessárias estão presentes
        features_faltando = [
            f for f in self.model_info['features'] 
            if f not in dados
        ]
        
        if features_faltando:
            return False, f"Features faltando: {', '.join(features_faltando)}"
        
        # Validar ranges
        umidade = dados.get('umidade_solo')
        if not (0 <= umidade <= 100):
            return False, "Umidade deve estar entre 0 e 100%"
        
        temperatura = dados.get('temperatura')
        if not (-10 <= temperatura <= 60):
            return False, "Temperatura deve estar entre -10°C e 60°C"
        
        nutrientes = dados.get('nutrientes_N')
        if nutrientes < 0:
            return False, "Nutrientes não podem ser negativos"
        
        return True, "Dados válidos"
    
    def info(self) -> Dict:
        """Retorna informações sobre o modelo"""
        info = self.model_info.copy()
        
        if self.model:
            info['tipo_modelo'] = type(self.model).__name__
            
            if hasattr(self.model, 'n_estimators'):
                info['n_estimators'] = self.model.n_estimators
            
            if hasattr(self.model, 'oob_score_'):
                info['oob_score'] = round(self.model.oob_score_, 4)
        
        return info
