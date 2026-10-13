import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk

# ============================================================
#  ☕  VIDYA'S COFFEE HOUSE  ☕
#  With multi-order + final receipt
# ============================================================

# ---------- COLOR PALETTE ----------
CREAM      = "#FFF8F0"
BROWN_DARK = "#3E2723"
BROWN_MED  = "#6D4C41"
CARAMEL    = "#D7A86E"
GREEN_OK   = "#2E7D32"
GREEN_BOX  = "#E8F5E9"
GOLD_BILL  = "#FFE082"
RED_CLEAR  = "#B71C1C"

# ---------- WINDOW ----------
window = tkinter.Tk()
window.title("☕ Vidya's Coffee House ☕")
window.geometry("1000x720")
window.configure(bg=CREAM)
window.resizable(False, False)

# ---------- ORDER STATE ----------
selected_price = 0
selected_name  = ""
order_items    = []   # list of (name, price, qty) tuples

# ---------- LOAD IMAGES ----------
big_photo    = ImageTk.PhotoImage(Image.open("g.jpg").resize((340, 340)))
bottom_photo = ImageTk.PhotoImage(Image.open("f.jpg").resize((520, 180)))

# ============================================================
#  HEADER
# ============================================================
header = tkinter.Frame(window, bg=BROWN_DARK, padx=20, pady=15,
                       highlightbackground=CARAMEL, highlightthickness=3)
header.pack(fill="x", padx=20, pady=(15, 5))

tkinter.Label(header, text="☕  VIDYA'S COFFEE HOUSE  ☕",
              font=("Georgia", 26, "bold"),
              fg=CREAM, bg=BROWN_DARK).pack()

tkinter.Label(window, text="Freshly Brewed  •  Served with Love",
              font=("Georgia", 12, "italic"),
              fg=BROWN_MED, bg=CREAM).pack(pady=(0, 10))

# ============================================================
#  MAIN BODY
# ============================================================
body = tkinter.Frame(window, bg=CREAM)
body.pack(fill="both", expand=True, padx=30)

left_col = tkinter.Frame(body, bg=CREAM)
left_col.pack(side="left", anchor="n", fill="both", expand=True)

right_col = tkinter.Frame(body, bg=CREAM)
right_col.pack(side="right", anchor="n", padx=(20, 0))

tkinter.Label(left_col, text="Our Menu",
              font=("Georgia", 18, "bold"),
              fg=BROWN_DARK, bg=CREAM).pack(anchor="w", pady=(5, 10))

# ============================================================
#  MENU BUTTON FUNCTIONS
# ============================================================
def update_selection(name, price):
    global selected_price, selected_name
    selected_price = price
    selected_name  = name
    select_lable.config(text=f"You Selected {name}  ✓")
    price_label.config(text=f"Price: ₹{price}")

def E_clicked(): update_selection("Espresso",   80)
def C_clicked(): update_selection("Cappuccino", 100)
def L_clicked(): update_selection("Latte",      150)
def M_clicked(): update_selection("Mocha",      200)

# ---------- MENU BUTTONS ----------
btn_style = dict(font=("Georgia", 13, "bold"),
                 fg=CREAM, bg=BROWN_DARK,
                 activebackground=BROWN_MED, activeforeground=CREAM,
                 width=22, pady=8,
                 highlightbackground=CARAMEL,
                 highlightthickness=2, bd=0, cursor="hand2")

tkinter.Button(left_col, text="☕  Espresso  —  ₹80",
               command=E_clicked, **btn_style).pack(anchor="w", pady=5)
tkinter.Button(left_col, text="🥛  Cappuccino  —  ₹100",
               command=C_clicked, **btn_style).pack(anchor="w", pady=5)
tkinter.Button(left_col, text="🍶  Latte  —  ₹150",
               command=L_clicked, **btn_style).pack(anchor="w", pady=5)
tkinter.Button(left_col, text="🍫  Mocha  —  ₹200",
               command=M_clicked, **btn_style).pack(anchor="w", pady=5)

# ============================================================
#  SELECTION BOX
# ============================================================
details_box = tkinter.Frame(left_col, bg=GREEN_BOX,
                            highlightbackground=GREEN_OK,
                            highlightthickness=2, padx=15, pady=10)
details_box.pack(anchor="w", pady=(15, 10), fill="x")

select_lable = tkinter.Label(details_box, text="No coffee selected!",
                             fg=BROWN_DARK, bg=GREEN_BOX,
                             font=("Georgia", 13, "italic"))
select_lable.pack(anchor="w")

price_label = tkinter.Label(details_box, text="Price: Rs. 0",
                            fg=BROWN_DARK, bg=GREEN_BOX,
                            font=("Georgia", 14, "bold"))
price_label.pack(anchor="w", pady=(3, 0))

# ============================================================
#  QUANTITY
# ============================================================
qty_frame = tkinter.Frame(left_col, bg=CREAM)
qty_frame.pack(anchor="w", pady=5)

tkinter.Label(qty_frame, text="Quantity:",
              font=("Georgia", 13, "bold"),
              fg=BROWN_DARK, bg=CREAM).grid(row=0, column=0, padx=(0, 10))

quantity_entry = tkinter.Entry(qty_frame, width=8,
                               font=("Georgia", 13),
                               fg=BROWN_DARK, bg="white",
                               justify="center",
                               highlightbackground=CARAMEL,
                               highlightthickness=2, bd=0)
quantity_entry.grid(row=0, column=1)

# ============================================================
#  ADD TO ORDER
# ============================================================
def add_to_order():
    global selected_price, selected_name   # ← must come FIRST

    if selected_price == 0:
        messagebox.showwarning("No Coffee Selected", "Please select a coffee first!")
        return

    try:
        qty = int(quantity_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid Quantity", "Please enter a valid number.")
        return

    if qty <= 0:
        messagebox.showwarning("Invalid Quantity", "Quantity must be at least 1.")
        return

    # Save to order list
    order_items.append((selected_name, selected_price, qty))
    subtotal = selected_price * qty

    # Show running order in bill label
    show_running_order()

    # Reset selection + qty
    quantity_entry.delete(0, "end")
    select_lable.config(text="No coffee selected!")
    price_label.config(text="Price: Rs. 0")

    selected_price = 0
    selected_name  = ""

    # Ask the user
    again = messagebox.askyesno("Order Added",
        f"Added {qty} × {order_items[-1][0]} (₹{subtotal})\n\n"
        "Do you want to order another coffee?")

    if not again:
        show_final_bill()
# ============================================================
#  RUNNING ORDER DISPLAY
# ============================================================
def show_running_order():
    if not order_items:
        bill_label.config(text="")
        return

    lines = ["🧾  Current Order:"]
    for name, price, qty in order_items:
        lines.append(f"   • {name}  ×{qty}  =  ₹{price * qty}")
    total = sum(p * q for _, p, q in order_items)
    lines.append(f"   ————————")
    lines.append(f"   Subtotal:  ₹{total}")
    bill_label.config(text="\n".join(lines), justify="left")

# ============================================================
#  FINAL BILL POPUP
# ============================================================
def show_final_bill():
    if not order_items:
        messagebox.showinfo("No Order", "Your order is empty!")
        return

    receipt = "☕  VIDYA'S COFFEE HOUSE  ☕\n"
    receipt += "─────────────────────────\n"
    receipt += "         FINAL BILL\n"
    receipt += "─────────────────────────\n\n"

    total = 0
    for name, price, qty in order_items:
        line_total = price * qty
        total += line_total
        receipt += f"{name:<12} ×{qty}    ₹{line_total}\n"

    gst = round(total * 0.05, 2)   # 5% GST (optional)
    grand = round(total + gst, 2)

    receipt += "\n─────────────────────────\n"
    receipt += f"Subtotal:      ₹{total}\n"
    receipt += f"GST (5%):      ₹{gst}\n"
    receipt += "─────────────────────────\n"
    receipt += f"GRAND TOTAL:   ₹{grand}\n"
    receipt += "─────────────────────────\n\n"
    receipt += "   Thank you! Visit again ☕"

    messagebox.showinfo("Final Bill", receipt)

    # Update main window bill label
    bill_label.config(text=f"🧾  Order Complete — Grand Total: ₹{grand}")

    # Clear order for next customer
    order_items.clear()

# ============================================================
#  ADD TO ORDER BUTTON  (main "Generate Bill" replaced)
# ============================================================
tkinter.Button(left_col, text="🧾  Add to Order",
               font=("Georgia", 13, "bold"),
               fg=CREAM, bg=GREEN_OK,
               activebackground="#1B5E20", activeforeground=CREAM,
               width=22, pady=8, bd=0, cursor="hand2",
               command=add_to_order).pack(anchor="w", pady=(15, 8))

bill_label = tkinter.Label(left_col, text="",
                           font=("Georgia", 11, "bold"),
                           fg=BROWN_DARK, bg=GOLD_BILL,
                           padx=15, pady=10,
                           justify="left", anchor="w",
                           highlightbackground=CARAMEL,
                           highlightthickness=2)
bill_label.pack(anchor="w", fill="x", pady=(0, 10))

# ============================================================
#  CLEAR BUTTON
# ============================================================
def clear_all():
    global selected_price, selected_name
    selected_price = 0
    selected_name  = ""
    order_items.clear()
    quantity_entry.delete(0, "end")
    select_lable.config(text="No coffee selected!")
    price_label.config(text="Price: Rs. 0")
    bill_label.config(text="")

tkinter.Button(left_col, text="🗑  Clear Order",
               font=("Georgia", 12, "bold"),
               fg=CREAM, bg=RED_CLEAR,
               activebackground="#7F0000", activeforeground=CREAM,
               width=22, pady=6, bd=0, cursor="hand2",
               command=clear_all).pack(anchor="w")

# ============================================================
#  RIGHT COLUMN — BIG PHOTO
# ============================================================
tkinter.Label(right_col, image=big_photo, bg=CREAM,
              highlightbackground=CARAMEL,
              highlightthickness=3).pack(pady=(5, 15))

tkinter.Label(right_col, text="Brewed to Perfection ☕",
              font=("Georgia", 12, "italic"),
              fg=BROWN_MED, bg=CREAM).pack()

# ============================================================
#  BOTTOM PHOTO
# ============================================================
bottom_frame = tkinter.Frame(window, bg=CREAM,
                             highlightbackground=CARAMEL,
                             highlightthickness=2)
bottom_frame.pack(side="bottom", fill="x", padx=30, pady=(10, 20))

tkinter.Label(bottom_frame, image=bottom_photo, bg=CREAM).pack()

# ============================================================
window.mainloop()
