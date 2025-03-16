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
