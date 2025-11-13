import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BASE_URL = "http://localhost:3000"

@pytest.fixture
def driver():
    """Sets up and tears down the browser for each test function."""
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Helper function for login
def login_helper(driver, username, password):
    driver.get(BASE_URL + "/login")
    driver.find_element(By.ID, "username-input").send_keys(username)
    driver.find_element(By.ID, "password-input").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

# 5 Test scenarios

def test_scenario1_happy_path_full_quiz(driver):
    """Scenario 1: Tests a successful login and quiz completion."""
    # Assuming a user 'testuser' with password '123' exists from seeding or prior test
    login_helper(driver, "testuser", "123")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "question-text")))
    
    # Loop through all 5 questions
    for i in range(5):
        question_text_element = driver.find_element(By.ID, "question-text")
        # Wait for the next question to be different from the last one
        WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, "question-text").text != getattr(question_text_element, 'text', ''))
        
        driver.find_element(By.CLASS_NAME, "option-button").click()
        time.sleep(0.5) # Brief pause to simulate user reading feedback

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "final-score-text")))
    score_text = driver.find_element(By.ID, "final-score-text").text
    assert "pontuação" in score_text.lower() or "score" in score_text.lower()

def test_scenario2_failed_login(driver):
    """Scenario 2: Tests login with incorrect credentials."""
    login_helper(driver, "testuser", "wrongpassword")
    
    # Check for an error message
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "error-message-div")) # Placeholder ID
    ).text
    assert "credenciais inválidas" in error_message.lower()

def test_scenario3_duplicate_registration(driver):
    """Scenario 3: Tests attempting to register a user that already exists."""
    driver.get(BASE_URL + "/register") # Assumes a '/register' page
    # TODO: replace IDs with the front-end HTML IDs
    driver.find_element(By.ID, "register-username-input").send_keys("testuser") # Use an existing user
    driver.find_element(By.ID, "register-password-input").send_keys("somepassword")
    driver.find_element(By.ID, "register-button").click()

    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "error-message-div"))
    ).text
    assert "nome de usuário já existe" in error_message.lower()

def test_scenario4_logout_and_session_check(driver):
    """Scenario 4: Tests successful logout and verifies session is terminated."""
    login_helper(driver, "testuser", "123")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "question-text")))

    # placeholder ID
    driver.find_element(By.ID, "logout-button").click()

    # After logout, expect to be on the login page
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-button")))
    
    # Now, try to access a protected route
    driver.get(BASE_URL + "/quiz")
    
    # The user should be redirected back to the login page, so the login button should be visible again
    assert driver.find_element(By.ID, "login-button").is_displayed()

def test_scenario5_reset_quiz_mid_game(driver):
    """Scenario 5: Tests the quiz reset functionality."""
    login_helper(driver, "testuser", "123")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "question-text")))

    # Answer two questions
    driver.find_element(By.CLASS_NAME, "option-button").click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "option-button").click()
    time.sleep(1)

    # placeholder ID
    driver.find_element(By.ID, "reset-quiz-button").click()

    # After reset, we should be back at question 1
    question_number_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "question-number-span")) # Placeholder ID
    )
    assert "1" in question_number_element.text