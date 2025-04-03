import mysql.connector

def connect_to_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root",
        database="Car_Service_Center"
    )
    return conn

def add_customer():
    name = input("Enter customer name: ")
    contact = input("Enter customer contact: ")
    vehicle = input("Enter vehicle details: ")

    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Customers (name, contact, vehicle)
        VALUES (%s, %s, %s)
    """, (name, contact, vehicle))

    conn.commit()
    conn.close()
    print(f"Customer '{name}' added successfully!")

def view_customers():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()
    conn.close()

    print("\nCustomers List:")
    for customer in customers:
        print(f"ID: {customer[0]}, Name: {customer[1]}, Contact: {customer[2]}, Vehicle: {customer[3]}")

def add_service():
    customer_id = int(input("Enter customer ID: "))
    service_type = input("Enter service type (e.g., Oil Change, Tire Replacement): ")
    cost = float(input("Enter service cost: "))
    date = input("Enter service date (YYYY-MM-DD): ")

    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Services (customer_id, service_type, cost, date)
        VALUES (%s, %s, %s, %s)
    """, (customer_id, service_type, cost, date))

    conn.commit()
    conn.close()
    print(f"Service '{service_type}' added successfully!")

def view_services():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, c.name, s.service_type, s.cost, s.date
        FROM Services s
        JOIN Customers c ON s.customer_id = c.id
    """)
    services = cursor.fetchall()
    conn.close()

    print("\nServices List:")
    for service in services:
        print(f"ID: {service[0]}, Customer: {service[1]}, Service: {service[2]}, Cost: {service[3]}, Date: {service[4]}")

def schedule_appointment():
    customer_id = int(input("Enter customer ID: "))
    date = input("Enter appointment date (YYYY-MM-DD): ")
    time = input("Enter appointment time (HH:MM): ")
    status = input("Enter status (Scheduled/Completed): ")

    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Appointments (customer_id, date, time, status)
        VALUES (%s, %s, %s, %s)
    """, (customer_id, date, time, status))

    conn.commit()
    conn.close()
    print(f"Appointment scheduled successfully for Customer ID {customer_id} on {date} at {time}!")

def view_appointments():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, c.name, a.date, a.time, a.status
        FROM Appointments a
        JOIN Customers c ON a.customer_id = c.id
    """)
    appointments = cursor.fetchall()
    conn.close()

    print("\nAppointments List:")
    for appointment in appointments:
        print(f"ID: {appointment[0]}, Customer: {appointment[1]}, Date: {appointment[2]}, Time: {appointment[3]}, Status: {appointment[4]}")

def generate_bill():
    customer_id = int(input("Enter customer ID: "))

    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(s.cost) AS total_cost
        FROM Services s
        WHERE s.customer_id = %s
    """, (customer_id,))
    total_cost = cursor.fetchone()[0]

    date = input("Enter invoice date (YYYY-MM-DD): ")
    cursor.execute("""
        INSERT INTO Invoices (customer_id, total_cost, date)
        VALUES (%s, %s, %s)
    """, (customer_id, total_cost, date))

    conn.commit()
    conn.close()
    print(f"Invoice generated successfully for Customer ID {customer_id} with Total Cost: {total_cost}")

def main_menu():
    while True:
        print("\nCar Service Center Management System")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Add Service")
        print("4. View Services")
        print("5. Schedule Appointment")
        print("6. View Appointments")
        print("7. Generate Bill")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_customer()
        elif choice == '2':
            view_customers()
        elif choice == '3':
            add_service()
        elif choice == '4':
            view_services()
        elif choice == '5':
            schedule_appointment()
        elif choice == '6':
            view_appointments()
        elif choice == '7':
            generate_bill()
        elif choice == '8':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
