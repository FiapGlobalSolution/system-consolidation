"""
Módulo para cálculos de área de plantio e insumos
Refatorado da Fase 1 (Menu_final.py)
"""

import math
import pandas as pd
from typing import Tuple, Dict, List, Optional
from pathlib import Path


class CalculoPlantio:
    """Classe para cálculos de área de plantio e gestão de insumos"""
    
    # Constantes de insumos por cultura
    INSUMOS_CONFIG = {
        'milho': {
            'litros_por_m2': 100,
            'tipo': 'Fertilizante',
            'forma_terreno': 'retangular'
        },
        'soja': {
            'litros_por_m2': 600,
            'tipo': 'Fosfato',
            'forma_terreno': 'circular'
        }
    }
    
    def __init__(self):
        """Inicializa o gerenciador de cálculos"""
        self.dados: List[Dict] = []
    
    def calcular_insumos_milho(self, area: float) -> Tuple[float, str]:
        """
        Calcula insumos necessários para plantio de milho
        
        Args:
            area: Área em metros quadrados
            
        Returns:
            Tupla com (quantidade de insumo em litros, tipo de insumo)
        """
        config = self.INSUMOS_CONFIG['milho']
        qnt_insumo = area * config['litros_por_m2']
        return qnt_insumo, config['tipo']
    
    def calcular_insumos_soja(self, area: float) -> Tuple[float, str]:
        """
        Calcula insumos necessários para plantio de soja
        
        Args:
            area: Área em metros quadrados
            
        Returns:
            Tupla com (quantidade de insumo em litros, tipo de insumo)
        """
        config = self.INSUMOS_CONFIG['soja']
        qnt_insumo = area * config['litros_por_m2']
        return qnt_insumo, config['tipo']
    
    def calcular_area_retangular(self, comprimento: float, largura: float) -> float:
        """
        Calcula área retangular (usado para milho)
        
        Args:
            comprimento: Comprimento em metros
            largura: Largura em metros
            
        Returns:
            Área em metros quadrados
        """
        if comprimento <= 0 or largura <= 0:
            raise ValueError("Comprimento e largura devem ser maiores que zero")
        return comprimento * largura
    
    def calcular_area_circular(self, raio: float) -> float:
        """
        Calcula área circular (usado para soja)
        
        Args:
            raio: Raio em metros
            
        Returns:
            Área em metros quadrados
        """
        if raio <= 0:
            raise ValueError("Raio deve ser maior que zero")
        return math.pi * (raio ** 2)
    
    def calcular_area_circular_por_diametro(self, diametro: float) -> float:
        """
        Calcula área circular a partir do diâmetro
        
        Args:
            diametro: Diâmetro em metros
            
        Returns:
            Área em metros quadrados
        """
        raio = diametro / 2
        return self.calcular_area_circular(raio)
    
    def calcular_area_circular_por_circunferencia(self, circunferencia: float) -> float:
        """
        Calcula área circular a partir da circunferência
        
        Args:
            circunferencia: Circunferência em metros
            
        Returns:
            Área em metros quadrados
        """
        raio = circunferencia / (2 * math.pi)
        return self.calcular_area_circular(raio)
    
    def adicionar_plantio(self, cultura: str, area: float, **kwargs) -> Dict:
        """
        Adiciona dados de plantio e retorna informações calculadas
        
        Args:
            cultura: Tipo de cultura ('milho' ou 'soja')
            area: Área em metros quadrados
            **kwargs: Informações adicionais (opcional)
            
        Returns:
            Dicionário com informações do plantio
        """
        cultura_lower = cultura.lower()
        
        if cultura_lower not in self.INSUMOS_CONFIG:
            raise ValueError(f"Cultura '{cultura}' não suportada. Use 'milho' ou 'soja'")
        
        # Calcular insumos baseado na cultura
        if cultura_lower == "milho":
            qnt_insumo, tipo_insumo = self.calcular_insumos_milho(area)
        else:  # soja
            qnt_insumo, tipo_insumo = self.calcular_insumos_soja(area)
        
        # Criar registro de plantio
        plantio_info = {
            "cultura": cultura.capitalize(),
            "area": round(area, 2),
            "tipo_insumo": tipo_insumo,
            "qnt_insumo": round(qnt_insumo, 2),
            **kwargs  # Adiciona campos extras se fornecidos
        }
        
        self.dados.append(plantio_info)
        return plantio_info
    
    def exportar_csv(self, filename: Optional[str] = None) -> bool:
        """
        Exporta dados para arquivo CSV
        
        Args:
            filename: Nome do arquivo (opcional, padrão: dados_plantio.csv)
            
        Returns:
            True se exportou com sucesso, False se não há dados
        """
        if not self.dados:
            return False
        
        if filename is None:
            from src.core.config import Config
            filename = str(Config.DATA_DIR / "dados_plantio.csv")
        
        df = pd.DataFrame(self.dados)
        df.to_csv(filename, index=False)
        return True
    
    def obter_dados(self) -> List[Dict]:
        """
        Retorna todos os dados armazenados
        
        Returns:
            Lista de dicionários com dados de plantio
        """
        return self.dados
    
    def obter_resumo(self) -> Dict:
        """
        Retorna resumo estatístico dos dados
        
        Returns:
            Dicionário com estatísticas dos plantios
        """
        if not self.dados:
            return {
                'total_registros': 0,
                'area_total': 0,
                'culturas': {}
            }
        
        df = pd.DataFrame(self.dados)
        
        resumo = {
            'total_registros': len(self.dados),
            'area_total': df['area'].sum(),
            'culturas': df['cultura'].value_counts().to_dict(),
            'area_media': df['area'].mean(),
            'insumo_total': df['qnt_insumo'].sum()
        }
        
        return resumo
    
    def limpar_dados(self):
        """Limpa todos os dados armazenados"""
        self.dados.clear()
    
    def remover_registro(self, index: int) -> bool:
        """
        Remove um registro específico
        
        Args:
            index: Índice do registro a ser removido
            
        Returns:
            True se removeu com sucesso, False caso contrário
        """
        try:
            self.dados.pop(index)
            return True
        except IndexError:
            return False
