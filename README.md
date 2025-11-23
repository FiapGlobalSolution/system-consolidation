# 🌾 FarmTech Solutions - Fase 7: Sistema Consolidado

## 📋 Descrição do Projeto

Sistema integrado de gestão para o agronegócio que consolida todas as funcionalidades desenvolvidas nas Fases 1 a 6 do projeto FarmTech Solutions da FIAP.

## 🎯 Objetivo

Integrar todos os serviços desenvolvidos anteriormente em um único sistema coeso, acessível através de um dashboard interativo, permitindo:

- Cálculos de área de plantio e manejo de insumos
- Integração com API meteorológica para decisões baseadas em clima
- Gestão completa de dados agrícolas (CRUD)
- Monitoramento IoT com sensores
- Previsões inteligentes usando Machine Learning
- Visão computacional para análise de saúde das plantas
- Sistema de alertas via AWS

## 🏗️ Estrutura do Projeto

```
Fase 7/
├── src/                          # Código-fonte principal
│   ├── core/                     # Núcleo do sistema
│   │   ├── controller.py         # Controlador central
│   │   └── config.py             # Configurações globais
│   ├── fase1/                    # Cálculos e clima
│   ├── fase2/                    # Gestão de dados
│   ├── fase3/                    # IoT
│   ├── fase4/                    # Machine Learning
│   └── fase6/                    # Visão computacional
├── data/                         # Dados
├── models/                       # Modelos treinados
├── database/                     # Banco de dados
├── utils/                        # Utilitários
├── app.py                        # Dashboard principal
├── requirements.txt              # Dependências
└── .env.example                  # Exemplo de configuração
```

## 🚀 Como Executar

### 1. Instalação

```bash
cd "Fase 7"
pip install -r requirements.txt
```

### 2. Configuração

Copie o arquivo `.env.example` para `.env` e configure suas credenciais:

```bash
cp .env.example .env
```

### 3. Executar o Dashboard

```bash
streamlit run app.py
```

## 📦 Funcionalidades por Fase

### Fase 1: Base de Dados e Clima
- ✅ Cálculo de área de plantio (milho e soja)
- ✅ Cálculo de insumos necessários
- ✅ Integração com API OpenWeatherMap
- ✅ Análise de previsão de chuva

### Fase 2: Banco de Dados Estruturado
- ✅ Modelos de dados (SQLAlchemy)
- ✅ CRUD completo para:
  - Funcionários
  - Insumos
  - Talhões
  - Financeiro
  - Relatórios
  - Tarefas

### Fase 3: IoT e Automação
- ✅ Integração com sensores ESP32
- ✅ Monitoramento de umidade, pH, nutrientes
- ✅ Controle de irrigação automatizada

### Fase 4: Machine Learning
- ✅ Modelo preditivo para irrigação
- ✅ Análise inteligente de sensores
- ✅ Recomendações baseadas em dados

### Fase 5: Cloud Computing
- 🚧 Infraestrutura AWS (Pessoa 2)
- 🚧 Sistema de mensageria e alertas

### Fase 6: Visão Computacional
- 🚧 YOLO para detecção de pragas (Pessoa 3)
- 🚧 Análise de saúde das plantas

## 👥 Equipe

- **Pessoa 1**: Arquiteto de Integração (Estrutura & Lógica)
- **Pessoa 2**: Engenheiro de Cloud & Dados (AWS & Mensageria)
- **Pessoa 3**: Especialista em IA & IoT (YOLO & Sensores)
- **Pessoa 4**: Frontend Lead & Documentador (Dashboard & Apresentação)

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Streamlit** - Dashboard interativo
- **SQLAlchemy** - ORM para banco de dados
- **Scikit-learn** - Machine Learning
- **Pandas/NumPy** - Análise de dados
- **Requests** - Integração com APIs
- **Oracle Database / SQLite** - Armazenamento

## 📝 Licença

Projeto acadêmico - FIAP 2024

## 🔗 Links Úteis

- [Documentação Streamlit](https://docs.streamlit.io)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org)

---

**Desenvolvido com ❤️ para o curso de Engenharia de Software - FIAP**

