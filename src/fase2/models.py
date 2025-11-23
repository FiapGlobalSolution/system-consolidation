"""
Modelos de dados do sistema FarmTech
Migrado da Fase 2 (agrogestor)
"""

from sqlalchemy import Identity, Float, Date, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Funcionarios(Base):
    """Modelo para funcionários da fazenda"""
    __tablename__ = 'funcionarios'
    
    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    nome = Column(String(100), nullable=False)
    funcao = Column(String(100), nullable=False)
    
    def __repr__(self):
        return f"<Funcionario(id={self.id}, nome='{self.nome}', funcao='{self.funcao}')>"


class Insumos(Base):
    """Modelo para insumos agrícolas"""
    __tablename__ = 'insumos'
    
    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(100), nullable=False)
    quantidade = Column(Integer, nullable=False)
    peso = Column(Float, nullable=False)
    data_validade = Column(Date, nullable=False)
    
    def __repr__(self):
        return f"<Insumo(id={self.id}, nome='{self.nome}', tipo='{self.tipo}')>"


class Talhoes(Base):
    """Modelo para talhões de plantio"""
    __tablename__ = 'talhoes'

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    nome = Column(String(100), nullable=False)
    area = Column(Float, nullable=False)
    cultura = Column(String(100), nullable=False)
    data_plantio = Column(Date, nullable=True)
    data_colheita = Column(Date, nullable=True)
    
    def __repr__(self):
        return f"<Talhao(id={self.id}, nome='{self.nome}', cultura='{self.cultura}')>"


class Financeiros(Base):
    """Modelo para controle financeiro"""
    __tablename__ = 'financeiro'

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    descricao = Column(String(200), nullable=False)
    tipo_movimentacao = Column(String(50), nullable=False)  # 'receita' ou 'despesa'
    valor = Column(Float, nullable=False)
    data = Column(Date, nullable=False)
    
    def __repr__(self):
        return f"<Financeiro(id={self.id}, tipo='{self.tipo_movimentacao}', valor={self.valor})>"


class Relatorios(Base):
    """Modelo para relatórios gerados"""
    __tablename__ = 'relatorios'

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)   # ex: 'vendas', 'estoque', etc.
    descricao = Column(String(200), nullable=True)
    data_geracao = Column(Date, nullable=False)
    
    def __repr__(self):
        return f"<Relatorio(id={self.id}, nome='{self.nome}', tipo='{self.tipo}')>"


class Tarefas(Base):
    """Modelo para tarefas e checklist"""
    __tablename__ = 'tarefas'

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    titulo = Column(String(100), nullable=False)
    descricao = Column(String(300), nullable=True)
    status = Column(String(50), nullable=False)  # ex: 'pendente', 'em andamento', 'concluída'
    data_inicio = Column(Date, nullable=True)
    data_conclusao = Column(Date, nullable=True)
    
    def __repr__(self):
        return f"<Tarefa(id={self.id}, titulo='{self.titulo}', status='{self.status}')>"
