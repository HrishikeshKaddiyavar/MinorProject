# MinorProject

DIGITAL ORDERING SYSTEM FOR HOTEL
(In-House Hotel Food Ordering System)

Project Overview
This project is a web-based Digital Ordering System designed for hotels and restaurants. It allows customers to view the menu and place food orders directly from their table, while staff can manage orders efficiently through the system.
The system reduces manual work, order errors, and service delays.

Problem Statement
Traditional pen-and-paper food ordering systems are slow and error-prone. Miscommunication between waiters and kitchen staff often leads to incorrect orders, delays, and poor customer experience. This project solves these issues using a centralized digital platform.

Objectives
• To automate the food ordering process inside hotels
• To reduce order processing time
• To avoid order miscommunication
• To improve customer satisfaction
• To provide a simple and user-friendly system

Features
• Category-wise food menu
• Add items to cart
• Place orders digitally
• Order management for staff
• Role-based access (customer, staff, admin)
• Simple and responsive UI

Technologies Used
• Backend: Django (Python)
• Frontend: HTML, CSS, JavaScript
• Database: SQLite (local) / PostgreSQL (deployment)
• Server: Gunicorn
• Hosting: Render / PythonAnywhere

Project Structure
• models.py – Database models
• views.py – Application logic
• urls.py – URL routing
• templates/ – HTML files
• static/ – CSS and JavaScript files
• settings.py – Project configuration

Installation and Setup (Local)

Step 1: Clone the repository
git clone <repository_url>
cd project_folder

Step 2: Create virtual environment
python -m venv venv
venv\Scripts\activate (Windows)

Step 3: Install dependencies
pip install -r requirements.txt

Step 4: Run migrations
python manage.py migrate

Step 5: Create admin user
python manage.py createsuperuser

Step 6: Run the server
python manage.py runserver

Step 7: Open in browser
http://127.0.0.1:8000/

Deployment (Free Hosting)
This project can be deployed for free using platforms like:
• Render
• PythonAnywhere
• Railway

Basic deployment steps:
• Push project to GitHub
• Connect GitHub repository to hosting platform
• Configure environment variables
• Set DEBUG=False
• Add allowed hosts
• Deploy and access live URL

Future Enhancements
• Online payment integration
• Order tracking in real-time
• Mobile app version
• Kitchen display system
• Customer feedback module

Conclusion
The Digital Ordering System for Hotel improves efficiency, accuracy, and customer experience by replacing traditional food ordering methods with a modern web-based solution.

Author
Hrishikesh Kaddiyavar
