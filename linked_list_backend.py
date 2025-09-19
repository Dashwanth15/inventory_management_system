# linked_list_backend.py

class Node:
    def __init__(self, item_name, quantity):
        self.item_name = item_name
        self.quantity = quantity
        self.next = None

class GroceryLinkedList:
    def __init__(self):
        self.head = None

    def add_item(self, item_name, quantity):
        new_node = Node(item_name, quantity)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def delete_item(self, item_name):
        current = self.head
        prev = None
        while current:
            if current.item_name == item_name:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False

    def update_item(self, item_name, new_quantity):
        current = self.head
        while current:
            if current.item_name == item_name:
                current.quantity = new_quantity
                return True
            current = current.next
        return False

    def view_items(self):
        items = []
        current = self.head
        while current:
            items.append((current.item_name, current.quantity))
            current = current.next
        return items

