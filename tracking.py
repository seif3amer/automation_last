from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def tracking(service_name, date):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    link = 'https://digital.gov.eg/'
    browser.get(link)
    main_window = browser.current_window_handle
    wait = WebDriverWait(browser, 10)

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"تسجيل الدخول")]'))
    )
    login_button.click()
    time.sleep(2)

    windows = browser.window_handles
    if len(windows) > 1:
        login_window = windows[-1]
        browser.switch_to.window(login_window)

    username_input = wait.until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    username_input.clear()
    username_input.send_keys("01128417941")

    next_button = wait.until(
        EC.element_to_be_clickable((By.ID, "kc-login"))
    )
    next_button.click()

    password_input = wait.until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_input.clear()
    password_input.send_keys("Seif@2003")

    login_submit = wait.until(
        EC.element_to_be_clickable((By.ID, "kc-login"))
    )
    login_submit.click()
    time.sleep(3)
    browser.switch_to.window(main_window)

    my_profile = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".leftLink"))
    )
    my_profile.click()
    time.sleep(2)

    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".secCard"))
    )
    time.sleep(1)

    card_found = False
    cards = browser.find_elements(By.CSS_SELECTOR, ".secCard")
    for card in cards:
        paragraphs = card.find_elements(By.TAG_NAME, "p")
        card_date = paragraphs[0].text
        card_service = paragraphs[1].text

        # شيل الثواني من card_date قبل المقارنة
        card_date_no_seconds = ":".join(card_date.split(":")[:2]) + " " + card_date.split()[-1]

        if date in card_date_no_seconds and service_name in card_service:
            follow_link = card.find_element(By.CSS_SELECTOR, "a.outlin-btn")
            browser.execute_script("arguments[0].scrollIntoView(true);", follow_link)
            time.sleep(0.5)
            browser.execute_script("arguments[0].click();", follow_link)
            time.sleep(2)
            card_found = True
            break

    if not card_found:
        browser.quit()
        return "الطلب مش موجود"

    element = wait.until(
        EC.presence_of_element_located((By.XPATH, "//h2[contains(@style, 'white-space: pre-line')]"))
    )

    if element.text.strip() == "تم الرد علي فتواكم.":
        done_btn = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'تم الانتهاء')]"))
        )
        browser.execute_script("arguments[0].scrollIntoView(true);", done_btn)
        time.sleep(0.5)
        browser.execute_script("arguments[0].click();", done_btn)

        result_btn = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'نتيجة الاستعلام')]"))
        )
        browser.execute_script("arguments[0].scrollIntoView(true);", result_btn)
        time.sleep(0.5)
        browser.execute_script("arguments[0].click();", result_btn)

        question = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".css-p9qzma"))
        ).text.strip()

        answer = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".css-19p1ioo"))
        ).text.strip()

        browser.quit()

        return f"السؤال: {question} | الإجابة: {answer}"

    else:
        browser.quit()
        return None
    
