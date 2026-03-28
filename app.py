from flask import Flask, render_template, request, redirect, url_for
from TransacNowMain import customers, register_customer, check_login, deposit, withdraw, transfer, get_balance, get_history

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        
        if check_login(user_id, password):
            return redirect(url_for('dashboard', user_id=user_id))
        else:
            message = "Wrong password or ID. Please try again."
            
    return render_template('index.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == 'POST':
        fullname = request.form['fullname']
        password = request.form['password']
        age = request.form['age']
        
        user_id = register_customer(fullname, password, age)
        message = f"Account created! Your User ID is {user_id}"
        
    return render_template('register.html', message=message)

@app.route('/dashboard/<user_id>', methods=['GET', 'POST'])
def dashboard(user_id):
    user = customers[user_id]
    message = ""
    
    if request.method == 'POST':
        action = request.form['action']
        
        # Safe conversion for amount
        try:
            amount = float(request.form.get('amount', 0))
        except ValueError:
            amount = 0
            
        target = request.form.get('target', None)
        
        if action == 'deposit':
            deposit(user_id, amount)
            message = f"Deposited ₱{amount}"
        elif action == 'withdraw':
            if withdraw(user_id, amount):
                message = f"Withdrew ₱{amount}"
            else:
                message = "Insufficient balance"
        elif action == 'transfer' and target:
            if transfer(user_id, target, amount):
                message = f"Transferred ₱{amount} to {target}"
            else:
                message = "Transfer failed. Check recipient ID or balance."
    
    balance = get_balance(user_id)
    history = get_history(user_id)
    
    return render_template('dashboard.html', user=user, balance=balance, history=history, message=message)

if __name__ == '__main__':
    app.run(debug=True)
