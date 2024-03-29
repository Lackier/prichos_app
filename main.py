import tkinter
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime

def display_data(sort_column="id", sort_order="ASC", filters=None):
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    filter_conditions = []
    filter_values = []
    if filters:
        for column, value in filters.items():
            if value:
                if column == 'price_from':
                    filter_conditions.append(f"price >= ?")
                    filter_values.append(f"{value}")
                elif column == 'price_to':
                    filter_conditions.append(f"price <= ?")
                    filter_values.append(f"{value}")
                elif column == 'price_range':
                    filter_conditions.append(f"price BETWEEN ? AND ?")
                    filter_values.extend(value)
                elif column == 'purchase_date_from':
                    filter_conditions.append(f"purchase_date >= ?")
                    filter_values.append(f"{value}")
                elif column == 'purchase_date_to':
                    filter_conditions.append(f"purchase_date <= ?")
                    filter_values.append(f"{value}")
                elif column == 'purchase_date_range':
                    filter_conditions.append(f"purchase_date BETWEEN ? AND ?")
                    filter_values.extend(value)
                else:
                    filter_conditions.append(f"{column} LIKE ?")
                    filter_values.append(f"%{value}%")

    filter_condition = " AND ".join(filter_conditions)
    if filter_condition:
        sql_query = f"SELECT * FROM Product_Data WHERE {filter_condition} ORDER BY {sort_column} {sort_order}"
        cursor.execute(sql_query, filter_values)
    else:
        cursor.execute(f"SELECT * FROM Product_Data ORDER BY {sort_column} {sort_order}")

    rows = cursor.fetchall()
    
    for row in rows:
        tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    
    conn.close()

def create_table():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Product_Data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_name TEXT,
                        price REAL,
                        quantity INTEGER,
                        weight REAL,
                        purchase_date DATE,
                        purchase_place TEXT,
                        categories TEXT
                    )''')
    conn.commit()
    conn.close()

def add_edit_item(selected_item=None):
    add_edit_window = tkinter.Toplevel(window)
    add_edit_window.title("Add/Edit Item")
    add_edit_window.transient(window)
    add_edit_window.grab_set()

    style = ttk.Style()
    style.configure("TLabel", padding=10)
    style.configure("TButton", padding=10, background="#FA7070", foreground="white")

    tkinter.Label(add_edit_window, text="Product Name:").grid(row=0, column=0, padx=5, pady=5)
    product_name_entry = tkinter.Entry(add_edit_window)
    product_name_entry.grid(row=0, column=1, padx=5, pady=5)

    tkinter.Label(add_edit_window, text="Price:").grid(row=1, column=0, padx=5, pady=5)
    price_entry = tkinter.Entry(add_edit_window)
    price_entry.grid(row=1, column=1, padx=5, pady=5)

    tkinter.Label(add_edit_window, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
    quantity_entry = tkinter.Entry(add_edit_window)
    quantity_entry.grid(row=2, column=1, padx=5, pady=5)

    tkinter.Label(add_edit_window, text="Weight:").grid(row=3, column=0, padx=5, pady=5)
    weight_entry = tkinter.Entry(add_edit_window)
    weight_entry.grid(row=3, column=1, padx=5, pady=5)

    tkinter.Label(add_edit_window, text="Purchase Date:").grid(row=4, column=0, padx=5, pady=5)
    purchase_date_entry = DateEntry(add_edit_window, date_pattern="dd/mm/yyyy")
    purchase_date_entry.grid(row=4, column=1, padx=5, pady=5)

    tkinter.Label(add_edit_window, text="Purchase Place:").grid(row=5, column=0, padx=5, pady=5)
    purchase_place_entry = tkinter.Entry(add_edit_window)
    purchase_place_entry.grid(row=5, column=1, padx=5, pady=5)

    tkinter.Label(add_edit_window, text="Categories:").grid(row=6, column=0, padx=5, pady=5)
    categories_entry = tkinter.Entry(add_edit_window)
    categories_entry.grid(row=6, column=1, padx=5, pady=5)

    if selected_item:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Product_Data WHERE id=?", (selected_item,))
        item_data = cursor.fetchone()
        conn.close()

        if item_data:
            product_name_entry.insert(0, item_data[1])
            price_entry.insert(0, item_data[2])
            quantity_entry.insert(0, item_data[3])
            weight_entry.insert(0, item_data[4])
            purchase_date_entry.set_date(item_data[5])
            purchase_place_entry.insert(0, item_data[6])
            categories_entry.insert(0, item_data[7])

    def submit():
        product_name = product_name_entry.get()
        price = float(price_entry.get())
        quantity = quantity_entry.get()
        weight = weight_entry.get()
        purchase_date = purchase_date_entry.get()
        purchase_place = purchase_place_entry.get()
        categories = categories_entry.get()

        if selected_item:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute('''UPDATE Product_Data SET product_name=?, price=?, quantity=?, weight=?, 
                              purchase_date=?, purchase_place=?, categories=? WHERE id=?''',
                           (product_name, price, quantity, weight, purchase_date, purchase_place, categories, selected_item))
        else:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Product_Data (product_name, price, quantity, weight, 
                              purchase_date, purchase_place, categories) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (product_name, price, quantity, weight, purchase_date, purchase_place, categories))

        conn.commit()
        conn.close()

        add_edit_window.grab_release()
        add_edit_window.destroy()
        display_data()

    submit_button = tkinter.Button(add_edit_window, text="Submit", command=submit)
    submit_button.grid(row=7, columnspan=2, padx=5, pady=5)

    def close_window():
        add_edit_window.grab_release()
        add_edit_window.destroy()

    close_button = tkinter.Button(add_edit_window, text="Close", command=close_window)
    close_button.grid(row=8, columnspan=2, padx=5, pady=5)

def delete_selected_item():
    selected_item = tree.selection()
    if selected_item:
        item_id = tree.item(selected_item, "values")[0]
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM Product_Data WHERE id=?''', (item_id,))
        conn.commit()
        conn.close()
        display_data()

def on_item_double_click(event):
    item = tree.selection()[0]
    item_id = tree.item(item, "values")[0]
    add_edit_item(item_id)

def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        delete_button.config(state="normal")
    else:
        delete_button.config(state="disabled")

def apply_filters():
    product_name_filter = product_name_filter_entry.get()
    price_filter_from = price_filter_from_entry.get()
    price_filter_to = price_filter_to_entry.get()
    quantity_filter = quantity_filter_entry.get()
    weight_filter = weight_filter_entry.get()
    purchase_date_filter_from = purchase_date_filter_from_entry.get()
    purchase_date_filter_to = purchase_date_filter_to_entry.get()
    purchase_place_filter = purchase_place_filter_entry.get()
    categories_filter = categories_filter_entry.get()

    filters = {}
    if product_name_filter:
        filters["product_name"] = product_name_filter
    if price_filter_from:
        filters["price_from"] = float(price_filter_from)
    if price_filter_to:
        filters["price_to"] = float(price_filter_to)
    if price_filter_from and price_filter_to:
        filters["price_range"] = [float(price_filter_from), float(price_filter_to)]
    if quantity_filter:
        filters["quantity"] = quantity_filter
    if weight_filter:
        filters["weight"] = weight_filter
    if purchase_date_filter_from:
        filters["purchase_date_from"] = purchase_date_filter_from
    if purchase_date_filter_to:
        filters["purchase_date_to"] = purchase_date_filter_to
    if purchase_date_filter_from and purchase_date_filter_to:
        filters["purchase_date_range"] = [purchase_date_filter_from, purchase_date_filter_to]
    if purchase_place_filter:
        filters["purchase_place"] = purchase_place_filter
    if categories_filter:
        filters["categories"] = categories_filter

    display_data(sort_column="id", sort_order="ASC", filters=filters)

def on_treeview_sort_column(treeview, col, reverse):
    for column in treeview["columns"]:
        treeview.heading(column, text=column)

    data = [(treeview.set(child, col), child) for child in treeview.get_children('')]
    data.sort(reverse=reverse)

    for index, (val, child) in enumerate(data):
        treeview.move(child, '', index)

    if reverse:
        treeview.heading(col, text=col + " ▼")
    else:
        treeview.heading(col, text=col + " ▲")

    treeview.heading(col, command=lambda: on_treeview_sort_column(treeview, col, not reverse))

window = tkinter.Tk()
window.title("PrichosApp")
window.geometry("800x600")
window.configure(bg="#FEFDED")

frame = tkinter.Frame(window)
frame.pack(fill="both", expand=True)

tree = ttk.Treeview(frame)
tree["columns"] = ("ID", "Product Name", "Price", "Quantity", "Weight", "Date", "Place", "Categories")
tree.heading("ID", text="ID")
tree.heading("Product Name", text="Product Name")
tree.heading("Price", text="Price")
tree.heading("Quantity", text="Quantity")
tree.heading("Weight", text="Weight")
tree.heading("Date", text="Date")
tree.heading("Place", text="Place")
tree.heading("Categories", text="Categories")

for column in tree["columns"]:
    tree.column(column, width=100)
tree.column("#0", width=0)
tree.column("ID", width=20)
tree.column("Price", width=30)
tree.column("Quantity", width=30)
tree.column("Weight", width=50)
tree.column("Date", width=50)

for col in tree["columns"]:
    tree.heading(col, text=col, command=lambda c=col: on_treeview_sort_column(tree, c, False))

vsb = tkinter.Scrollbar(frame, orient="vertical", command=tree.yview)
vsb.pack(side="right", fill="y")

tree.configure(yscrollcommand=vsb.set)
tree.pack(fill="both", expand=True)

tree.bind("<Double-1>", on_item_double_click)
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Filter entry widgets
filters_frame = tkinter.Frame(window)
filters_frame.pack(pady=10)

# First row of filters
first_row_filters_frame = tkinter.Frame(filters_frame)
first_row_filters_frame.pack(side="top", padx=5, pady=5)

product_name_filter_label = tkinter.Label(first_row_filters_frame, text="Product Name:")
product_name_filter_label.pack(side="left")
product_name_filter_entry = tkinter.Entry(first_row_filters_frame, width=15)
product_name_filter_entry.pack(side="left", padx=5)

price_filter_label = tkinter.Label(first_row_filters_frame, text="Price:")
price_filter_label.pack(side="left", padx=5)
price_filter_from_entry = tkinter.Entry(first_row_filters_frame, width=8)
price_filter_from_entry.pack(side="left", padx=(0, 5))
price_to_filter_label = tkinter.Label(first_row_filters_frame, text="to")
price_to_filter_label.pack(side="left")
price_filter_to_entry = tkinter.Entry(first_row_filters_frame, width=8)
price_filter_to_entry.pack(side="left", padx=(0, 5))

quantity_filter_label = tkinter.Label(first_row_filters_frame, text="Quantity:")
quantity_filter_label.pack(side="left", padx=5)
quantity_filter_entry = tkinter.Entry(first_row_filters_frame, width=8)
quantity_filter_entry.pack(side="left", padx=(0, 5))

weight_filter_label = tkinter.Label(first_row_filters_frame, text="Weight:")
weight_filter_label.pack(side="left", padx=5)
weight_filter_entry = tkinter.Entry(first_row_filters_frame, width=8)
weight_filter_entry.pack(side="left", padx=(5, 10))

# Second row of filters
second_row_filters_frame = tkinter.Frame(filters_frame)
second_row_filters_frame.pack(side="top", padx=5, pady=5)

purchase_date_filter_label = tkinter.Label(second_row_filters_frame, text="Purchase Date:")
purchase_date_filter_label.pack(side="left", padx=5)
purchase_date_filter_from_entry = DateEntry(second_row_filters_frame, date_pattern="dd/mm/yyyy", width=10)
purchase_date_filter_from_entry.delete(0, "end")
purchase_date_filter_from_entry.pack(side="left", padx=0)
purchase_date_clear_button1 = tkinter.Button(second_row_filters_frame, text="<-", command=lambda: purchase_date_filter_from_entry.delete(0, "end"))
purchase_date_clear_button1.pack(side="left", padx=(5, 0))
purchase_date_to_filter_label = tkinter.Label(second_row_filters_frame, text="to")
purchase_date_to_filter_label.pack(side="left")
purchase_date_filter_to_entry = DateEntry(second_row_filters_frame, date_pattern="dd/mm/yyyy", width=10)
purchase_date_filter_to_entry.delete(0, "end")
purchase_date_filter_to_entry.pack(side="left", padx=0)
purchase_date_clear_button2 = tkinter.Button(second_row_filters_frame, text="<-", command=lambda: purchase_date_filter_to_entry.delete(0, "end"))
purchase_date_clear_button2.pack(side="left", padx=(5, 0))

purchase_place_filter_label = tkinter.Label(second_row_filters_frame, text="Purchase Place:")
purchase_place_filter_label.pack(side="left", padx=5)
purchase_place_filter_entry = tkinter.Entry(second_row_filters_frame, width=15)
purchase_place_filter_entry.pack(side="left", padx=5)

categories_filter_label = tkinter.Label(second_row_filters_frame, text="Categories:")
categories_filter_label.pack(side="left", padx=5)
categories_filter_entry = tkinter.Entry(second_row_filters_frame, width=15)
categories_filter_entry.pack(side="left", padx=5)

filter_button = tkinter.Button(filters_frame, text="Apply", command=apply_filters)
filter_button.pack(pady=5)

# Button frame
button_frame = tkinter.Frame(window)
button_frame.pack(pady=10)

display_button = tkinter.Button(button_frame, text="Show All", command=lambda: display_data("id", "ASC"), width=20, bg="#A1C398", fg="white", pady=10)
display_button.grid(row=0, column=0, padx=5)

add_edit_button = tkinter.Button(button_frame, text="Add/Edit", command=add_edit_item, width=20, bg="#A1C398", fg="white", pady=10)
add_edit_button.grid(row=0, column=1, padx=5)

delete_button = tkinter.Button(button_frame, text="Delete", command=delete_selected_item, state="disabled", width=20, bg="#A1C398", fg="white", pady=10)
delete_button.grid(row=0, column=2, padx=5)

create_table()
display_data()

window.mainloop()
