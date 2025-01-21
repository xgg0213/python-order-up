from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Order, Table, Employee, MenuItem, MenuItemType, db
from ..forms import TableAssignmentForm, MenuItemAssignmentForm

bp = Blueprint("orders", __name__, url_prefix="")


@bp.route("/")
@login_required
def index():
    # Get forms
    assign_table_form = TableAssignmentForm()
    menu_item_form = MenuItemAssignmentForm()

    # Get tables and open orders
    tables = Table.query.order_by(Table.number).all()
    open_orders = Order.query.filter(Order.finished == False)
    busy_table_ids = [order.table_id for order in open_orders]
    open_tables = [table for table in tables if table.id not in busy_table_ids]

    # Set choices for the forms
    assign_table_form.tables.choices = [(t.id, f"Table {t.number}") for t in open_tables]
    assign_table_form.servers.choices = [(e.id, e.name) for e in Employee.query.all()]

    # Get menu items grouped by type
    menu_items = MenuItem.query.join(MenuItemType).order_by(MenuItemType.name, MenuItem.name).all()
    menu_items_by_type = {}
    for item in menu_items:
        if item.type.name not in menu_items_by_type:
            menu_items_by_type[item.type.name] = []
        menu_items_by_type[item.type.name].append(item)

    # Get current user's open orders
    your_orders = Order.query.filter(
        Order.employee_id == current_user.id,
        Order.finished == False
    ).all()

    return render_template(
        "orders.html",
        assign_table_form=assign_table_form,
        menu_item_form=menu_item_form,
        menu_items_by_type=menu_items_by_type,
        your_orders=your_orders
    )

@bp.route("/tables/assign", methods=["POST"])
@login_required
def assign_table():
    form = TableAssignmentForm()
    if form.validate_on_submit():
        order = Order(
            employee_id=form.servers.data,
            table_id=form.tables.data,
            finished=False
        )
        db.session.add(order)
        db.session.commit()
    return redirect(url_for(".index"))

@bp.route("/orders/<int:id>/close", methods=["POST"])
@login_required
def close_table(id):
    order = Order.query.get(id)
    if order:
        order.finished = True
        db.session.commit()
    return redirect(url_for(".index"))

@bp.route("/orders/<int:id>/items", methods=["POST"])
@login_required
def add_to_order(id):
    form = MenuItemAssignmentForm()
    if form.validate_on_submit():
        order = Order.query.get(id)
        if order:
            for item_id in form.menu_item_ids.data:
                detail = OrderDetail(order_id=id, menu_item_id=item_id)
                db.session.add(detail)
            db.session.commit()
    return redirect(url_for(".index"))