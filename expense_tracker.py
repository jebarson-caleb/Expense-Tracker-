import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import json
import os
from tkcalendar import DateEntry  # Requires pip install tkcalendar


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("1000x600")

        # Initialize variables
        self.expenses = []
        self.categories = [
            "Food", "Transportation", "Housing", "Utilities",
            "Entertainment", "Healthcare", "Education", "Shopping",
            "Other"
        ]

        # Create data file if it doesn't exist
        self.data_file = "expenses.json"
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump([], f)

        # Load existing data
        self.load_data()

        # Create GUI
        self.create_widgets()

    def create_widgets(self):
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Add Expense Tab
        self.add_expense_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_expense_frame, text="Add Expense")
        self.create_add_expense_tab()

        # View Expenses Tab
        self.view_expenses_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.view_expenses_frame, text="View Expenses")
        self.create_view_expenses_tab()

        # Statistics Tab
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Statistics")
        self.create_stats_tab()

    def create_add_expense_tab(self):
        # Date
        ttk.Label(self.add_expense_frame, text="Date:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.date_entry = DateEntry(self.add_expense_frame, date_pattern='y-mm-dd')
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.date_entry.set_date(date.today())

        # Category
        ttk.Label(self.add_expense_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(
            self.add_expense_frame,
            textvariable=self.category_var,
            values=self.categories
        )
        self.category_combobox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.category_combobox.current(0)

        # Amount
        ttk.Label(self.add_expense_frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.amount_var = tk.DoubleVar()
        self.amount_entry = ttk.Entry(self.add_expense_frame, textvariable=self.amount_var)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # Description
        ttk.Label(self.add_expense_frame, text="Description:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.description_var = tk.StringVar()
        self.description_entry = ttk.Entry(
            self.add_expense_frame,
            textvariable=self.description_var,
            width=40
        )
        self.description_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        # Add Button
        self.add_button = ttk.Button(
            self.add_expense_frame,
            text="Add Expense",
            command=self.add_expense
        )
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_view_expenses_tab(self):
        # Filter Frame
        filter_frame = ttk.Frame(self.view_expenses_frame)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)

        # Date Range Filter
        ttk.Label(filter_frame, text="From:").grid(row=0, column=0, padx=5, pady=5)
        self.from_date = DateEntry(filter_frame, date_pattern='y-mm-dd')
        self.from_date.grid(row=0, column=1, padx=5, pady=5)
        self.from_date.set_date(date(date.today().year, 1, 1))

        ttk.Label(filter_frame, text="To:").grid(row=0, column=2, padx=5, pady=5)
        self.to_date = DateEntry(filter_frame, date_pattern='y-mm-dd')
        self.to_date.grid(row=0, column=3, padx=5, pady=5)
        self.to_date.set_date(date.today())

        # Category Filter
        ttk.Label(filter_frame, text="Category:").grid(row=0, column=4, padx=5, pady=5)
        self.filter_category_var = tk.StringVar()
        self.filter_category_combobox = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_category_var,
            values=["All"] + self.categories
        )
        self.filter_category_combobox.grid(row=0, column=5, padx=5, pady=5)
        self.filter_category_combobox.current(0)

        # Filter Button
        filter_button = ttk.Button(
            filter_frame,
            text="Filter",
            command=self.filter_expenses
        )
        filter_button.grid(row=0, column=6, padx=5, pady=5)

        # Reset Button
        reset_button = ttk.Button(
            filter_frame,
            text="Reset",
            command=self.reset_filters
        )
        reset_button.grid(row=0, column=7, padx=5, pady=5)

        # Treeview for expenses
        self.tree = ttk.Treeview(
            self.view_expenses_frame,
            columns=("Date", "Category", "Amount", "Description"),
            show="headings"
        )

        # Configure columns
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")

        self.tree.column("Date", width=100)
        self.tree.column("Category", width=120)
        self.tree.column("Amount", width=100)
        self.tree.column("Description", width=300)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.view_expenses_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Delete Button
        delete_button = ttk.Button(
            self.view_expenses_frame,
            text="Delete Selected",
            command=self.delete_expense
        )
        delete_button.pack(pady=5)

        # Populate tree with all expenses initially
        self.update_treeview()

    def create_stats_tab(self):
        # Stats Frame
        stats_frame = ttk.Frame(self.stats_frame)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Total Expenses
        ttk.Label(stats_frame, text="Total Expenses:").grid(row=0, column=0, sticky=tk.W)
        self.total_var = tk.StringVar()
        self.total_var.set("$0.00")
        ttk.Label(stats_frame, textvariable=self.total_var, font=('Arial', 12, 'bold')).grid(row=0, column=1,
                                                                                             sticky=tk.W)

        # By Category
        ttk.Label(stats_frame, text="By Category:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))

        # Treeview for category stats
        self.stats_tree = ttk.Treeview(
            stats_frame,
            columns=("Category", "Amount", "Percentage"),
            show="headings"
        )

        self.stats_tree.heading("Category", text="Category")
        self.stats_tree.heading("Amount", text="Amount")
        self.stats_tree.heading("Percentage", text="Percentage")

        self.stats_tree.column("Category", width=150)
        self.stats_tree.column("Amount", width=100)
        self.stats_tree.column("Percentage", width=100)

        self.stats_tree.grid(row=2, column=0, columnspan=2, sticky=tk.W + tk.E, pady=5)

        # Monthly Summary
        ttk.Label(stats_frame, text="Monthly Summary:").grid(row=3, column=0, sticky=tk.W, pady=(10, 0))

        # Treeview for monthly stats
        self.monthly_tree = ttk.Treeview(
            stats_frame,
            columns=("Month", "Amount"),
            show="headings"
        )

        self.monthly_tree.heading("Month", text="Month")
        self.monthly_tree.heading("Amount", text="Amount")

        self.monthly_tree.column("Month", width=150)
        self.monthly_tree.column("Amount", width=100)

        self.monthly_tree.grid(row=4, column=0, columnspan=2, sticky=tk.W + tk.E, pady=5)

        # Update stats
        self.update_stats()

    def add_expense(self):
        try:
            expense_date = self.date_entry.get_date()
            category = self.category_var.get()
            amount = self.amount_var.get()
            description = self.description_var.get()

            if not category or amount <= 0:
                messagebox.showerror("Error", "Please enter valid category and amount")
                return

            expense = {
                "date": expense_date.strftime("%Y-%m-%d"),
                "category": category,
                "amount": amount,
                "description": description
            }

            self.expenses.append(expense)
            self.save_data()
            self.update_treeview()
            self.update_stats()

            # Clear fields
            self.amount_var.set(0)
            self.description_var.set("")

            messagebox.showinfo("Success", "Expense added successfully")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_treeview(self, expenses=None):
        if expenses is None:
            expenses = self.expenses

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add new items
        for expense in expenses:
            self.tree.insert("", tk.END, values=(
                expense["date"],
                expense["category"],
                f"${expense['amount']:.2f}",
                expense["description"]
            ))

    def filter_expenses(self):
        from_date = self.from_date.get_date()
        to_date = self.to_date.get_date()
        category = self.filter_category_var.get()

        filtered = []
        for expense in self.expenses:
            expense_date = datetime.strptime(expense["date"], "%Y-%m-%d").date()

            date_ok = (expense_date >= from_date) and (expense_date <= to_date)
            category_ok = (category == "All") or (expense["category"] == category)

            if date_ok and category_ok:
                filtered.append(expense)

        self.update_treeview(filtered)

    def reset_filters(self):
        self.from_date.set_date(date(date.today().year, 1, 1))
        self.to_date.set_date(date.today())
        self.filter_category_combobox.current(0)
        self.update_treeview()

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete")
            return

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete the selected expense?")
        if not confirm:
            return

        for item in selected:
            values = self.tree.item(item, "values")
            date_str = values[0]
            amount = float(values[2][1:])  # Remove $ and convert to float

            # Find and remove the expense
            for i, expense in enumerate(self.expenses):
                if (expense["date"] == date_str and
                        float(expense["amount"]) == amount and
                        expense["category"] == values[1]):
                    del self.expenses[i]
                    break

        self.save_data()
        self.update_treeview()
        self.update_stats()
        messagebox.showinfo("Success", "Expense deleted successfully")

    def update_stats(self):
        # Calculate total
        total = sum(expense["amount"] for expense in self.expenses)
        self.total_var.set(f"${total:.2f}")

        # Clear existing stats
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)
        for item in self.monthly_tree.get_children():
            self.monthly_tree.delete(item)

        # Calculate by category
        category_totals = {}
        for expense in self.expenses:
            category = expense["category"]
            amount = expense["amount"]
            category_totals[category] = category_totals.get(category, 0) + amount

        # Add to treeview
        for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total) * 100 if total > 0 else 0
            self.stats_tree.insert("", tk.END, values=(
                category,
                f"${amount:.2f}",
                f"{percentage:.1f}%"
            ))

        # Calculate monthly totals
        monthly_totals = {}
        for expense in self.expenses:
            date_str = expense["date"]
            month = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m")
            amount = expense["amount"]
            monthly_totals[month] = monthly_totals.get(month, 0) + amount

        # Add to treeview
        for month, amount in sorted(monthly_totals.items()):
            self.monthly_tree.insert("", tk.END, values=(
                month,
                f"${amount:.2f}"
            ))

    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                self.expenses = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.expenses = []

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.expenses, f, indent=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()