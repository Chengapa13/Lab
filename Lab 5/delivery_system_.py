"""Manage food delivery orders and save the queue as JSON."""

import json
from datetime import datetime

ORDERS = {}
MENU = {}
VALID_STATUSES = ["placed", "cooking", "out_for_delivery", "delivered"]


def create_order(customer, items, order_history=None):
    """Create a valid order and return its ID."""
    if not isinstance(customer, str) or not customer.strip():
        raise ValueError("Customer name cannot be empty")
    if not isinstance(items, list) or not items:
        raise ValueError("An order must contain a list of items")
    for item in items:
        if item not in MENU:
            raise ValueError(f"Unknown menu item: {item}")
    if order_history is None:
        order_history = []
    order_id = max(ORDERS, default=0) + 1
    ORDERS[order_id] = {
        "customer": customer.strip(),
        "items": items.copy(),
        "total": sum(MENU[item] for item in items),
        "status": "placed",
    }
    order_history.append(order_id)
    return order_id


def update_order_status(order_id, status):
    """Update an existing order using one of the valid statuses."""
    if order_id not in ORDERS:
        raise ValueError(f"Order ID not found: {order_id}")
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    ORDERS[order_id]["status"] = status


def read_menu_config(filename="menu.json"):
    """Read the menu, or use the default if the file is unavailable."""
    try:
        with open(filename, encoding="utf-8") as menu_file:
            loaded_menu = json.load(menu_file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Using default menu: {error}")
        loaded_menu = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}
    if not isinstance(loaded_menu, dict) or not loaded_menu:
        raise ValueError("Menu must be a non-empty JSON object")
    for dish, price in loaded_menu.items():
        if not dish.strip() or type(price) not in (int, float) or price < 0:
            raise ValueError("Menu needs named dishes and non-negative prices")
    MENU.clear()
    MENU.update(loaded_menu)


def daily_revenue():
    """Return the total value of delivered orders."""
    return sum(
        order["total"] for order in ORDERS.values()
        if order["status"] == "delivered"
    )


def backup_orders(filename="orders.json"):
    """Save orders as JSON without using pickle."""
    with open(filename, "w", encoding="utf-8") as backup_file:
        json.dump(ORDERS, backup_file, indent=4)


def restore_orders(filename="orders.json"):
    """Restore orders and convert JSON string keys back to integer IDs."""
    with open(filename, encoding="utf-8") as backup_file:
        saved_orders = json.load(backup_file)
    restored_orders = {
        int(order_id): order for order_id, order in saved_orders.items()
    }
    ORDERS.clear()
    ORDERS.update(restored_orders)


def print_queue():
    """Print the customer, status and total for each order."""
    print(f"Order queue at {datetime.now()}")
    for order_id, order in ORDERS.items():
        print(order_id, order["customer"], order["status"], order["total"])


def main():
    """Run a small example and show how invalid requests are handled."""
    read_menu_config()
    asha_order = create_order("Asha", ["pizza", "coke"])
    ravi_order = create_order("Ravi", ["burger", "fries"])
    update_order_status(asha_order, "delivered")
    for customer, items in [("Ravi", ["burger", "sushi"]), ("", [])]:
        try:
            create_order(customer, items)
        except ValueError as error:
            print("Order rejected:", error)
    for order_id, status in [(ravi_order, "teleported"), (42, "delivered")]:
        try:
            update_order_status(order_id, status)
        except ValueError as error:
            print("Status update rejected:", error)
    print("Revenue today:", daily_revenue())
    backup_orders()
    restore_orders()
    print_queue()


if __name__ == "__main__":
    main()
