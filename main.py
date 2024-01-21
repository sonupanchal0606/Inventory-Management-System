import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
from tkcalendar import Calendar


class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")

        # Create Excel files if not exists
        self.create_excel_files()

        # Create GUI components
        self.create_gui()

    def create_excel_files(self):
        # Purchase_Data sheet
        try:
            self.purchase_file = "C:\\Users\\shashank\\Desktop\\Sonu\\Purchase_Data.xlsx"
            try:
                pd.read_excel(self.purchase_file)
            except FileNotFoundError:
                pd.DataFrame(columns=["Client Name", "Product Name", "Product Code", "Price", "Quantity",
                                      "Total Amount", "Date of Purchase", "Payment Mode", "Balance Amount"]).to_excel(
                    self.purchase_file, index=False)

            # Sales_Data sheet
            self.sales_file = "C:\\Users\\shashank\\Desktop\\Sonu\\Sales_Data.xlsx"
            try:
                pd.read_excel(self.sales_file)
            except FileNotFoundError:
                pd.DataFrame(columns=["Client Name", "Contact Number", "Address", "GST Number", "Product Name",
                                      "Product Code", "Price", "Quantity", "Discount (%)", "Total Amount",
                                      "Total Amount after Discount", "Remaining Balance"]).to_excel(self.sales_file,
                                                                                                    index=False)

            # Stock sheet
            self.stock_file = "C:\\Users\\shashank\\Desktop\\Sonu\\Stock.xlsx"
            try:
                pd.read_excel(self.stock_file)
            except FileNotFoundError:
                pd.DataFrame(columns=["Product Name", "Product Code", "Price", "Quantity"]).to_excel(self.stock_file,
                                                                                                     index=False)
        except PermissionError as e:
            print(f"Permission error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def create_gui(self):
        # Buttons
        tk.Button(self.root, text="Add Purchase Data", command=self.add_purchase_data).pack(pady=10)
        tk.Button(self.root, text="Add Sales Data", command=self.add_sales_data).pack(pady=10)
        tk.Button(self.root, text="Add Stock Data", command=self.add_stock_data).pack(pady=10)
        tk.Button(self.root, text="Print Bill", command=self.print_bill).pack(pady=10)

    def add_purchase_data(self):
        purchase_window = tk.Toplevel(self.root)
        purchase_window.title("Add Purchase Data")

        # Labels and Entry widgets
        tk.Label(purchase_window, text="Client Name").grid(row=0, column=0, padx=10, pady=10)
        client_name_entry = tk.Entry(purchase_window)
        client_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(purchase_window, text="Product Name").grid(row=1, column=0, padx=10, pady=10)
        product_name_entry = tk.Entry(purchase_window)
        product_name_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(purchase_window, text="Product Code").grid(row=2, column=0, padx=10, pady=10)
        product_code_entry = tk.Entry(purchase_window)
        product_code_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(purchase_window, text="Price").grid(row=3, column=0, padx=10, pady=10)
        price_entry = tk.Entry(purchase_window)
        price_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(purchase_window, text="Quantity").grid(row=4, column=0, padx=10, pady=10)
        quantity_entry = tk.Entry(purchase_window)
        quantity_entry.grid(row=4, column=1, padx=10, pady=10)

        # Date of Purchase
        tk.Label(purchase_window, text="Date of Purchase:").grid(row=5, column=0, padx=10, pady=10)
        date_entry = tk.Entry(purchase_window)
        date_entry.grid(row=5, column=1, padx=10, pady=10)
        # date_button = tk.Button(purchase_window, text="Select Date", command=lambda: self.select_date(date_entry))
        # date_button.grid(row=5, column=2, pady=10)

        # Payment Mode
        tk.Label(purchase_window, text="Payment Mode:").grid(row=6, column=0, padx=10, pady=10)
        payment_mode_var = tk.StringVar(value="UPI")
        payment_mode_options = ["UPI", "Cash", "Internet Banking", "Cheque"]
        for i, mode in enumerate(payment_mode_options):
            tk.Radiobutton(purchase_window, text=mode, variable=payment_mode_var, value=mode).grid(row=6, column=1 + i,
                                                                                                   padx=10, pady=10)
        # tk.Label(purchase_window, text="Payment Mode").grid(row=7, column=0, padx=10, pady=10)

        tk.Label(purchase_window, text="Balance Amount").grid(row=7, column=0, padx=10, pady=10)
        balance_amount_entry = tk.Entry(purchase_window)
        balance_amount_entry.grid(row=7, column=1, padx=10, pady=10)

        # Submit button
        # tk.Button(purchase_window, text="Submit", command=lambda: self.submit_purchase_data(entries, purchase_window)).pack(pady=10)
        submit_button = tk.Button(purchase_window, text="Submit", command=lambda: self.submit_purchase_data(
            client_name_entry.get(),
            product_name_entry.get(),
            product_code_entry.get(),
            price_entry.get(),
            quantity_entry.get(),
            date_entry.get(),
            payment_mode_var.get(),
            balance_amount_entry.get(),
            purchase_window
        ))
        submit_button.grid(row=12, column=0, columnspan=2, pady=10)

    # def select_date(self, date_entry):
    #     def on_date_selected():
    #         date_str = cal.get_date()
    #         date_entry.delete(0, tk.END)
    #         date_entry.insert(0, date_str)
    #         top.destroy()

        # top = tk.Toplevel(self.root)
        # cal = Calendar(top, font="Arial 14", selectmode="day", cursor="hand1", year=2022, month=1, day=1)
        # cal.grid(row=0, column=0, padx=20, pady=20, columnspan=7)
        # tk.Button(top, text="OK", command=on_date_selected).grid(row=1, column=0, columnspan=7, pady=10)

    def submit_purchase_data(self, client_name, product_name, product_code, price, quantity, date_of_purchase,
                             payment_mode, balance_amount, window):
        try:
            # Convert string values to appropriate data types
            price = float(price)
            quantity = int(quantity)
            balance_amount = float(balance_amount)
            total_amount = price * quantity

            # Create a DataFrame with the purchase data
            purchase_data = pd.DataFrame({
                "Client Name": [client_name],
                "Product Name": [product_name],
                "Product Code": [product_code],
                "Price": [price],
                "Quantity": [quantity],
                "Total Amount": [total_amount],
                "Date of Purchase": [date_of_purchase],
                "Payment Mode": [payment_mode],
                "Balance Amount": [balance_amount]
            })

            # Convert the "Date of Purchase" column to datetime format
            purchase_data["Date of Purchase"] = pd.to_datetime(purchase_data["Date of Purchase"])

            # Read the existing Excel file
            existing_data = pd.read_excel(self.purchase_file)

            # Append the new DataFrame to the existing data
            combined_data = existing_data._append(purchase_data, ignore_index=True)

            # Write the combined data back to the Excel file
            combined_data.to_excel(self.purchase_file, index=False)

            # Display success message
            messagebox.showinfo("Success", "Purchase data added successfully.")

            # Close the purchase window
            window.destroy()

        except ValueError:
            # Handle errors related to invalid data types
            messagebox.showerror("Error", "Invalid data types. Please enter valid numeric values.")

        except Exception as e:
            # Handle other exceptions
            messagebox.showerror("Error", f"An error occurred: {e}")

    def add_sales_data(self):
        sales_window = tk.Toplevel(self.root)
        sales_window.title("Add Sales Data")

        # Create labels and entry widgets
        # labels = ["Client Name", "Contact Number", "Address", "GST Number", "Product Name",
        #           "Product Code", "Price", "Quantity", "Discount (%)", "Total Amount",
        #           "Total Amount after Discount", "Remaining Balance"]
        # entries = [tk.Entry(sales_window) for _ in labels]
        #
        # for label, entry in zip(labels, entries):
        #     tk.Label(sales_window, text=label).pack(pady=5)
        #     entry.pack(pady=5)

        # Submit button
        # tk.Button(sales_window, text="Submit", command=lambda: self.submit_sales_data(entries, sales_window)).pack(pady=10)

        # Entry widgets
        client_name_entry = tk.Entry(sales_window)
        contact_number_entry = tk.Entry(sales_window)
        address_entry = tk.Entry(sales_window)
        gst_number_entry = tk.Entry(sales_window)
        product_name_entry = tk.Entry(sales_window)
        product_code_entry = tk.Entry(sales_window)
        price_entry = tk.Entry(sales_window)
        quantity_entry = tk.Entry(sales_window)
        discount_entry = tk.Entry(sales_window)
        remaining_balance_entry = tk.Entry(sales_window)

        # Labels
        tk.Label(sales_window, text="Client Name:").grid(row=0, column=0, pady=5)
        client_name_entry.grid(row=0, column=1, pady=5)

        tk.Label(sales_window, text="Contact Number:").grid(row=0, column=2, pady=5)
        contact_number_entry.grid(row=0, column=3, pady=5)

        tk.Label(sales_window, text="Address:").grid(row=1, column=0, pady=5)
        address_entry.grid(row=1, column=1, pady=5)

        tk.Label(sales_window, text="GST Number:").grid(row=1, column=2, pady=5)
        gst_number_entry.grid(row=1, column=3, pady=5)

        tk.Label(sales_window, text="Product Name:").grid(row=4, column=0, pady=5)
        product_name_entry.grid(row=4, column=1, pady=5)

        tk.Label(sales_window, text="Product Code:").grid(row=4, column=2, pady=5)
        product_code_entry.grid(row=4, column=3, pady=5)

        tk.Label(sales_window, text="Price:").grid(row=5, column=0, pady=5)
        price_entry.grid(row=5, column=1, pady=5)

        tk.Label(sales_window, text="Quantity:").grid(row=5, column=2, pady=5)
        quantity_entry.grid(row=5, column=3, pady=5)

        tk.Label(sales_window, text="Discount (%):").grid(row=6, column=0, pady=5)
        discount_entry.grid(row=6, column=1, pady=5)

        tk.Label(sales_window, text="Remaining Balance").grid(row=6, column=2, pady=5)
        remaining_balance_entry.grid(row=6, column=3, pady=5)

        # Submit button
        tk.Button(sales_window, text="Submit", command=lambda: self.submit_sales_data(
            client_name_entry.get(),
            contact_number_entry.get(),
            address_entry.get(),
            gst_number_entry.get(),
            product_name_entry.get(),
            product_code_entry.get(),
            price_entry.get(),
            quantity_entry.get(),
            discount_entry.get(),
            remaining_balance_entry.get(),
            sales_window
        )).grid(row=9, column=0, columnspan=2, pady=10)

    def submit_sales_data(self, client_name, contact_number, address, gst_number, product_name,
                          product_code, price, quantity, discount_percentage, remaining_balance, window):
        try:
            # Validate numeric inputs
            price = float(price)
            quantity = int(quantity)
            discount_percentage = float(discount_percentage)

            # Calculate total amount and total amount after discount
            total_amount = price * quantity
            total_amount_after_discount = total_amount - (discount_percentage / 100 * total_amount)

            # Assuming you have defined self.sales_file as the path to your Sales_Data Excel file
            sales_data = pd.DataFrame([[client_name, contact_number, address, gst_number,
                                        product_name, product_code, price, quantity,
                                        discount_percentage, total_amount,
                                        total_amount_after_discount, remaining_balance]],
                                      columns=["Client Name", "Contact Number", "Address", "GST Number",
                                               "Product Name", "Product Code", "Price", "Quantity",
                                               "Discount (%)", "Total Amount", "Total Amount after Discount",
                                               "Remaining Balance"])

            # sales_data.to_excel(self.sales_file, mode="a", index=False, header=False)
            # Read the existing Excel file
            existing_data = pd.read_excel(self.sales_file)

            # Append the new DataFrame to the existing data
            combined_data = existing_data._append(sales_data, ignore_index=True)

            # Write the combined data back to the Excel file
            combined_data.to_excel(self.sales_file, index=False)

            messagebox.showinfo("Success", "Sales data added successfully.")
            window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Invalid numeric value entered.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def add_stock_data(self):
        stock_window = tk.Toplevel(self.root)
        stock_window.title("Add Stock Data")

        # Create labels and entry widgets
        labels = ["Product Name", "Product Code", "Price", "Quantity"]
        entries = [tk.Entry(stock_window) for _ in labels]

        for label, entry in zip(labels, entries):
            tk.Label(stock_window, text=label).pack(pady=5)
            entry.pack(pady=5)

        # Submit button
        tk.Button(stock_window, text="Submit", command=lambda: self.submit_stock_data(entries, stock_window)).pack(
            pady=10)

    def submit_stock_data(self, entries, window):
        data = [entry.get() for entry in entries]
        if all(data):
            try:
                stock_data = pd.DataFrame([data], columns=["Product Name", "Product Code", "Price", "Quantity"])

                # Read the existing Excel file
                existing_data = pd.read_excel(self.stock_file)

                # Append the new DataFrame to the existing data
                combined_data = existing_data._append(stock_data, ignore_index=True)

                # Write the combined data back to the Excel file
                combined_data.to_excel(self.stock_file, index=False)

                # stock_data.to_excel(self.stock_file, mode="a", index=False, header=False)
                messagebox.showinfo("Success", "Stock data added successfully.")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Please fill in all the fields.")

    def print_bill(self):
        # Implement bill printing logic here
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()
