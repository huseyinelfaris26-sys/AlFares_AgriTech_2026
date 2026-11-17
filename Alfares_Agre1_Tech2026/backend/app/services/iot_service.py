from typing import Dict, Any
from datetime import datetime

class IoTService:
    def __init__(self, broker: str = "localhost", port: int = 1883):
        self.broker = broker
        self.port = port
        self.connected = False
        self.sensors_data: Dict[str, Any] = {}

    def connect(self):
        self.connected = True
        return True

    def publish(self, topic: str, payload: dict):
        if not self.connected:
            self.connect()
        print(f"[IoT] Publish to {topic}: {payload}")
        return True

    def get_sensor_reading(self, sensor_id: str) -> dict:
        import random
        return {
            "sensor_id": sensor_id,
            "timestamp": datetime.utcnow().isoformat(),
            "soil_moisture": round(random.uniform(20, 60), 1),
            "soil_temp": round(random.uniform(15, 30), 1),
            "air_temp": round(random.uniform(18, 35), 1),
            "humidity": random.randint(30, 80),
            "battery": random.randint(60, 100)
        }

    def subscribe_field(self, field_id: str):
        topic = f"farm/{field_id}/sensors/#"
        print(f"[IoT] Subscribed to {topic}")
        return topic

iot_service = IoTService()
