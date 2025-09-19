import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from queue_backend import OrderQueue
from linked_list_backend import GroceryLinkedList
from storage import save_data, load_data


class InventorySystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("800x600")

        self.order_queue = OrderQueue()
        loaded_queue, loaded_items = load_data()
        self.order_queue.queue = loaded_queue
        self.orders_items = loaded_items

        self.frames = {}

        for F in (LandingPage, OrderInputPage, OrderDetailPage, ViewOrdersPage):
            frame = F(self.root, self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame(LandingPage)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()


class CustomStyle(ttk.Style):
    def __init__(self):
        super().__init__()
        self.theme_use("clam")

        self.configure("Custom.TButton",
                       font=("Helvetica", 10, "bold"),
                       foreground="#ffffff",
                       background="#4CAF50",
                       padding=6)
        self.map("Custom.TButton",
                 foreground=[("active", "#ffffff")],
                 background=[("!disabled", "#4CAF50"), ("active", "#45a049")])

        self.configure("Danger.TButton",
                       font=("Helvetica", 10, "bold"),
                       foreground="#ffffff",
                       background="#f44336",
                       padding=6)
        self.map("Danger.TButton",
                 foreground=[("active", "#ffffff")],
                 background=[("!disabled", "#f44336"), ("active", "#d32f2f")])

class LandingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f2f2f2")
        self.controller = controller

        header = tk.Label(self, text="📦 Inventory Management System", font=("Segoe UI", 30, "bold"), bg="#f2f2f2", fg="#2c3e50")
        header.pack(pady=(80, 30))
        header.configure(highlightbackground="#2c3e50", highlightthickness=2)

        ttk.Button(self, text="🚀 Get Started", style="Custom.TButton", command=lambda: controller.show_frame(OrderInputPage)).pack(pady=15)
        ttk.Button(self, text="ℹ️ Learn More", style="Custom.TButton", command=self.show_info).pack()

    def show_info(self):
        messagebox.showinfo("About", "This is an inventory system using Queues and Linked Lists for DSA demonstration.")


class OrderInputPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller

        tk.Label(self, text="📋 Enter Number of Orders", font=("Helvetica", 18, "bold"), bg="#ffffff").pack(pady=30)

        self.order_entry = ttk.Entry(self, font=("Helvetica", 14), justify="center", width=15)
        self.order_entry.pack(pady=10)

        ttk.Button(self, text="Submit Orders", style="Custom.TButton", command=self.store_orders).pack(pady=10)
        ttk.Button(self, text="⬅️ Back", style="Custom.TButton", command=lambda: controller.show_frame(LandingPage)).pack(pady=5)

    def store_orders(self):
        num_orders = self.order_entry.get()
        if not num_orders.isdigit():
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        num_orders = int(num_orders)
        self.controller.order_queue.queue.clear()
        self.controller.orders_items.clear()

        for i in range(1, num_orders + 1):
            order_id = f"Order {i}"
            self.controller.order_queue.enqueue(order_id)
            self.controller.orders_items[order_id] = GroceryLinkedList()

        messagebox.showinfo("Success", f"{num_orders} orders added to the queue.")

        self.controller.frames[OrderDetailPage].set_order(self.controller.order_queue.peek())
        self.controller.show_frame(OrderDetailPage)


class OrderDetailPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f9f9f9")
        self.controller = controller
        self.current_order = None

        CustomStyle()

        tk.Label(self, text="🛒 Order Details", font=("Helvetica", 20, "bold"), bg="#f9f9f9").pack(pady=10)

        self.order_label = tk.Label(self, text="", font=("Helvetica", 16), bg="#f9f9f9", fg="#333")
        self.order_label.pack(pady=5)

        input_frame = tk.Frame(self, bg="#f9f9f9")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Item Name:", font=("Helvetica", 12), bg="#f9f9f9").grid(row=0, column=0, padx=5)
        self.item_name_entry = ttk.Entry(input_frame, width=15)
        self.item_name_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Quantity:", font=("Helvetica", 12), bg="#f9f9f9").grid(row=0, column=2, padx=5)
        self.quantity_entry = ttk.Entry(input_frame, width=10)
        self.quantity_entry.grid(row=0, column=3, padx=5)

        ttk.Button(input_frame, text="➕ Add", style="Custom.TButton", command=self.add_item).grid(row=0, column=4, padx=5)
        ttk.Button(input_frame, text="🔁 Update", style="Custom.TButton", command=self.update_item).grid(row=0, column=5, padx=5)
        ttk.Button(input_frame, text="❌ Delete", style="Danger.TButton", command=self.delete_item).grid(row=0, column=6, padx=5)

        self.items_listbox = tk.Listbox(self, width=60, height=10, font=("Courier", 11), bg="#e8f5e9", fg="#1b5e20", bd=2, relief="groove")
        self.items_listbox.pack(pady=10)

        self.feedback_label = tk.Label(self, text="", font=("Helvetica", 10), bg="#f9f9f9", fg="green")
        self.feedback_label.pack()

        nav_frame = tk.Frame(self, bg="#f9f9f9")
        nav_frame.pack(pady=10)

        self.prev_btn = ttk.Button(nav_frame, text="⬅️ Previous", style="Custom.TButton", command=self.prev_order)
        self.prev_btn.grid(row=0, column=0, padx=10)

        self.next_btn = ttk.Button(nav_frame, text="Next ➡️", style="Custom.TButton", command=self.next_order)
        self.next_btn.grid(row=0, column=1, padx=10)

        ttk.Button(nav_frame, text="🏠 Home", style="Custom.TButton", command=lambda: controller.show_frame(LandingPage)).grid(row=0, column=2, padx=10)
        ttk.Button(nav_frame, text="💾 Save", style="Custom.TButton", command=self.save_all).grid(row=0, column=3, padx=10)
        ttk.Button(nav_frame, text="📁 View All Orders", style="Custom.TButton", command=self.view_all_orders).grid(row=0, column=4, padx=10)

    def set_order(self, order_id):
        self.current_order = order_id
        self.order_label.config(text=f"Currently Editing: {order_id}")
        self.refresh_items()
        self.update_nav_buttons()

    def refresh_items(self):
        self.items_listbox.delete(0, tk.END)
        linked_list = self.controller.orders_items.get(self.current_order)
        if linked_list:
            for item_name, qty in linked_list.view_items():
                self.items_listbox.insert(tk.END, f"{item_name:<20} : {qty}")
        self.feedback_label.config(text="")

    def update_nav_buttons(self):
        queue = self.controller.order_queue.queue
        idx = queue.index(self.current_order) if self.current_order in queue else -1
        self.prev_btn.config(state="normal" if idx > 0 else "disabled")
        self.next_btn.config(state="normal" if idx < len(queue) - 1 else "disabled")

    def add_item(self):
        name = self.item_name_entry.get().strip()
        qty = self.quantity_entry.get().strip()
        if not name or not qty.isdigit():
            self.feedback_label.config(text="❗ Invalid name or quantity.", fg="red")
            return

        linked_list = self.controller.orders_items.get(self.current_order)
        if linked_list:
            linked_list.add_item(name, int(qty))
            self.refresh_items()
            self.feedback_label.config(text=f"✅ Added '{name}' with qty {qty}.", fg="green")
            self.item_name_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)

    def delete_item(self):
        name = self.item_name_entry.get().strip()
        if not name:
            self.feedback_label.config(text="❗ Enter item name to delete.", fg="red")
            return

        linked_list = self.controller.orders_items.get(self.current_order)
        if linked_list:
            if linked_list.delete_item(name):
                self.feedback_label.config(text=f"✅ Deleted '{name}'.", fg="green")
            else:
                self.feedback_label.config(text=f"❗ '{name}' not found.", fg="orange")
            self.refresh_items()

    def update_item(self):
        name = self.item_name_entry.get().strip()
        qty = self.quantity_entry.get().strip()
        if not name or not qty.isdigit():
            self.feedback_label.config(text="❗ Invalid name or quantity.", fg="red")
            return

        linked_list = self.controller.orders_items.get(self.current_order)
        if linked_list:
            if linked_list.update_item(name, int(qty)):
                self.feedback_label.config(text=f"✅ Updated '{name}' to qty {qty}.", fg="green")
            else:
                self.feedback_label.config(text=f"❗ '{name}' not found.", fg="orange")
            self.refresh_items()

    def next_order(self):
        queue = self.controller.order_queue.queue
        idx = queue.index(self.current_order)
        if idx < len(queue) - 1:
            self.set_order(queue[idx + 1])

    def prev_order(self):
        queue = self.controller.order_queue.queue
        idx = queue.index(self.current_order)
        if idx > 0:
            self.set_order(queue[idx - 1])

    def save_all(self):
        save_data(self.controller.order_queue, self.controller.orders_items)
        self.feedback_label.config(text="✅ Data saved successfully!", fg="blue")

    def view_all_orders(self):
        self.controller.frames[ViewOrdersPage].refresh_order_data()
        self.controller.show_frame(ViewOrdersPage)


class ViewOrdersPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#fdfdfd")
        self.controller = controller

        tk.Label(self, text="📆 All Ordered Items", font=("Helvetica", 20, "bold"), bg="#fdfdfd").pack(pady=10)

        self.orders_text = tk.Text(self, width=80, height=25, font=("Courier", 11), bg="#fffde7", fg="#3e2723")
        self.orders_text.pack(pady=10)

        ttk.Button(self, text="⬅️ Back", style="Custom.TButton", command=lambda: controller.show_frame(OrderDetailPage)).pack(pady=5)

    def refresh_order_data(self):
        self.orders_text.delete(1.0, tk.END)
        for order_id, linked_list in self.controller.orders_items.items():
            self.orders_text.insert(tk.END, f"{order_id}:")
            self.orders_text.insert(tk.END, "\n")
            for item_name, qty in linked_list.view_items():
                self.orders_text.insert(tk.END, f"  - {item_name}: {qty}\n")
            self.orders_text.insert(tk.END, "\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = InventorySystemApp(root)
    root.mainloop()
