import sqlite3
import os
import sys
sys.path.append(os.path.dirname(__file__) + '/..')
from models.database import Database, Student, FeeStructure, Payment

def add_sample_data():
    db = Database()
    db.get_connection()  # Ensure database is created

    # Add sample students
    students_data = [
        ('John Doe', 'Male', '2015-05-15', 1, 'Jane Doe', '0241234567', 'Accra, Ghana'),
        ('Mary Smith', 'Female', '2014-08-20', 2, 'Bob Smith', '0247654321', 'Tema, Ghana'),
        ('Peter Johnson', 'Male', '2013-03-10', 5, 'Alice Johnson', '0209876543', 'Cape Coast, Ghana'),
        ('Sarah Williams', 'Female', '2012-11-25', 6, 'David Williams', '0271122334', 'Kumasi, Ghana'),
        ('Michael Brown', 'Male', '2011-07-05', 12, 'Emma Brown', '0264455667', 'Takoradi, Ghana'),
    ]

    for data in students_data:
        student_id = Student.generate_student_id()
        Student.add((student_id,) + data)

    # Add sample fees structure
    fees_data = [
        (1, 'First Term', 500.00),
        (1, 'Second Term', 500.00),
        (1, 'Third Term', 500.00),
        (2, 'First Term', 550.00),
        (2, 'Second Term', 550.00),
        (2, 'Third Term', 550.00),
        (5, 'First Term', 600.00),
        (5, 'Second Term', 600.00),
        (5, 'Third Term', 600.00),
        (6, 'First Term', 650.00),
        (6, 'Second Term', 650.00),
        (6, 'Third Term', 650.00),
        (12, 'First Term', 700.00),
        (12, 'Second Term', 700.00),
        (12, 'Third Term', 700.00),
    ]

    for class_id, term, amount in fees_data:
        FeeStructure.set_fee(class_id, term, amount)

    # Add sample payments
    payments_data = [
        ('ST0001', 500.00, 'First Term', '2024-09-01', 'Cash'),
        ('ST0002', 550.00, 'First Term', '2024-09-02', 'Mobile Money'),
        ('ST0003', 300.00, 'First Term', '2024-09-03', 'Cash'),
        ('ST0004', 650.00, 'First Term', '2024-09-04', 'Bank Transfer'),
        ('ST0005', 350.00, 'First Term', '2024-09-05', 'Cash'),
    ]

    for data in payments_data:
        receipt_number = Payment.generate_receipt_number()
        Payment.add(data + (receipt_number,))

    print("Sample data added successfully!")

if __name__ == '__main__':
    add_sample_data()