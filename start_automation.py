from automation import Automation, CREDENTIALS, SERVICE_CREDENTIALS


class StartAutomation(Automation):

    def __init__(self):
        super().__init__()

    def run(self, service_name, collected_data: dict):
        # جيب الـ credentials الصح بناءً على الخدمة
        user_key = SERVICE_CREDENTIALS.get(service_name, "seif")
        creds = CREDENTIALS[user_key]

        self.log_in(creds["mobile"], creds["password"])
        self.search_service(service_name)
        self.service_page()

        if service_name == "طلب فتوى":
            subject = collected_data.get("subject")
            question = collected_data.get("question")
            return self.talb_fatw(subject, question)

        elif service_name == "استعلام عن الرقم التأميني":
            return self.insurance_number()

        elif service_name == "استعلام عن المعاش المنصرف للقائم بالصرف":
            return self.maash()

        elif service_name == "استعلام عن مخالفات رخص القيادة":
            license_number = collected_data.get("license_number")
            license_type = collected_data.get("license_type")
            governate = collected_data.get("governate")
            issue_place = collected_data.get("issue_place")
            return self.Driving_License(license_number, license_type, governate, issue_place)

        return None