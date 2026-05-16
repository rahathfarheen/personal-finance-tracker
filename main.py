import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

print(f"\n{BLUE}🚀 Welcome to Personal Finance Tracker{RESET}\n")

df = pd.read_csv('data.csv')

def show_menu():
    print("\n" + "="*70)
    print(f"{BLUE}🎉 Personal Finance Tracker{RESET}")
    print("=" * 65)
    print(f"{GREEN}1.{RESET} View All Transactions")
    print(f"{GREEN}2.{RESET} Add New Transaction")
    print(f"{GREEN}3.{RESET} View Summary")
    print(f"{GREEN}4.{RESET} Show Expense Pie Chart")
    print(f"{GREEN}5.{RESET}Delete transaction")
    print(f"{GREEN}6.{RESET}Search Transactions")
    print(f"{GREEN}7.{RESET}Monthly Summary")
    print(f"{GREEN}8.{RESET}Bar Chart")
    print(f"{GREEN}9.{RESET}Backup Data")
    print(f"{GREEN}10.{RESET}Exit")

    print("=" * 70)

while True:
    show_menu()
    choice = input(f"\n{YELLOW}Enter your choice (1-10):{RESET}").strip()

    if choice == '1':
        print("\nYour Transactions:")
        print(df.to_string(index=False)) 

    elif choice == '2':
        print("\n--- Add New Transaction ---")
        date = datetime.now().strftime('%d-%m-%Y')
        desc = input("Enter Description: ")
        category = input("Enter Category: ")
        trans_type = input("Enter Type (Income/Expense): ")
        
        try:
            amount = float(input("Enter Amount: "))
            
            # Fixed Add Transaction Code
            new_row = pd.DataFrame([{
                'Date': date,
                'Description': desc,
                'Category': category,
                'Type': trans_type,
                'Amount': amount
            }])
            
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv('data.csv', index=False)
            print(f"\n{GREEN}✅ Transaction added successfully!{RESET}")
            
        except ValueError:
            print("❌ Invalid amount! Please enter a number.")
    
    elif choice == '3':
        income = df[df['Type'] == 'income']['Amount'].sum()
        expense = df[df['Type'] == 'expense']['Amount'].sum()
        balance = income - expense
    
        print("\n=== Financial Summary ===")
        print(f"Total Income    : ₹{income}")
        print(f"Total Expense   : ₹{expense}")
        print(f"Current Balance : ₹{balance}")

    elif choice == '4':
        expense_df = df[df['Type'] == 'expense']
        if not expense_df.empty:
            category_expense = expense_df.groupby('Category')['Amount'].sum()
            plt.figure(figsize=(8, 6))
            plt.pie(category_expense, labels=category_expense.index, autopct='%1.1f%%', startangle=90)
            plt.title('Expense Breakdown by Category')
            plt.axis('equal')
            plt.show()
        else:
            print("No expense data available yet!")
    elif choice == '5':
            print("\nYour Current Transactions:")
            print(df.to_string(index=False))
        
            try:
                index = int(input("\nEnter the Index number to delete: "))
                if 0 <= index < len(df):
                    deleted_row = df.iloc[index]
                    print(f"\nDeleting: {deleted_row['Description']} - ₹{deleted_row['Amount']}")
                    confirm = input("Are you sure? (y/n): ").strip().lower()
                    if confirm == 'y':
                        df = df.drop(index).reset_index(drop=True)
                        df.to_csv('data.csv', index=False)
                        print(f"{GREEN}✅ Transaction deleted successfully!{RESET}")
                    else:
                        print("❌ Deletion cancelled.")
                else:
                    print("❌ Invalid index number!")
            except:
                print("❌ Invalid input! Please enter a number.")
    elif choice == '6':  # Fixed Search
        keyword = input("Enter keyword to search (Description/Category): ").lower()
        result = df[df['Description'].str.lower().str.contains(keyword, na=False) | 
                   df['Category'].str.lower().str.contains(keyword, na=False)]
        print(f"\n{BLUE}Search Results:{RESET}")
        if result.empty:
            print("No matching transactions found.")
        else:
            print(result.to_string(index=False))

    elif choice == '7':  # Fixed Monthly Summary
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
        df['Month'] = df['Date'].dt.strftime('%Y-%m')
        monthly = df.groupby('Month').agg({
            'Amount': 'sum'
        }).rename(columns={'Amount': 'Total'})
        print(f"\n{BLUE}Monthly Summary:{RESET}")
        print(monthly)

    elif choice == '8':  # Fixed Bar Chart
        expense = df[df['Type'] == 'expense'].groupby('Category')['Amount'].sum()
        if not expense.empty:
            expense.plot(kind='bar', figsize=(10, 6), color='skyblue')
            plt.title('Expenses by Category')
            plt.ylabel('Amount (₹)')
            plt.xlabel('Category')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        else:
            print("No expense data available!")

    elif choice == '9':  # Backup
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(backup_name, index=False)
        print(f"{GREEN}✅ Backup created successfully: {backup_name}{RESET}")

    elif choice == '10':
        print(f"\n{GREEN}Thank you for using Personal Finance Tracker! 👋{RESET}")
        break

    else:
        print(f"{RED}❌ Invalid choice! Please enter 1-10.{RESET}")
    
    print(f"\n{YELLOW}Total Transactions: {len(df)} | Current Balance: ₹{(df[df['Type'] == 'income']['Amount'].sum() - df[df['Type'] == 'expense']['Amount'].sum()):.2f}{RESET}")

    input(f"\n{YELLOW}Press Enter to continue...{RESET}")