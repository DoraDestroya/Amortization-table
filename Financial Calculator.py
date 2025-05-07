import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math

def calculate_amortization():
    try:
        loan_amount = float(loan_amount_entry.get())
        num_months = int(num_months_entry.get())
        annual_interest_rate = float(annual_interest_rate_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter numeric values.")
        return

    if annual_interest_rate < 0 or loan_amount < 0 or num_months <= 0:
        messagebox.showerror("Error", "Invalid input. Loan amount and interest rate cannot be negative, and the number of months must be positive.")
        return

    monthly_interest_rate = annual_interest_rate / 12
    try:
        monthly_payment = (loan_amount * monthly_interest_rate) / (1 - math.pow(1 + monthly_interest_rate, -num_months))
    except ZeroDivisionError:
        messagebox.showerror("Error", "Invalid input resulting in division by zero. Please check your inputs.")
        return

    # Clear previous table
    for item in table.get_children():
        table.delete(item)

    remaining_balance = loan_amount
    for month in range(1, num_months + 1):
        interest_paid = monthly_interest_rate * remaining_balance
        principal_paid = monthly_payment - interest_paid
        remaining_balance -= principal_paid
        table.insert("", tk.END, values=(month, f"{remaining_balance + principal_paid:.2f}", f"{monthly_payment:.2f}", f"{interest_paid:.2f}", f"{principal_paid:.2f}", f"{remaining_balance:.2f}"))

# Create the main window
root = tk.Tk()
root.title("Real Estate Financial Calculator")

# Input fields
loan_amount_label = tk.Label(root, text="Loan Amount:")
loan_amount_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
loan_amount_entry = tk.Entry(root)
loan_amount_entry.grid(row=0, column=1, padx=5, pady=5)

num_months_label = tk.Label(root, text="Number of Months:")
num_months_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
num_months_entry = tk.Entry(root)
num_months_entry.grid(row=1, column=1, padx=5, pady=5)

annual_interest_rate_label = tk.Label(root, text="Annual Interest Rate (e.g., 0.05):")
annual_interest_rate_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
annual_interest_rate_entry = tk.Entry(root)
annual_interest_rate_entry.grid(row=2, column=1, padx=5, pady=5)

# Calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate_amortization)
calculate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Amortization table display
columns = ("Month", "Beginning Balance", "Monthly Payment", "Interest Paid", "Principal Paid", "Ending Balance")
table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=120)  # Adjust column width as needed

table.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()