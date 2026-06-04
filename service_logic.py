from start_automation import StartAutomation


def execute_service(service_name: str, collected_data: dict) -> dict:
    try:
        bot = StartAutomation()
        result = bot.run(service_name, collected_data)

        if service_name == "طلب فتوى":
            if result:
                return {"success": True, "content": None, "submitted_at": result}
            else:
                return {"success": False, "content": None, "submitted_at": ""}

        elif service_name == "استعلام عن الرقم التأميني":
            if result and result != "ليس لديك رقم تاميني":
                return {"success": True, "content": result, "submitted_at": ""}
            else:
                return {"success": False, "content": None, "submitted_at": ""}

        elif service_name == "استعلام عن المعاش المنصرف للقائم بالصرف":
            if result:
                return {"success": True, "content": result, "submitted_at": ""}
            else:
                return {"success": False, "content": None, "submitted_at": ""}

        elif service_name == "استعلام عن مخالفات رخص القيادة":
            if result and result != "رقم الرخصة خطاء":
                return {"success": True, "content": result, "submitted_at": ""}
            else:
                return {"success": False, "content": None, "submitted_at": ""}

        return {"success": False, "content": None, "submitted_at": ""}

    except Exception as e:
        return {"success": False, "content": f"حدث خطأ: {str(e)}", "submitted_at": ""}