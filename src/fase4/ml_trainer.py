# src/fase4/ml_trainer.py
"""
Módulo para treinamento do modelo de Machine Learning.
Baseado na Fase 4 - modelagem_ml.py
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.core.config import ML_MODEL_PATH, ML_DATA_PATH


class MLTrainer:
    """Classe para treinamento do modelo de previsão de irrigação"""
    
    def __init__(self):
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    def gerar_dataset(self, num_samples: int = 1000, salvar: bool = True) -> pd.DataFrame:
        """
        Gera dataset artificial para treinamento
        
        Args:
            num_samples: Número de amostras
            salvar: Se deve salvar em CSV
            
        Returns:
            DataFrame com dados gerados
        """
        print(f"📊 Gerando dataset com {num_samples} amostras...")
        
        data = {
            'umidade_solo': np.random.uniform(15, 95, num_samples).round(2),
            'temperatura': np.random.uniform(10, 40, num_samples).round(2),
            'nutrientes_N': np.random.uniform(40, 250, num_samples).round(2),
        }
        df = pd.DataFrame(data)
        
        # Lógica para target: irrigar se umidade < 40 (com ruído)
        noise = np.random.normal(0, 5, num_samples)
        df['acao_irrigacao'] = np.where((df['umidade_solo'] + noise) < 40, 1, 0)
        
        if salvar:
            # Garantir que o diretório existe
            Path(ML_DATA_PATH).parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(ML_DATA_PATH, index=False)
            print(f"✅ Dataset salvo em: {ML_DATA_PATH}")
        
        return df
    
    def carregar_dados(self, filepath: str = None) -> pd.DataFrame:
        """
        Carrega dados de um arquivo CSV
        
        Args:
            filepath: Caminho do arquivo (usa ML_DATA_PATH se None)
            
        Returns:
            DataFrame com os dados
        """
        filepath = filepath or ML_DATA_PATH
        
        if not Path(filepath).exists():
            print(f"⚠️  Arquivo não encontrado: {filepath}")
            print("   Gerando dataset automaticamente...")
            return self.gerar_dataset()
        
        print(f"📂 Carregando dados de: {filepath}")
        return pd.read_csv(filepath)
    
    def preparar_dados(self, df: pd.DataFrame, test_size: float = 0.3):
        """
        Prepara dados para treinamento
        
        Args:
            df: DataFrame com os dados
            test_size: Proporção de dados para teste
        """
        X = df[['umidade_solo', 'temperatura', 'nutrientes_N']]
        y = df['acao_irrigacao']
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        print(f"✅ Dados preparados:")
        print(f"   Treino: {len(self.X_train)} amostras")
        print(f"   Teste: {len(self.X_test)} amostras")
    
    def treinar(self, n_estimators: int = 100):
        """
        Treina o modelo RandomForest
        
        Args:
            n_estimators: Número de árvores
        """
        print(f"\n🤖 Treinando modelo RandomForest ({n_estimators} árvores)...")
        
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=42,
            oob_score=True
        )
        
        self.model.fit(self.X_train, self.y_train)
        print("✅ Treinamento concluído!")
    
    def avaliar(self) -> dict:
        """
        Avalia o modelo treinado
        
        Returns:
            Dicionário com métricas de avaliação
        """
        print("\n📊 Avaliando modelo...")
        
        y_pred = self.model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        
        print(f"\n✅ Acurácia: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print("\n📋 Relatório de Classificação:")
        print(classification_report(
            self.y_test, y_pred,
            target_names=['Não Irrigar (0)', 'Irrigar (1)']
        ))
        print("\n📊 Matriz de Confusão:")
        print(confusion_matrix(self.y_test, y_pred))
        
        # Importância das features
        importancias = self.model.feature_importances_
        print("\n🔍 Importância das Features:")
        for nome, importancia in zip(['Umidade Solo', 'Temperatura', 'Nutrientes N'], importancias):
            print(f"   {nome}: {importancia:.4f}")
        
        return {
            'accuracy': accuracy,
            'feature_importance': {
                'umidade_solo': importancias[0],
                'temperatura': importancias[1],
                'nutrientes_N': importancias[2]
            }
        }
    
    def salvar_modelo(self, filepath: str = None):
        """
        Salva o modelo treinado
        
        Args:
            filepath: Caminho para salvar (usa ML_MODEL_PATH se None)
        """
        filepath = filepath or ML_MODEL_PATH
        
        # Garantir que o diretório existe
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(self.model, filepath)
        print(f"\n✅ Modelo salvo em: {filepath}")
    
    def pipeline_completo(self):
        """Executa pipeline completo de treinamento"""
        print("=" * 60)
        print("🚀 INICIANDO PIPELINE COMPLETO DE TREINAMENTO ML")
        print("=" * 60)
        
        # 1. Gerar/Carregar dados
        df = self.carregar_dados()
        
        # 2. Preparar dados
        self.preparar_dados(df)
        
        # 3. Treinar modelo
        self.treinar()
        
        # 4. Avaliar
        metricas = self.avaliar()
        
        # 5. Salvar
        self.salvar_modelo()
        
        print("\n" + "=" * 60)
        print("✅ PIPELINE CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        
        return metricas


def main():
    """Função principal para executar treinamento"""
    trainer = MLTrainer()
    trainer.pipeline_completo()


if __name__ == "__main__":
    main()

