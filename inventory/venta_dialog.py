from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox

class VentaDialog(QDialog):
    def __init__(self, inventario_manager, parent=None):
        super().__init__(parent)
        self.inventario_manager = inventario_manager
        self.setWindowTitle("Realizar Venta")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.producto_input = QLineEdit()
        self.producto_input.setPlaceholderText("Producto")
        layout.addWidget(self.producto_input)

        self.cantidad_input = QLineEdit()
        self.cantidad_input.setPlaceholderText("Cantidad")
        layout.addWidget(self.cantidad_input)

        self.importe_input = QLineEdit()
        self.importe_input.setPlaceholderText("Importe")
        layout.addWidget(self.importe_input)

        self.vender_button = QPushButton("Vender")
        self.vender_button.clicked.connect(self.realizar_venta)
        layout.addWidget(self.vender_button)

        self.setLayout(layout)

    def realizar_venta(self):
        producto = self.producto_input.text()
        cantidad = self.cantidad_input.text()
        importe = self.importe_input.text()
        if producto and cantidad.isdigit() and importe.replace('.', '', 1).isdigit():
            try:
                self.inventario_manager.realizar_venta(producto, int(cantidad))
                self.accept()
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Error", "Por favor, introduce un producto, una cantidad y un importe válidos.")

    def get_data(self):
        return self.producto_input.text(), int(self.cantidad_input.text()), float(self.importe_input.text())