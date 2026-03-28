import random

customers = {
    "1001": {
        "fullname": "Sample User",
        "age": "20",
        "password": "1234",
        "balance": 1000,
        "history": []
    }
}

def generate_unique_id():
    while True:
        uid = str(random.randint(1000, 9999))
        if uid not in customers:
            return uid

def register_customer(fullname, password, age):
    user_id = generate_unique_id()
    customers[user_id] = {
        "fullname": fullname,
        "age": age,
        "password": password,
        "balance": 0,
        "history": []
    }
    return user_id

def check_login(user_id, password):
    return user_id in customers and customers[user_id]["password"] == password

def get_balance(user_id):
    return customers[user_id]["balance"]

def deposit(user_id, amount):
    customers[user_id]["balance"] += amount
    customers[user_id]["history"].append(f"Deposited ₱{amount}")

def withdraw(user_id, amount):
    if amount <= customers[user_id]["balance"]:
        customers[user_id]["balance"] -= amount
        customers[user_id]["history"].append(f"Withdrew ₱{amount}")
        return True
    return False

def transfer(sender_id, recipient_id, amount):
    if recipient_id in customers and amount <= customers[sender_id]["balance"]:
        customers[sender_id]["balance"] -= amount
        customers[recipient_id]["balance"] += amount
        customers[sender_id]["history"].append(
            f"Transferred ₱{amount} to {customers[recipient_id]['fullname']} (ID: {recipient_id})"
        )
        customers[recipient_id]["history"].append(
            f"Received ₱{amount} from {customers[sender_id]['fullname']} (ID: {sender_id})"
        )
        return True
    return False

def get_history(user_id):
    return customers[user_id]["history"]
    