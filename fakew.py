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
    random.seed(i)  # Ensure reproducibility for each user

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

    # Transactions
    transactions = []
    total_spent = 0
    for _ in range(20):
        date = datetime.now() - timedelta(days=random.randint(1, 365))
        amount = random.randint(500, 5000)
        sent = random.choice(["sent", "received"])
        if sent == "sent":
            total_spent += amount
        transactions.append({"date": date.strftime('%Y-%m-%d'), "amount": amount, "transaction_type": sent})

    # Loans
    loans = []
    missed_payments = 0
    for _ in range(20):
        due_date = datetime.now() + timedelta(days=random.randint(-30, 365))
        repaid = random.choice([True, False])
        if not repaid:
            missed_payments += 1
        loans.append({
            "bank": random.choice(banks),
            "amount": random.randint(50000, 500000),
            "due_date": due_date.strftime('%Y-%m-%d'),
            "repaid": repaid
        })

    # Mortgages
    mortgages = []
    for _ in range(20):
        due_date = datetime.now() + timedelta(days=random.randint(-30, 365))
        repaid = random.choice([True, False])
        if not repaid:
            missed_payments += 1
        mortgages.append({
            "amount": random.randint(100000, 1000000),
            "due_date": due_date.strftime('%Y-%m-%d'),
            "repaid": repaid
        })

    # Bills
    bills = []
    for _ in range(20):
        bills.append({
            "provider": random.choice(["Electricity", "Water", "Internet", random.choice(ott_platforms)]),
            "amount": random.randint(100, 999),
            "due_date": (datetime.now() + timedelta(days=random.randint(-30, 30))).strftime('%Y-%m-%d'),
            "paid": random.choice([True, False])
        })

    # EMIs
    emis = []
    for _ in range(20):
        emis.append({
            "item": random.choice(emi_items),
            "amount": random.randint(500, 5000),
            "due_date": (datetime.now() + timedelta(days=random.randint(-30, 30))).strftime('%Y-%m-%d'),
            "paid": random.choice([True, False])
        })

    # Calculations
    late_payment_risk = min(10, missed_payments)
    app_score = 700 - (100 if late_payment_risk > 5 else 0) - (missed_payments * 10)
    target_saving = random.randint(5000, 10000)
    profit = target_saving - total_spent

    # User Data
    user_data = {
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
        "late_payment_risk": late_payment_risk,
        "app_score": max(300, app_score),
        "target_saving": target_saving,
        "profit": profit
    }
    
    users.append(user_data)

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

    mortgages_due = [m["amount"] for m in user["mortgages"] if not m["repaid"]]
    bills_due = [b["amount"] for b in user["bills"] if not b["paid"]]
    emis_due = [e["amount"] for e in user["emis"] if not e["paid"]]

    total_due = sum(mortgages_due) + sum(bills_due) + sum(emis_due)
    total_obligations = len(user["bills"]) + len(user["emis"]) + len(user["mortgages"])
    missed_payments = len(mortgages_due) + len(bills_due) + len(emis_due)

    # Calculate Late Payment Risk Score (0 - 10, float)
    if total_obligations > 0:
        late_payment_risk = (missed_payments / total_obligations) * 10
    else:
        late_payment_risk = 0

    # Calculate Credit Utilization
    credit_utilization = (user["credit_card"]["balance"] / user["credit_card"]["limit"]) * 100

    # Financial Health Score (Dynamic)
    base_score = 800
    base_score -= late_payment_risk * 5
    base_score -= (credit_utilization / 2)  # Higher utilization reduces score
    base_score -= (total_due / 10000)  # More due payments lower the score

    financial_health_percentage = max(0, min(100, base_score / 8))  # Convert to 0-100%

    return jsonify({
        "card_number": card_number,
        "card_type": user["credit_card"]["type"],
        "total_mortgages_due": sum(mortgages_due),
        "count_mortgages_due": len(mortgages_due),
        "total_bills_due": sum(bills_due),
        "count_bills_due": len(bills_due),
        "total_emis_due": sum(emis_due),
        "count_emis_due": len(emis_due),
        "app_score": max(300, base_score),
        "late_payment_risk": round(late_payment_risk, 2),
        "financial_health_percentage": round(financial_health_percentage, 2)
    })
