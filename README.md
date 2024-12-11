# Pharmacy Management System

The Pharmacy Management System is a web application designed to streamline and automate various processes involved in managing a pharmacy. This system provides an efficient platform for pharmacy staff to handle inventory, sales, and customer management effectively.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Custom Error Pages](#custom-error-pages)
- [License](#license)

## Requirements

This project requires the following Python packages:

- `Django==5.1`
- `asgiref==3.8.1`
- `requests==2.32.3`
- `psycopg2==2.9.9`
- `psycopg2-binary==2.9.9`
- `Pillow==10.4.0`
- `cryptography==43.0.0`
- `PyJWT==2.9.0`
- `msal==1.30.0`
- `certifi==2024.7.4`
- `charset-normalizer==3.3.2`
- `idna==3.8`
- `sqlparse==0.5.1`
- `tzdata==2024.1`
- `urllib3==2.2.2`
- `cffi==1.17.0`
- `pycparser==2.22`
- `app==0.0.1` (Your custom app)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Yashparmar1125/PharmacyManagement_System.git
   cd pharmacy_management_system
2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    # Activate the virtual environment
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
3. **Install the required packages**:
    ```bash
   pip install -r requirements.txt
   
4. **Set up the database**:

    Ensure PostgreSQL is installed and running..
    Create a database for your project(pharmacy.db).

5. **Update your settings**:

    Open settings.py and update the database configuration as needed.

6. **Run migrations**:
    ```bash
   python manage.py makemigrations
   python manage.py migrate
   
7. **Create superuser**:
    ```bash
   python manage.py createsuperuser

**Usage**:

To run the server locally, use the following command:

```bash

python manage.py runserver





