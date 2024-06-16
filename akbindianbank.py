from datetime import datetime

class BankAccount:
    def __init__(self, name, pin, balance=0):
        self.name = name
        self.pin = pin
        self.balance = balance
        self.transactions = []  # To keep a record of transactions
        self.beneficiaries = {}  # To store beneficiary accounts
        self.beneficiary_nicknames = {}  # To store beneficiary nicknames
        self.overdraft_limit = 0
        self.frozen = False
        self.savings_goal = 0
        self.contact_info = ""
        self.transaction_limit = None
        self.online_banking_enabled = True
        self.sms_alerts_enabled = True
        self.cheque_book_ordered = False
        self.card_reported_lost = False
        self.loan_application_status = "None"
        self.spending_alert_limit = None
        self.two_factor_enabled = False
        self.low_balance_alert_threshold = None
        self.debit_card_blocked = False

    def verify_pin(self, input_pin):
        return self.pin == input_pin

    def deposit(self, amount):
        if self.frozen:
            print("Account is frozen. Cannot deposit funds.")
            return
        if amount > 0:
            self.balance += amount
            self.transactions.append((datetime.now(), f"Deposited ₹{amount}"))
            print(f"Deposited ₹{amount}. New Balance: ₹{self.balance}")
            self.check_spending_alert(amount)
        else:
            print("Invalid amount for deposit.")

    def withdraw(self, amount):
        if self.frozen:
            print("Account is frozen. Cannot withdraw funds.")
            return
        if self.debit_card_blocked:
            print("Debit card is blocked. Cannot withdraw funds.")
            return
        if self.transaction_limit and amount > self.transaction_limit:
            print(f"Transaction limit exceeded. Your limit is ₹{self.transaction_limit}")
            return
        if 0 < amount <= self.balance + self.overdraft_limit:
            self.balance -= amount
            self.transactions.append((datetime.now(), f"Withdrew ₹{amount}"))
            print(f"Withdrew ₹{amount}. New Balance: ₹{self.balance}")
            self.check_spending_alert(amount)
            self.check_low_balance_alert()
        else:
            print("Insufficient funds.")

    def transfer(self, amount, other_account):
        if self.frozen:
            print("Account is frozen. Cannot transfer funds.")
            return
        if self.debit_card_blocked:
            print("Debit card is blocked. Cannot transfer funds.")
            return
        if 0 < amount <= self.balance + self.overdraft_limit:
            self.balance -= amount
            other_account.balance += amount
            self.transactions.append((datetime.now(), f"Transferred ₹{amount} to {other_account.name}"))
            print(f"Transferred ₹{amount} to {other_account.name}. New Balance: ₹{self.balance}")
            self.check_spending_alert(amount)
            self.check_low_balance_alert()
        else:
            print("Insufficient funds for transfer.")

    def get_balance(self):
        return self.balance

    def view_account_details(self):
        return str(self)

    def add_beneficiary(self, beneficiary_name, beneficiary_account, nickname=None):
        self.beneficiaries[beneficiary_name] = beneficiary_account
        if nickname:
            self.beneficiary_nicknames[beneficiary_name] = nickname
        self.transactions.append((datetime.now(), f"Added beneficiary {beneficiary_name}"))
        print(f"Beneficiary {beneficiary_name} added.")

    def remove_beneficiary(self, beneficiary_name):
        if beneficiary_name in self.beneficiaries:
            del self.beneficiaries[beneficiary_name]
            if beneficiary_name in self.beneficiary_nicknames:
                del self.beneficiary_nicknames[beneficiary_name]
            self.transactions.append((datetime.now(), f"Removed beneficiary {beneficiary_name}"))
            print(f"Beneficiary {beneficiary_name} removed.")
        else:
            print("Beneficiary not found.")

    def set_beneficiary_nickname(self, beneficiary_name, nickname):
        if beneficiary_name in self.beneficiaries:
            self.beneficiary_nicknames[beneficiary_name] = nickname
            self.transactions.append((datetime.now(), f"Set nickname for beneficiary {beneficiary_name} to {nickname}"))
            print(f"Nickname for beneficiary {beneficiary_name} set to {nickname}.")
        else:
            print("Beneficiary not found.")

    def freeze_account(self):
        self.frozen = True
        self.transactions.append((datetime.now(), "Account frozen"))
        print("Account has been frozen.")

    def unfreeze_account(self):
        self.frozen = False
        self.transactions.append((datetime.now(), "Account unfrozen"))
        print("Account has been unfrozen.")

    def view_transaction_history_by_date(self, date):
        print(f"Transactions for {date}:")
        for txn_date, txn in self.transactions:
            if txn_date.date() == date:
                print(f"{txn_date} - {txn}")

    def print_account_statement(self):
        print(f"Account Statement for {self.name}:")
        for txn_date, txn in self.transactions:
            print(f"{txn_date} - {txn}")

    def request_account_statement_via_email(self, email):
        self.transactions.append((datetime.now(), f"Requested account statement to be sent to {email}"))
        print(f"Account statement will be sent to {email}.")

    def set_spending_alerts(self, limit):
        self.spending_alert_limit = limit
        self.transactions.append((datetime.now(), f"Set spending alert limit to ₹{limit}"))
        print(f"Spending alert limit set to ₹{limit}")

    def check_spending_alert(self, amount):
        if self.spending_alert_limit and amount > self.spending_alert_limit:
            print(f"Alert: You have spent ₹{amount}, which is above your set limit of ₹{self.spending_alert_limit}.")

    def enable_two_factor_authentication(self):
        self.two_factor_enabled = True
        self.transactions.append((datetime.now(), "Enabled two-factor authentication"))
        print("Two-factor authentication enabled.")

    def disable_two_factor_authentication(self):
        self.two_factor_enabled = False
        self.transactions.append((datetime.now(), "Disabled two-factor authentication"))
        print("Two-factor authentication disabled.")

    def view_recent_transactions(self, count=5):
        print(f"Last {count} transactions:")
        for txn_date, txn in self.transactions[-count:]:
            print(f"{txn_date} - {txn}")

    def update_contact_info(self, new_contact_info):
        old_contact_info = self.contact_info
        self.contact_info = new_contact_info
        self.transactions.append((datetime.now(), "Updated contact information"))
        print(f"Contact information updated from {old_contact_info} to {new_contact_info}")

    def change_account_pin(self, new_pin):
        self.pin = new_pin
        self.transactions.append((datetime.now(), "Changed account PIN"))
        print("Account PIN changed successfully.")

    def enable_sms_alerts(self):
        self.sms_alerts_enabled = True
        self.transactions.append((datetime.now(), "Enabled SMS alerts"))
        print("SMS alerts enabled.")

    def disable_sms_alerts(self):
        self.sms_alerts_enabled = False
        self.transactions.append((datetime.now(), "Disabled SMS alerts"))
        print("SMS alerts disabled.")

    def view_account_holder_profile(self):
        print(f"Account holder profile: Name: {self.name}, Contact Info: {self.contact_info}, Balance: ₹{self.balance}")

    def set_transaction_limit(self, limit):
        self.transaction_limit = limit
        self.transactions.append((datetime.now(), f"Set transaction limit: ₹{limit}"))
        print(f"Transaction limit set to ₹{limit}")

    def check_transaction_limit(self):
        if self.transaction_limit is not None:
            print(f"Your transaction limit is ₹{self.transaction_limit}")
        else:
            print("No transaction limit set.")

    def enable_online_banking(self):
        self.online_banking_enabled = True
        self.transactions.append((datetime.now(), "Enabled online banking"))
        print("Online banking enabled.")

    def disable_online_banking(self):
        self.online_banking_enabled = False
        self.transactions.append((datetime.now(), "Disabled online banking"))
        print("Online banking disabled.")

    def order_cheque_book(self):
        self.cheque_book_ordered = True
        self.transactions.append((datetime.now(), "Ordered cheque book"))
        print("Cheque book ordered successfully.")

    def report_lost_card(self):
        self.card_reported_lost = True
        self.transactions.append((datetime.now(), "Reported lost/stolen card"))
        print("Card reported lost/stolen. A new card will be issued.")

    def apply_for_loan(self, amount):
        self.loan_application_status = "Pending"
        self.transactions.append((datetime.now(), f"Applied for loan: ₹{amount}"))
        print(f"Loan application for ₹{amount} is pending approval.")

    def set_low_balance_alert(self, threshold):
        self.low_balance_alert_threshold = threshold
        self.transactions.append((datetime.now(), f"Set low balance alert threshold to ₹{threshold}"))
        print(f"Low balance alert threshold set to ₹{threshold}")

    def check_low_balance_alert(self):
        if self.low_balance_alert_threshold and self.balance < self.low_balance_alert_threshold:
            print(f"Alert: Your balance is below the set threshold of ₹{self.low_balance_alert_threshold}. Current balance: ₹{self.balance}")

    def block_debit_card(self):
        self.debit_card_blocked = True
        self.transactions.append((datetime.now(), "Blocked debit card"))
        print("Debit card has been blocked.")

    def unblock_debit_card(self):
        self.debit_card_blocked = False
        self.transactions.append((datetime.now(), "Unblocked debit card"))
        print("Debit card has been unblocked.")

    def __str__(self):
        return f"Account holder: {self.name}, Balance: ₹{self.balance}, Contact Info: {self.contact_info}"

def main():
    print("Welcome to the AKB Indian Bank")
    print("Create an account to get started.")
    
    name = input("Enter your name: ")
    pin = input("Create a new PIN: ")
    initial_balance = float(input("Enter initial deposit amount: ₹"))
    account = BankAccount(name, pin, initial_balance)
    
    print(f"Account created successfully! Name: {account.name}, Initial Balance: ₹{account.balance}")
    
    while True:
        input_pin = input("Enter your PIN to continue: ")
        if account.verify_pin(input_pin):
            print("\n1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. Transfer")
            print("5. View Account Details")
            print("6. Add Beneficiary")
            print("7. Remove Beneficiary")
            print("8. Freeze Account")
            print("9. Unfreeze Account")
            print("10. View Transaction History by Date")
            print("11. Print Account Statement")
            print("12. Request Account Statement via Email")
            print("13. Set Spending Alerts")
            print("14. View Recent Transactions")
            print("15. Update Contact Information")
            print("16. Change Account PIN")
            print("17. Enable Two-Factor Authentication")
            print("18. Disable Two-Factor Authentication")
            print("19. View Account Holder's Profile")
            print("20. Set Transaction Limit")
            print("21. Check Transaction Limit")
            print("22. Enable Online Banking")
            print("23. Disable Online Banking")
            print("24. Order Cheque Book")
            print("25. Report Lost/Stolen Card")
            print("26. Apply for Loan")
            print("27. Set Low Balance Alert")
            print("28. Block Debit Card")
            print("29. Unblock Debit Card")
            print("30. Set Beneficiary Nickname")
            print("31. Exit")
            
            choice = input("Enter your choice: ")

            if not account.verify_pin(input_pin):
                print("Incorrect PIN. Please try again.")
                continue
            
            if choice == '1':
                amount = float(input("Enter deposit amount: ₹"))
                account.deposit(amount)
            elif choice == '2':
                amount = float(input("Enter withdrawal amount: ₹"))
                account.withdraw(amount)
            elif choice == '3':
                print(f"Your balance: ₹{account.get_balance()}")
            elif choice == '4':
                other_name = input("Enter the recipient's name: ")
                if other_name in account.beneficiaries:
                    other_account = account.beneficiaries[other_name]
                    amount = float(input("Enter transfer amount: ₹"))
                    account.transfer(amount, other_account)
                else:
                    print("Beneficiary not found. Please add the beneficiary first.")
            elif choice == '5':
                print(account.view_account_details())
            elif choice == '6':
                beneficiary_name = input("Enter the beneficiary's name: ")
                beneficiary_initial_balance = 0  # Assuming new account with zero balance for simplicity
                beneficiary_account = BankAccount(beneficiary_name, pin)
                nickname = input("Enter a nickname for the beneficiary (optional): ")
                account.add_beneficiary(beneficiary_name, beneficiary_account, nickname)
            elif choice == '7':
                beneficiary_name = input("Enter the beneficiary's name to remove: ")
                account.remove_beneficiary(beneficiary_name)
            elif choice == '8':
                account.freeze_account()
            elif choice == '9':
                account.unfreeze_account()
            elif choice == '10':
                date_str = input("Enter the date (YYYY-MM-DD): ")
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                account.view_transaction_history_by_date(date)
            elif choice == '11':
                account.print_account_statement()
            elif choice == '12':
                email = input("Enter the email to receive the account statement: ")
                account.request_account_statement_via_email(email)
            elif choice == '13':
                limit = float(input("Enter spending alert limit: ₹"))
                account.set_spending_alerts(limit)
            elif choice == '14':
                count = int(input("Enter the number of recent transactions to view: "))
                account.view_recent_transactions(count)
            elif choice == '15':
                new_contact_info = input("Enter new contact information: ")
                account.update_contact_info(new_contact_info)
            elif choice == '16':
                new_pin = input("Enter new PIN: ")
                account.change_account_pin(new_pin)
            elif choice == '17':
                account.enable_two_factor_authentication()
            elif choice == '18':
                account.disable_two_factor_authentication()
            elif choice == '19':
                account.view_account_holder_profile()
            elif choice == '20':
                limit = float(input("Enter transaction limit: ₹"))
                account.set_transaction_limit(limit)
            elif choice == '21':
                account.check_transaction_limit()
            elif choice == '22':
                account.enable_online_banking()
            elif choice == '23':
                account.disable_online_banking()
            elif choice == '24':
                account.order_cheque_book()
            elif choice == '25':
                account.report_lost_card()
            elif choice == '26':
                amount = float(input("Enter loan amount: ₹"))
                account.apply_for_loan(amount)
            elif choice == '27':
                threshold = float(input("Enter low balance alert threshold: ₹"))
                account.set_low_balance_alert(threshold)
            elif choice == '28':
                account.block_debit_card()
            elif choice == '29':
                account.unblock_debit_card()
            elif choice == '30':
                beneficiary_name = input("Enter the beneficiary's name: ")
                nickname = input("Enter the new nickname for the beneficiary: ")
                account.set_beneficiary_nickname(beneficiary_name, nickname)
            elif choice == '31':
                print("Thank you for banking with us!")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            print("Incorrect PIN. Please try again.")

if __name__ == "__main__":
    main()
