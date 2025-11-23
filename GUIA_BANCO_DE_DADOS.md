# 💾 Guia de Conexão com Banco de Dados - FarmTech

## 🎯 Opções Disponíveis

O sistema suporta **2 tipos de banco de dados**:

1. **SQLite** (Padrão) - Funciona automaticamente ✅
2. **Oracle Database** - Para produção (requer configuração)

---

## 📦 OPÇÃO 1: SQLite (Já Funcionando! ✅)

### ✅ Já está conectado automaticamente!

O SQLite é criado automaticamente na primeira execução. **Não precisa fazer nada!**

### 📍 Localização do Banco:
```
Fase 7/database/farmtech.db
```

### 🔧 Configuração (arquivo `.env`):
```env
SQLITE_DB_PATH=database/farmtech.db
```

### 💻 Como Usar no Código:

#### Método 1: Usar o Controlador (Recomendado)
```python
from src.core.controller import FarmTechController

# Inicializar controlador (banco já conecta automaticamente)
controller = FarmTechController()

# Testar conexão
controller.testar_conexao_db()  # Retorna True se OK

# Obter sessão para operações CRUD
session = controller.obter_sessao_db()

# Exemplo: Consultar funcionários
from src.fase2.models import Funcionarios

funcionarios = session.query(Funcionarios).all()
for func in funcionarios:
    print(f"{func.nome} - {func.funcao}")

session.close()
```

#### Método 2: Usar DatabaseHandler Diretamente
```python
from src.fase2.database import DatabaseHandler
from src.fase2.models import Base, Funcionarios

# Criar handler SQLite
db = DatabaseHandler(db_type="sqlite")

# Criar tabelas (se não existirem)
db.create_tables(Base)

# Testar conexão
db.test_connection()  # ✅ Conexão com banco de dados OK

# Obter sessão
session = db.get_session()

# Inserir dados
novo_funcionario = Funcionarios(
    nome="João Silva",
    funcao="Agrônomo"
)
session.add(novo_funcionario)
session.commit()

# Consultar
funcionarios = session.query(Funcionarios).all()
for func in funcionarios:
    print(f"{func.id}: {func.nome} - {func.funcao}")

session.close()
```

### 🔍 Visualizar Dados (Ferramentas):

Você pode usar qualquer ferramenta SQLite para visualizar os dados:

1. **DB Browser for SQLite** (Grátis)
   - Download: https://sqlitebrowser.org/
   - Abrir: `database/farmtech.db`

2. **VS Code Extension**
   - Instalar: "SQLite Viewer" ou "SQLite"
   - Clicar com direito em `farmtech.db` > Open Database

3. **Linha de Comando**
   ```bash
   sqlite3 database/farmtech.db
   .tables                    # Ver tabelas
   SELECT * FROM funcionarios; # Consultar
   .quit                      # Sair
   ```

---

## 🏢 OPÇÃO 2: Oracle Database (Para Produção)

### 📋 Pré-requisitos:

1. Ter acesso a um servidor Oracle
2. Ter credenciais (usuário, senha, host)
3. Instalar biblioteca Python:
   ```bash
   pip install oracledb
   ```

### 🔧 Configuração:

#### 1. Editar arquivo `.env`:
```env
# Descomentar e configurar:
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=oracle.fiap.com.br
DB_PORT=1521
DB_SERVICE=orcl
```

#### 2. Usar no Código:
```python
from src.fase2.database import DatabaseHandler
from src.fase2.models import Base

# Criar handler Oracle
db = DatabaseHandler(db_type="oracle")

# Criar tabelas
db.create_tables(Base)

# Testar conexão
if db.test_connection():
    print("Conectado ao Oracle!")
    
# Usar normalmente
session = db.get_session()
# ... suas operações CRUD
session.close()
```

### ⚠️ Importante Oracle:
- As tabelas usam `Identity(start=1)` que requer Oracle 12c+
- Se usar Oracle 11g, será necessário adaptar os models para usar `Sequence`

---

## 🎯 Como Escolher Qual Banco Usar

### Use **SQLite** se:
- ✅ Desenvolvimento local
- ✅ Testes e prototipagem
- ✅ Projeto individual/pequeno
- ✅ Não precisa de múltiplos usuários simultâneos

### Use **Oracle** se:
- ✅ Ambiente de produção
- ✅ Múltiplos usuários simultâneos
- ✅ Grande volume de dados
- ✅ Requisitos empresariais (FIAP pode pedir)

---

## 📊 Tabelas Criadas Automaticamente

O sistema cria estas tabelas:

```sql
-- Funcionários
CREATE TABLE funcionarios (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    funcao VARCHAR(100) NOT NULL
);

-- Insumos
CREATE TABLE insumos (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    quantidade INTEGER NOT NULL,
    peso FLOAT NOT NULL,
    data_validade DATE NOT NULL
);

-- Talhões
CREATE TABLE talhoes (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    area FLOAT NOT NULL,
    cultura VARCHAR(100) NOT NULL,
    data_plantio DATE,
    data_colheita DATE
);

-- Financeiro
CREATE TABLE financeiro (
    id INTEGER PRIMARY KEY,
    descricao VARCHAR(200) NOT NULL,
    tipo_movimentacao VARCHAR(50) NOT NULL,
    valor FLOAT NOT NULL,
    data DATE NOT NULL
);

-- Relatórios
CREATE TABLE relatorios (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    descricao VARCHAR(200),
    data_geracao DATE NOT NULL
);

-- Tarefas
CREATE TABLE tarefas (
    id INTEGER PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descricao VARCHAR(300),
    status VARCHAR(50) NOT NULL,
    data_inicio DATE,
    data_conclusao DATE
);
```

---

## 🧪 Testando a Conexão

### Teste Rápido (Terminal):
```bash
cd "/Users/letgomez/Downloads/Projetos FIAP/Fase 7"

python -c "from src.fase2.database import DatabaseHandler; \
db = DatabaseHandler('sqlite'); \
db.test_connection()"
```

**Resultado esperado:**
```
✅ Conexão SQLite configurada: database/farmtech.db
✅ Conexão com banco de dados OK
```

### Teste Completo:
```bash
python test_sistema.py
```

---

## 💡 Exemplos Práticos

### Exemplo 1: Adicionar Funcionário
```python
from src.core.controller import FarmTechController
from src.fase2.models import Funcionarios
from datetime import date

controller = FarmTechController()
session = controller.obter_sessao_db()

# Criar funcionário
funcionario = Funcionarios(
    nome="Maria Santos",
    funcao="Engenheira Agrônoma"
)

session.add(funcionario)
session.commit()
print(f"✅ Funcionário {funcionario.id} adicionado!")

session.close()
```

### Exemplo 2: Listar Todos os Insumos
```python
from src.core.controller import FarmTechController
from src.fase2.models import Insumos

controller = FarmTechController()
session = controller.obter_sessao_db()

insumos = session.query(Insumos).all()

if insumos:
    for insumo in insumos:
        print(f"{insumo.nome} ({insumo.tipo}): {insumo.quantidade} unidades")
else:
    print("Nenhum insumo cadastrado")

session.close()
```

### Exemplo 3: Inserir Dados Iniciais
```python
from src.fase2.database import DatabaseHandler
from src.fase2.models import Base, Funcionarios, Talhoes
from datetime import date

# Conectar
db = DatabaseHandler("sqlite")
db.create_tables(Base)
session = db.get_session()

# Adicionar funcionários
funcionarios = [
    Funcionarios(nome="João Silva", funcao="Gerente"),
    Funcionarios(nome="Maria Santos", funcao="Agrônoma"),
    Funcionarios(nome="Pedro Costa", funcao="Técnico")
]

for func in funcionarios:
    session.add(func)

# Adicionar talhões
talhoes = [
    Talhoes(
        nome="Talhão Norte",
        area=5000.0,
        cultura="Milho",
        data_plantio=date(2024, 10, 1)
    ),
    Talhoes(
        nome="Talhão Sul",
        area=3500.0,
        cultura="Soja",
        data_plantio=date(2024, 9, 15)
    )
]

for talhao in talhoes:
    session.add(talhao)

session.commit()
print("✅ Dados iniciais inseridos!")

session.close()
```

---

## 🔒 Segurança

### ✅ Boas Práticas:

1. **Nunca commite o arquivo `.env`** (já está no .gitignore)
2. **Use `.env.example`** para documentar variáveis necessárias
3. **Para Oracle, use credenciais específicas** do seu ambiente

### ⚠️ Atenção:
- O `.env` atual tem uma API key de exemplo
- Em produção, use suas próprias credenciais
- Nunca compartilhe senhas em repositórios públicos

---

## ❓ Problemas Comuns

### Problema 1: "Arquivo não encontrado"
**Solução:** O SQLite cria automaticamente. Se der erro, verifique:
```bash
# Criar diretório se não existir
mkdir -p database
```

### Problema 2: "Tabelas não existem"
**Solução:** As tabelas são criadas automaticamente. Force a criação:
```python
from src.fase2.database import DatabaseHandler
from src.fase2.models import Base

db = DatabaseHandler("sqlite")
db.create_tables(Base)
```

### Problema 3: "Oracle connection failed"
**Solução:** Verifique:
1. Credenciais no `.env` estão corretas
2. Biblioteca instalada: `pip install oracledb`
3. Servidor Oracle está acessível

---

## 📚 Referências

- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/
- **SQLite Docs:** https://www.sqlite.org/docs.html
- **Oracle Python Driver:** https://python-oracledb.readthedocs.io/

---

## ✅ Resumo Rápido

```python
# RESUMO: Como usar o banco de dados

# 1. Forma mais simples (via Controller):
from src.core.controller import FarmTechController
controller = FarmTechController()
session = controller.obter_sessao_db()
# ... suas operações
session.close()

# 2. Forma direta (via DatabaseHandler):
from src.fase2.database import DatabaseHandler
db = DatabaseHandler("sqlite")  # ou "oracle"
session = db.get_session()
# ... suas operações
session.close()

# 3. Testar conexão:
controller.testar_conexao_db()  # ou db.test_connection()
```

---

**✨ O banco SQLite já está funcionando automaticamente!**  
**Basta usar o controlador e começar a inserir dados!** 🚀

