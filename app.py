import matplotlib
matplotlib.use('Agg')  # Use Agg backend to avoid GUI-related errors
import matplotlib.pyplot as plt

from flask import Flask, render_template, jsonify, send_file
import io
import base64
import threading
import random
import time
from collections import deque
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)

# This will hold the recent fraud detection results
fraud_results = deque(maxlen=10)  # Keep the latest 10 results
total_transactions = 0
total_fraudulent = 0

# Function to simulate inserting fraud results into the queue
def simulate_fraud_insertion():
    global total_transactions, total_fraudulent
    while True:
        total_transactions += 1
        fraud_status = "fraud" if random.random() < 0.2 else "normal"
        if fraud_status == "fraud":
            total_fraudulent += 1
        fraud_results.append({"transaction_id": random.randint(1000, 9999), "fraud_status": fraud_status})
        time.sleep(1)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fraud_detection', methods=['GET'])
def get_fraud_detection_data():
    return jsonify(list(fraud_results))

@app.route('/kpis', methods=['GET'])
def get_kpis():
    return jsonify({
        "total_transactions": total_transactions,
        "total_fraudulent": total_fraudulent,
        "fraud_percentage": (total_fraudulent / total_transactions * 100) if total_transactions else 0
    })

@app.route('/pie_chart')
def pie_chart():
    fraud_percentage = (total_fraudulent / total_transactions * 100) if total_transactions else 0
    # Create a pie chart for fraud vs normal transactions
    labels = 'Fraud', 'Normal'
    sizes = [fraud_percentage, 100 - fraud_percentage]
    colors = ['red', 'green']
    explode = (0.1, 0)  # explode fraud slice
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Convert to PNG image
    img = io.BytesIO()
    FigureCanvas(fig).print_png(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/line_chart')
def line_chart():
    # Create a line chart to show fraudulent transactions over time
    x = list(range(len(fraud_results)))
    y = [1 if result["fraud_status"] == "fraud" else 0 for result in fraud_results]  # Convert fraud status to 1 (fraud) and 0 (normal)

    fig, ax = plt.subplots()
    ax.plot(x, y, label='Fraudulent Transactions', color='blue')
    ax.set(xlabel='Transaction Count', ylabel='Fraudulent',
           title='Fraudulent Transactions Trend')
    ax.grid()

    # Convert to PNG image
    img = io.BytesIO()
    FigureCanvas(fig).print_png(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    # Start the simulation thread
    threading.Thread(target=simulate_fraud_insertion, daemon=True).start()
    app.run(debug=True)
