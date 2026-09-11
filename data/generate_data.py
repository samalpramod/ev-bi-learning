from itertools import count
from multiprocessing import connection

import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker("en_IN")

CITIES = [
    ("Delhi", "Delhi", 28.6139, 77.2090),
    ("Mumbai", "Maharashtra", 19.0760, 72.8777),
    ("Bengaluru", "Karnataka", 12.9716, 77.5946),
    ("Hyderabad", "Telangana", 17.3850, 78.4867),
    ("Chennai", "Tamil Nadu", 13.0827, 80.2707),
    ("Pune", "Maharashtra", 18.5204, 73.8567),
    ("Kolkata", "West Bengal", 22.5726, 88.3639),
    ("Ahmedabad", "Gujarat", 23.0225, 72.5714),
]

def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='evcharge_bi',
            user='root',
            password='Nextg@2024#'
        )
        if conn.is_connected():
            print("Connected to MySQL database")
            return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

           
def generate_operators(connection, count=10):
    cursor = connection.cursor()
    operator_ids = []
    query = "SELECT COUNT(*) AS operator_count FROM operators"
    cursor.execute(query)
    startnum =  cursor.fetchone()[0]
    for i in range(count):
        opcode = "OP" + str(startnum + 1).zfill(3)
        opname = "Operator "+str(startnum+1).zfill(3)
        status ="ACTIVE"
        created_at = datetime.now()
    
        query = """
        INSERT INTO operators (code, name, status, created_at)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (opcode,opname, status, created_at))
        print("Record inserted successfully.")
        operator_id = cursor.lastrowid
        operator_ids.append(operator_id)
        startnum+=1
    connection.commit()
    return operator_ids

def generate_locations(connection, operator_ids, count=5):
    location_ids = []
    cursor = connection.cursor()
    operator_index = 0;
    for i in range(count):
        operator_id = operator_ids[operator_index]
        operator_index+= 1
        if operator_index>=len(operator_ids):
            operator_index=0
        city, state, city_lat, city_long = random.choice(CITIES)
        latitude = city_lat + random.uniform(-0.05, 0.05)
        longitude = city_long + random.uniform(-0.05, 0.05)
        location_name = f"EV Station - {city} {i + 1:03d}"
        location_type = random.choice([
            "HIGHWAY",
            "MALL",
            "OFFICE",
            "RESIDENTIAL",
            "PUBLIC",
            "TRANSIT"
        ])    
        status = "ACTIVE"
        created_at = datetime.now()

        print(operator_id,location_name,city,state,latitude,longitude,location_type,status,created_at)
        query = """
        INSERT INTO locations
        (operator_id, name, city, state, latitude, longitude,
         location_type, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (operator_id, location_name, city, state, latitude, longitude, location_type, status, created_at))
        location_ids.append(cursor.lastrowid)
    connection.commit()
    return location_ids

def generate_charge_points(connection, location_ids, count=10):
    CONNECTOR_TYPES = [
    "CCS2",
    "TYPE2",
    "CHADEMO"
    ]

    POWER_RATINGS = [
        7.4,
        22.0,
        30.0,
        60.0,
        120.0
    ]
    charge_point_ids = []
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) AS cp_count FROM charge_points"
        cursor.execute(query)
        startnum =  cursor.fetchone()[0]
        for i in range(count):
            charge_point_code = f"CP{startnum + 1:05d}"
            location_id = random.choice(location_ids)
            connector_type = random.choice(CONNECTOR_TYPES)
            power_rating = random.choice(POWER_RATINGS)
            status = random.choice(['AVAILABLE','CHARGING','FAULTED','OFFLINE'])
            created_at = datetime.now()
            query = """
            INSERT INTO charge_points
            (location_id, charge_point_code, connector_type, power_kw, status, commissioned_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (location_id, charge_point_code, connector_type, power_rating, status, created_at))
            charge_point_ids.append(cursor.lastrowid)
            startnum += 1
        connection.commit()
        print("Generated charge points:", charge_point_ids)
        return charge_point_ids
    except Exception:
        connection.rollback()
        raise

def generate_customers(connection, count=10):
    cursor = connection.cursor()
    FIRST_NAMES = [
    "Rahul", "Amit", "Priya", "Neha", "Rohit", "Kuldeep", "Anjali", "Suresh", "Ritu", "Aakash",
    "Ankit", "Sneha", "Vikas", "Pooja", "Arjun","Rajesh", "Divya", "Ayesha", "Vikram", "Sakshi",
    "Karan", "Nisha", "Sanjay", "Kavita", "Manish", "Hardeep", "Ramesh", "Sunita", "Deepak", "Anjali"
    ]

    LAST_NAMES = [
        "Sharma", "Kumar", "Singh", "Patel", "Verma","Shah", "Chatterjee", "Nair", "Rao", "Kapoor",
        "Gupta", "Mehta", "Joshi", "Malhotra", "Reddy","Singh", "Bose", "Chakraborty", "Iyer", "Das", "Chopra", "Mishra",
        "Iyer", "Das", "Chopra", "Mishra", "Agarwal", "Bhatia", "Choudhury", "Dutta", "Ghosh", "Jain", "Khanna", "Lal", "Mishra", "Pillai",
    ]

    customer_ids = []
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) AS cust_count FROM customers"
        cursor.execute(query)
        startnum =  cursor.fetchone()[0]
        for i in range(count):
            customer_id = f"CP{startnum + 1:05d}"
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            name = f"{first_name} {last_name}"
            email = f"{first_name.lower()}.{last_name.lower()}{i + 1}@example.com"
            city, state, _, _ = random.choice(CITIES)
            created_at = datetime.now()
            query = """
           INSERT INTO customers
           (customer_code, name, email, city, state, created_at)
           VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (customer_id, name, email, city, state, created_at))
            customer_ids.append(cursor.lastrowid)
            startnum += 1
        connection.commit()
        print("Generated customers:", customer_ids)
        return customer_ids
    except Exception:
        connection.rollback()
        raise


    
    
def generate_transactions(connection,charge_point_ids,customer_ids,count=20):
    transaction_ids = []
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM transactions"
        cursor.execute(query)
        startnum = cursor.fetchone()[0]
        
        for i in range(count):
            transaction_code = f"TXN{startnum + 1:07d}"
            charge_point_id = random.choice(charge_point_ids)
            customer_id = random.choice(customer_ids)
            start_date = datetime(2025, 1, 1)
            end_date = datetime(2026, 8, 31)
            days_range = (end_date - start_date).days
            start_time = start_date + timedelta(days=random.randint(0, days_range),hours=random.randint(0, 23),minutes=random.randint(0, 59)            )
            duration_minutes = random.randint(10, 180)
            end_time = start_time + timedelta(minutes=duration_minutes)
            energy_kwh = round(random.uniform(5, 80), 3)
            tariff_per_kwh = 18.0
            amount = round(energy_kwh * tariff_per_kwh, 2)
            status = random.choices(["COMPLETED", "CANCELLED", "FAILED"],weights=[90, 5, 5],k=1)[0]
            #created_at = datetime.now()
            
            query = """
            INSERT INTO transactions
            (transaction_code, charge_point_id, customer_id, start_time, end_time, energy_kwh,duration_minutes, amount, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (transaction_code, charge_point_id, customer_id, start_time, end_time, energy_kwh,duration_minutes, amount, status))
            transaction_ids.append(cursor.lastrowid)
            startnum += 1

        connection.commit()
        print("Generated transactions:", transaction_ids)

        return transaction_ids

    except Exception:
        connection.rollback()
        raise    
    
def get_ids(connection, table_name):
    cursor = connection.cursor()
    query = f"SELECT id FROM {table_name} ORDER BY id"
    cursor.execute(query)

    rows = cursor.fetchall()

    return [row[0] for row in rows]

def generate_payments(connection,count=20):
    cursor = connection.cursor()
    query = "SELECT id,amount,end_time FROM transactions ORDER BY id"
    cursor.execute(query)
    transactions = cursor.fetchall()
    try:
        for transaction in transactions:
            transaction_id = transaction[0]
            amount = transaction[1]
            end_time = transaction[2]
            
            payment_method = random.choice(["UPI", "CARD", "NET_BANKING", "WALLET"])
            payment_status = random.choices(["SUCCESS", "FAILED", "REFUNDED"],weights=[92, 5, 3],k=1)[0]
            payment_date = datetime.now()
            query ="""
            INSERT INTO payments
            (
                transaction_id,
                payment_method,
                payment_status,
                payment_time,
                amount
            )
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (transaction_id, payment_method, payment_status, payment_date, amount))
        connection.commit()
    except Exception:
        connection.rollback()
        raise    
    
def main():

    connection = connect_to_mysql()

    try:
        if connection.is_connected():

            operator_ids = generate_operators(
                connection,
                10
            )

            location_ids = generate_locations(
                connection,
                operator_ids,
                50
            )

            charge_point_ids = generate_charge_points(
                connection,
                location_ids,
                200
            )

            customer_ids = generate_customers(
                connection,
                1000
            )

            transaction_ids = generate_transactions(
                connection,
                charge_point_ids,
                customer_ids,
                50000
            )

            generate_payments(
                connection
            )

            print("================================")
            print("FINAL DATA GENERATION COMPLETED")
            print("================================")

    finally:
        if connection.is_connected():
            connection.close()
    
if __name__ == "__main__":
    main()
