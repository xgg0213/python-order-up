from dotenv import load_dotenv
load_dotenv()

# Regardless of the lint error you receive,
# load_dotenv must run before running this
# so that the environment variables are
# properly loaded.
from app import app, db
from app.models import Employee, Menu, MenuItem, MenuItemType, Table, Order, OrderDetail


with app.app_context():
    # Drop and recreate all tables
    db.drop_all()
    db.create_all()

    # Create an Employee
    employee = Employee(name="Margot", employee_number=1234, password="password")
    db.session.add(employee)
    db.session.commit()

    # Create MenuItemTypes
    beverages = MenuItemType(name="Beverages")
    entrees = MenuItemType(name="Entrees")
    sides = MenuItemType(name="Sides")

    # Create a Menu
    dinner = Menu(name="Dinner")

    # Create MenuItems
    fries = MenuItem(name="French fries", price=3.50, type=sides, menu=dinner)
    drp = MenuItem(name="Dr. Pepper", price=1.0, type=beverages, menu=dinner)
    jambalaya = MenuItem(name="Jambalaya", price=21.98, type=entrees, menu=dinner)

    # Add data to the session
    # db.session.add_all([beverages, entrees, sides, dinner])
    db.session.add(dinner)

    # Commit the session
    db.session.commit()


    # Create 10 tables dynamically
    tables = [Table(number=i, capacity=(i % 6) + 2) for i in range(1, 11)]

    # Add and commit the tables
    db.session.add_all(tables)
    db.session.commit()


    # Use existing table and menu items to create an order
    table1 = Table.query.filter_by(number=1).first()
    order = Order(employee=employee, table=table1, finished=False)
    db.session.add(order)
    db.session.commit()

    # Add order details
    burger = MenuItem.query.filter_by(name="Burger").first()
    if not burger:
        burger = MenuItem(name="Burger", price=9.99, menu=dinner, type=entrees)
        db.session.add(burger)
    fries = MenuItem.query.filter_by(name="French fries").first()
    if not fries:
        fries = MenuItem(name="French fries", price=3.50, menu=dinner, type=sides)
        db.session.add(fries)
    detail1 = OrderDetail(order=order, menu_item=burger)
    detail2 = OrderDetail(order=order, menu_item=fries)
    db.session.add_all([detail1, detail2])
    db.session.commit()