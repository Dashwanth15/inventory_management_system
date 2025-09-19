import pickle
import logging

def save_data(order_queue, orders_items, filename='inventory_data.pkl'):
    try:
        with open(filename, 'wb') as f:
            pickle.dump((order_queue.queue, orders_items), f)
    except Exception as e:
        logging.error(f"Failed to save data: {e}")

def load_data(filename='inventory_data.pkl'):
    try:
        with open(filename, 'rb') as f:
            queue, orders_items = pickle.load(f)
            return queue, orders_items
    except FileNotFoundError:
        return [], {}
    except Exception as e:
        logging.error(f"Failed to load data: {e}")
        return [], {}
