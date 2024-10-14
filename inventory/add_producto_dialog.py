from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox

class AddProductoDialog(QDialog):
    def __init__(self, inventario_manager, parent=None):
        super().__init__(parent)
        self.inventario_manager = inventario_manager
        self.setWindowTitle("Añadir Producto")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.producto_input = QLineEdit()
        self.producto_input.setPlaceholderText("Producto")
        layout.addWidget(self.producto_input)

        self.cantidad_input = QLineEdit()
        self.cantidad_input.setPlaceholderText("Cantidad")
        layout.addWidget(self.cantidad_input)

        self.precio_input = QLineEdit()
        self.precio_input.setPlaceholderText("Precio")
        layout.addWidget(self.precio_input)

        self.add_button = QPushButton("Añadir")
        self.add_button.clicked.connect(self.add_producto)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_producto(self):
        producto = self.producto_input.text()
        cantidad = self.cantidad_input.text()
        precio = self.precio_input.text()
        if producto and cantidad.isdigit() and precio.replace('.', '', 1).isdigit():
            self.inventario_manager.add_producto(producto, int(cantidad), float(precio))
            QMessageBox.information(self, "Éxito", "Producto añadido exitosamente.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Por favor, introduce un producto, una cantidad y un precio válidos.")