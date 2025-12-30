#!/usr/bin/env python3
"""
BOOKNEST Receipt Generator - GUI Version
A graphical interface to generate book order receipts
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from datetime import datetime
from typing import List
from PIL import Image, ImageDraw, ImageFont
import io


class BookOrder:
    def __init__(self, title: str, format: str, quantity: int, price: float):
        self.title = title
        self.format = format
        self.quantity = quantity
        self.price = price
    
    def get_total(self):
        return self.price * self.quantity


class BookNestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 BOOKNEST Receipt Generator")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a1a")
        
        self.orders = []
        
        # Set style
        self.setup_style()
        self.create_widgets()
    
    def setup_style(self):
        """Setup custom styles"""
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure frame styles
        style.configure('Card.TLabelframe', background='#2d2d2d', foreground='#ffffff', 
                       borderwidth=2, relief='flat')
        style.configure('Card.TLabelframe.Label', background='#2d2d2d', foreground='#ffd700',
                       font=('Helvetica', 11, 'bold'))
        
        # Configure label styles
        style.configure('TLabel', background='#2d2d2d', foreground='#ffffff',
                       font=('Helvetica', 10))
        
        # Configure entry styles
        style.configure('TEntry', fieldbackground='#3d3d3d', foreground='#ffffff',
                       insertcolor='#ffffff', borderwidth=1)
        
        style.configure('TFrame', background='#2d2d2d')
    
    def create_widgets(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg='#1a1a1a', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(main_frame, bg='#ffd700', height=80)
        header.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(header, text="📚 BOOKNEST", 
                              font=("Helvetica", 28, "bold"), 
                              bg="#ffd700", fg="#1a1a1a")
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(header, text="RECEIPT GENERATOR", 
                                 font=("Helvetica", 12), 
                                 bg="#ffd700", fg="#1a1a1a")
        subtitle_label.pack()
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg='#1a1a1a')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== BOOK ORDER SECTION =====
        book_frame = ttk.LabelFrame(content_frame, text="📖 BOOK ORDER", 
                                   style='Card.TLabelframe', padding=15)
        book_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Book Title
        ttk.Label(book_frame, text="Book Title:").grid(row=0, column=0, sticky=tk.W, pady=8, padx=5)
        self.title_entry = ttk.Entry(book_frame, width=50, font=('Helvetica', 10))
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=5)
        
        # Format, Quantity, Price in one row
        details_frame = tk.Frame(book_frame, bg='#2d2d2d')
        details_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Format
        ttk.Label(details_frame, text="Format:").pack(side=tk.LEFT, padx=5)
        self.format_entry = ttk.Entry(details_frame, width=8, font=('Helvetica', 10))
        self.format_entry.pack(side=tk.LEFT, padx=5)
        self.format_entry.insert(0, "PB")
        
        # Quantity
        ttk.Label(details_frame, text="Qty:").pack(side=tk.LEFT, padx=(20, 5))
        self.quantity_entry = ttk.Entry(details_frame, width=8, font=('Helvetica', 10))
        self.quantity_entry.pack(side=tk.LEFT, padx=5)
        self.quantity_entry.insert(0, "1")
        
        # Price
        ttk.Label(details_frame, text="Price (₱):").pack(side=tk.LEFT, padx=(20, 5))
        self.price_entry = ttk.Entry(details_frame, width=12, font=('Helvetica', 10))
        self.price_entry.pack(side=tk.LEFT, padx=5)
        
        # Add Book Button
        add_book_btn = tk.Button(book_frame, text="➕ Add Book to Receipt", 
                                command=self.add_book,
                                bg="#4CAF50", fg="white", 
                                font=("Helvetica", 10, "bold"),
                                padx=15, pady=8, cursor="hand2",
                                relief=tk.FLAT, borderwidth=0,
                                activebackground="#66BB6A", activeforeground="white")
        add_book_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Books List
        list_label = ttk.Label(book_frame, text="📚 Books in this receipt:", 
                              font=("Helvetica", 10, "bold"))
        list_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        list_frame = tk.Frame(book_frame, bg='#2d2d2d')
        list_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        scrollbar = tk.Scrollbar(list_frame, bg='#3d3d3d')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.books_listbox = tk.Listbox(list_frame, height=5, 
                                        font=('Courier', 9),
                                        bg='#3d3d3d', fg='#ffffff',
                                        selectbackground='#ffd700',
                                        selectforeground='#1a1a1a',
                                        yscrollcommand=scrollbar.set)
        self.books_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.books_listbox.yview)
        
        # Remove and Clear buttons
        btn_frame = tk.Frame(book_frame, bg='#2d2d2d')
        btn_frame.grid(row=5, column=0, columnspan=2, pady=8)
        
        remove_btn = tk.Button(btn_frame, text="🗑️ Remove Selected", 
                              command=self.remove_book,
                              bg="#e74c3c", fg="white", 
                              font=("Helvetica", 9),
                              padx=10, pady=5, cursor="hand2",
                              relief=tk.FLAT, borderwidth=0,
                              activebackground="#e57373", activeforeground="white")
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(btn_frame, text="🔄 Clear All", 
                             command=self.clear_all_books,
                             bg="#9E9E9E", fg="white", 
                             font=("Helvetica", 9),
                             padx=10, pady=5, cursor="hand2",
                             relief=tk.FLAT, borderwidth=0,
                             activebackground="#BDBDBD", activeforeground="white")
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        book_frame.columnconfigure(1, weight=1)
        
        # ===== CUSTOMER INFO SECTION =====
        customer_frame = ttk.LabelFrame(content_frame, text="👤 CUSTOMER INFO", 
                                       style='Card.TLabelframe', padding=15)
        customer_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Name
        ttk.Label(customer_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=8, padx=5)
        self.name_entry = ttk.Entry(customer_frame, width=50, font=('Helvetica', 10))
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=5)
        
        # Address
        ttk.Label(customer_frame, text="Address:").grid(row=1, column=0, sticky=tk.W, pady=8, padx=5)
        self.address_entry = ttk.Entry(customer_frame, width=50, font=('Helvetica', 10))
        self.address_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=5)
        
        # Phone
        ttk.Label(customer_frame, text="Phone:").grid(row=2, column=0, sticky=tk.W, pady=8, padx=5)
        self.phone_entry = ttk.Entry(customer_frame, width=50, font=('Helvetica', 10))
        self.phone_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=5)
        
        customer_frame.columnconfigure(1, weight=1)
        
        # ===== PAYMENT SECTION =====
        payment_frame = ttk.LabelFrame(content_frame, text="💳 PAYMENT METHOD", 
                                      style='Card.TLabelframe', padding=15)
        payment_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(payment_frame, text="GCash Number:").grid(row=0, column=0, sticky=tk.W, pady=8, padx=5)
        self.payment_entry = ttk.Entry(payment_frame, width=50, font=('Helvetica', 10))
        self.payment_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=5)
        self.payment_entry.insert(0, "09164097987")
        
        ttk.Label(payment_frame, text="Shipping Fee (₱):").grid(row=1, column=0, sticky=tk.W, pady=8, padx=5)
        self.shipping_entry = ttk.Entry(payment_frame, width=50, font=('Helvetica', 10))
        self.shipping_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=5)
        self.shipping_entry.insert(0, "0")
        
        ttk.Label(payment_frame, text="(Leave 0 for +SF)", font=('Helvetica', 8, 'italic')).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        payment_frame.columnconfigure(1, weight=1)
        
        # ===== GENERATE BUTTON =====
        button_frame = tk.Frame(content_frame, bg='#1a1a1a')
        button_frame.pack(fill=tk.X, pady=10)
        
        generate_btn = tk.Button(button_frame, text="🧾 GENERATE RECEIPT", 
                                command=self.generate_receipt,
                                bg="#ffd700", fg="#1a1a1a", 
                                font=("Helvetica", 16, "bold"),
                                padx=30, pady=15, cursor="hand2",
                                relief=tk.FLAT, borderwidth=0,
                                activebackground="#ffed4e", activeforeground="#1a1a1a")
        generate_btn.pack(expand=True)
    
    def add_book(self):
        """Add a book to the order list"""
        title = self.title_entry.get().strip()
        format_type = self.format_entry.get().strip()
        
        try:
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid quantity and price!")
            return
        
        if not title:
            messagebox.showerror("Error", "Please enter a book title!")
            return
        
        if quantity <= 0 or price < 0:
            messagebox.showerror("Error", "Quantity must be positive and price cannot be negative!")
            return
        
        # Add to orders list
        order = BookOrder(title, format_type, quantity, price)
        self.orders.append(order)
        
        # Update listbox
        display_text = f"{len(self.orders)}. {title[:30]:<30} | {format_type:<4} | Qty:{quantity} | ₱{price:.0f} | Total: ₱{order.get_total():.0f}"
        self.books_listbox.insert(tk.END, display_text)
        
        # Clear entries
        self.title_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.title_entry.focus()
        
        messagebox.showinfo("Success", f"✓ Added: {title}")
    
    def remove_book(self):
        """Remove selected book from the list"""
        selection = self.books_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a book to remove!")
            return
        
        index = selection[0]
        self.books_listbox.delete(index)
        del self.orders[index]
        
        # Renumber the list
        self.books_listbox.delete(0, tk.END)
        for i, order in enumerate(self.orders, 1):
            display_text = f"{i}. {order.title[:30]:<30} | {order.format:<4} | Qty:{order.quantity} | ₱{order.price:.0f} | Total: ₱{order.get_total():.0f}"
            self.books_listbox.insert(tk.END, display_text)
        
        messagebox.showinfo("Success", "✓ Book removed!")
    
    def clear_all_books(self):
        """Clear all books from the list"""
        if not self.orders:
            messagebox.showinfo("Info", "No books to clear!")
            return
        
        if messagebox.askyesno("Confirm", "Clear all books from the receipt?"):
            self.orders = []
            self.books_listbox.delete(0, tk.END)
            messagebox.showinfo("Success", "✓ All books cleared!")
    
    def generate_receipt(self):
        """Generate and display the receipt"""
        # Check if there are books
        if not self.orders:
            messagebox.showerror("Error", "Please add at least one book to the receipt!")
            return
        
        # Get shipping fee
        try:
            shipping_fee = float(self.shipping_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid shipping fee (or 0 for +SF)!")
            return
        
        # Get customer info
        customer_name = self.name_entry.get().strip()
        customer_address = self.address_entry.get().strip()
        customer_phone = self.phone_entry.get().strip()
        payment_method = self.payment_entry.get().strip()
        
        # Generate receipt text
        receipt_text = self.create_receipt_text(
            customer_name, customer_address, customer_phone, 
            payment_method, shipping_fee
        )
        
        # Create new window to show receipt
        self.show_receipt_window(receipt_text)
    
    def create_receipt_text(self, name, address, phone, payment, shipping_fee):
        """Create simple clean receipt"""
        lines = []
        
        # Header
        lines.append("")
        lines.append("=" * 80)
        lines.append("")
        lines.append("                    📚  B O O K N E S T")
        lines.append("                       Your Literary Haven")
        lines.append("")
        lines.append("                         ORDER INVOICE")
        lines.append(f"                   {datetime.now().strftime('%B %d, %Y')}")
        lines.append("")
        lines.append("=" * 80)
        lines.append("")
        
        # Table
        lines.append("SL    TITLE                                  FORMAT  QTY    PRICE      TOTAL")
        lines.append("-" * 80)
        
        for idx, order in enumerate(self.orders, 1):
            title = order.title[:36]
            lines.append(f"{idx:<5} {title:<40} {order.format:<6} {order.quantity:<6} {order.price:>7.2f}  {order.get_total():>7.2f}")
        
        lines.append("-" * 80)
        
        subtotal = sum(order.get_total() for order in self.orders)
        
        lines.append("")
        lines.append(f"                                                  SUBTOTAL:  {subtotal:>10.2f}")
        
        # Handle shipping fee - if 0 show +SF, otherwise show amount
        if shipping_fee == 0:
            lines.append(f"                                                  SHIPPING:  {'+ SF':>10}")
            lines.append("")
            lines.append("=" * 80)
            lines.append(f"                                                  ★ TOTAL:   {subtotal:>10.2f} + SF ★")
        else:
            lines.append(f"                                                  SHIPPING:  {shipping_fee:>10.2f}")
            total = subtotal + shipping_fee
            lines.append("")
            lines.append("=" * 80)
            lines.append(f"                                                  ★ TOTAL:   {total:>10.2f} ★")
        
        lines.append("=" * 80)
        lines.append("")
        
        # Payment - highlighted
        lines.append("★ PAYMENT METHOD ★")
        lines.append(f"  ★★ GCash: {payment} ★★")
        lines.append("")
        
        # Shipping
        lines.append("SHIPPING INFORMATION")
        lines.append(f"  Status:   NEEDED FOR SHIPMENT")
        lines.append(f"  Name:     {name}")
        lines.append(f"  Address:  {address}")
        lines.append(f"  Phone:    {phone}")
        lines.append("")
        
        # Reminders
        lines.append("IMPORTANT REMINDERS")
        lines.append("-" * 80)
        lines.append("• NO CANCELLATION or CHANGING of orders once invoice is issued.")
        lines.append("• Payment deadline: within 24 hours. Prompt payments appreciated!")
        lines.append("• Late payments: P10 fee per day. Unpaid orders marked as joyjoy miner.")
        lines.append("• Shipping days: Friday, Saturday, or Sunday only.")
        lines.append("• Storage: Up to 1 month. Unclaimed books forfeited (no refund).")
        lines.append("• Seller not responsible for damages from extended storage.")
        lines.append("")
        lines.append("=" * 80)
        lines.append("                     Thank you for your order!")
        lines.append("=" * 80)
        lines.append("")
        
        lines.append("")
        
        return "\n".join(lines)
    
    def show_receipt_window(self, receipt_text):
        """Show receipt in a new window with beautiful GUI design"""
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("📚 BOOKNEST Receipt")
        
        # Make it fullscreen
        receipt_window.attributes('-fullscreen', True)
        receipt_window.configure(bg='#ffffff')
        
        # ESC key to exit fullscreen
        receipt_window.bind('<Escape>', lambda e: receipt_window.attributes('-fullscreen', False))
        
        # Main container - full width with padding
        main_frame = tk.Frame(receipt_window, bg='#ffffff')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=100, pady=30)
        
        # Header with Black & Gold design
        header_frame = tk.Frame(main_frame, bg='#1a1a1a', relief=tk.RAISED, bd=3)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Create a row for BOOKNEST title and date
        title_row = tk.Frame(header_frame, bg='#1a1a1a')
        title_row.pack(fill=tk.X, padx=30, pady=15)
        
        # Left side - BOOKNEST branding
        left_side = tk.Frame(title_row, bg='#1a1a1a')
        left_side.pack(side=tk.LEFT)
        
        tk.Label(left_side, text="BOOKNEST", 
                font=("Helvetica", 28, "bold"), 
                bg="#1a1a1a", fg="#ffd700").pack(anchor='w')
        
        # Right side - Invoice and Date
        right_side = tk.Frame(title_row, bg='#1a1a1a')
        right_side.pack(side=tk.RIGHT)
        
        tk.Label(right_side, text="ORDER INVOICE", 
                font=("Helvetica", 16, "bold"), 
                bg="#1a1a1a", fg="#ffd700").pack(anchor='e')
        tk.Label(right_side, text=f"DATE: {datetime.now().strftime('%b %d, %Y')}", 
                font=("Helvetica", 11), 
                bg="#1a1a1a", fg="#ffffff").pack(anchor='e', pady=(2, 0))
        
        # Scrollable content area
        canvas_frame = tk.Frame(main_frame, bg='#ffffff')
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        canvas = tk.Canvas(canvas_frame, bg='#ffffff', highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Parse and display receipt content beautifully
        self.create_beautiful_receipt(scrollable_frame, receipt_text)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Store scrollable_frame for image export
        self.current_receipt_frame = scrollable_frame
        self.current_receipt_window = receipt_window
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg='#ffffff')
        button_frame.pack(pady=15)
        
        # Save as Image button
        image_btn = tk.Button(button_frame, text="🖼️ Save as Image", 
                            command=lambda: self.save_receipt_as_image(scrollable_frame),
                            bg="#ffd700", fg="#1a1a1a", font=("Helvetica", 11, "bold"),
                            padx=20, pady=10, cursor="hand2", relief=tk.FLAT,
                            activebackground="#e6c200", activeforeground="#1a1a1a")
        image_btn.pack(side=tk.LEFT, padx=5)
        
        # Copy button
        copy_btn = tk.Button(button_frame, text="📋 Copy to Clipboard", 
                            command=lambda: self.copy_to_clipboard(receipt_text),
                            bg="#90ee90", fg="#1a1a1a", font=("Helvetica", 11, "bold"),
                            padx=20, pady=10, cursor="hand2", relief=tk.FLAT,
                            activebackground="#7cdb7c", activeforeground="#1a1a1a")
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Save button
        save_btn = tk.Button(button_frame, text="💾 Save to File", 
                            command=lambda: self.save_receipt(receipt_text),
                            bg="#1a1a1a", fg="#ffd700", font=("Helvetica", 11, "bold"),
                            padx=20, pady=10, cursor="hand2", relief=tk.FLAT,
                            activebackground="#2d2d2d", activeforeground="#ffd700")
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # Close button
        close_btn = tk.Button(button_frame, text="✖ Close", 
                             command=receipt_window.destroy,
                             bg="#666666", fg="white", font=("Helvetica", 11, "bold"),
                             padx=20, pady=10, cursor="hand2", relief=tk.FLAT,
                             activebackground="#555555", activeforeground="white")
        close_btn.pack(side=tk.RIGHT, padx=5)
    
    def create_beautiful_receipt(self, parent, receipt_text):
        """Create beautiful GUI receipt with improved color palette"""
        # Parse receipt text to extract data
        lines = receipt_text.split('\n')
        
        # Center container with subtle background
        center_container = tk.Frame(parent, bg='#f8f9fa')
        center_container.pack(expand=True, padx=100, pady=20)
        
        # Cancellation Notice with soft yellow background
        notice_top = tk.Frame(center_container, bg='#fff9e6', relief=tk.SOLID, bd=2)
        notice_top.pack(padx=10, pady=10, fill=tk.X)
        
        tk.Label(notice_top, 
                text="⚠️ Please be reminded that cancellations or changes to orders are not allowed once the invoice has been issued.",
                font=("Helvetica", 10, "bold"), bg='#fff9e6', fg='#856404', 
                wraplength=1000, justify=tk.CENTER, pady=10).pack()
        
        tk.Label(notice_top, 
                text="Kindly note that we sell pre-loved books unless stated otherwise. These may show signs of wear such as foxing, tanning, or minor water damage. We encourage you to check the product video or request additional photos before confirming your order.",
                font=("Helvetica", 9), bg='#fff9e6', fg='#6c5d03', 
                wraplength=1000, justify=tk.CENTER, pady=8).pack()
        
        # Order Details Table with modern styling
        table_frame = tk.Frame(center_container, bg='#ffffff', relief=tk.SOLID, bd=2)
        table_frame.pack(padx=10, pady=15)
        
        # Table title
        tk.Label(table_frame, text="📚 ORDER DETAILS", 
                font=("Helvetica", 14, "bold"), 
                bg='#2c3e50', fg='#ffd700', 
                pady=12).pack(fill=tk.X)
        
        # Table header
        header_frame = tk.Frame(table_frame, bg='#34495e', relief=tk.RAISED, bd=1)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        tk.Label(header_frame, text="TITLE", width=40, font=("Helvetica", 11, "bold"), 
                bg='#34495e', fg='#ffffff', anchor='center').pack(side=tk.LEFT, padx=3, pady=10)
        tk.Label(header_frame, text="FORMAT", width=12, font=("Helvetica", 11, "bold"), 
                bg='#34495e', fg='#ffffff', anchor='center').pack(side=tk.LEFT, padx=3, pady=10)
        tk.Label(header_frame, text="QTY", width=8, font=("Helvetica", 11, "bold"), 
                bg='#34495e', fg='#ffffff', anchor='center').pack(side=tk.LEFT, padx=3, pady=10)
        tk.Label(header_frame, text="PRICE", width=12, font=("Helvetica", 11, "bold"), 
                bg='#34495e', fg='#ffffff', anchor='center').pack(side=tk.LEFT, padx=3, pady=10)
        
        # Order items
        for idx, order in enumerate(self.orders):
            bg_color = '#ecf0f1' if idx % 2 == 0 else '#ffffff'
            item_frame = tk.Frame(table_frame, bg=bg_color, relief=tk.FLAT, bd=0)
            item_frame.pack(fill=tk.X, padx=0, pady=1)
            
            tk.Label(item_frame, text=order.title[:38], width=40, 
                    font=("Helvetica", 10), bg=bg_color, fg='#2c3e50', anchor='center').pack(side=tk.LEFT, padx=3, pady=12)
            tk.Label(item_frame, text=order.format, width=12, 
                    font=("Helvetica", 10), bg=bg_color, fg='#2c3e50', anchor='center').pack(side=tk.LEFT, padx=3, pady=12)
            tk.Label(item_frame, text=str(order.quantity), width=8, 
                    font=("Helvetica", 10), bg=bg_color, fg='#2c3e50', anchor='center').pack(side=tk.LEFT, padx=3, pady=12)
            tk.Label(item_frame, text=f"₱{order.price:.0f}", width=12, 
                    font=("Helvetica", 10, "bold"), bg=bg_color, fg='#27ae60', anchor='center').pack(side=tk.LEFT, padx=3, pady=12)
        
        # Calculate totals
        subtotal = sum(order.get_total() for order in self.orders)
        
        # Extract shipping info from text
        shipping_fee = 0
        shipping_text = ""
        has_shipping = False
        for line in lines:
            if "SHIPPING:" in line:
                if "+ SF" in line or "+SF" in line:
                    shipping_text = "+SF"
                    has_shipping = True
                else:
                    parts = line.split()
                    if len(parts) > 1:
                        try:
                            # Try to extract numeric value
                            shipping_text = parts[-1].replace("₱", "").strip()
                            shipping_fee = float(shipping_text)
                            has_shipping = True
                        except:
                            shipping_text = "+SF"
                            has_shipping = True
        
        # Final Payment Section - Vibrant and Eye-catching
        final_payment_frame = tk.Frame(center_container, bg='#ffd700', relief=tk.RAISED, bd=4)
        final_payment_frame.pack(padx=10, pady=20, fill=tk.X)
        
        # Add decorative top border
        tk.Frame(final_payment_frame, bg='#f39c12', height=4).pack(fill=tk.X)
        
        tk.Label(final_payment_frame, text="💰 TOTAL AMOUNT TO PAY 💰", 
                font=("Helvetica", 16, "bold"), 
                bg='#ffd700', fg='#2c3e50', 
                pady=15).pack()
        
        # Show breakdown with better styling
        breakdown_frame = tk.Frame(final_payment_frame, bg='#ffd700')
        breakdown_frame.pack(pady=8)
        
        tk.Label(breakdown_frame, text=f"Books Total: ₱{subtotal:.2f}", 
                font=("Helvetica", 13), bg='#ffd700', fg='#2c3e50').pack(pady=3)
        
        if has_shipping and shipping_fee > 0:
            tk.Label(breakdown_frame, text=f"Shipping Fee: ₱{shipping_fee:.2f}", 
                    font=("Helvetica", 13), bg='#ffd700', fg='#2c3e50').pack(pady=3)
            final_total = subtotal + shipping_fee
            
            # Prominent total amount with shadow effect
            total_container = tk.Frame(final_payment_frame, bg='#2c3e50', relief=tk.RAISED, bd=3)
            total_container.pack(pady=12, padx=30)
            tk.Label(total_container, text=f"₱ {final_total:.2f}", 
                    font=("Helvetica", 36, "bold"), bg='#2c3e50', fg='#ffd700', 
                    padx=30, pady=15).pack()
        else:
            tk.Label(breakdown_frame, text="Shipping Fee: To be determined", 
                    font=("Helvetica", 13, "italic"), bg='#ffd700', fg='#7f6000').pack(pady=3)
            
            # Prominent total with +SF
            total_container = tk.Frame(final_payment_frame, bg='#2c3e50', relief=tk.RAISED, bd=3)
            total_container.pack(pady=12, padx=30)
            tk.Label(total_container, text=f"₱ {subtotal:.2f} + SF", 
                    font=("Helvetica", 36, "bold"), bg='#2c3e50', fg='#ffd700', 
                    padx=30, pady=15).pack()
        
        tk.Label(final_payment_frame, text="⚠️ PAY THIS EXACT AMOUNT ⚠️", 
                font=("Helvetica", 13, "bold"), 
                bg='#ffd700', fg='#c0392b', 
                pady=12).pack()
        
        # Add decorative bottom border
        tk.Frame(final_payment_frame, bg='#f39c12', height=4).pack(fill=tk.X)
        
        # Two column layout for Payment and Shipping
        columns_frame = tk.Frame(center_container, bg='#f8f9fa')
        columns_frame.pack(padx=10, pady=15, fill=tk.X)
        
        # Left column - Payment Method with modern green
        payment_frame = tk.Frame(columns_frame, bg='#d4edda', relief=tk.SOLID, bd=3)
        payment_frame.pack(side=tk.LEFT, padx=8, pady=0, fill=tk.BOTH, expand=True)
        
        # Header stripe
        tk.Frame(payment_frame, bg='#28a745', height=4).pack(fill=tk.X)
        
        tk.Label(payment_frame, text="💳 PAYMENT METHOD", 
                font=("Helvetica", 13, "bold"), 
                bg='#d4edda', fg='#155724', 
                pady=15).pack()
        
        # Extract GCash from text
        gcash_number = ""
        for line in lines:
            if "GCash:" in line:
                gcash_number = line.split("GCash:")[-1].strip().replace("★", "")
        
        # GCash badge with better styling
        gcash_container = tk.Frame(payment_frame, bg='#007bff', relief=tk.RAISED, bd=2)
        gcash_container.pack(pady=10)
        
        tk.Label(gcash_container, text="G", 
                font=("Helvetica", 24, "bold"), 
                bg='#007bff', fg='white', 
                width=2, height=1, padx=8, pady=5).pack()
        
        tk.Label(payment_frame, text=gcash_number, 
                font=("Helvetica", 14, "bold"), 
                bg='#d4edda', fg='#155724', 
                pady=12).pack()
        
        # Right column - Shipping Info with warm orange
        ship_frame = tk.Frame(columns_frame, bg='#fff3cd', relief=tk.SOLID, bd=3)
        ship_frame.pack(side=tk.RIGHT, padx=8, pady=0, fill=tk.BOTH, expand=True)
        
        # Header stripe
        tk.Frame(ship_frame, bg='#ff9800', height=4).pack(fill=tk.X)
        
        tk.Label(ship_frame, text="📦 NEEDED FOR SHIPMENT", 
                font=("Helvetica", 13, "bold"), 
                bg='#fff3cd', fg='#856404', 
                pady=15).pack()
        
        # Extract shipping info
        name = address = phone = ""
        for line in lines:
            if "Name:" in line:
                name = line.split("Name:")[-1].strip()
            elif "Address:" in line:
                address = line.split("Address:")[-1].strip()
            elif "Phone:" in line:
                phone = line.split("Phone:")[-1].strip()
        
        info_container = tk.Frame(ship_frame, bg='#fff3cd')
        info_container.pack(fill=tk.X, padx=15, pady=12)
        
        tk.Label(info_container, text=f"NAME: {name}", 
                font=("Helvetica", 11, "bold"), bg='#fff3cd', fg='#856404', anchor='w').pack(fill=tk.X, pady=4)
        tk.Label(info_container, text=f"ADDRESS: {address}", 
                font=("Helvetica", 11), bg='#fff3cd', fg='#856404', anchor='w', wraplength=400).pack(fill=tk.X, pady=4)
        tk.Label(info_container, text=f"PHONE: {phone}", 
                font=("Helvetica", 11, "bold"), bg='#fff3cd', fg='#856404', anchor='w').pack(fill=tk.X, pady=4)
        
        # Important Reminders Section with modern dark design
        reminder_frame = tk.Frame(center_container, bg='#2c3e50', relief=tk.SOLID, bd=4)
        reminder_frame.pack(padx=10, pady=20, fill=tk.X)
        
        # Gold accent stripe
        tk.Frame(reminder_frame, bg='#ffd700', height=5).pack(fill=tk.X)
        
        tk.Label(reminder_frame, text="📌 IMPORTANT REMINDERS", 
                font=("Helvetica", 15, "bold"), 
                bg='#2c3e50', fg='#ffd700', 
                pady=15).pack()
        
        reminder_text = tk.Frame(reminder_frame, bg='#2c3e50')
        reminder_text.pack(fill=tk.X, padx=25, pady=15)
        
        # Exact reminders from the image with better formatting
        reminders = [
            "• Strictly NO CANCELLATION or CHANGING of orders once the invoice has been issued.",
            "• Payment deadline: within 24 hours of receiving your invoice. Prompt payments are highly appreciated!",
            "• Late payments: A ₱10 fee per day will be charged for overdue payments. Unpaid orders may be marked as joyjoy minor.",
            "• If you wish to have your books shipped, please send a message.",
            "• 🚚 Shipping days: Friday, Saturday, or Sunday only.",
            "• Books may be stored for up to one (1) month from the date of purchase. Unclaimed or unshipped books after this period will be forfeited / donated with no refund.",
            "• The seller is not responsible for any damages (such as foxing, tanning, discoloration, or wear) that may occur if books are stored (piling) for an extended time."
        ]
        
        for idx, reminder in enumerate(reminders):
            # Highlight first item (NO CANCELLATION)
            fg_color = '#ffd700' if idx == 0 else '#ecf0f1'
            font_weight = 'bold' if idx == 0 else 'normal'
            
            tk.Label(reminder_text, text=reminder,
                    font=("Helvetica", 11, font_weight), bg='#2c3e50', fg=fg_color, 
                    anchor='w', justify=tk.LEFT, wraplength=1100).pack(fill=tk.X, pady=4, anchor='w')
        
        # Bottom accent stripe
        tk.Frame(reminder_frame, bg='#ffd700', height=5).pack(fill=tk.X)
    
    def save_receipt_as_image(self, frame):
        """Save the receipt as a PNG image using Pillow"""
        try:
            # Update the frame to ensure everything is rendered
            frame.update_idletasks()
            
            # Get the dimensions of the frame
            x = frame.winfo_rootx()
            y = frame.winfo_rooty()
            width = frame.winfo_width()
            height = frame.winfo_height()
            
            # Use pillow ImageGrab to capture the frame
            try:
                from PIL import ImageGrab
                # Capture the screen area where the frame is
                image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
                
                # Ask user where to save
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                    initialfile=f"BOOKNEST_Receipt_{timestamp}.png"
                )
                
                if filename:
                    image.save(filename, "PNG")
                    messagebox.showinfo("Success", f"Receipt saved as image:\n{filename}")
            except ImportError:
                messagebox.showerror("Error", "PIL/Pillow is required to save as image.\nInstall it with: pip install Pillow")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")
    
    def copy_to_clipboard(self, text):
        """Copy receipt to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Success", "Receipt copied to clipboard!")
    
    def save_receipt(self, text):
        """Save receipt to a text file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"BOOKNEST_Receipt_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
            messagebox.showinfo("Success", f"Receipt saved as:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save receipt:\n{str(e)}")


def main():
    root = tk.Tk()
    app = BookNestGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
