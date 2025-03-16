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
    random.seed(i)
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
    for _ in range(20):
        date = datetime.now() - timedelta(days=random.randint(1, 365))
        amount = random.randint(500, 5000)
        sent = random.choice(["sent", "received"])
        if sent == "sent":
            total_spent += amount
        transactions.append({"date": date.strftime('%Y-%m-%d'), "amount": amount, "transaction_type": sent})

    loans, mortgages, bills, emis = [], [], [], []
    missed_payments = 0
    total_debt = 0
    
    for _ in range(20):
        amount = random.randint(50000, 500000)
        due_date = datetime.now() + timedelta(days=random.randint(-30, 365))
        repaid = random.choice([True, False])
        if not repaid:
            missed_payments += 1
        total_debt += amount if not repaid else 0
        loans.append({"bank": random.choice(banks), "amount": amount, "due_date": due_date.strftime('%Y-%m-%d'), "repaid": repaid})

    for _ in range(20):
        amount = random.randint(100000, 1000000)
        due_date = datetime.now() + timedelta(days=random.randint(-30, 365))
        repaid = random.choice([True, False])
        if not repaid:
            missed_payments += 1
        total_debt += amount if not repaid else 0
        mortgages.append({"amount": amount, "due_date": due_date.strftime('%Y-%m-%d'), "repaid": repaid})

    for _ in range(20):
        amount = random.randint(100, 999)
        bills.append({"provider": random.choice(["Electricity", "Water", "Internet", random.choice(ott_platforms)]), "amount": amount, "due_date": (datetime.now() + timedelta(days=random.randint(-30, 30))).strftime('%Y-%m-%d'), "paid": random.choice([True, False])})
    
    for _ in range(20):
        amount = random.randint(500, 5000)
        emis.append({"item": random.choice(emi_items), "amount": amount, "due_date": (datetime.now() + timedelta(days=random.randint(-30, 30))).strftime('%Y-%m-%d'), "paid": random.choice([True, False])})
    
    debt_ratio = total_debt / (credit_card["limit"] if credit_card["limit"] else 1)
    late_payment_score = max(0, min(10, 10 - (missed_payments * 0.5)))
    app_score = max(300, 700 - (missed_payments * 10) - (debt_ratio * 100))
    target_saving = random.randint(5000, 10000)
    profit = target_saving - total_spent
    financial_health = max(0, min(100, (app_score / 7) - (late_payment_score * 5) - (debt_ratio * 30) + (profit / 1000) * 5))
    
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

if __name__ == '__main__':
    app.run(debug=True)
