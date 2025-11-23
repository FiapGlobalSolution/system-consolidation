"""
Funções auxiliares e utilitários gerais
"""

import re
import uuid
from datetime import datetime
from typing import Optional


def formatar_data(data: datetime, formato: str = "%d/%m/%Y %H:%M") -> str:
    """
    Formata um objeto datetime para string
    
    Args:
        data: Objeto datetime
        formato: String de formato (padrão: dd/mm/yyyy hh:mm)
        
    Returns:
        String formatada
    """
    return data.strftime(formato)


def validar_email(email: str) -> bool:
    """
    Valida formato de email
    
    Args:
        email: String com email
        
    Returns:
        True se válido, False caso contrário
    """
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao, email))


def gerar_id() -> str:
    """
    Gera um ID único
    
    Returns:
        String com UUID
    """
    return str(uuid.uuid4())


def truncar_texto(texto: str, max_chars: int = 50) -> str:
    """
    Trunca texto longo adicionando reticências
    
    Args:
        texto: Texto a truncar
        max_chars: Número máximo de caracteres
        
    Returns:
        Texto truncado
    """
    if len(texto) <= max_chars:
        return texto
    return texto[:max_chars-3] + "..."


def converter_celsius_fahrenheit(celsius: float) -> float:
    """Converte Celsius para Fahrenheit"""
    return (celsius * 9/5) + 32


def converter_fahrenheit_celsius(fahrenheit: float) -> float:
    """Converte Fahrenheit para Celsius"""
    return (fahrenheit - 32) * 5/9


def formatar_moeda(valor: float, simbolo: str = "R$") -> str:
    """
    Formata valor monetário
    
    Args:
        valor: Valor numérico
        simbolo: Símbolo da moeda
        
    Returns:
        String formatada
    """
    return f"{simbolo} {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

