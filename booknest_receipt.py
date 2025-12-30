#!/usr/bin/env python3
"""
BOOKNEST Receipt Generator
Generates order invoices/receipts for book orders
"""

from datetime import datetime
from typing import List, Dict


class BookOrder:
    def __init__(self, title: str, format: str, quantity: int, price: float):
        self.title = title
        self.format = format
        self.quantity = quantity
        self.price = price
    
    def get_total(self):
        return self.price * self.quantity


class Receipt:
    def __init__(self):
        self.orders: List[BookOrder] = []
        self.payment_method = ""
        self.customer_name = ""
        self.customer_address = ""
        self.customer_phone = ""
        self.shipping_fee = 0
    
    def add_order(self, title: str, format: str, quantity: int, price: float):
        """Add a book order to the receipt"""
        order = BookOrder(title, format, quantity, price)
        self.orders.append(order)
    
    def set_customer_info(self, name: str = "", address: str = "", phone: str = ""):
        """Set customer information"""
        self.customer_name = name
        self.customer_address = address
        self.customer_phone = phone
    
    def set_payment_method(self, method: str):
        """Set payment method (e.g., GCash number)"""
        self.payment_method = method
    
    def set_shipping_fee(self, fee: float):
        """Set shipping fee"""
        self.shipping_fee = fee
    
    def calculate_subtotal(self):
        """Calculate subtotal of all orders"""
        return sum(order.get_total() for order in self.orders)
    
    def calculate_total(self):
        """Calculate total including shipping fee"""
        return self.calculate_subtotal() + self.shipping_fee
    
    def generate_receipt(self):
        """Generate and print the receipt"""
        receipt_width = 90
        
        # Header
        print("=" * receipt_width)
        print("  📚 BOOKNEST".ljust(40) + "ORDER INVOICE".rjust(50))
        print(f"  {'DATE: ' + datetime.now().strftime('%b.%d, %Y').upper()}".rjust(receipt_width))
        print("=" * receipt_width)
        print()
        
        # Important Notice
        print("Please be reminded that cancellations or changes to orders are not allowed once the invoice has been issued.")
        print("Kindly note that we sell pre-loved books unless stated otherwise. These may show signs of wear such as")
        print("foxing, tanning, or minor water damage. We encourage you to check the product video or request additional")
        print("photos before confirming your order.")
        print()
        
        # Order Table Header
        print("-" * receipt_width)
        print(f"{'TITLE':<40} {'FORMAT':<15} {'QTY':<10} {'PRICE':>10}")
        print("-" * receipt_width)
        
        # Order Items
        for order in self.orders:
            print(f"{order.title:<40} {order.format:<15} {order.quantity:<10} {order.price:>10.0f}")
        
        print("-" * receipt_width)
        
        # Subtotal and Shipping Fee
        subtotal = self.calculate_subtotal()
        if self.shipping_fee > 0:
            print(f"{'SUBTOTAL:':<80} {subtotal:.0f}")
            print(f"{'SHIPPING FEE:':<80} {self.shipping_fee:.0f}")
            print()
            print(f"{'TOTAL:':<80} {self.calculate_total():.0f}")
        else:
            print(f"{'TOTAL:':<80} {subtotal:.0f}+SF")
        
        print()
        print("=" * receipt_width)
        
        # Payment and Customer Info
        print()
        print(f"PAYMENT METHOD".ljust(40) + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━".rjust(50))
        print(f"  📱 {self.payment_method}".ljust(40) + "NEEDED FOR SHIPMENT".rjust(50))
        print(f"{'':40} NAME: {self.customer_name}")
        print(f"{'':40} ADDRESS: {self.customer_address}")
        print(f"{'':40} PHONE NUMBER: {self.customer_phone}")
        print()
        
        # Important Reminders
        print("=" * receipt_width)
        print("IMPORTANT REMINDERS")
        print("-" * receipt_width)
        print("• Strictly NO CANCELLATION or CHANGING of orders once the invoice has been issued.")
        print()
        print("• Payment deadline: within 24 hours of receiving your invoice. Prompt payments are highly appreciated!")
        print()
        print("• Late payments: A ₱10 fee per day will be charged for overdue payments. Unpaid orders may be marked")
        print("  as joyjoy miner.")
        print()
        print("• If you wish to have your books shipped, please send a message.")
        print()
        print("• 📦 Shipping days: Friday, Saturday, or Sunday only.")
        print()
        print("• Books may be stored for up to one (1) month from the date of purchase. Unclaimed or unshipped books")
        print("  after this period will be forfeited / donated with no refund.")
        print()
        print("• The seller is not responsible for any damages (such as foxing, tanning, discoloration, or wear) that")
        print("  may occur if books are stored (piling) for an extended time.")
        print("=" * receipt_width)
        print()


def main():
    """Demo: Generate a sample receipt"""
    
    # Create a new receipt
    receipt = Receipt()
    
    # Add book order
    receipt.add_order(
        title="AMERICANAH",
        format="PB",
        quantity=1,
        price=250
    )
    
    # Set customer information
    receipt.set_customer_info(
        name="",
        address="",
        phone=""
    )
    
    # Set payment method
    receipt.set_payment_method("09164097987")
    
    # Set shipping fee (0 if not yet determined)
    receipt.set_shipping_fee(0)
    
    # Generate and print the receipt
    receipt.generate_receipt()
    
    print("\n" + "="*90)
    print("To customize this receipt, modify the values in the main() function above.")
    print("You can add multiple books by calling receipt.add_order() multiple times.")
    print("="*90)


if __name__ == "__main__":
    main()
