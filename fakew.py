from flask import Flask, jsonify, request
import random
import hashlib

app = Flask(__name__)

first_names = ["Amit", "Priya", "Rahul", "Sneha", "Vikram", "Ananya", "Arjun", "Deepika", "Kunal", "Pooja"]
last_names = ["Sharma", "Verma", "Patel", "Nair", "Reddy", "Singh", "Gupta", "Das", "Iyer", "Chopra"]
banks = ["HDFC", "SBI", "ICICI", "Axis"]

users = []

for i in range(100):
    random.seed(i)

    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    email = f"{full_name.replace(' ', '').lower()}@example.com"
    phone = f"98{random.randint(10000000, 99999999)}"
    password = hashlib.sha256(full_name.encode()).hexdigest()[:10]

    card = {
        "number": f"{random.randint(4000, 4999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
        "type": random.choice(["Credit", "Debit", "Prepaid"]),
        "bank": random.choice(banks),
        "limit": random.randint(50000, 500000),
        "balance": random.randint(0, 50000),
    }

    transactions, loans, mortgages, bills, emis = [], [], [], [], []
    total_spent, missed_payments = 0, 0

    for _ in range(20):
        amount = random.randint(500, 5000)
        transactions.append({"amount": amount, "transaction_type": random.choice(["sent", "received"])})
        total_spent += amount  

        bills.append({"amount": random.randint(100, 999), "paid": random.choice([True, False])})
        emis.append({"amount": random.randint(500, 5000), "paid": random.choice([True, False])})
        repaid = random.choice([True, False])
        loans.append({"amount": random.randint(50000, 500000), "repaid": repaid})
        mortgages.append({"amount": random.randint(100000, 1000000), "repaid": repaid})
        if not repaid:
            missed_payments += 1

    # Scores
    late_payment_risk = min(10, missed_payments)
    app_score = max(300, 700 - (100 if late_payment_risk > 5 else 0) - (missed_payments * 10))
    target_saving = random.randint(5000, 10000)
    profit = target_saving - total_spent  

    debt_ratio = (sum(m["amount"] for m in mortgages if not m["repaid"]) + 
                  sum(b["amount"] for b in bills if not b["paid"]) + 
                  sum(e["amount"] for e in emis if not e["paid"])) / (card["balance"] + 1)

    financial_health = max(0, min(100, (app_score / 7) - (late_payment_risk * 5) - (debt_ratio * 30) + (profit / 1000) * 5))

    users.append({
        "name": full_name,
        "email": email,
        "phone": phone,
        "password": password,
        "card": card,
        "transactions": transactions,
        "loans": loans,
        "mortgages": mortgages,
        "bills": bills,
        "emis": emis,
        "late_payment_risk": late_payment_risk,
        "app_score": app_score,
        "target_saving": target_saving,
        "profit": profit,
        "total_spent": total_spent
    })

@app.route('/summary', methods=['GET'])
def get_summary():
    card_number = request.args.get("card")

    if not card_number:
        return jsonify({"error": "Card number is required"}), 400

    user = next((u for u in users if u["card"]["number"] == card_number), None)

    if not user:
        return jsonify({"error": "User not found"}), 404

    mortgages_due = [m["amount"] for m in user["mortgages"] if not m["repaid"]]
    bills_due = [b["amount"] for b in user["bills"] if not b["paid"]]
    emis_due = [e["amount"] for e in user["emis"] if not e["paid"]]

    return jsonify({
        "card_number": card_number,
        "card_type": user["card"]["type"],
        "bank": user["card"]["bank"],
        "total_mortgages_due": sum(mortgages_due),
        "count_mortgages_due": len(mortgages_due),
        "total_bills_due": sum(bills_due),
        "count_bills_due": len(bills_due),
        "total_emis_due": sum(emis_due),
        "count_emis_due": len(emis_due),
        "app_score": user["app_score"],
        "late_payment_risk": user["late_payment_risk"],
        "financial_health_percentage": round(user["financial_health"], 2),
        "profit": user["profit"],
        "target_saving": user["target_saving"],
        "total_amount_spent": user["total_spent"]
    })

if __name__ == '__main__':
    app.run(debug=True)
