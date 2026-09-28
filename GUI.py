from Hotel import *
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

# استدعاء الكلاسات والـ Enums من ملف Hotel.py
from Hotel import (
    Hotel, Room, Guest, Reservation, Invoice, Service, ServiceOrder,
    Room_type, StatusRoom, StatusReservation, Membership_type
)

class HotelGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Management System")
        self.geometry("1180x720")
        self.configure(bg="#2c3e50")

        self.hotel = Hotel()

        self.create_sidebar()
        self.create_main_container()
        self.show_dashboard()

    def create_sidebar(self):
        sidebar = tk.Frame(self, bg="#34495e", width=220)
        sidebar.pack(side="left", fill="y")

        lbl_title = tk.Label(sidebar, text="🏨 Hotel System", font=("Segoe UI", 18, "bold"), bg="#34495e", fg="#ecf0f1", pady=20)
        lbl_title.pack()

        buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("🛏️ Rooms", self.show_rooms_page),
            ("👤 Guests", self.show_guests_page),
            ("📅 Reservations", self.show_reservations_page),
            ("🧾 Invoices & Payment", self.show_invoice_page)
        ]

        for text, command in buttons:
            btn = tk.Button(sidebar, text=text, font=("Segoe UI", 12), bg="#2c3e50", fg="white", bd=0,
                            activebackground="#1abc9c", activeforeground="white", anchor="w", padx=20, pady=12, command=command)
            btn.pack(fill="x", pady=2)

    def create_main_container(self):
        self.main_frame = tk.Frame(self, bg="#ecf0f1")
        self.main_frame.pack(side="right", fill="both", expand=True)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ==========================================
    # Validation Methods
    # ==========================================
    @staticmethod
    def phone_number_is_valid(number: str):
        str_num = str(number).strip()
        if str_num.startswith('+') and str_num[1:].isdigit():
            return
        if str_num.isdigit():
            return
        raise ValueError(f"'{number}' is an invalid phone number")

    @staticmethod
    def validate_email(email: str):
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email format (must contain '@' and '.')")

    # ==========================================
    # 1. Dashboard
    # ==========================================
    def show_dashboard(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="System Dashboard", font=("Segoe UI", 18, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(anchor="nw", padx=20, pady=20)

        stats_frame = tk.Frame(self.main_frame, bg="#ecf0f1")
        stats_frame.pack(fill="x", padx=20)

        cards = [
            ("Total Rooms", str(len(self.hotel.rooms)), "#3498db"),
            ("Total Guests", str(len(self.hotel.guests)), "#2ecc71"),
            ("Total Reservations", str(len(self.hotel.reservations)), "#f39c12")
        ]

        for title, val, color in cards:
            card = tk.Frame(stats_frame, bg=color, width=220, height=100, padx=15, pady=15)
            card.pack(side="left", expand=True, fill="both", padx=5)
            tk.Label(card, text=title, font=("Segoe UI", 12), bg=color, fg="white").pack(anchor="w")
            tk.Label(card, text=val, font=("Segoe UI", 22, "bold"), bg=color, fg="white").pack(anchor="e")

    # ==========================================
    # 2. Rooms Management
    # ==========================================
    def show_rooms_page(self):
        self.clear_main_frame()

        header = tk.Frame(self.main_frame, bg="#ecf0f1")
        header.pack(fill="x", padx=20, pady=15)

        tk.Label(header, text="Rooms List", font=("Segoe UI", 16, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(side="left")

        search_frame = tk.Frame(header, bg="#ecf0f1")
        search_frame.pack(side="left", padx=15)

        tk.Label(search_frame, text="Search:", bg="#ecf0f1", font=("Segoe UI", 10)).pack(side="left", padx=2)
        search_entry = tk.Entry(search_frame, font=("Segoe UI", 10), width=12)
        search_entry.pack(side="left", padx=2)

        btn_search = tk.Button(search_frame, text="🔍", bg="#3498db", fg="white", bd=0, padx=8,
                               command=lambda: self.populate_rooms_table(tree, search_entry.get()))
        btn_search.pack(side="left", padx=2)

        btn_delete = tk.Button(header, text="🗑️ Delete", bg="#e74c3c", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=8, pady=5,
                               command=lambda: self.delete_selected_room(tree))
        btn_delete.pack(side="right", padx=3)

        btn_edit = tk.Button(header, text="✏️ Modify", bg="#f39c12", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=8, pady=5,
                              command=lambda: self.open_edit_room_dialog(tree))
        btn_edit.pack(side="right", padx=3)

        btn_add = tk.Button(header, text="+ Add Room", bg="#2ecc71", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=8, pady=5,
                            command=self.open_add_room_dialog)
        btn_add.pack(side="right", padx=3)

        tree_frame = tk.Frame(self.main_frame)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("room_number", "type", "price", "status", "max_occupancy")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        tree.heading("room_number", text="Room #")
        tree.heading("type", text="Room Type")
        tree.heading("price", text="Price / Night")
        tree.heading("status", text="Status")
        tree.heading("max_occupancy", text="Max Occupancy")

        tree.pack(fill="both", expand=True)
        self.populate_rooms_table(tree)

    def populate_rooms_table(self, tree, query=""):
        for item in tree.get_children():
            tree.delete(item)

        query = query.lower().strip()
        for room in self.hotel.rooms.values():
            if query in str(room.room_number).lower() or query in room.room_type.name.lower() or query in room.status.name.lower():
                tree.insert("", "end", values=(room.room_number, room.room_type.name, f"${room.price_per_night:.2f}", room.status.name, room.max_occupancy))

    def delete_selected_room(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a room to delete!")
            return

        room_num = int(tree.item(selected_item)["values"][0])
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Room #{room_num}?"):
            if room_num in self.hotel.rooms:
                del self.hotel.rooms[room_num]
                self.hotel.save_all()
                messagebox.showinfo("Success", f"Room #{room_num} deleted!")
                self.show_rooms_page()

    def open_add_room_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add New Room")
        dialog.geometry("400x450")
        dialog.grab_set()

        next_room_num = self.hotel.generate_next_room_number()
        tk.Label(dialog, text=f"Auto-Generated Room #: {next_room_num}", font=("Segoe UI", 12, "bold"), fg="#2c3e50").pack(anchor="w", padx=20, pady=15)

        tk.Label(dialog, text="Price per Night ($):", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        price_entry = tk.Entry(dialog, font=("Segoe UI", 10))
        price_entry.pack(fill="x", padx=20, pady=5)

        tk.Label(dialog, text="Max Occupancy:", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        occupancy_entry = tk.Entry(dialog, font=("Segoe UI", 10))
        occupancy_entry.insert(0, "2")
        occupancy_entry.pack(fill="x", padx=20, pady=5)

        tk.Label(dialog, text="Room Type:", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        type_cb = ttk.Combobox(dialog, values=[t.name for t in Room_type], state="readonly", font=("Segoe UI", 10))
        type_cb.pack(fill="x", padx=20, pady=5)
        type_cb.current(0)

        def save_room():
            try:
                price = float(price_entry.get().strip())
                if price <= 0:
                    messagebox.showerror("Validation Error", "Price must be greater than 0!")
                    return
                occupancy = int(occupancy_entry.get().strip())
                if occupancy <= 0:
                    messagebox.showerror("Validation Error", "Occupancy must be at least 1!")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Please enter valid numeric values!")
                return

            selected_type = Room_type[type_cb.get().strip()]
            new_room = Room(next_room_num, selected_type, price, max_occupancy=occupancy)
            self.hotel.add_room(new_room)

            messagebox.showinfo("Success", f"Room #{next_room_num} added successfully!")
            dialog.destroy()
            self.show_rooms_page()

        tk.Button(dialog, text="💾 Save Room", bg="#2ecc71", fg="white", font=("Segoe UI", 11, "bold"), bd=0, pady=8, command=save_room).pack(fill="x", padx=20, pady=20)

    def open_edit_room_dialog(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a room to modify!")
            return

        room_num = int(tree.item(selected_item)["values"][0])
        room = self.hotel.rooms.get(room_num)
        if not room:
            return

        dialog = tk.Toplevel(self)
        dialog.title(f"Modify Room #{room_num}")
        dialog.geometry("400x480")
        dialog.grab_set()

        tk.Label(dialog, text=f"Modifying Room #{room_num}", font=("Segoe UI", 12, "bold"), fg="#2c3e50").pack(anchor="w", padx=20, pady=15)

        tk.Label(dialog, text="Price per Night ($):", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        price_entry = tk.Entry(dialog, font=("Segoe UI", 10))
        price_entry.insert(0, str(room.price_per_night))
        price_entry.pack(fill="x", padx=20, pady=5)

        tk.Label(dialog, text="Max Occupancy:", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        occupancy_entry = tk.Entry(dialog, font=("Segoe UI", 10))
        occupancy_entry.insert(0, str(room.max_occupancy))
        occupancy_entry.pack(fill="x", padx=20, pady=5)

        tk.Label(dialog, text="Room Type:", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        type_cb = ttk.Combobox(dialog, values=[t.name for t in Room_type], state="readonly", font=("Segoe UI", 10))
        type_cb.pack(fill="x", padx=20, pady=5)
        type_cb.set(room.room_type.name)

        tk.Label(dialog, text="Status:", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        status_cb = ttk.Combobox(dialog, values=[s.name for s in StatusRoom], state="readonly", font=("Segoe UI", 10))
        status_cb.pack(fill="x", padx=20, pady=5)
        status_cb.set(room.status.name)

        def save_changes():
            try:
                price = float(price_entry.get().strip())
                if price <= 0:
                    messagebox.showerror("Validation Error", "Price must be greater than 0!")
                    return
                occupancy = int(occupancy_entry.get().strip())
                if occupancy <= 0:
                    messagebox.showerror("Validation Error", "Occupancy must be at least 1!")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Please enter valid numeric values!")
                return

            r_type = Room_type[type_cb.get().strip()]
            r_status = StatusRoom[status_cb.get().strip()]

            self.hotel.update_room(room_num, price, occupancy, r_type, r_status)

            messagebox.showinfo("Success", f"Room #{room_num} updated successfully!")
            dialog.destroy()
            self.show_rooms_page()

        tk.Button(dialog, text="💾 Save Changes", bg="#f39c12", fg="white", font=("Segoe UI", 11, "bold"), bd=0, pady=8, command=save_changes).pack(fill="x", padx=20, pady=20)

    # ==========================================
    # 3. Guests Management & Service Orders
    # ==========================================
    def show_guests_page(self):
        self.clear_main_frame()

        header = tk.Frame(self.main_frame, bg="#ecf0f1")
        header.pack(fill="x", padx=20, pady=15)

        tk.Label(header, text="Guest Directory", font=("Segoe UI", 16, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(side="left")

        search_frame = tk.Frame(header, bg="#ecf0f1")
        search_frame.pack(side="left", padx=10)

        tk.Label(search_frame, text="Search:", bg="#ecf0f1", font=("Segoe UI", 10)).pack(side="left", padx=2)
        search_entry = tk.Entry(search_frame, font=("Segoe UI", 10), width=12)
        search_entry.pack(side="left", padx=2)

        btn_search = tk.Button(search_frame, text="🔍", bg="#3498db", fg="white", bd=0, padx=8,
                               command=lambda: self.populate_guests_table(tree, search_entry.get()))
        btn_search.pack(side="left", padx=2)

        btn_delete = tk.Button(header, text="🗑️ Delete", bg="#e74c3c", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=8, pady=5,
                               command=lambda: self.delete_selected_guest(tree))
        btn_delete.pack(side="right", padx=2)

        # تحويل فتح دالة الخدمة لتقرأ العنصر المظلل من الجدول مباشرة
        btn_service = tk.Button(header, text="🛒 Add Service Order", bg="#9b59b6", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=8, pady=5,
                                command=lambda: self.open_add_service_dialog(tree))
        btn_service.pack(side="right", padx=2)

        btn_edit = tk.Button(header, text="✏️ Modify", bg="#f39c12", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=8, pady=5,
                              command=lambda: self.open_edit_guest_dialog(tree))
        btn_edit.pack(side="right", padx=2)

        btn_add = tk.Button(header, text="+ Add Guest", bg="#2ecc71", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=8, pady=5,
                            command=self.open_add_guest_dialog)
        btn_add.pack(side="right", padx=2)

        tree_frame = tk.Frame(self.main_frame)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("id", "name", "email", "phone", "national_id", "membership", "points")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        tree.heading("id", text="Guest ID")
        tree.heading("name", text="Full Name")
        tree.heading("email", text="Email")
        tree.heading("phone", text="Phone")
        tree.heading("national_id", text="National ID/Passport")
        tree.heading("membership", text="Membership")
        tree.heading("points", text="Loyalty Points")

        tree.pack(fill="both", expand=True)
        self.populate_guests_table(tree)

    def populate_guests_table(self, tree, query=""):
        for item in tree.get_children():
            tree.delete(item)

        query = query.lower().strip()
        for guest in self.hotel.guests.values():
            full_name = f"{guest.first_name} {guest.last_name}"
            if query in str(guest.guest_id).lower() or query in full_name.lower() or query in str(guest.email).lower() or query in str(guest.phone).lower():
                tree.insert("", "end", values=(guest.guest_id, full_name, guest.email, guest.phone, guest.national_id_or_passport, guest.membership_type.name, f"{guest.loyalty_points:.1f}"))

    def delete_selected_guest(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a guest to delete!")
            return

        guest_id = int(tree.item(selected_item)["values"][0])
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Guest #{guest_id}?"):
            if guest_id in self.hotel.guests:
                del self.hotel.guests[guest_id]
                self.hotel.save_all()
                messagebox.showinfo("Success", f"Guest #{guest_id} deleted!")
                self.show_guests_page()

    def open_add_guest_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add New Guest")
        dialog.geometry("420x560")
        dialog.grab_set()

        next_guest_id = self.hotel.generate_next_guest_id()
        tk.Label(dialog, text=f"Auto-Generated Guest ID: {next_guest_id}", font=("Segoe UI", 12, "bold"), fg="#2c3e50").pack(anchor="w", padx=20, pady=10)

        fields = [("First Name:", "fname"), ("Last Name:", "lname"), ("Email:", "email"), ("Phone:", "phone"), ("National ID / Passport:", "national_id")]
        entries = {}
        for label, key in fields:
            tk.Label(dialog, text=label, font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=1)
            entry = tk.Entry(dialog, font=("Segoe UI", 10))
            entry.pack(fill="x", padx=20, pady=3)
            entries[key] = entry

        tk.Label(dialog, text="Membership Type:", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=1)
        mem_cb = ttk.Combobox(dialog, values=[m.name for m in Membership_type], state="readonly", font=("Segoe UI", 10))
        mem_cb.pack(fill="x", padx=20, pady=3)
        mem_cb.current(0)

        def save_guest():
            fname = entries["fname"].get().strip()
            lname = entries["lname"].get().strip()
            email = entries["email"].get().strip()
            phone = entries["phone"].get().strip()
            nat_id = entries["national_id"].get().strip()

            if not fname or not lname:
                messagebox.showerror("Validation Error", "First and Last names are required!")
                return
            if not nat_id:
                messagebox.showerror("Validation Error", "National ID / Passport cannot be empty!")
                return

            try:
                self.phone_number_is_valid(phone)
            except ValueError as e:
                messagebox.showerror("Validation Error", str(e))
                return

            try:
                self.validate_email(email)
            except ValueError as e:
                messagebox.showerror("Validation Error", str(e))
                return

            new_guest = Guest(
                guest_id=next_guest_id,
                first_name=fname,
                last_name=lname,
                email=email,
                phone=phone,
                national_id_or_passport=nat_id,
                membership_type=Membership_type[mem_cb.get().strip()],
                loyalty_points=0.0
            )
            self.hotel.register_guest(new_guest)
            messagebox.showinfo("Success", f"Guest #{next_guest_id} registered!")
            dialog.destroy()
            self.show_guests_page()

        tk.Button(dialog, text="💾 Save Guest", bg="#2ecc71", fg="white", font=("Segoe UI", 11, "bold"), bd=0, pady=8, command=save_guest).pack(fill="x", padx=20, pady=15)

    def open_edit_guest_dialog(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a guest to modify!")
            return

        guest_id = int(tree.item(selected_item)["values"][0])
        guest = self.hotel.guests.get(guest_id)
        if not guest:
            return

        dialog = tk.Toplevel(self)
        dialog.title(f"Modify Guest #{guest_id}")
        dialog.geometry("420x560")
        dialog.grab_set()

        tk.Label(dialog, text=f"Modifying Guest #{guest_id}", font=("Segoe UI", 12, "bold"), fg="#2c3e50").pack(anchor="w", padx=20, pady=10)

        fields = [
            ("First Name:", "fname", guest.first_name),
            ("Last Name:", "lname", guest.last_name),
            ("Email:", "email", guest.email),
            ("Phone:", "phone", guest.phone),
            ("National ID / Passport:", "national_id", guest.national_id_or_passport)
        ]
        entries = {}
        for label, key, val in fields:
            tk.Label(dialog, text=label, font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=1)
            entry = tk.Entry(dialog, font=("Segoe UI", 10))
            entry.insert(0, str(val))
            entry.pack(fill="x", padx=20, pady=3)
            entries[key] = entry

        tk.Label(dialog, text="Membership Type:", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=1)
        mem_cb = ttk.Combobox(dialog, values=[m.name for m in Membership_type], state="readonly", font=("Segoe UI", 10))
        mem_cb.pack(fill="x", padx=20, pady=3)
        mem_cb.set(guest.membership_type.name)

        def save_changes():
            fname = entries["fname"].get().strip()
            lname = entries["lname"].get().strip()
            email = entries["email"].get().strip()
            phone = entries["phone"].get().strip()
            nat_id = entries["national_id"].get().strip()

            if not fname or not lname:
                messagebox.showerror("Validation Error", "First and Last names are required!")
                return
            if not nat_id:
                messagebox.showerror("Validation Error", "National ID / Passport cannot be empty!")
                return

            try:
                self.phone_number_is_valid(phone)
            except ValueError as e:
                messagebox.showerror("Validation Error", str(e))
                return

            try:
                self.validate_email(email)
            except ValueError as e:
                messagebox.showerror("Validation Error", str(e))
                return

            guest.first_name = fname
            guest.last_name = lname
            guest.email = email
            guest.phone = phone
            guest.national_id_or_passport = nat_id
            guest.membership_type = Membership_type[mem_cb.get().strip()]

            self.hotel.save_all()
            messagebox.showinfo("Success", f"Guest #{guest_id} updated!")
            dialog.destroy()
            self.show_guests_page()

        tk.Button(dialog, text="💾 Save Changes", bg="#f39c12", fg="white", font=("Segoe UI", 11, "bold"), bd=0, pady=8, command=save_changes).pack(fill="x", padx=20, pady=15)

    def open_add_service_dialog(self, tree):
        # 1. التحقق من تحديد النزيل في الجدول أولاً
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a guest from the list first to add a service order!")
            return

        guest_id = int(tree.item(selected_item)["values"][0])
        selected_guest = self.hotel.guests.get(guest_id)

        if not selected_guest:
            messagebox.showerror("Error", "Selected guest not found!")
            return

        # 2. التحقق من وجود حجز قائم وغير ملغى للنزيل المظلل والمحدد فقط
        active_res = next(
            (r for r in self.hotel.reservations.values()
             if r.guest.guest_id == selected_guest.guest_id and r.status != StatusReservation.CANCELLED),
            None
        )

        if not active_res:
            messagebox.showerror("Error", f"Guest '{selected_guest.first_name} {selected_guest.last_name}' has no active reservation!")
            return

        # 3. فتح النافذة بملف النزيل المحدد مسبقاً
        dialog = tk.Toplevel(self)
        dialog.title(f"Add Service Order - Guest #{guest_id}")
        dialog.geometry("450x420")
        dialog.grab_set()

        tk.Label(dialog, text=f"Add Service Order for {selected_guest.first_name} {selected_guest.last_name}", 
                 font=("Segoe UI", 11, "bold"), fg="#2c3e50").pack(anchor="w", padx=20, pady=10)

        tk.Label(dialog, text=f"Active Reservation ID: #{active_res.reservation_id} (Room #{active_res.room.room_number})", 
                 font=("Segoe UI", 10, "italic"), fg="#7f8c8d").pack(anchor="w", padx=20, pady=2)

        tk.Label(dialog, text="Service Name (e.g., Room Service, Spa):", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=5)
        srv_name_entry = tk.Entry(dialog, font=("Segoe UI", 10))
        srv_name_entry.pack(fill="x", padx=20, pady=3)

        tk.Label(dialog, text="Price per unit ($):", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=5)
        srv_price_entry = tk.Entry(dialog, font=("Segoe UI", 10))
        srv_price_entry.pack(fill="x", padx=20, pady=3)

        tk.Label(dialog, text="Quantity:", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=5)
        srv_qty_entry = tk.Entry(dialog, font=("Segoe UI", 10))
        srv_qty_entry.insert(0, "1")
        srv_qty_entry.pack(fill="x", padx=20, pady=3)

        def add_service():
            s_name = srv_name_entry.get().strip()
            if not s_name:
                messagebox.showerror("Validation Error", "Service name is required!")
                return

            try:
                s_price = float(srv_price_entry.get().strip())
                if s_price <= 0:
                    messagebox.showerror("Validation Error", "Service price must be greater than 0!")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Please enter a valid numeric price!")
                return

            try:
                s_qty = int(srv_qty_entry.get().strip())
                if s_qty <= 0:
                    messagebox.showerror("Validation Error", "Quantity must be at least 1!")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Please enter a valid integer for quantity!")
                return

            # ربط الخدمة بالحجز القائم للنزيل المحدد فقط
            srv_id = len(getattr(selected_guest, 'service_orders', [])) + 1
            srv = Service(service_id=srv_id, service_name=s_name, price=s_price)
            order = ServiceOrder(order_id=srv_id, reservation_id=active_res.reservation_id, service=srv, quantity=s_qty)

            selected_guest.add_service_order(order)
            self.hotel.save_all()

            messagebox.showinfo("Success", f"Service order added for {selected_guest.first_name}! Total: ${s_price * s_qty:.2f}")
            dialog.destroy()

        tk.Button(dialog, text="🛒 Add Service Order", bg="#9b59b6", fg="white", font=("Segoe UI", 11, "bold"), bd=0, pady=8, command=add_service).pack(fill="x", padx=20, pady=20)

    # ==========================================
    # 4. Reservations Management
    # ==========================================
    def show_reservations_page(self):
        self.clear_main_frame()

        header = tk.Frame(self.main_frame, bg="#ecf0f1")
        header.pack(fill="x", padx=20, pady=15)

        tk.Label(header, text="Reservations List", font=("Segoe UI", 16, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(side="left")

        search_frame = tk.Frame(header, bg="#ecf0f1")
        search_frame.pack(side="left", padx=10)

        tk.Label(search_frame, text="Search:", bg="#ecf0f1", font=("Segoe UI", 10)).pack(side="left", padx=2)
        search_entry = tk.Entry(search_frame, font=("Segoe UI", 10), width=12)
        search_entry.pack(side="left", padx=2)

        btn_search = tk.Button(search_frame, text="🔍", bg="#3498db", fg="white", bd=0, padx=8,
                               command=lambda: self.populate_reservations_table(tree, search_entry.get()))
        btn_search.pack(side="left", padx=2)

        btn_delete = tk.Button(header, text="🗑️ Delete", bg="#e74c3c", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=8, pady=5,
                               command=lambda: self.delete_selected_reservation(tree))
        btn_delete.pack(side="right", padx=2)

        btn_edit = tk.Button(header, text="✏️ Modify", bg="#f39c12", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=8, pady=5,
                              command=lambda: self.open_edit_reservation_dialog(tree))
        btn_edit.pack(side="right", padx=2)

        btn_add = tk.Button(header, text="+ Add Reservation", bg="#2ecc71", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=8, pady=5,
                            command=self.open_add_reservation_dialog)
        btn_add.pack(side="right", padx=2)

        tree_frame = tk.Frame(self.main_frame)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("res_id", "guest", "room", "check_in", "check_out", "status")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        tree.heading("res_id", text="Res ID")
        tree.heading("guest", text="Guest Name")
        tree.heading("room", text="Room #")
        tree.heading("check_in", text="Check-In")
        tree.heading("check_out", text="Check-Out")
        tree.heading("status", text="Status")

        tree.pack(fill="both", expand=True)
        self.populate_reservations_table(tree)

    def populate_reservations_table(self, tree, query=""):
        for item in tree.get_children():
            tree.delete(item)

        query = query.lower().strip()
        for res in self.hotel.reservations.values():
            guest_name = f"{res.guest.first_name} {res.guest.last_name}"
            if (query in str(res.reservation_id).lower() or query in guest_name.lower() or
                query in str(res.room.room_number).lower() or query in res.status.name.lower()):
                tree.insert("", "end", values=(res.reservation_id, guest_name, res.room.room_number, res.check_in_date.strftime("%Y-%m-%d"), res.check_out_date.strftime("%Y-%m-%d"), res.status.name))

    def delete_selected_reservation(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a reservation to delete!")
            return

        res_id = int(tree.item(selected_item)["values"][0])
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Reservation #{res_id}?"):
            if res_id in self.hotel.reservations:
                del self.hotel.reservations[res_id]
                self.hotel.save_all()
                messagebox.showinfo("Success", f"Reservation #{res_id} deleted!")
                self.show_reservations_page()

    def open_add_reservation_dialog(self):
        if not self.hotel.guests or not self.hotel.rooms:
            messagebox.showwarning("Warning", "Please add Guests and Rooms first!")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Add New Reservation")
        dialog.geometry("450x500")
        dialog.grab_set()

        next_res_id = self.hotel.generate_next_reservation_id()
        tk.Label(dialog, text=f"Auto-Generated Res ID: {next_res_id}", font=("Segoe UI", 12, "bold"), fg="#2c3e50").pack(anchor="w", padx=20, pady=10)

        guests_dict = {f"{g.guest_id} - {g.first_name} {g.last_name}": g.guest_id for g in self.hotel.guests.values()}
        tk.Label(dialog, text="Select Guest:", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        guest_cb = ttk.Combobox(dialog, values=list(guests_dict.keys()), state="readonly", font=("Segoe UI", 10))
        guest_cb.pack(fill="x", padx=20, pady=3)
        guest_cb.current(0)

        rooms_dict = {f"Room #{r.room_number} ({r.room_type.name})": r.room_number for r in self.hotel.rooms.values()}
        tk.Label(dialog, text="Select Room:", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        room_cb = ttk.Combobox(dialog, values=list(rooms_dict.keys()), state="readonly", font=("Segoe UI", 10))
        room_cb.pack(fill="x", padx=20, pady=3)
        room_cb.current(0)

        today_str = date.today().strftime("%Y-%m-%d")
        tk.Label(dialog, text="Check-In Date (YYYY-MM-DD):", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        cin_entry = tk.Entry(dialog, font=("Segoe UI", 10))
        cin_entry.insert(0, today_str)
        cin_entry.pack(fill="x", padx=20, pady=3)

        tk.Label(dialog, text="Check-Out Date (YYYY-MM-DD):", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        cout_entry = tk.Entry(dialog, font=("Segoe UI", 10))
        cout_entry.insert(0, today_str)
        cout_entry.pack(fill="x", padx=20, pady=3)

        tk.Label(dialog, text="Number of Guests:", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        guests_num_entry = tk.Entry(dialog, font=("Segoe UI", 10))
        guests_num_entry.insert(0, "1")
        guests_num_entry.pack(fill="x", padx=20, pady=3)

        def save_reservation():
            try:
                cin = datetime.strptime(cin_entry.get().strip(), "%Y-%m-%d").date()
                cout = datetime.strptime(cout_entry.get().strip(), "%Y-%m-%d").date()
                if cout <= cin:
                    messagebox.showerror("Validation Error", "Check-Out Date must be after Check-In Date!")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid Date Format! Please use YYYY-MM-DD.")
                return

            try:
                num_g = int(guests_num_entry.get().strip())
                if num_g <= 0:
                    messagebox.showerror("Validation Error", "Number of guests must be at least 1!")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Please enter a valid integer for number of guests!")
                return

            try:
                res = self.hotel.create_reservation(
                    guest_id=guests_dict[guest_cb.get()],
                    room_number=rooms_dict[room_cb.get()],
                    check_in_date=cin,
                    check_out_date=cout,
                    number_of_guests=num_g
                )
                messagebox.showinfo("Success", f"Reservation #{res.reservation_id} saved!")
                dialog.destroy()
                self.show_reservations_page()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create reservation: {e}")

        tk.Button(dialog, text="💾 Save Reservation", bg="#2ecc71", fg="white", font=("Segoe UI", 11, "bold"), bd=0, pady=8, command=save_reservation).pack(fill="x", padx=20, pady=15)

    def open_edit_reservation_dialog(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a reservation to modify!")
            return

        res_id = int(tree.item(selected_item)["values"][0])
        res = self.hotel.reservations.get(res_id)
        if not res:
            return

        dialog = tk.Toplevel(self)
        dialog.title(f"Modify Reservation #{res_id}")
        dialog.geometry("450x500")
        dialog.grab_set()

        tk.Label(dialog, text=f"Modifying Reservation #{res_id}", font=("Segoe UI", 12, "bold"), fg="#2c3e50").pack(anchor="w", padx=20, pady=10)

        tk.Label(dialog, text="Check-In Date (YYYY-MM-DD):", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        cin_entry = tk.Entry(dialog, font=("Segoe UI", 10))
        cin_entry.insert(0, res.check_in_date.strftime("%Y-%m-%d"))
        cin_entry.pack(fill="x", padx=20, pady=3)

        tk.Label(dialog, text="Check-Out Date (YYYY-MM-DD):", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        cout_entry = tk.Entry(dialog, font=("Segoe UI", 10))
        cout_entry.insert(0, res.check_out_date.strftime("%Y-%m-%d"))
        cout_entry.pack(fill="x", padx=20, pady=3)

        tk.Label(dialog, text="Number of Guests:", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        guests_num_entry = tk.Entry(dialog, font=("Segoe UI", 10))
        guests_num_entry.insert(0, str(res.number_of_guests))
        guests_num_entry.pack(fill="x", padx=20, pady=3)

        tk.Label(dialog, text="Status:", font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=2)
        status_cb = ttk.Combobox(dialog, values=[s.name for s in StatusReservation], state="readonly", font=("Segoe UI", 10))
        status_cb.pack(fill="x", padx=20, pady=3)
        status_cb.set(res.status.name)

        def save_changes():
            try:
                cin = datetime.strptime(cin_entry.get().strip(), "%Y-%m-%d").date()
                cout = datetime.strptime(cout_entry.get().strip(), "%Y-%m-%d").date()
                if cout <= cin:
                    messagebox.showerror("Validation Error", "Check-Out Date must be after Check-In Date!")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid Date Format! Please use YYYY-MM-DD.")
                return

            try:
                num_g = int(guests_num_entry.get().strip())
                if num_g <= 0:
                    messagebox.showerror("Validation Error", "Number of guests must be at least 1!")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Please enter a valid integer for number of guests!")
                return

            status_enum = StatusReservation[status_cb.get().strip()]
            self.hotel.update_reservation(res_id, cin, cout, num_g, status_enum)

            messagebox.showinfo("Success", f"Reservation #{res_id} updated!")
            dialog.destroy()
            self.show_reservations_page()

        tk.Button(dialog, text="💾 Save Changes", bg="#f39c12", fg="white", font=("Segoe UI", 11, "bold"), bd=0, pady=8, command=save_changes).pack(fill="x", padx=20, pady=15)

    # ==========================================
    # 5. Invoices & Payments
    # ==========================================
    def show_invoice_page(self):
        self.clear_main_frame()

        header = tk.Frame(self.main_frame, bg="#ecf0f1")
        header.pack(fill="x", padx=20, pady=15)

        tk.Label(header, text="Invoices & Payments", font=("Segoe UI", 16, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(side="left")

        if not self.hotel.reservations:
            tk.Label(self.main_frame, text="No reservations available to generate invoices.", font=("Segoe UI", 12), bg="#ecf0f1", fg="#7f8c8d").pack(anchor="w", padx=20, pady=20)
            return

        content_frame = tk.Frame(self.main_frame, bg="#ecf0f1")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        left_frame = tk.Frame(content_frame, bg="#ffffff", bd=1, relief="solid")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left_frame, text="Select Reservation:", font=("Segoe UI", 11, "bold"), bg="#ffffff").pack(anchor="w", padx=10, pady=10)

        res_tree = ttk.Treeview(left_frame, columns=("id", "guest", "room"), show="headings", height=12)
        res_tree.heading("id", text="ID")
        res_tree.heading("guest", text="Guest")
        res_tree.heading("room", text="Room")
        res_tree.column("id", width=40)
        res_tree.column("guest", width=120)
        res_tree.column("room", width=50)
        res_tree.pack(fill="both", expand=True, padx=10, pady=5)

        for res in self.hotel.reservations.values():
            res_tree.insert("", "end", values=(res.reservation_id, f"{res.guest.first_name} {res.guest.last_name}", res.room.room_number))

        right_frame = tk.Frame(content_frame, bg="#ffffff", bd=1, relief="solid")
        right_frame.pack(side="right", fill="both", expand=True)

        tk.Label(right_frame, text="Invoice Summary", font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#2c3e50").pack(anchor="w", padx=15, pady=10)

        details_lbl = tk.Label(right_frame, text="Select a reservation from the left table to calculate total.", font=("Segoe UI", 10), bg="#ffffff", justify="left")
        details_lbl.pack(anchor="w", padx=15, pady=10)

        def on_select_reservation(event):
            selected = res_tree.selection()
            if not selected:
                return
            res_id = int(res_tree.item(selected[0])["values"][0])
            reservation = self.hotel.reservations.get(res_id)

            if reservation:
                inv = Invoice(reservation)
                room_sub = inv.calculate_room_subtotal()
                srv_sub = inv.calculate_services_subtotal()
                subtotal = inv.calculate_subtotal()
                discount = inv.calculate_discount()
                tax = inv.calculate_tax()
                grand_total = inv.calculate_grand_total()

                services_text = ""
                guest_orders = [o for o in getattr(reservation.guest, 'service_orders', []) if o.reservation_id == res_id]
                if guest_orders:
                    services_text = "\n--- Ordered Services ---\n"
                    for o in guest_orders:
                        services_text += f" • {o.service.service_name} (x{o.quantity}): ${o.service.price * o.quantity:.2f}\n"

                text = (
                    f"Reservation ID: #{reservation.reservation_id}\n"
                    f"Guest Name: {reservation.guest.first_name} {reservation.guest.last_name}\n"
                    f"Room Number: #{reservation.room.room_number}\n"
                    f"----------------------------------------\n"
                    f"Room Cost: ${room_sub:.2f}\n"
                    f"Services Cost: ${srv_sub:.2f}\n"
                    f"{services_text}"
                    f"----------------------------------------\n"
                    f"Subtotal: ${subtotal:.2f}\n"
                    f"Membership Discount: -${discount:.2f}\n"
                    f"Tax (14%): +${tax:.2f}\n"
                    f"----------------------------------------\n"
                    f"Grand Total: ${grand_total:.2f}"
                )
                details_lbl.config(text=text)

        res_tree.bind("<<TreeviewSelect>>", on_select_reservation)


if __name__ == "__main__":
    app = HotelGUI()
    app.mainloop()