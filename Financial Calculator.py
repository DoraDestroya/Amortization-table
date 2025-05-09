import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math

# --- Amortization Calculator Function ---
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
    for item in amort_table.get_children():
        amort_table.delete(item)

    remaining_balance = loan_amount
    for month in range(1, num_months + 1):
        interest_paid = monthly_interest_rate * remaining_balance
        principal_paid = monthly_payment - interest_paid
        remaining_balance -= principal_paid
        amort_table.insert("", tk.END, values=(month, f"{remaining_balance + principal_paid:.2f}", f"{monthly_payment:.2f}", f"{interest_paid:.2f}", f"{principal_paid:.2f}", f"{remaining_balance:.2f}"))

# --- NPV Calculator Function ---
def calculate_npv():
    try:
        discount_rate = float(npv_discount_rate_entry.get())
        cash_flows = [float(cf.strip()) for cf in npv_cash_flows_entry.get().split(',')]
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a numeric discount rate and comma-separated cash flows.")
        return

    if discount_rate < 0:
        messagebox.showerror("Error", "Discount rate cannot be negative.")
        return

    npv = 0
    for t, cf in enumerate(cash_flows):
        npv += cf / ((1 + discount_rate) ** t)
    npv_result_var.set(f"NPV: {npv:.2f}")

# --- Main Window and Notebook ---
root = tk.Tk()
root.title("Real Estate Financial Calculator")

notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=5, pady=5)

# --- Amortization Tab ---
amort_frame = ttk.Frame(notebook)
notebook.add(amort_frame, text="Amortization")

loan_amount_label = tk.Label(amort_frame, text="Loan Amount:")
loan_amount_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
loan_amount_entry = tk.Entry(amort_frame)
loan_amount_entry.grid(row=0, column=1, padx=5, pady=5)

num_months_label = tk.Label(amort_frame, text="Number of Months:")
num_months_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
num_months_entry = tk.Entry(amort_frame)
num_months_entry.grid(row=1, column=1, padx=5, pady=5)

annual_interest_rate_label = tk.Label(amort_frame, text="Annual Interest Rate (e.g., 0.05):")
amort_frame.grid_columnconfigure(0, weight=1)
amort_frame.grid_columnconfigure(1, weight=1)
annual_interest_rate_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
annual_interest_rate_entry = tk.Entry(amort_frame)
annual_interest_rate_entry.grid(row=2, column=1, padx=5, pady=5)

calculate_button = tk.Button(amort_frame, text="Calculate", command=calculate_amortization)
calculate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

columns = ("Month", "Beginning Balance", "Monthly Payment", "Interest Paid", "Principal Paid", "Ending Balance")
amort_table = ttk.Treeview(amort_frame, columns=columns, show="headings")
for col in columns:
    amort_table.heading(col, text=col)
    amort_table.column(col, width=120)
amort_table.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# --- NPV Tab ---
npv_frame = ttk.Frame(notebook)
notebook.add(npv_frame, text="Net Present Value")

npv_discount_rate_label = tk.Label(npv_frame, text="Discount Rate (e.g., 0.05):")
npv_discount_rate_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
npv_discount_rate_entry = tk.Entry(npv_frame)
npv_discount_rate_entry.grid(row=0, column=1, padx=5, pady=5)

npv_cash_flows_label = tk.Label(npv_frame, text="Cash Flows (comma-separated):")
npv_cash_flows_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
npv_cash_flows_entry = tk.Entry(npv_frame, width=40)
npv_cash_flows_entry.grid(row=1, column=1, padx=5, pady=5)

npv_result_var = tk.StringVar()
npv_result_label = tk.Label(npv_frame, textvariable=npv_result_var, font=("Arial", 12, "bold"))
npv_result_label.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

npv_calculate_button = tk.Button(npv_frame, text="Calculate NPV", command=calculate_npv)
npv_calculate_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

root.mainloop()