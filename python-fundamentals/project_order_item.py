import csv
from pathlib import Path


def create_csv_file(path, order_items, total, vat, grand_total):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Item Name", "Cost"])
        # for item in order_items:
        #     writer.writerow([item[0], f"{item[1]:.2f}"])
        writer.writerows([[item[0], f"{item[1]:.2f}"] for item in order_items])
        writer.writerow(["Total", f"{total:.2f}"])
        writer.writerow(["VAT", f"{vat:.2f}"])
        writer.writerow(["Grand Total", f"{grand_total:.2f}"])
        print(f"Order saved to {path}")


def calculate_total_cost(order_items):
    total = sum(item[1] for item in order_items)
    vat = total * 0.20
    grand_total = total + vat
    # This will return a tuple containing the total, vat, and grand_total
    return total, vat, grand_total


def get_user_order():
    order_items = []

    while True:
        name = input(
            "Enter the order item name (or type 'c' to cancel, when you're done type 'done'): "
        )
        if name.lower() == "c":
            print("Order canceled. please start again.")
            return None
        if name.lower() == "done":
            print("Order completed.")
            break
        try:
            order_cost = float(input(f"{name} - price: "))

        except ValueError:
            print("Invalid input. Please enter a valid order number.")
            continue
        print(f"Order item: {name}, Cost: {order_cost:.2f}")
        order_items.append((name, order_cost))
    return order_items


def main():

    # Get the order number from the user
    try:
        order_number = int(input("Enter the order number: "))
        print(f"Starting taking order for: {order_number}")
    except ValueError:
        print("Invalid input. Please enter a valid order number. Canceling order.")
        return
    # Create a file path for the order
    path = Path(__file__).parent / f"order_{order_number}.csv"
    print(f"Order will be saved to: {path}")
    # Get order items from the user
    order_items = get_user_order()
    if order_items is None:
        print("Order was canceled. Nothing was saved.")
        return
    if not order_items:
        print("No order items were entered. Canceling order.")
        return
    # Calculate the total cost, VAT, and grand total
    total, vat, grand_total = calculate_total_cost(order_items)
    print(f"Total: {total:.2f}, VAT: {vat:.2f}, Grand Total: {grand_total:.2f}")
    # Save the order to a CSV file
    create_csv_file(path, order_items, total, vat, grand_total)
    # with open(path, "w") as file:
    #     file.write("Item Name,Cost\n")
    #     for item in order_items:
    #         file.write(f"{item[0]},{item[1]:.2f}\n")
    #     file.write(f"Total,{total:.2f}\n")
    #     file.write(f"VAT,{vat:.2f}\n")
    #     file.write(f"Grand Total,{grand_total:.2f}\n")


if __name__ == "__main__":
    main()
