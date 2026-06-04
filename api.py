import json
import threading
import uuid
from flask import Flask
from flask_restx import Api, Resource, fields
from service_logic import execute_service
from tracking import tracking

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Service Automation API",
    description="API for automating Egyptian government services",
    doc="/swagger"
)

ns = api.namespace("api", description="Service Execution")

# Execute Models
request_model = api.model("ServiceExecutionRequest", {
    "ServiceName": fields.String(required=True, description="اسم الخدمة", example="طلب فتوى"),
    "CollectedData": fields.String(
        required=False,
        description="JSON string فيه البيانات",
        example='{"subject":"موضوع","question":"السؤال هنا"}'
    )
})

response_model = api.model("ServiceExecutionResponse", {
    "Success": fields.Boolean(description="نجح ولا لأ"),
    "Content": fields.String(description="النتيجة أو رسالة الخطأ"),
    "SubmittedAt": fields.String(description="وقت تقديم الطلب")
})

# Tracking Models
tracking_request_model = api.model("ServiceTrackingRequest", {
    "ServiceName": fields.String(required=True, description="اسم الخدمة", example="طلب فتوى"),
    "SubmittedAt": fields.String(required=True, description="وقت تقديم الطلب", example="الخميس، 4 يونيو 2026 في 02:51 ص")
})

tracking_response_model = api.model("ServiceTrackingResponse", {
    "Content": fields.String(description="النتيجة أو null لو لسه بيتعالج")
})

results_store = {}


def run_automation(task_id, service_name, collected_data):
    result = execute_service(service_name, collected_data)
    results_store[task_id] = result


@ns.route("/execute-service")
class ExecuteService(Resource):

    @ns.expect(request_model, validate=True)
    @ns.marshal_with(response_model)
    def post(self):
        """تنفيذ خدمة حكومية"""
        body = api.payload

        service_name = body.get("ServiceName")
        collected_data_raw = body.get("CollectedData")

        collected_data = {}
        if collected_data_raw:
            try:
                collected_data = json.loads(collected_data_raw)
            except json.JSONDecodeError:
                return {"Success": False, "Content": "CollectedData مش JSON صح", "SubmittedAt": ""}, 400

        task_id = str(uuid.uuid4())
        thread = threading.Thread(target=run_automation, args=(task_id, service_name, collected_data))
        thread.start()
        thread.join(timeout=120)

        result = results_store.pop(task_id, None)

        if result is None:
            return {"Success": False, "Content": "انتهى الوقت المحدد، حاول تاني", "SubmittedAt": ""}

        return {
            "Success": result["success"],
            "Content": result["content"],
            "SubmittedAt": result.get("submitted_at", "")
        }


@ns.route("/track-service")
class TrackService(Resource):

    @ns.expect(tracking_request_model, validate=True)
    @ns.marshal_with(tracking_response_model)
    def post(self):
        """تتبع حالة خدمة"""
        body = api.payload

        service_name = body.get("ServiceName")
        submitted_at = body.get("SubmittedAt")

        try:
            result = tracking(service_name, submitted_at)
            return {"Content": result}
        except Exception as e:
            return {"Content": None}


if __name__ == "__main__":
    app.run(debug=False, port=5000)