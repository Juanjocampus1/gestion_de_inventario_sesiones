# inventory/inventario_manager.py
import mysql.connector
import logging

logger = logging.getLogger(__name__)

class InventarioManager:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="curso",
                database="inventory"
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            logger.error(f"Error connecting to database: {err}")
            raise

    def get_products(self):
        try:
            self.cursor.execute("SELECT * FROM products")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            logger.error(f"Error fetching products: {err}")
            return []

    def add_product(self, name, quantity, price):
        try:
            self.cursor.execute("INSERT INTO products (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
            self.connection.commit()
            logger.info(f"Product {name} added successfully")
        except mysql.connector.Error as err:
            logger.error(f"Error adding product: {err}")
            raise

    def update_product(self, product_id, quantity):
        try:
            self.cursor.execute("UPDATE products SET quantity=%s WHERE id=%s", (quantity, product_id))
            self.connection.commit()
            logger.info(f"Product {product_id} updated successfully")
        except mysql.connector.Error as err:
            logger.error(f"Error updating product: {err}")
            raise

    def delete_product(self, product_id):
        try:
            self.cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
            self.connection.commit()
            logger.info(f"Product {product_id} deleted successfully")
        except mysql.connector.Error as err:
            logger.error(f"Error deleting product: {err}")
            raise

    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()