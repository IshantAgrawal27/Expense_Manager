import json
import os
import csv
import datetime

class ExpenseManager:
    def __init__(self, filename="expense_data.json"):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        default_data = {
            "balance": 0.0, 
            "transactions": [], 
            "assets": [],       
            "liabilities": []   
        }
        
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                loaded_data = json.load(file)
                if "assets" not in loaded_data: loaded_data["assets"] = []
                if "liabilities" not in loaded_data: loaded_data["liabilities"] = []
                if "debts" in loaded_data:
                    loaded_data["assets"] = loaded_data.pop("debts")
                return loaded_data
        else:
            return default_data

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    # --- CORE FUNCTIONS ---
    def add_transaction(self, amount, category, t_type):
        if t_type == "income":
            self.data["balance"] += amount
        elif t_type == "expense":
            self.data["balance"] -= amount

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction = {
            "date": timestamp,
            "type": t_type,
            "amount": amount,
            "category": category
        }
        self.data["transactions"].append(transaction)
        self.save_data()
        print(f"\n✅ Recorded {t_type}: ₹{amount} ({category})")

    def get_monthly_stats(self):
        total_income = sum(t['amount'] for t in self.data['transactions'] if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in self.data['transactions'] if t['type'] == 'expense')
        cashflow = total_income - total_expense
        return total_income, total_expense, cashflow

    def view_detailed_history(self):
        print("\n" + "="*40)
        print(" 📜 INCOME & EXPENSE HISTORY")
        print("="*40)

        print("\n🟢 INCOME CASHFLOW")
        print(f"{'Date':<20} | {'Source':<15} | {'Amount (₹)'}")
        print("-" * 50)
        total_inc = 0
        for t in self.data['transactions']:
            if t['type'] == 'income':
                print(f"{t['date']:<20} | {t['category']:<15} | ₹{t['amount']}")
                total_inc += t['amount']
        print("-" * 50)
        print(f"💰 TOTAL INCOME: ₹{total_inc}")

        print("\n\n🔴 EXPENSE CASHFLOW")
        print(f"{'Date':<20} | {'Category':<15} | {'Amount (₹)'}")
        print("-" * 50)
        total_exp = 0
        for t in self.data['transactions']:
            if t['type'] == 'expense':
                print(f"{t['date']:<20} | {t['category']:<15} | ₹{t['amount']}")
                total_exp += t['amount']
        print("-" * 50)
        print(f"💸 TOTAL EXPENSE: ₹{total_exp}")
        print("="*40)

    # --- NET WORTH CALCULATION ---
    def show_net_worth(self):
        wallet = self.data['balance']
        total_assets = sum(p['amount'] for p in self.data['assets'])
        total_liabilities = sum(p['amount'] for p in self.data['liabilities'])
        net_worth = wallet + total_assets - total_liabilities

        print("\n" + "="*40)
        print(" 💎 YOUR ACTUAL NET WORTH")
        print("="*40)
        print(f"💵 Wallet Balance:         ₹ {wallet:,.2f}")
        print(f"➕ Money Lended (Assets):   ₹ {total_assets:,.2f}")
        print(f"➖ Money Borrowed (Debt):   ₹ {total_liabilities:,.2f}")
        print("-" * 40)
        
        if net_worth >= 0:
            print(f"✅ ACTUAL VALUE:           ₹ {net_worth:,.2f}")
        else:
            print(f"⚠️ ACTUAL VALUE:           -₹ {abs(net_worth):,.2f} (In Debt)")
        print("="*40)

    # --- LENDING ---
    def lend_money(self, name, amount):
        self.add_transaction(amount, f"Lent to {name}", "expense")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        found = False
        for person in self.data["assets"]:
            if person["name"].lower() == name.lower():
                person["amount"] += amount
                person["date"] = timestamp
                found = True
                break
        if not found:
            self.data["assets"].append({"name": name, "amount": amount, "date": timestamp})
        self.save_data()

    def receive_repayment(self, name, amount):
        found = False
        for person in self.data["assets"]:
            if person["name"].lower() == name.lower():
                if amount > person["amount"]:
                    print(f"❌ Error: They only owe you ₹{person['amount']}.")
                    return
                self.add_transaction(amount, f"Repayment from {name}", "income")
                person["amount"] -= amount
                if person["amount"] <= 0:
                    self.data["assets"].remove(person)
                    print(f"🎉 {name} has fully paid you back!")
                else:
                    print(f"✅ Balance updated. They still owe ₹{person['amount']}.")
                self.save_data()
                return
        if not found: print(f"❌ Error: {name} is not in your lending list.")

    # --- BORROWING ---
    def borrow_money(self, name, amount):
        self.add_transaction(amount, f"Borrowed from {name}", "income")
        found = False
        for person in self.data["liabilities"]:
            if person["name"].lower() == name.lower():
                person["amount"] += amount
                found = True
                break
        if not found:
            self.data["liabilities"].append({"name": name, "amount": amount})
        self.save_data()
        print(f"⚠️  You now owe {name} ₹{amount}.")

    def return_money(self, name, amount):
        found = False
        for person in self.data["liabilities"]:
            if person["name"].lower() == name.lower():
                if amount > person["amount"]:
                    print(f"❌ Error: You only owe {name} ₹{person['amount']}.")
                    return
                
                self.add_transaction(amount, f"Returned to {name}", "expense")
                person["amount"] -= amount
                
                if person["amount"] <= 0:
                    self.data["liabilities"].remove(person)
                    print(f"🎉 Great! You have paid off {name}.")
                else:
                    print(f"✅ Payment recorded. You still owe {name} ₹{person['amount']}.")
                self.save_data()
                return
        if not found: print(f"❌ Error: You don't have a record of owing {name}.")

    # --- EXPORT & RESET ---
    def export_to_csv(self):
        if not self.data['transactions']:
            print("⚠️ No data to export.")
            return
        filename = "expense_report.csv"
        try:
            # FIX APPLIED HERE: encoding='utf-8' added
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Type", "Category", "Amount (₹)"])
                for t in self.data['transactions']:
                    date_str = t.get('date', 'N/A')
                    writer.writerow([date_str, t['type'].title(), t['category'], t['amount']])
            print(f"\n✅ Data exported to '{filename}'")
        except PermissionError: print(f"\n❌ Error: Close the CSV file first.")

    def reset_data(self):
        self.data = {"balance": 0.0, "transactions": [], "assets": [], "liabilities": []}
        self.save_data()
        print("\n⚠️  All data has been reset to 0.")


# --- MAIN MENU UI ---
def main():
    manager = ExpenseManager()
    while True:
        print("\n" + "="*35)
        print(" 💰 FINAL EXPENSE MANAGER")
        print("="*35)
        
        income, expense, cashflow = manager.get_monthly_stats()
        print(f"💵 Wallet Balance:  ₹{manager.data['balance']:.2f}")
        print(f"📊 Net Cashflow:    ₹{cashflow:.2f}")
        print("-" * 35)

        print("1. Add Income")
        print("2. Add Expense")
        print("3. View History (Income vs Expense)")
        print("4. 🟢 Lending (People owe ME)")
        print("5. 🔴 Borrowing (I owe PEOPLE)")
        print("6. Export to Excel")
        print("7. Reset Data")
        print("8. Exit")
        print("9. 💎 View Actual Value (Net Worth)")
        
        choice = input("\nSelect Option (1-9): ")

        if choice == '1':
            try:
                amt = float(input("Amount (₹): "))
                cat = input("Source: ")
                manager.add_transaction(amt, cat, "income")
            except ValueError: print("❌ Invalid number.")

        elif choice == '2':
            try:
                amt = float(input("Amount (₹): "))
                cat = input("Category: ")
                manager.add_transaction(amt, cat, "expense")
            except ValueError: print("❌ Invalid number.")

        elif choice == '3': manager.view_detailed_history()

        elif choice == '4':
            print("\n--- 🟢 PEOPLE WHO OWE ME ---")
            if not manager.data['assets']: print("  (No active loans)")
            for p in manager.data['assets']: 
                date_str = p.get('date', 'N/A')
                print(f"  📅 {date_str} | 👤 {p['name']}: ₹{p['amount']}")
            print("-" * 20)
            print("1. Lend Money")
            print("2. Mark as Paid")
            print("3. Back")
            sub = input("Select: ")
            if sub == '1':
                n = input("Name: "); a = float(input("Amount: "))
                manager.lend_money(n, a)
            elif sub == '2':
                n = input("Name: "); a = float(input("Amount: "))
                manager.receive_repayment(n, a)

        elif choice == '5':
            print("\n--- 🔴 PEOPLE I OWE ---")
            if not manager.data['liabilities']: print("  (You are debt-free!)")
            for p in manager.data['liabilities']: print(f"  👤 {p['name']}: ₹{p['amount']}")
            print("-" * 20)
            print("1. Borrow Money")
            print("2. Return Money")
            print("3. Back")
            sub = input("Select: ")
            if sub == '1':
                n = input("Name: "); a = float(input("Amount: "))
                manager.borrow_money(n, a)
            elif sub == '2':
                n = input("Name: "); a = float(input("Amount: "))
                manager.return_money(n, a)

        elif choice == '6': manager.export_to_csv()
        elif choice == '7':
             if input("Confirm reset? (y/n): ").lower() == 'y': manager.reset_data()
        elif choice == '8': break
        
        elif choice == '9':
            manager.show_net_worth()

if __name__ == "__main__":
    main()