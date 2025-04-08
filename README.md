Grahak Bhandar 🛒

A simple yet powerful Grocery Shop Management System built using Flask and SQLite. It features both Admin and Customer interfaces to manage products, customers, sales, and shopping seamlessly.

🔧 Technologies Used
🐍 Python (Flask)

💾 MySql

🌐 HTML5, CSS3 (External stylesheets only)

🖥️ Visual Studio Code

📌 Features
👨‍💼 Admin Panel
Add, View, Update, Delete Products

Add and View Customers

View Sales and Billing History

Clean dashboard with navigation

🛍️ Shop Interface
Browse available products

Add to bucket (cart)

Buy Now functionality with quantity management

Real-time bill generation

🗂️ Project Structure
```
grahak-bhandar/
│
├── static/
│   └── css/
│       └── styles.css           # External CSS file
│
├── templates/
│   ├── home.html                # Homepage
│   ├── shop.html                # Shop Interface
│   ├── admin.html               # Admin Panel (Products & Customers)
│   └── base.html (if used)
│
├── app.py                       # Main Flask Application
└── README.md                    # Project Documentation

```
⚙️ Setup Instructions
Clone the repository:

```
git clone https://github.com/yourusername/grahak-bhandar.git
cd grahak-bhandar
Create a virtual environment (optional but recommended):
```
```
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
Install required packages:
```
```
pip install flask
Run the application:
```
```
python app.py
Open your browser and visit:
```
```
http://127.0.0.1:5000/
```

🗃️ Database Schema
products(id, name, category, price, quantity)

customers(id, name, phone)

sales(id, product_name, price, quantity, total, timestamp)

📸 Screenshots
Add screenshots of:

Home Page

![WhatsApp Image 2025-04-06 at 21 39 05_9e4e5528](https://github.com/user-attachments/assets/3454e9bb-316a-4b63-9e16-5fb351ca5e9f)

Admin Panel

![image](https://github.com/user-attachments/assets/04004b63-25f0-4772-9181-2b080efef000)


Shop Interface

![image](https://github.com/user-attachments/assets/6479a768-2502-4b2a-8636-9b7906fa5cca)


📈 Future Enhancements
Admin login system

Customer authentication & registration

Online payment gateway integration

Email/SMS invoice generation

Responsive mobile-friendly layout

🙌 Acknowledgment
This project was developed as part of a DBMS Mini Project at Pimpri Chinchwad University .

Developed by: Patil Rameshwar D
