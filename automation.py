from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta

CREDENTIALS = {
    "seif":  {"mobile": "01128417941", "password": "Seif@2003"},
    "nahed": {"mobile": "01121352002", "password": "Nahed@1111"},
    "sherif":{"mobile": "01143082288", "password": "Qpalzm@2004"},
}

SERVICE_CREDENTIALS = {
    "طلب فتوى":                                "seif",
    "استعلام عن الرقم التأميني":               "sherif",
    "استعلام عن المعاش المنصرف للقائم بالصرف": "nahed",
    "استعلام عن مخالفات رخص القيادة":          "seif",
}


class Automation:
    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.link = 'https://digital.gov.eg/'
        self.browser.get(self.link)
        self.wait = WebDriverWait(self.browser, 30)
        self.main_window = self.browser.current_window_handle

    def format_datetime_ar(self, dt):
        days = [
            "الاثنين", "الثلاثاء", "الأربعاء",
            "الخميس", "الجمعة", "السبت", "الأحد"
        ]
        months = [
            "يناير", "فبراير", "مارس", "أبريل",
            "مايو", "يونيو", "يوليو", "أغسطس",
            "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
        ]

        day_name = days[dt.weekday()]
        month_name = months[dt.month - 1]
        hour = dt.hour
        period = "ص" if hour < 12 else "م"
        hour_12 = hour % 12
        if hour_12 == 0:
            hour_12 = 12

        return (
            f"{day_name}، {dt.day} {month_name} {dt.year} "
            f"في {hour_12:02d}:{dt.minute:02d} {period}"
        )

    def log_in(self, mobile_number, password):
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"تسجيل الدخول")]'))
        )
        login_button.click()
        time.sleep(2)

        windows = self.browser.window_handles
        if len(windows) > 1:
            login_window = windows[-1]
            self.browser.switch_to.window(login_window)

        username_input = self.wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_input.clear()
        username_input.send_keys(mobile_number)

        next_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "kc-login"))
        )
        next_button.click()

        password_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_input.clear()
        password_input.send_keys(password)

        login_submit = self.wait.until(
            EC.element_to_be_clickable((By.ID, "kc-login"))
        )
        login_submit.click()
        time.sleep(3)

    def search_service(self, service_name):
        self.browser.switch_to.window(self.main_window)
        search_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="أنا محتاج..."]'))
        )
        search_input.clear()
        search_input.send_keys(service_name)

        link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{service_name}')]"))
        )
        link.click()
        time.sleep(3)

    def service_page(self):
        try:
            checkbox_label = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"أوافق على الشروط")]'))
            )
            self.browser.execute_script("arguments[0].scrollIntoView();", checkbox_label)
            time.sleep(1)
            checkbox_label.click()
        except:
            pass

        start_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="بدء الخدمة"]]'))
        )
        start_button.click()
        time.sleep(3)

    def talb_fatw(self, subject, question):
        dropdown_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Open']"))
        )
        dropdown_btn.click()

        option = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(),'{subject}')]"))
        )
        option.click()

        text_area = self.wait.until(
            EC.presence_of_element_located((By.ID, "question"))
        )
        text_area.send_keys(question)
        time.sleep(2)

        next_btm = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'التالي')]"))
        )
        next_btm.click()
        completion_time = self.format_datetime_ar(datetime.now())
        time.sleep(5)

        request_number = self.browser.find_element(
            By.XPATH, "//td[contains(text(), 'رقم الطلب:')]/following-sibling::td").text
        self.browser.quit()
        return completion_time

    def Driving_License(self, license_number, license_type, governate, issue_place):
        license_number_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "LicenseNumber"))
        )
        license_number_input.clear()
        license_number_input.send_keys(license_number)
        time.sleep(1)

        arrows = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[@aria-label='Open']"))
        )
        arrows[0].click()
        option = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//ul[@role='listbox']//li[contains(text(), '{license_type}')]"))
        )
        self.browser.execute_script("arguments[0].click();", option)
        time.sleep(1)

        arrows = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[@aria-label='Open']"))
        )
        arrows[1].click()
        option = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//ul[@role='listbox']//li[contains(text(), '{governate}')]"))
        )
        self.browser.execute_script("arguments[0].click();", option)
        time.sleep(1)

        arrows = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[@aria-label='Open']"))
        )
        arrows[2].click()
        option = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//ul[@role='listbox']//li[contains(text(), '{issue_place}')]"))
        )
        self.browser.execute_script("arguments[0].click();", option)
        time.sleep(1)

        next_btm = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'التالي')]"))
        )
        next_btm.click()
        time.sleep(5)
        self.browser.quit()
        return "رقم الرخصة خطاء"

    def insurance_number(self):
        next_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'التالي')]"))
        )
        self.browser.execute_script("arguments[0].scrollIntoView();", next_btn)
        time.sleep(1)
        self.browser.execute_script("arguments[0].click();", next_btn)
        time.sleep(5)

        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.MuiTable-root"))
        )

        rows = self.browser.find_elements(By.CSS_SELECTOR, "tr.MuiTableRow-root")
        insurance_num = None

        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, "td.MuiTableCell-root")
            if len(cells) >= 2:
                label = cells[0].text.strip()
                value = cells[1].text.strip()
                if "الرقم التأمينى" in label:
                    insurance_num = value
                    break

        self.browser.quit()
        return insurance_num if insurance_num else "ليس لديك رقم تاميني"

    def maash(self):
        next_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'التالي')]"))
        )
        next_btn.click()
        time.sleep(5)

        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "MuiDataGrid-virtualScrollerRenderZone"))
        )

        rows = self.browser.find_elements(By.CSS_SELECTOR, ".MuiDataGrid-row")
        results = []
        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, ".MuiDataGrid-cellContent")
            if len(cells) >= 4:
                owner_name = cells[1].text
                net_income = cells[3].text
                results.append(f"{owner_name} - {net_income}")
        self.browser.quit()
        return " | ".join(results) if results else None