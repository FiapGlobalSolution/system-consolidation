"""
Módulo para integração com API de previsão do tempo
Refatorado da Fase 1 (painel_monitoramento.py)
"""

import requests
from datetime import datetime
from typing import Dict, Optional, Tuple, List


class ClimaService:
    """Serviço para consulta de previsão do tempo usando OpenWeatherMap API"""
    
    BASE_URL_FORECAST = "http://api.openweathermap.org/data/2.5/forecast"
    BASE_URL_CURRENT = "http://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self, api_key: str):
        """
        Inicializa o serviço de clima
        
        Args:
            api_key: Chave da API OpenWeatherMap
        """
        self.api_key = api_key
        self.ultima_consulta = None
    
    def buscar_previsao(self, cidade: str, pais_cod: str = "BR", 
                       num_timestamps: int = 8) -> Optional[Dict]:
        """
        Busca previsão do tempo para cidade especificada
        
        Args:
            cidade: Nome da cidade
            pais_cod: Código do país (padrão: BR)
            num_timestamps: Número de previsões a buscar (cada uma = 3h)
            
        Returns:
            Dicionário com dados da API ou None se falhar
        """
        params = {
            'q': f"{cidade},{pais_cod}",
            'appid': self.api_key,
            'units': 'metric',  # Celsius
            'lang': 'pt_br',
            'cnt': num_timestamps
        }
        
        try:
            response = requests.get(self.BASE_URL_FORECAST, params=params, timeout=10)
            response.raise_for_status()
            self.ultima_consulta = datetime.now()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                print("❌ Erro: Chave de API inválida ou não autorizada.")
            elif response.status_code == 404:
                print(f"❌ Erro: Cidade '{cidade}' não encontrada.")
            else:
                print(f"❌ Erro HTTP: {http_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"❌ Erro de requisição: {req_err}")
            return None
    
    def buscar_clima_atual(self, cidade: str, pais_cod: str = "BR") -> Optional[Dict]:
        """
        Busca clima atual para cidade especificada
        
        Args:
            cidade: Nome da cidade
            pais_cod: Código do país (padrão: BR)
            
        Returns:
            Dicionário com dados atuais ou None se falhar
        """
        params = {
            'q': f"{cidade},{pais_cod}",
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'pt_br'
        }
        
        try:
            response = requests.get(self.BASE_URL_CURRENT, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao buscar clima atual: {e}")
            return None
    
    def analisar_chuva(self, dados_api: Dict, limite_horas: int = 6) -> Tuple[bool, List[Dict]]:
        """
        Analisa se há previsão de chuva nas próximas horas
        
        Args:
            dados_api: Dados retornados pela API de previsão
            limite_horas: Número de horas para análise (padrão: 6h)
            
        Returns:
            Tupla (chuva_detectada, lista_previsoes)
        """
        if not dados_api or 'list' not in dados_api or not dados_api['list']:
            return False, []
        
        chuva_detectada = False
        previsoes = []
        
        # Cada timestamp da API representa 3 horas
        count_timestamps = limite_horas // 3
        
        for previsao in dados_api['list'][:count_timestamps]:
            timestamp_dt = datetime.fromtimestamp(previsao['dt'])
            temp = previsao['main']['temp']
            feels_like = previsao['main']['feels_like']
            humidity = previsao['main']['humidity']
            weather_desc = previsao['weather'][0]['description']
            
            # Probabilidade de precipitação (0 a 1, convertemos para %)
            pop = previsao.get('pop', 0) * 100
            
            # Volume de chuva nas últimas 3h em mm
            rain_volume_3h = previsao.get('rain', {}).get('3h', 0)
            
            # Lógica para considerar chuva significativa
            # Ajuste estes limiares conforme necessidade
            if pop > 50 or rain_volume_3h > 0.5:
                chuva_detectada = True
            
            previsao_info = {
                'timestamp': timestamp_dt,
                'temp': round(temp, 1),
                'sensacao_termica': round(feels_like, 1),
                'umidade': humidity,
                'descricao': weather_desc.capitalize(),
                'prob_chuva': round(pop, 1),
                'volume_chuva': round(rain_volume_3h, 2),
                'ha_chuva_significativa': pop > 50 or rain_volume_3h > 0.5
            }
            
            previsoes.append(previsao_info)
        
        return chuva_detectada, previsoes
    
    def obter_info_cidade(self, dados_api: Dict) -> Dict:
        """
        Extrai informações da cidade dos dados da API
        
        Args:
            dados_api: Dados retornados pela API
            
        Returns:
            Dicionário com informações da cidade
        """
        if not dados_api or 'city' not in dados_api:
            return {}
        
        cidade_info = dados_api.get('city', {})
        
        return {
            'nome': cidade_info.get('name', 'N/A'),
            'pais': cidade_info.get('country', 'N/A'),
            'coordenadas': {
                'latitude': cidade_info.get('coord', {}).get('lat'),
                'longitude': cidade_info.get('coord', {}).get('lon')
            },
            'populacao': cidade_info.get('population'),
            'timezone': cidade_info.get('timezone')
        }
    
    def recomendar_irrigacao(self, dados_api: Dict, limite_horas: int = 6) -> Dict:
        """
        Recomenda se deve irrigar baseado na previsão do tempo
        
        Args:
            dados_api: Dados da API de previsão
            limite_horas: Horas para análise
            
        Returns:
            Dicionário com recomendação
        """
        chuva_detectada, previsoes = self.analisar_chuva(dados_api, limite_horas)
        
        recomendacao = {
            'deve_irrigar': not chuva_detectada,
            'motivo': '',
            'confianca': 'alta' if chuva_detectada else 'media',
            'previsoes': previsoes
        }
        
        if chuva_detectada:
            recomendacao['motivo'] = (
                f"Previsão de chuva significativa nas próximas {limite_horas} horas. "
                "Irrigação não recomendada."
            )
        else:
            recomendacao['motivo'] = (
                f"Sem previsão de chuva significativa nas próximas {limite_horas} horas. "
                "Irrigação pode prosseguir baseada em outros sensores."
            )
        
        return recomendacao
    
    def formatar_previsao_texto(self, previsoes: List[Dict]) -> str:
        """
        Formata lista de previsões em texto legível
        
        Args:
            previsoes: Lista de previsões
            
        Returns:
            String formatada
        """
        linhas = ["=== PREVISÃO DO TEMPO ===\n"]
        
        for prev in previsoes:
            linha = (
                f"🕐 {prev['timestamp'].strftime('%d/%m %H:%M')} - "
                f"{prev['descricao']} - "
                f"🌡️ {prev['temp']}°C - "
                f"💧 {prev['prob_chuva']}% chuva"
            )
            if prev['volume_chuva'] > 0:
                linha += f" ({prev['volume_chuva']}mm)"
            linhas.append(linha)
        
        return "\n".join(linhas)
