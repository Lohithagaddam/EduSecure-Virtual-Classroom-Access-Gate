import json
import boto3
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("VirtualClassroomAccessGate")

def lambda_handler(event, context):

    # Handle API Gateway request body
    if isinstance(event.get("body"), str):
        data = json.loads(event["body"])
    else:
        data = event

    rfid_id = data.get("rfid_id", "")
    classroom = data.get("classroom", "Cloud Computing")

    if not rfid_id:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "rfid_id is required"
            })
        }

    # Get student details from DynamoDB
    response = table.get_item(
        Key={"rfid_id": rfid_id}
    )

    item = response.get("Item")

    if item and item.get("status") == "ACTIVE":
        status = "ACCESS ALLOWED"
        student_id = item.get("student_id", "UNKNOWN")
        name = item.get("name", "Unknown")
        registered_classroom = item.get("classroom", classroom)
    else:
        status = "ACCESS DENIED"
        student_id = "UNKNOWN"
        name = "Unknown"
        registered_classroom = classroom

    result = {
        "rfid_id": rfid_id,
        "student_id": student_id,
        "name": name,
        "classroom": registered_classroom,
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(result)
    }