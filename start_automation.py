from automation import Automation, CREDENTIALS, SERVICE_CREDENTIALS


class StartAutomation(Automation):

    def _init_(self):
        super()._init_()

    def run(self, service_name, request_data: dict):
        # جيب الـ credentials الصح بناءً على الخدمة
        user_key = SERVICE_CREDENTIALS.get(service_name, "seif")
        creds = CREDENTIALS[user_key]

        self.log_in(creds["mobile"], creds["password"])
        self.search_service(service_name)
        self.service_page()

        if service_name == "طلب فتوى":
            subject = request_data.get("الموضوع")
            question = request_data.get("نص سؤال الفتوي")
            return self.talb_fatw(subject, question)

        elif service_name == "استعلام عن الرقم التأميني":
            return self.insurance_number()

        elif service_name == "الاستعلام عن المعاش المنصرف للقائم بالصرف":
            return self.maash()

        elif service_name == "استعلام عن مخالفات رخص القيادة":
            license_number = request_data.get("رقم الرخصة")
            license_type = request_data.get("نوع الترخيص")
            governate = request_data.get("المحافظة")
            issue_place = request_data.get("وحدة الترخيص")
            return self.Driving_License(license_number, license_type, governate, issue_place)

        return None