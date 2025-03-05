from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

locations = ['New York', 'San Francisco', 'Chicago', 'Houston', 'Miami']
devices = ['iPhone', 'Android', 'Web', 'Tablet']

def generate_transaction():
    return {
        "transaction_id": random.randint(1000, 9999),
        "user_id": random.randint(1, 100),
        "amount": random.randint(50, 5000),
        "location": random.choice(locations),
        "device": random.choice(devices),
        "timestamp": datetime.utcnow().isoformat(),
        "fraud_status": "fraud" if random.random() < 0.1 else "normal"
    }

while True:
    transaction = generate_transaction()
    producer.send('transactions', value=transaction)
    print(f"Sent transaction: {transaction}")
    time.sleep(1)
