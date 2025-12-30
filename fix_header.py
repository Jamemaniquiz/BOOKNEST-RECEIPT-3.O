#!/usr/bin/env python3
# Quick fix to update header colors

with open('booknest_gui.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the header section
content = content.replace('font=("Helvetica", 32, "bold"), \n                bg="#ffd700", fg="#1a1a1a"', 
                         'font=("Helvetica", 36, "bold"), \n                bg="#1a1a1a", fg="#ffd700"')
content = content.replace('font=("Helvetica", 14), \n                bg="#ffd700", fg="#1a1a1a", \n                pady=5',
                         'font=("Helvetica", 14, "italic"), \n                bg="#1a1a1a", fg="#90ee90", \n                pady=8')
content = content.replace('pady=15).pack()', 'pady=20).pack()')
content = content.replace('info_frame.pack(fill=tk.X, pady=10)', 'info_frame.pack(pady=15)')
content = content.replace('font=("Helvetica", 20, "bold")', 'font=("Helvetica", 22, "bold")')
content = content.replace('tk.Label(info_frame, text=datetime.now().strftime(\'%B %d, %Y\'), \n                font=("Helvetica", 12), \n                bg="#ffffff", fg="#666666").pack()',
                         'tk.Label(info_frame, text=f"DATE: {datetime.now().strftime(\'%B %d, %Y\')}", \n                font=("Helvetica", 12), \n                bg="#ffffff", fg="#666666").pack(pady=5)')

with open('booknest_gui.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Header updated successfully!")
