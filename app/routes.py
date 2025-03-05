from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# Set template folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "../templates")
app.template_folder = TEMPLATE_DIR

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["fraud_detection"]
transactions_col = db["transactions"]

# 🏠 Home Route
@app.route('/')
def home():
    return render_template('index.html')

# 🟢 GET: Latest Fraud Transactions (With Pagination)
@app.route('/latest_fraud_transactions')
def latest_fraud_transactions():
    page = int(request.args.get("page", 1))  # Default to page 1
    per_page = 10  # Show 10 transactions per page
    skip = (page - 1) * per_page

    fraud_cases = list(
        transactions_col.find({"fraud_status": "fraud"})
        .sort("timestamp", -1)
        .skip(skip)
        .limit(per_page)
    )

    # Normalize data structure
    cleaned_transactions = []
    for txn in fraud_cases:
        if "data" in txn and isinstance(txn["data"], list):
            txn_dict = {
                "transaction_id": txn["data"][0],
                "user_id": txn["data"][1],
                "amount": txn["data"][2],
                "location": txn["data"][3] if txn["data"][3] else "Unknown",
                "device": txn["data"][4],
                "timestamp": txn["data"][5],
                "fraud_status": txn.get("fraud_status", "unknown")
            }
        else:
            txn_dict = {
                "transaction_id": txn.get("transaction_id", "N/A"),
                "user_id": txn.get("user_id", "N/A"),
                "amount": txn.get("amount", 0),
                "location": txn.get("location", "Unknown"),
                "device": txn.get("device", "Unknown"),
                "timestamp": txn.get("timestamp", "Invalid Date"),
                "fraud_status": txn.get("fraud_status", "unknown")
            }
        cleaned_transactions.append(txn_dict)

    total_fraud_cases = transactions_col.count_documents({"fraud_status": "fraud"})

    return jsonify({
        "transactions": cleaned_transactions,
        "page": page,
        "per_page": per_page,
        "total_transactions": total_fraud_cases
    })

# 🟢 GET: Fraud Statistics
@app.route('/fraud_statistics')
def fraud_statistics():
    total = transactions_col.count_documents({})
    fraudulent = transactions_col.count_documents({"fraud_status": "fraud"})

    pipeline = [
        {"$match": {"fraud_status": "fraud", "location": {"$ne": None, "$ne": "", "$exists": True}}},
        {"$group": {"_id": "$location", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    top_fraud_locations = list(transactions_col.aggregate(pipeline))

    return jsonify({
        "total_transactions": total,
        "total_fraudulent": fraudulent,
        "fraud_rate": round((fraudulent / total * 100), 2) if total else 0,
        "top_fraud_locations": [{"location": loc["_id"], "count": loc["count"]} for loc in top_fraud_locations if loc["_id"]]
    })


# 🟢 GET: Fraud Cases by User
@app.route('/fraud_by_user')
def fraud_by_user():
    pipeline = [
        {"$match": {"fraud_status": "fraud", "user_id": {"$ne": None, "$exists": True}}},
        {"$group": {"_id": "$user_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    fraud_users = list(transactions_col.aggregate(pipeline))

    return jsonify([
        {"user_id": str(user["_id"]), "fraud_cases": user["count"]}
        for user in fraud_users if user["_id"] is not None
    ])

# 🟢 DELETE: Remove All Transactions (Reset Database)
@app.route('/delete_all_transactions', methods=['DELETE'])
def delete_all_transactions():
    result = transactions_col.delete_many({})
    return jsonify({"message": "Deleted all transactions", "deleted_count": result.deleted_count})

if __name__ == '__main__':
    app.run(debug=True)
