import json
from pathlib import Path

INVENTORY_PATH = Path("APP/data/inventory.json")

#load current inventory
def load_inventory():
    if INVENTORY_PATH.exists():
        with open(INVENTORY_PATH, "r") as f:
            return json.load(f)
        return {}


def save_inventory(data):
    with open(INVENTORY_PATH,"w") as f:
        json.dump(data,f, indent=2)


def check_inventory(product:str,quantity:int):
    inventory= load_inventory()
    currnet_stock = inventory.get(product, 0)
    if currnet_stock>= quantity:
        inventory[product]-= quantity
        save_inventory(inventory)
        