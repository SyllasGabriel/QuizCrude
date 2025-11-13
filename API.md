# Quiz App API Documentation

Este guide explica como interagir com o backend para o Quiz App.

**Base URL:** `http://127.0.0.1:5000`

**Nota Importante:** Esta API usa um sistema de autenticação por sessão. Após um login bem-sucedido, o servidor enviará um header `Set-Cookie`. O navegador irá gerenciar este cookie automaticamente para todas as requisições futuras.

---

## 1. Endpoints de Autenticação

### **Registrar Novo Usuário**
-   **Endpoint:** `POST /api/auth/register`
-   **Corpo da Requisição (JSON):** `{ "username": "...", "password": "..." }`
-   **Respostas:**
    -   `201 Created`: `{ "message": "Registro bem-sucedido. Faça login." }`
    -   `409 Conflict`: `{ "message": "Nome de usuário já existe." }`

### **Login de Usuário**
-   **Endpoint:** `POST /api/auth/login`
-   **Corpo da Requisição (JSON):** `{ "username": "...", "password": "..." }`
-   **Resposta (`200 OK`):** `{ "message": "Login bem-sucedido.", "username": "..." }`

### **Logout de Usuário**
-   **Endpoint:** `POST /api/auth/logout`
-   **Resposta (`200 OK`):** `{ "message": "Logout bem-sucedido." }`

---

## 2. Endpoints de Gameplay do Quiz

(Estes endpoints requerem que o usuário esteja logado)

### **Obter Pergunta Atual**
-   **Endpoint:** `GET /api/quiz/question`
-   **Resposta (Quiz Ativo):** `{ "status": "active", "question": { ... } }`
-   **Resposta (Quiz Finalizado):** `{ "status": "completed", "message": "..." }`

### **Enviar Resposta**
-   **Endpoint:** `POST /api/quiz/submit`
-   **Corpo da Requisição (JSON):** `{ "answer": "Paris" }`
-   **Resposta (`200 OK`):** `{ "correct": true, "new_score": 1 }`

### **Obter Resultado Final**
-   **Endpoint:** `GET /api/quiz/results`
-   **Resposta (`200 OK`):** `{ "score": 5, "total_questions": 5, ... }`

---

## 3. Endpoints de Gerenciamento de Perguntas (CRUD)

(Estes endpoints são para uma interface administrativa e requerem login)

### **Ler Todas as Perguntas (Read)**
-   **Endpoint:** `GET /api/quiz/questions/all`
-   **Descrição:** Retorna uma lista com todas as perguntas no banco de dados.
-   **Resposta (`200 OK`):** `[ { "id": 1, "text": "...", "options": [...] }, ... ]`

### **Criar Nova Pergunta (Create)**
-   **Endpoint:** `POST /api/quiz/questions`
-   **Descrição:** Adiciona uma nova pergunta ao banco de dados.
-   **Corpo da Requisição (JSON):**
    ```json
    {
        "text": "Qual é o líder dos Autobots?",
        "options": ["Bumblebee", "Megatron", "Optimus Prime", "Ironhide",]
        "correct_answer": 2
    }
    ```
-   **Resposta (`201 Created`):** `{ "message": "Question created successfully", "id": 7 }`

### **Atualizar Pergunta Existente (Update)**
-   **Endpoint:** `PUT /api/quiz/questions/<int:question_id>`
-   **Descrição:** Modifica os dados de uma pergunta específica.
-   **Corpo da Requisição (JSON):** (Envie apenas os campos que deseja alterar)
    ```json
    {
        "text": "Quem é o principal inimigo dos Autobots??",
        "options": ["Starscream", "Megatron", "Shockwave", "Soundwave",]
        "correct_answer": 1
    }
    ```
-   **Respostas:**
    -   `200 OK`: `{ "message": "Question updated successfully" }`
    -   `404 Not Found`: `{ "error": "Question not found" }`

### **Deletar Pergunta (Delete)**
-   **Endpoint:** `DELETE /api/quiz/questions/<int:question_id>`
-   **Descrição:** Remove uma pergunta do banco de dados.
-   **Respostas:**
    -   `200 OK`: `{ "message": "Question deleted successfully" }`
    -   `404 Not Found`: `{ "error": "Question not found" }`