import datetime
import random 

accounts = {}

generated_account_numbers = set()


bank_Code = "500"
branch_codes = {
    "001": "Jaffna Branch",
    "002": "Colombo Branch",
    "003": "Kandy Branch",
    "004": "Galle Branch"
}

# --- Core Functions ---

def generate_unique_account_number(selected_branch_code):
    """Generates a unique account number based on branch and a random sequence."""
    while True:
        # Generate a random 6-digit customer number for more uniqueness
        customer_number = str(random.randint(100000, 999999))
        full_account_number = f"{bank_Code}{selected_branch_code}{customer_number}"
        # Ensure the generated number hasn't been used before
        if full_account_number not in generated_account_numbers:
            generated_account_numbers.add(full_account_number)
            return full_account_number

def get_branch_name(branch_code):
    """Retrieves the branch name from the branch_codes dictionary."""
    return branch_codes.get(branch_code, "Unknown Branch") # Use .get for safety

def record_transaction(account_number, transaction_type, amount):
    """Adds a transaction record to the specified account."""
    if account_number in accounts:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction = {
            "timestamp": timestamp,
            "type": transaction_type,
            "amount": amount,
            "balance_after": accounts[account_number]["balance"] # Record balance *after* the transaction
        }
        accounts[account_number]["transactions"].append(transaction)
    # No else needed, as this is called after confirming account exists

def create_account():
    """Handles the creation of a new bank account."""
    print("\n--- Create New Account ---")
    print("Available Branches:")
    for code, name in branch_codes.items():
        print(f"  {code}: {name}")

    selected_branch_code = input("Enter the branch code: ")
    if selected_branch_code not in branch_codes:
        print("Error: Invalid branch code.")
        return

    name = input("Enter account holder name: ")
    if not name.strip(): # Basic validation for name
        print("Error: Account holder name cannot be empty.")
        return

    try:
        initial_balance = float(input("Enter initial deposit amount: "))
        if initial_balance < 0:
            print("Error: Initial deposit cannot be negative.")
            return
    except ValueError:
        print("Error: Invalid amount entered. Please enter a number.")
        return

    # Generate unique account number
    account_number = generate_unique_account_number(selected_branch_code)

    # Store account details
    accounts[account_number] = {
        "name": name,
        "balance": initial_balance,
        "transactions": [] # Initialize empty transaction list
        
    }

    # Record the initial deposit as the first transaction
    if initial_balance > 0:
         # Manually add initial deposit transaction *after* setting balance
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        initial_transaction = {
            "timestamp": timestamp,
            "type": "initial deposit",
            "amount": initial_balance,
            "balance_after": initial_balance
        }
        accounts[account_number]["transactions"].append(initial_transaction)


    print("-" * 20)
    print(f"Account created successfully!")
    print(f"Account Number: {account_number}")
    print(f"Account Holder: {name}")
    print(f"Initial Balance: {initial_balance:.2f}")
    print("-" * 20)


def deposit_money():
    """Handles depositing money into an existing account."""

    print("\n--- Deposit Money ---")
    account_number = input("Enter account number: ")

    if account_number not in accounts:
        print("Error: Account not found.")
        return
    is_correct_amount = False
    

    try:
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print("Error: Deposit amount must be positive.")
            return
    except ValueError:
        print("Error: Invalid amount entered. Please enter a number.")
        return

    # Update balance
    accounts[account_number]["balance"] += amount
    new_balance = accounts[account_number]["balance"]

    # Record transaction
    record_transaction(account_number, "deposit", amount)

    print(f"Deposit successful.")
    print(f"New balance for account {account_number}: {new_balance:.2f}")

def withdraw_money():
    """Handles withdrawing money from an existing account."""
    print("\n--- Withdraw Money ---")
    account_number = input("Enter account number: ")

    if account_number not in accounts:
        print("Error: Account not found.")
        return

    try:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0:
            print("Error: Withdrawal amount must be positive.")
            return
    except ValueError:
        print("Error: Invalid amount entered. Please enter a number.")
        return

    # Check sufficient funds
    if accounts[account_number]["balance"] < amount:
        print("Error: Insufficient funds.")
        print(f"Available balance: {accounts[account_number]['balance']:.2f}")
        return

    # Update balance
    accounts[account_number]["balance"] -= amount
    new_balance = accounts[account_number]["balance"]

    # Record transaction
    record_transaction(account_number, "withdrawal", amount)

    print(f"Withdrawal successful.")
    print(f"New balance for account {account_number}: {new_balance:.2f}")

def check_balance():
    """Displays the current balance of an account."""
    print("\n--- Check Balance ---")
    account_number = input("Enter account number: ")

    if account_number in accounts:
        balance = accounts[account_number]["balance"]
        print(f"Current balance for account {account_number}: {balance:.2f}")
    else:
        print("Error: Account not found.")

def view_transaction_history():
    """Displays the transaction history for an account."""
    print("\n--- Transaction History ---")
    account_number = input("Enter account number: ")

    if account_number in accounts:
        transactions = accounts[account_number]["transactions"]
        print(f"\nTransaction History for Account: {account_number}")
        print(f"Account Holder: {accounts[account_number]['name']}")
        print("-" * 60)
        if not transactions:
            print("No transactions found for this account.")
        else:
            print(f"{'Timestamp':<20} | {'Type':<15} | {'Amount':<10} | {'Balance After':<15}")
            print("-" * 60)
            for tx in transactions:
                print(f"{tx['timestamp']:<20} | {tx['type'].title():<15} | {tx['amount']:<10.2f} | {tx['balance_after']:<15.2f}")
        print("-" * 60)
    else:
        print("Error: Account not found.")

# --- Menu and Main Loop ---

def display_menu():
    """Prints the main menu options."""
    print("\n===== Simple Banking System =====")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Check Balance")
    print("5. Transaction History")
    print("6. Exit")
    print("================================")

def main():
    """Main function to run the banking system."""
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            create_account()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            view_transaction_history()
        elif choice == '6':
            print("Exiting the banking system. Goodbye!")
            break # Exit the while loop
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

        input("\nPress Enter to continue...") # Pause for user to read output

    main()
