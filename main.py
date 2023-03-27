from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home1():
    return render_template("base.html")

@app.route('/home', methods=['GET'])
def home():
    return render_template("home.html")

 #Endpoint to calculate SIP required
@app.route('/sip', methods=["POST", "GET"])
def sip():
    if request.method == "POST":
        data = request.form
        target_value = data['target_value']
        annual_rate_of_return = data['annual_rate_of_return']
        years = data['years']
        final_value = calculate_final_value1(target_value, annual_rate_of_return, years)
        #year_end_value = calculate(final_value, annual_rate_of_return, years)
        return redirect(url_for("output1", final_val={'target_value':target_value,'annual_rate_of_return':annual_rate_of_return,'years':years,'required_sip':final_value}))
    else: 
        return render_template("sip.html")

def calculate_final_value1(target_value, annual_rate_of_return, years):
    annual_rate_of_return = int(annual_rate_of_return) / 1200
    years = int(years) * 12
    final_value = (int(target_value) * annual_rate_of_return) / ((annual_rate_of_return+1) * (((annual_rate_of_return+1) ** years)-1))
    #print(final_value)
    return round(final_value, 2)

@app.route('/sip/required/<final_val>')
def output1(final_val):
    return jsonify(final_val)


#Endpoint to calculate number of withdrawals until depleted
@app.route('/withdrawals', methods=["POST", "GET"])
def withdrawals():
    if request.method == "POST":
        data = request.form
        initial_investment = data['initial_investment']
        withdrawal_amount = data['withdrawal_amount']
        withdrawal_frequency = data['withdrawal_frequency']
        inflation_rate = data['inflation_rate']
        roi = data['roi']
        final_value = calculate_final_value2(initial_investment , withdrawal_amount, withdrawal_frequency, inflation_rate, roi)
        return redirect(url_for("output2", final_val={'initial_investment':initial_investment,'withdrawal_amount':withdrawal_amount,'withdrawal_frequency': withdrawal_frequency,'inflation_rate':inflation_rate, 'roi':roi, 'num_withdrawals_until_depleted':final_value}))
    else: 
        return render_template("withdrawals.html")

def calculate_final_value2(initial_investment, withdrawal_amount, withdrawal_frequency, inflation_rate, roi):
    roi = float(roi)/1200

    inflation_rate = float(inflation_rate)/100
    count = int(0)
    withdrawal_amount = float(withdrawal_amount)
    initial_investment1 = float(initial_investment)
    Total_withdrawal = float(0)

    while initial_investment1 > 0:
        initial_investment1 += float(initial_investment) * ((1 + roi) ** float(withdrawal_frequency))
        withdrawal_amount += float(withdrawal_amount) * inflation_rate
        Total_withdrawal += withdrawal_amount
        initial_investment1 -= withdrawal_amount
        count += 1
        if initial_investment1 <= 0:
            break

    #print(count)
    return count

@app.route('/withdrawals/swp/num_until_depleted/<final_val>')
def output2(final_val):
    return jsonify(final_val)


#Endpoint to calculate total withdrawal amount
@app.route('/total_withdrawal', methods=["POST", "GET"])
def total_withdrawal():
    if request.method == "POST":
        data = request.form
        initial_investment = data['initial_investment']
        withdrawal_amount = data['withdrawal_amount']
        withdrawal_frequency = data['withdrawal_frequency']
        inflation_rate = data['inflation_rate']
        roi = data['roi']
        final_value = calculate_final_value3(initial_investment , withdrawal_amount, withdrawal_frequency, inflation_rate, roi)
        return redirect(url_for("output3", final_val={'initial_investment':initial_investment,'withdrawal_amount':withdrawal_amount,'withdrawal_frequency': withdrawal_frequency,'inflation_rate':inflation_rate, 'roi':roi, 'Total_withdrawal':final_value}))
    else: 
        return render_template("total_withdrawal.html")

def calculate_final_value3(initial_investment, withdrawal_amount, withdrawal_frequency, inflation_rate, roi):
    roi = float(roi)/1200

    inflation_rate = float(inflation_rate)/100
    count = int(0)
    withdrawal_amount = float(withdrawal_amount)
    initial_investment1 = float(initial_investment)
    Total_withdrawal = float(0)

    while initial_investment1 > 0:
        initial_investment1 += float(initial_investment) * ((1 + roi) ** float(withdrawal_frequency))
        withdrawal_amount += float(withdrawal_amount) * inflation_rate
        Total_withdrawal += withdrawal_amount
        initial_investment1 -= withdrawal_amount
        count += 1
        if initial_investment1 <= 0:
            break

    #print(count)
    return (round(Total_withdrawal, 2))

@app.route('/withdrawals/swp/total_withdrawn/<final_val>')
def output3(final_val):
    return jsonify(final_val)


if __name__== "__main__":
    app.run(debug = True)