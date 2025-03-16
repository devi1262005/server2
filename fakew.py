from flask import Flask, jsonify
import random
import hashlib
from datetime import datetime, timedelta

app = Flask(__name__)

first_names = ["Amit", "Priya", "Rahul", "Sneha", "Vikram", "Ananya", "Arjun", "Deepika", "Kunal", "Pooja"]
last_names = ["Sharma", "Verma", "Patel", "Nair", "Reddy", "Singh", "Gupta", "Das", "Iyer", "Chopra"]
ott_platforms = ["Netflix", "Amazon Prime", "Disney+", "Hotstar", "Hulu", "Apple TV+"]

random.seed(42)
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
    
    transactions = []
    total_spent = 0
    for _ in range(random.randint(5, 15)):
        date = datetime.now() - timedelta(days=random.randint(1, 365))
        amount = random.randint(500, 5000)
        sent = random.choice(["sent", "received"])
        if sent == "sent":
            total_spent += amount
        transactions.append({"date": date.strftime('%Y-%m-%d'), "amount": amount, "transaction_type": sent})
    
    loans = []
    missed_payments = 0
    for _ in range(random.randint(1, 5)):
        due_date = datetime.now() + timedelta(days=random.randint(-30, 365))
        repaid = random.choice([True, False])
        if not repaid:
            missed_payments += 1
        loans.append({"bank": random.choice(["HDFC", "SBI", "ICICI", "Axis"]), "amount": random.randint(50000, 500000), "due_date": due_date.strftime('%Y-%m-%d'), "repaid": repaid})
    
    mortgages = []
    for _ in range(random.randint(0, 3)):
        due_date = datetime.now() + timedelta(days=random.randint(-30, 365))
        repaid = random.choice([True, False])
        if not repaid:
            missed_payments += 1
        mortgages.append({"amount": random.randint(100000, 1000000), "due_date": due_date.strftime('%Y-%m-%d'), "repaid": repaid})
    
    bills = []
    for _ in range(random.randint(2, 5)):
        bills.append({
            "provider": random.choice(["Electricity", "Water", "Internet", random.choice(ott_platforms)]),
            "amount": random.randint(100, 999),
            "due_date": (datetime.now() + timedelta(days=random.randint(-30, 30))).strftime('%Y-%m-%d'),
            "paid": random.choice([True, False])
        })
    
    late_payment_risk = min(10, missed_payments)  
    app_score = 700 - (100 if late_payment_risk > 5 else 0) - (missed_payments * 10)
    target_saving = 50000
    profit = target_saving - total_spent
    
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
        "late_payment_risk": late_payment_risk,
        "app_score": max(300, app_score),
        "target_saving": target_saving,
        "profit": profit
    })

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/summary', methods=['GET'])
def get_summary():
    total_spent = sum(user["target_saving"] - user["profit"] for user in users)
    return jsonify({
        "total_amount_spent": total_spent,
        "target_saving": 50000,
        "profit": 50000 - total_spent
    })

if __name__ == '__main__':
    app.run(debug=True)
