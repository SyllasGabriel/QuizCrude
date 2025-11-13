# Projeto Integrador: Aplicação de Quiz (Testes e Automação)

Este projeto foi desenvolvido como parte da disciplina de "Testes e Automação de Software". O objetivo é criar uma aplicação web completa do tipo "Quiz", implementando uma API backend robusta e uma suíte de testes abrangente, incluindo testes de sistema (End-to-End) e testes de performance.

## 🚀 Tecnologias Utilizadas

-   **Backend:**
    -   Python 3.11+
    -   Flask (Microframework web)
    -   Flask-SQLAlchemy (ORM para o banco de dados)
    -   Flask-Login (Gerenciamento de sessão e autenticação)
    -   SQLite (Banco de dados)
-   **Testes:**
    -   Locust (Testes de Performance)
    -   Selenium (Automação de UI)
    -   Pytest (Estrutura para os testes de sistema)

## 📁 Estrutura do Projeto

O repositório está organizado da seguinte forma:

```
/
├── backend/            # Contém todo o código-fonte da API Flask
│   ├── instance/       # Onde o banco de dados SQLite é criado
│   ├── routes/         # Blueprints para as rotas de autenticação e quiz
│   ├── app.py          # Ponto de entrada da aplicação Flask
│   ├── models.py       # Definição dos modelos do banco de dados (User, Question)
│   └── locustfile.py   # Script para os testes de performance
├── frontend/           # 
├── tests/              # Contém os testes automatizados
│   └── selenium_pytest/
│       └── test_e2e_quiz_flow.py # Script com os 5 cenários E2E
├── evidencias/         # Prints, logs dos resultados dos testes
├── .gitignore
├── API.md              # Documentação completa da API
├── README.md           # Este arquivo
└── requirements.txt    # Lista de dependências Python
```

## ⚙️ Backend: Setup e Execução

Para executar o backend localmente, siga os passos abaixo.

### Pré-requisitos
-   Python 3.11 ou superior
-   `pip` e `venv` (geralmente inclusos com Python)

### Instalação e Execução

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd <nome-do-repositorio>
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Crie e popule o banco de dados:**
    Execute o comando customizado do Flask para criar o arquivo `quiz.db` e adicionar as perguntas iniciais.
    ```bash
    # (Dentro da pasta /backend)
    cd backend
    flask seed-db
    ```

5.  **Rode a aplicação:**
    ```bash
    # (Ainda dentro da pasta /backend)
    python app.py
    ```

O servidor backend estará rodando em `http://127.0.0.1:5000`.

## 🧪 Como Executar os Testes

### Testes de Performance (Locust)

Estes testes avaliam a performance da API do backend e **não dependem do front-end**.

1.  Certifique-se de que o servidor backend (`python app.py`) está rodando.
2.  Abra um **novo terminal**, ative o ambiente virtual e navegue até a pasta `backend`.
3.  Inicie o Locust:
    ```bash
    locust -f locustfile.py --host http://127.0.0.1:5000
    ```
4.  Abra seu navegador e acesse `http://localhost:8089`.
5.  Preencha o número de usuários (ex: 50) e a taxa de surgimento (ex: 5), e inicie o teste.

### Testes de Sistema (Selenium + Pytest)

Estes testes simulam um usuário real no navegador e **dependem tanto do backend quanto do front-end estarem rodando**.

1.  Certifique-se de que o backend e o front-end estão rodando.
2.  No terminal, com o ambiente virtual ativo, navegue até a raiz do projeto.
3.  Execute o Pytest:
    ```bash
    pytest
    ```
    O Pytest encontrará e executará automaticamente todos os cenários definidos em `tests/selenium_pytest/`.

## 🐳 (Bônus) Como Executar com Docker

Com o Docker Desktop instalado e rodando, você pode executar o backend em um contêiner isolado com apenas dois comandos.

1.  **Construa a imagem Docker:**
    (Na raiz do projeto)
    ```bash
    docker build -t quiz-backend .
    ```

2.  **Rode o contêiner:**
    ```bash
    docker run -p 5000:5000 quiz-backend
    ```
    O backend estará acessível da mesma forma em `http://127.0.0.1:5000`.

## 📖 Documentação da API

Para detalhes completos sobre todos os endpoints disponíveis, os formatos de requisição e resposta, e o fluxo de uso da API, consulte o arquivo [**API.md**](./API.md).

## 👥 Autores

-   [] - Backend e Testes
-   [] 
-   []