# Real-Time Fraud Detection System

## 📌 Overview
I developed a **Real-Time Fraud Detection System** using **Apache Kafka**, **Apache Spark**, **MongoDB**, **Flask**, and **JavaScript**. This project processes live transaction data, detects fraudulent activities using Spark Streaming, and visualizes insights on a web dashboard.

---

## 🚀 Technologies Used

| Component   | Technology Used |
|------------|----------------|
| Streaming  | Apache Kafka   |
| Processing | Apache Spark (PySpark) |
| Storage    | MongoDB        |
| Backend API | Flask        |
| Frontend   | HTML, CSS, JavaScript (jQuery, Chart.js) |
| Deployment | Docker, GitHub |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/MrAdithya21/Real-Time-Fraud-Detection.git
cd Real-Time-Fraud-Detection
```

### 2️⃣ Start Kafka & Zookeeper
Make sure Kafka & Zookeeper are running:
```bash
zookeeper-server-start.sh config/zookeeper.properties &
kafka-server-start.sh config/server.properties &
```

### 3️⃣ Start Kafka Producer
Run the Kafka Producer to stream transaction data:
```bash
python kafka/producer.py
```

### 4️⃣ Start Spark Streaming Job
Run the Kafka Consumer (Spark Streaming)
```bash
spark-submit --jars /path/to/kafka-spark-jars/spark-sql-kafka-0-10_2.12-3.5.5.jar \
             spark/fraud_streaming.py
```

### 5️⃣ Start Flask API
```bash
python app/routes.py
```

### 6️⃣ Run Frontend
Open http://127.0.0.1:5000 in your browser.

---

## 📊 Web Dashboard Features
✔️ **Live Fraud Transactions Table** – Displays the latest fraudulent transactions.  
✔️ **Fraud KPIs** – Shows total transactions, fraud count, and fraud percentage.  
✔️ **Top 5 Fraud Locations** – Visualizes fraud hotspots.  
✔️ **Fraud Pie Chart** – Compares total vs fraudulent transactions.  

---

## 📡 API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/latest_fraud_transactions` | GET | Fetch latest fraud transactions (pagination) |
| `/fraud_statistics` | GET | Get fraud count, percentage, and top fraud locations |
| `/fraud_by_user` | GET | Get fraud cases grouped by users |
| `/delete_all_transactions` | DELETE | Clear all fraud data |

---

## 🏗️ **System Architecture**

```plaintext
+---------------+      +----------------+      +---------------------+      +---------------+
|  Kafka Producer  | -> |  Kafka Broker  | -> |  Spark Streaming  | -> |  MongoDB  |
+---------------+      +----------------+      +---------------------+      +---------------+
                                                            |
                                                            v
                                                 +----------------+
                                                 |  Flask API    |
                                                 +----------------+
                                                            |
                                                            v
                                                 +----------------+
                                                 |  Web Dashboard |
                                                 +----------------+
```

---

## 🔥 Screenshots
**Fraud Transactions Table:**  
<img width="1175" alt="Screenshot 2025-03-05 at 9 43 20 AM" src="https://github.com/user-attachments/assets/a609ab52-0852-4c32-b382-82ab0fb96c11" />

**Total vs Fraud Transactions Pie Chart:**  
<img width="368" alt="Screenshot 2025-03-05 at 9 43 57 AM" src="https://github.com/user-attachments/assets/19f345e2-2dab-4bce-a1f0-5119ba98e9d3" />

**MongoDB Database:**
<img width="1512" alt="Screenshot 2025-03-05 at 9 47 23 AM" src="https://github.com/user-attachments/assets/30bd0121-5c94-4db8-86da-1b0c31d1761a" />


---

## 📌 Future Enhancements
🔹 Deploy on **AWS / Azure**  
🔹 Integrate **Machine Learning** for Fraud Prediction  
🔹 Implement **Real-time SMS/Email alerts** for fraud transactions  

---

## 🏆 Contributors
👨‍💻 **Adithya Singupati** - Developer 💻

---

## 📜 License
This project is licensed under the **MIT License**.

---

## ✅ Features in the README
✔️ **Detailed Architecture Diagram**  
✔️ **Technology Stack**  
✔️ **Step-by-Step Setup Guide**  
✔️ **API Endpoints & Features**  
✔️ **Future Enhancements**  
✔️ **Proper Markdown Formatting**  

Now you can **copy & paste** this `README.md` into your **GitHub repository**. 🎯 Let me know if you need modifications! 🚀

