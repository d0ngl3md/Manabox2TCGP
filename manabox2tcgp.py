import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import ttkbootstrap as tb  # Provides themed GUI components using ttkbootstrap

# Main processing function to update pricing and quantity
def process_data(inv_df, price_df, floor, price_source, markup, inventory_format):
    # Normalize keys across both datasets for consistent matching
    def build_key(name, set_name, number, condition):
        return (
            name.strip().lower(),          # Normalize card name
            set_name.strip().lower(),      # Normalize set name
            str(number).strip(),           # Normalize collector number
            condition.strip().lower()      # Keep case like "near mint" vs "near mint foil"
        )

    inventory_dict = {}  # Key: (name, set, number, condition), Value: quantity

    # If the inventory format is Manabox, normalize its columns and build keys
    if inventory_format == 'Manabox':
        # Convert foil indicator to "Near Mint" or "Near Mint Foil" condition for matching
        inv_df['Condition'] = inv_df['Foil'].apply(
            lambda x: 'Near Mint Foil' if x.strip().lower() == 'foil' else 'Near Mint'
        )
        for _, row in inv_df.iterrows():
            key = build_key(row['Name'], row['Set name'], row['Collector number'], row['Condition'])
            inventory_dict[key] = row.get('Quantity', 0)

    else:  # TCGPlayer inventory
        for _, row in inv_df.iterrows():
            key = build_key(row['Product Name'], row['Set Name'], row['Number'], row['Condition'])
            inventory_dict[key] = row.get('Total Quantity', 0)  # Use "Total Quantity" column

    output_rows = []

    # Iterate through each row in the pricing CSV to update pricing and quantity
    for _, row in price_df.iterrows():
        key = build_key(row['Product Name'], row['Set Name'], row['Number'], row['Condition'])
        qty = inventory_dict.get(key, 0)  # Lookup quantity from inventory
        try:
            qty = int(qty)
        except:
            qty = 0

        if qty <= 0:
            continue  # Skip items with zero quantity

        try:
            selected_price = float(row.get(price_source, 0))  # Use Market or Low
        except:
            selected_price = 0.0

        # Apply price floor and markup
        final_price = max(selected_price, floor)
        final_price = round(final_price * (1 + markup / 100.0), 2)

        new_row = row.copy()
        new_row['Add to Quantity'] = qty  # Always use 'Add to Quantity'
        new_row['TCG Marketplace Price'] = final_price  # Set adjusted price
        output_rows.append(new_row)

    result_df = pd.DataFrame(output_rows)

    # Filter output to only include items with > 0 quantity
    return result_df[result_df['Add to Quantity'] > 0]

# Main GUI event handler
def run_tool():
    inv_file = inventory_file_var.get()
    price_file = price_file_var.get()
    if not inv_file or not price_file:
        messagebox.showerror("Error", "Please select both inventory and price files.")
        return

    # Try reading both input CSV files
    try:
        inv_df = pd.read_csv(inv_file)
        price_df = pd.read_csv(price_file)
    except Exception as e:
        messagebox.showerror("File Error", str(e))
        return

    # Parse float inputs or use defaults
    try:
        floor = float(floor_entry.get())
    except:
        floor = 0.0
    try:
        markup = float(markup_entry.get())
    except:
        markup = 0.0

    price_source = price_var.get()         # e.g. "TCG Market Price"
    inventory_format = format_var.get()    # Either "Manabox" or "TCGPlayer"

    # Process data and prompt for output file save location
    try:
        result_df = process_data(inv_df, price_df, floor, price_source, markup, inventory_format)
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", title="Save Output CSV")
        if save_path:
            result_df.to_csv(save_path, index=False)
            messagebox.showinfo("Success", "File saved successfully!")
    except Exception as e:
        messagebox.showerror("Processing Error", str(e))

# File selection helper for inventory CSV
def browse_inventory():
    path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if path:
        inventory_file_var.set(path)

# File selection helper for price CSV
def browse_price():
    path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if path:
        price_file_var.set(path)

# --- GUI SETUP STARTS HERE ---
root = tb.Window(themename="vapor")  # Use ttkbootstrap theme "vapor"
root.title("TCGPlayer Inventory Tool")

frame = ttk.Frame(root, padding=20)
frame.pack()

# Variables for user selections
price_var = tk.StringVar(value='TCG Low Price')
format_var = tk.StringVar(value='Manabox')  # Default selection
inventory_file_var = tk.StringVar()
price_file_var = tk.StringVar()

# Aliases for easier GUI widget usage
Label = ttk.Label
Entry = ttk.Entry
Button = ttk.Button
Combobox = ttk.Combobox

# --- GUI ELEMENTS ---
Label(frame, text="Inventory File:").grid(row=0, column=0, sticky='e')
Entry(frame, textvariable=inventory_file_var, width=40).grid(row=0, column=1)
Button(frame, text="Browse", command=browse_inventory).grid(row=0, column=2)

Label(frame, text="Price File:").grid(row=1, column=0, sticky='e')
Entry(frame, textvariable=price_file_var, width=40).grid(row=1, column=1)
Button(frame, text="Browse", command=browse_price).grid(row=1, column=2)

Label(frame, text="Use price source:").grid(row=2, column=0, sticky='e')
price_select = Combobox(frame, textvariable=price_var, values=['TCG Low Price', 'TCG Market Price'], width=20)
price_select.grid(row=2, column=1)

Label(frame, text="Markup (%):").grid(row=3, column=0, sticky='e')
markup_entry = Entry(frame)
markup_entry.insert(0, "0")  # Default value
markup_entry.grid(row=3, column=1)

Label(frame, text="Price Floor:").grid(row=4, column=0, sticky='e')
floor_entry = Entry(frame)
floor_entry.insert(0, "0")  # Default value
floor_entry.grid(row=4, column=1)

Label(frame, text="Inventory format:").grid(row=5, column=0, sticky='e')
format_select = Combobox(frame, textvariable=format_var, values=['Manabox', 'TCGPlayer'], width=20)
format_select.grid(row=5, column=1)

run_button = Button(frame, text="Run", command=run_tool)
run_button.grid(row=6, column=0, columnspan=3, pady=10)

root.mainloop()
