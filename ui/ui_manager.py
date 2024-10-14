from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox

class UIManager:
    def __init__(self, parent):
        self.parent = parent

    def create_inventory_table(self):
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Producto", "Precio", "Cantidad"])
        return table

    def update_inventory_table(self, table, inventario):
        table.setRowCount(len(inventario))
        for row, (producto, datos) in enumerate(inventario.items()):
            table.setItem(row, 0, QTableWidgetItem(producto))
            table.setItem(row, 1, QTableWidgetItem(str(datos['precio'])))
            table.setItem(row, 2, QTableWidgetItem(str(datos['cantidad'])))

    def show_message(self, title, message):
        QMessageBox.information(self.parent, title, message)

    def show_warning(self, title, message):
        QMessageBox.warning(self.parent, title, message)