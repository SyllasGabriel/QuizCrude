# Documentação da API do Quiz App

Este guia explica como interagir com o backend do Quiz App.

**URL Base:** `http://127.0.0.1:5000`

**Nota Importante:** Esta API usa um sistema de autenticação baseado em sessão. Após um login bem-sucedido, o servidor enviará de volta um cabeçalho `Set-Cookie`. O navegador lidará automaticamente com este cookie e o enviará de volta com todas as solicitações subsequentes. Você não precisa gerenciar tokens manualmente.

---

## 1. Endpoints de Autenticação

Estes endpoints lidam com o registro de usuário, login e status da sessão.

### **Registrar um Novo Usuário**
-   **Endpoint:** `POST /api/auth/register`
-   **Descrição:** Cria uma nova conta de usuário.
-   **Corpo da Solicitação (JSON):**
    ```json
    {
        "username": "newuser",
        "password": "password123"
    }
    ```
-   **Respostas:**
    -   `201 Created`: O usuário foi criado com sucesso.
      ```json
      { "message": "Registro bem-sucedido. Faça login." }
      ```
    -   `409 Conflict`: O nome de usuário já existe.
      ```json
      { "message": "Nome de usuário já existe." }
      ```
    -   `400 Bad Request`: Nome de usuário ou senha não foi fornecido.

### **Fazer Login de um Usuário**
-   **Endpoint:** `POST /api/auth/login`
-   **Descrição:** Autentica um usuário e inicia uma sessão.
-   **Corpo da Solicitação (JSON):**
    ```json
    {
        "username": "testuser",
        "password": "123"
    }
    ```
-   **Respostas:**
    -   `200 OK`: Login bem-sucedido. O cookie de sessão é definido.
      ```json
      {
          "message": "Login bem-sucedido.",
          "username": "testuser"
      }
      ```
    -   `401 Unauthorized`: Credenciais inválidas.
      ```json
      { "message": "Credenciais inválidas." }
      ```

### **Fazer Logout de um Usuário**
-   **Endpoint:** `POST /api/auth/logout`
-   **Descrição:** Encerra a sessão atual do usuário.
-   **Corpo da Solicitação:** (Nenhum)
-   **Resposta:**
    -   `200 OK`: Logout bem-sucedido. O cookie de sessão é limpo.
      ```json
      { "message": "Logout bem-sucedido." }
      ```

---

## 2. Endpoints de Jogabilidade do Quiz

Estes endpoints controlam o fluxo do quiz. **Todos os endpoints aqui exigem que o usuário esteja logado.**

### **Obter a Pergunta Atual**
-   **Endpoint:** `GET /api/quiz/question`
-   **Descrição:** Busca a pergunta atual com base no estado da sessão do usuário. Chame este endpoint para iniciar o quiz e para obter cada pergunta subsequente.
-   **Respostas:**
    -   **Se o quiz estiver ativo (`200 OK`):**
      ```json
      {
          "status": "active",
          "current_question_number": 1,
          "score": 0,
          "question": {
              "id": 1,
              "text": "Qual a capital da França?",
              "options": ["Londres", "Paris", "Roma", "Berlim"]
          }
      }
      ```
    -   **Se o quiz estiver finalizado (`200 OK`):**
      ```json
      {
          "status": "completed",
          "message": "Quiz finalizado. Acesse /api/quiz/results."
      }
      ```

### **Enviar uma Resposta**
-   **Endpoint:** `POST /api/quiz/submit`
-   **Descrição:** Envia a resposta do usuário para a pergunta atual e avança o estado do quiz.
-   **Corpo da Solicitação (JSON):**
    ```json
    {
        "answer": "Paris"
    }
    ```
-   **Resposta (`200 OK`):**
    ```json
    {
        "message": "Resposta processada.",
        "correct": true,
        "new_score": 1
    }
    ```

### **Obter Resultados Finais**
-   **Endpoint:** `GET /api/quiz/results`
-   **Descrição:** Busca a pontuação final. **Importante:** Chamar este endpoint limpará o progresso do quiz do usuário da sessão, permitindo que ele jogue novamente.
-   **Resposta (`200 OK`):**
    ```json
    {
        "message": "Resultado Final",
        "score": 5,
        "total_questions": 5,
        "percentage": 100.0
    }
    ```

---

## 3. Fluxo de Trabalho Típico do Front-End

1.  **Carregamento Inicial da Página:** Verifique se o usuário já está logado chamando `GET /api/quiz/question` ou um endpoint de status similar. Se retornar um `401`, mostre a página de login.
2.  **Login:** O usuário envia o formulário de login. Chame `POST /api/auth/login`. Em caso de sucesso, mostre a visualização "Iniciar Quiz".
3.  **Iniciar Quiz:** Chame `GET /api/quiz/question`.
4.  **Exibir Pergunta:** Use o JSON da etapa anterior para renderizar a pergunta e as opções de resposta.
5.  **Usuário Responde:** O usuário clica em uma opção. Chame `POST /api/quiz/submit` com a resposta dele.
6.  **Obter Próxima Pergunta:** Imediatamente após o retorno da chamada de envio, chame `GET /api/quiz/question` novamente.
7.  **Loop:** Repita as etapas 4-6 até que a resposta de `/question` seja `{"status": "completed"}`.
8.  **Mostrar Resultados:** Quando o quiz estiver completo, chame `GET /api/quiz/results` e exiba a pontuação final.