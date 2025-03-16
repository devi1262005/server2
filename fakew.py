from flask import Flask, jsonify, request
import random
import hashlib
from datetime import datetime, timedelta

app = Flask(__name__)

first_names = ["Amit", "Priya", "Rahul", "Sneha", "Vikram", "Ananya", "Arjun", "Deepika", "Kunal", "Pooja"]
last_names = ["Sharma", "Verma", "Patel", "Nair", "Reddy", "Singh", "Gupta", "Das", "Iyer", "Chopra"]
ott_platforms = ["Netflix", "Amazon Prime", "Disney+", "Hotstar", "Hulu", "Apple TV+"]
banks = ["HDFC", "SBI", "ICICI", "Axis"]
emi_items = ["Car Loan", "Phone EMI", "Laptop EMI", "Home Loan", "Furniture EMI"]

users = []

for i in range(100):
    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    email = f"{full_name.replace(' ', '').lower()}@example.com"
    phone = f"98{random.randint(10000000, 99999999)}"
    password = hashlib.sha256(full_name.encode()).hexdigest()[:10]

    credit_card = {
        "number": f"{random.randint(4000, 4999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
        "type": random.choice(["Visa", "MasterCard", "RuPay"]),
        "limit": random.randint(50000, 500000),
        "balance": random.randint(0, 50000),
    }

    transactions, total_spent = [], 0
    for _ in range(20):
        amount = random.randint(500, 5000)
        sent = random.choice(["sent", "received"])
        if sent == "sent":
            total_spent += amount
        transactions.append({"amount": amount, "transaction_type": sent})

    loans, mortgages, bills, emis, missed_payments, total_obligations = [], [], [], [], 0, 0
    
    for _ in range(20):
        repaid = random.choice([True, False])
        amount = random.randint(50000, 500000)
        total_obligations += amount
        if not repaid:
            missed_payments += 1
        loans.append({"bank": random.choice(banks), "amount": amount, "repaid": repaid})
        
    for _ in range(20):
        repaid = random.choice([True, False])
        amount = random.randint(100000, 1000000)
        total_obligations += amount
        if not repaid:
            missed_payments += 1
        mortgages.append({"amount": amount, "repaid": repaid})
        
    for _ in range(20):
        paid = random.choice([True, False])
        amount = random.randint(100, 999)
        total_obligations += amount
        if not paid:
            missed_payments += 1
        bills.append({"provider": random.choice(ott_platforms), "amount": amount, "paid": paid})
        
    for _ in range(20):
        paid = random.choice([True, False])
        amount = random.randint(500, 5000)
        total_obligations += amount
        if not paid:
            missed_payments += 1
        emis.append({"item": random.choice(emi_items), "amount": amount, "paid": paid})
    
    debt_ratio = total_obligations / max(1, credit_card["limit"])  # Prevent division by zero
    late_payment_score = max(0, 100 - (missed_payments / max(1, total_obligations) * 100))
    app_score = max(300, 700 - int(missed_payments * 10))
    target_saving = random.randint(5000, 10000)
    profit = target_saving - total_spent
    financial_health = max(0, min(100, (app_score / 7) - (late_payment_score / 5) - (debt_ratio * 30) + (profit / 1000) * 5))
    
    users.append({
        "name": full_name,
        "email": email,
        "phone": phone,
        "password": password,
        "credit_card": credit_card,
        "transactions": transactions,
        "loans": loans,
        "mortgages": mortgages,
        "bills": bills,
        "emis": emis,
        "late_payment_score": late_payment_score,
        "app_score": app_score,
        "target_saving": target_saving,
        "profit": profit,
        "financial_health": financial_health
    })

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/summary', methods=['GET'])
def get_summary():
    card_number = request.args.get("card")
    if not card_number:
        return jsonify({"error": "Card number is required"}), 400
    user = next((u for u in users if u["credit_card"]["number"] == card_number), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "card_number": card_number,
        "card_type": user["credit_card"]["type"],
        "app_score": user["app_score"],
        "late_payment_score": user["late_payment_score"],
        "financial_health": user["financial_health"]
    })

if __name__ == '__main__':
    app.run(debug=True)
