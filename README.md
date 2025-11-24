# Teste Prático - API de Tarefas

Este projeto é uma API simples para gerenciamento de tarefas, desenvolvida em Python utilizando Flask e SQLAlchemy. O objetivo é demonstrar conhecimentos em criação de APIs REST, manipulação de banco de dados e testes automatizados.

## Estrutura do Projeto

```
app/
  app.py            # Arquivo principal da aplicação Flask
  model.py          # Definição dos modelos do banco de dados
  requirements.txt  # Dependências do projeto
  routes.py         # Rotas/endpoints da API
  sqlar.py          # Configuração do banco de dados
  instance/         # Configurações e arquivos específicos de instância
  tests/
    test_tasks.py   # Testes automatizados com pytest
```

## Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd login/app
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**
   ```bash
   python app.py
   ```
   A API estará disponível em `http://127.0.0.1:5000/`.

## Endpoints Principais

- `POST /tarefas` - Cria uma nova tarefa
- `GET /tarefas` - Lista todas as tarefas

## Testes Automatizados

Os testes estão localizados em `app/tests/test_tasks.py` e utilizam o framework `pytest`.

### Como rodar os testes

1. Certifique-se de estar no diretório `app`.
2. Execute o comando:
   ```bash
   pytest tests/test_tasks.py
   ```

Os testes cobrem:
- Criação de tarefas
- Validação de campos obrigatórios
- Listagem de tarefas

## Observações
- O banco de dados utilizado nos testes é um SQLite temporário (`test.db`).
- Para fins de teste, o banco é criado e descartado automaticamente.

---

Desenvolvido por [Seu Nome].