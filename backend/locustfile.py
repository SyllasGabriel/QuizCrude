from locust import HttpUser, task, between
import random

class QuizUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # todo user simulado tem um usernae único
        self.username = f"user_{random.randint(1, 100000)}"
        self.password = "password123"

        # registro
        self.client.post("/api/auth/register", json={
            "username": self.username,
            "password": self.password
        })

        # login
        response = self.client.post("/api/auth/login", json={
            "username": self.username,
            "password": self.password
        })

        # login check
        if response.status_code != 200:
            print(f"Login failed for user {self.username}")
            self.environment.runner.quit()
            return

        self.quiz_finished = False

    @task
    def take_quiz(self):
        """Simula um usuário fazendo o quiz"""
        if self.quiz_finished:
            self.on_start()
            return
        
        # handles non 200 responses
        with self.client.get("/api/quiz/question", catch_response=True, name="/api/quiz/question") as response:
            # check if the request was successful
            if not response.ok:
                response.failure(f"Failed to get question, status code: {response.status_code}")
                return
            
            try:
                data = response.json()
            except ValueError:
                response.failure("Response was not valid JSON")
                return
            
            if data.get("status") == "completed":
                self.client.get("/api/quiz/results", name="/api/quiz/results")
                self.quiz_finished = True
                return
            
            question = data.get("question")
            if question and question.get("options"):
                chosen_answer = random.choice(question.get("options"))

                with self.client.post("/api/quiz/submit",
                                        json={"answer": chosen_answer},
                                        catch_response=True,
                                        name="/api/quiz/submit") as post_response:
                    if not post_response.ok:
                        post_response.failure(f"Failed to submit answer, status: {post_response.status_code}")
