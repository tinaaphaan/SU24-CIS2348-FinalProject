# Tina Phan | PSID: 2064343

# Import necessary libraries
import csv
from datetime import datetime

# Define function to load data from CSV files
def open_csv(filename):
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")

# Define function to sort by manufacturer name for FullInventory file
def manufacturer_sort(item):
    return item[1]

# Define function to sort by item ID for item type Inventory files
def itemID_sort(item):
    return item[0]

# Define function to sort by service date for PastServiceDateInventory file
def serviceDate_sort(item):
    return datetime.strptime(item[4], "%m/%d/%Y")

# Define function to sort by price for DamagedInventory file
def price_sort(item):
    return int(item[3])

# Define main function
def main():
    manufacturer_data = open_csv('ManufacturerList.csv')
    price_data = open_csv('PriceList.csv')
    service_data = open_csv('ServiceDatesList.csv')

    # Create respective dictionaries for price and service date
    prices = {row[0]: row[1] for row in price_data}
    services = {row[0]: row[1] for row in service_data}

    # Create list for full inventory data
    full_inventory = []
    # Create full inventory data
    for item in manufacturer_data:
        item_id = item[0]
        manufacturer_name = item[1]
        item_type = item[2]
        damaged = item[3] if len(item) > 3 else ''
        price = prices.get(item_id, '')
        service_date = services.get(item_id, '')

        full_inventory.append([item_id, manufacturer_name, item_type, price, service_date, damaged])

    # Write to FullInventory.csv
    full_inventory_sorted = sorted(full_inventory, key=manufacturer_sort)
    with open('FullInventory.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for item in full_inventory_sorted:
            writer.writerow(item)

    # Write to item type inventory CSV files
    item_types = set(item[2] for item in full_inventory)
    for item_type in item_types:
        item_type_inventory = [item for item in full_inventory if item[2] == item_type]
        item_type_inventory_sorted = sorted(item_type_inventory, key=itemID_sort)
        with open(f'{item_type}Inventory.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for item in item_type_inventory_sorted:
                writer.writerow(item)

    # Create datetime for when the program is executed
    today = datetime.today()
    
    # Write to PastServiceDateInventory.csv
    past_service_inventory = [item for item in full_inventory if datetime.strptime(item[4], "%m/%d/%Y") < today]
    past_service_inventory_sorted = sorted(past_service_inventory, key=serviceDate_sort)
    with open('PastServiceDateInventory.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for item in past_service_inventory_sorted:
            writer.writerow(item)

    # Write to DamagedInventory.csv
    damaged_inventory = [item for item in full_inventory if item[5]]
    damaged_inventory_sorted = sorted(damaged_inventory, key=price_sort, reverse=True)
    with open('DamagedInventory.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for item in damaged_inventory_sorted:
            writer.writerow(item)

# Call the main function to execute program
if __name__ == '__main__':
    main()
