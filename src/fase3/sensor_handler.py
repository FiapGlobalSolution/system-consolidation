"""
Módulo para gerenciamento de dados de sensores IoT
Adaptado da Fase 3 (painel_monitoramento.py)
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from aws_alert import send_alert



@dataclass
class SensorData:
    """Estrutura de dados para leituras de sensores"""
    timestamp: datetime
    umidade: float  # Porcentagem (0-100)
    ph: float  # pH do solo (0-14)
    fosforo_presente: bool  # Presença de fósforo
    potassio_presente: bool  # Presença de potássio
    bomba_ligada: bool  # Status da bomba de irrigação
    temperatura: Optional[float] = None  # Temperatura ambiente (opcional)
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SensorData':
        """Cria instância a partir de dicionário"""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


class SensorHandler:
    """Gerenciador de dados de sensores IoT"""
    
    # Limiares padrão para decisões
    LIMIAR_UMIDADE_BAIXA = 50  # % abaixo disso considera seco
    LIMIAR_PH_MINIMO = 5.5
    LIMIAR_PH_MAXIMO = 7.5
    
    def __init__(self):
        """Inicializa o handler de sensores"""
        self.historico: List[SensorData] = []
        self.ultima_leitura: Optional[SensorData] = None
    
    def gerar_dados_simulados(self, n_leituras: int = 20, 
                             intervalo_minutos: int = 5) -> List[SensorData]:
        """
        Gera dados simulados de sensores para demonstração
        
        Args:
            n_leituras: Número de leituras a gerar
            intervalo_minutos: Intervalo entre leituras
            
        Returns:
            Lista de SensorData simulados
        """
        dados = []
        tempo_inicial = datetime.now() - timedelta(minutes=n_leituras * intervalo_minutos)
        
        for i in range(n_leituras):
            tempo_atual = tempo_inicial + timedelta(minutes=i * intervalo_minutos)
            
            # Gerar valores aleatórios realistas
            umidade = random.uniform(30, 85)
            ph = random.uniform(5.5, 7.5)
            fosforo = random.choice([True, False])
            potassio = random.choice([True, False])
            temperatura = random.uniform(15, 35)
            
            # Lógica: bomba liga se umidade < limiar
            bomba_ligada = umidade < self.LIMIAR_UMIDADE_BAIXA
            
            sensor_data = SensorData(
                timestamp=tempo_atual,
                umidade=round(umidade, 2),
                ph=round(ph, 2),
                fosforo_presente=fosforo,
                potassio_presente=potassio,
                bomba_ligada=bomba_ligada,
                temperatura=round(temperatura, 1)
            )
            
            dados.append(sensor_data)
        
        self.historico.extend(dados)
        if dados:
            self.ultima_leitura = dados[-1]
        
        return dados
    
    def adicionar_leitura(self, umidade: float, ph: float, 
                         fosforo: bool, potassio: bool,
                         temperatura: Optional[float] = None) -> SensorData:
        """
        Adiciona uma nova leitura de sensor (dados reais ou simulados)
        
        Args:
            umidade: Umidade do solo (%)
            ph: pH do solo
            fosforo: Presença de fósforo
            potassio: Presença de potássio
            temperatura: Temperatura ambiente (opcional)
            
        Returns:
            SensorData criado
        """
        # Decide se deve ligar a bomba
        bomba_ligada = self.decidir_irrigacao(umidade, ph)
        
        sensor_data = SensorData(
            timestamp=datetime.now(),
            umidade=round(umidade, 2),
            ph=round(ph, 2),
            fosforo_presente=fosforo,
            potassio_presente=potassio,
            bomba_ligada=bomba_ligada,
            temperatura=round(temperatura, 1) if temperatura else None
        )
        
        self.historico.append(sensor_data)
        self.ultima_leitura = sensor_data
        
        return sensor_data
    
    def decidir_irrigacao(self, umidade: float, ph: float) -> bool:
        """
        Decide se deve ligar a bomba de irrigação
        
        Args:
            umidade: Umidade do solo atual
            ph: pH do solo atual
            
        Returns:
            True se deve irrigar, False caso contrário
        """
        # Lógica: irrigar se umidade baixa E pH está na faixa adequada
        umidade_baixa = umidade < self.LIMIAR_UMIDADE_BAIXA
        ph_adequado = self.LIMIAR_PH_MINIMO <= ph <= self.LIMIAR_PH_MAXIMO
        
        return umidade_baixa and ph_adequado
    
    def obter_ultima_leitura(self) -> Optional[SensorData]:
        """Retorna a última leitura registrada"""
        return self.ultima_leitura
    
    def obter_historico(self, limite: Optional[int] = None) -> List[SensorData]:
        """
        Retorna histórico de leituras
        
        Args:
            limite: Número máximo de leituras (mais recentes)
            
        Returns:
            Lista de SensorData
        """
        if limite:
            return self.historico[-limite:]
        return self.historico
    
    def obter_estatisticas(self) -> Dict:
        """
        Calcula estatísticas do histórico de sensores
        
        Returns:
            Dicionário com estatísticas
        """
        if not self.historico:
            return {
                'total_leituras': 0,
                'umidade_media': 0,
                'ph_medio': 0
            }
        
        umidades = [s.umidade for s in self.historico]
        phs = [s.ph for s in self.historico]
        bombas_ligadas = sum(1 for s in self.historico if s.bomba_ligada)
        
        return {
            'total_leituras': len(self.historico),
            'umidade_media': round(sum(umidades) / len(umidades), 2),
            'umidade_minima': round(min(umidades), 2),
            'umidade_maxima': round(max(umidades), 2),
            'ph_medio': round(sum(phs) / len(phs), 2),
            'ph_minimo': round(min(phs), 2),
            'ph_maximo': round(max(phs), 2),
            'ativacoes_bomba': bombas_ligadas,
            'percentual_irrigacao': round(bombas_ligadas / len(self.historico) * 100, 1)
        }
    
    def limpar_historico(self):
        """Limpa todo o histórico de leituras"""
        self.historico.clear()
        self.ultima_leitura = None
    
    def exportar_para_dict(self) -> List[Dict]:
        """
        Exporta histórico para lista de dicionários
        
        Returns:
            Lista de dicionários com dados dos sensores
        """
        return [s.to_dict() for s in self.historico]
    
    def verificar_alertas(self) -> List[str]:
        """
        Verifica condições de alerta baseado na última leitura
        
        Returns:
            Lista de alertas (strings)
        """
        if not self.ultima_leitura:
            return []
        
        alertas = []
        
        # Alerta: Umidade crítica
        if self.ultima_leitura.umidade < 30:
            alertas.append("⚠️ CRÍTICO: Umidade do solo muito baixa (<30%)")
        elif self.ultima_leitura.umidade < self.LIMIAR_UMIDADE_BAIXA:
            alertas.append("⚠️ ATENÇÃO: Umidade do solo baixa")
        
        # Alerta: pH fora da faixa
        if self.ultima_leitura.ph < self.LIMIAR_PH_MINIMO:
            alertas.append(f"⚠️ pH muito ácido ({self.ultima_leitura.ph})")
        elif self.ultima_leitura.ph > self.LIMIAR_PH_MAXIMO:
            alertas.append(f"⚠️ pH muito alcalino ({self.ultima_leitura.ph})")
        
        # Alerta: Falta de nutrientes
        if not self.ultima_leitura.fosforo_presente:
            alertas.append("⚠️ Fósforo (P) não detectado")
        if not self.ultima_leitura.potassio_presente:
            alertas.append("⚠️ Potássio (K) não detectado")

        # ENVIAR PARA AWS SE TIVER ALERTA CRÍTICO
        if alertas:  
            mensagem = " | ".join(alertas)  
            send_alert(f"ALERTA DETECTADO: {mensagem}")
        
        return alertas

