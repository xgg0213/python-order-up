from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin 
from werkzeug.security import generate_password_hash, check_password_hash 

db = SQLAlchemy()

class Employee(db.Model, UserMixin):  # Your class definition
    # Mapping attributes, here
    __tablename__="employees"

    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Name, not nullable
    employee_number = db.Column(db.Integer, nullable=False, unique=True)  # Unique, not nullable
    hashed_password = db.Column(db.String(255), nullable=False)  # Password, not nullable

    orders = db.relationship("Order", back_populates="employee", cascade="all, delete-orphan")

    # Password Property (getter)
    @property
    def password(self):
        return self.hashed_password

    # Password Property (setter)
    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    # Verify Password
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<Employee(id={self.id}, name='{self.name}', employee_number={self.employee_number})>"
    
# Menu model
class Menu(db.Model):
    __tablename__ = "menus"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)  # Name of the menu (e.g., "Lunch Menu")

    # Relationships
    items = db.relationship("MenuItem", back_populates="menu", cascade="all, delete-orphan")  # One-to-many relationship with MenuItem

    def __repr__(self):
        return f"<Menu(id={self.id}, name='{self.name}')>"
    

# MenuItemType model
class MenuItemType(db.Model):
    __tablename__ = "menu_item_types"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)  # Name of the menu item type (e.g., "Entree")

    # Relationships
    menu_items = db.relationship("MenuItem", back_populates="type", cascade="all, delete-orphan")  # One-to-many relationship with MenuItem

    def __repr__(self):
        return f"<MenuItemType(id={self.id}, name='{self.name}')>"


# MenuItem model
class MenuItem(db.Model):
    __tablename__ = "menu_items"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # Name of the menu item (e.g., "Burger")
    price = db.Column(db.Float, nullable=False)  # Price of the menu item
    menu_id = db.Column(db.Integer, db.ForeignKey("menus.id"), nullable=False)  # Foreign key to Menu
    menu_type_id = db.Column(db.Integer, db.ForeignKey("menu_item_types.id"), nullable=False)  # Foreign key to MenuItemType

    # Relationships
    menu = db.relationship("Menu", back_populates="items")  # Many-to-one relationship with Menu
    type = db.relationship("MenuItemType", back_populates="menu_items")  # Many-to-one relationship with MenuItemType

    def __repr__(self):
        return f"<MenuItem(id={self.id}, name='{self.name}', price={self.price})>"
    
# Table model
class Table(db.Model):
    __tablename__="tables"

    # Columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    number = db.Column(db.Integer, nullable=False, unique=True)  # Unique table number
    capacity = db.Column(db.Integer, nullable=False)  # Seating capacity

    orders = db.relationship("Order", back_populates="table", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Table(id={self.id}, number={self.number}, capacity={self.capacity})>"
    
# Order model
class Order(db.Model):
    __tablename__ = "orders"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)  # Foreign key to Employee
    table_id = db.Column(db.Integer, db.ForeignKey("tables.id"), nullable=False)  # Foreign key to Table
    finished = db.Column(db.Boolean, nullable=False, default=False)  # Indicates if the order is finished

    # Relationships
    employee = db.relationship("Employee", back_populates="orders")  # Link to Employee
    table = db.relationship("Table", back_populates="orders")  # Link to Table
    details = db.relationship("OrderDetail", back_populates="order", cascade="all, delete-orphan")  # Link to OrderDetail

    def __repr__(self):
        return f"<Order(id={self.id}, employee_id={self.employee_id}, table_id={self.table_id}, finished={self.finished})>"


# OrderDetail model
class OrderDetail(db.Model):
    __tablename__ = "order_details"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)  # Foreign key to Order
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable=False)  # Foreign key to MenuItem

    # Relationships
    order = db.relationship("Order", back_populates="details")  # Link back to Order
    menu_item = db.relationship("MenuItem")  # Link to MenuItem

    def __repr__(self):
        return f"<OrderDetail(id={self.id}, order_id={self.order_id}, menu_item_id={self.menu_item_id})>"
