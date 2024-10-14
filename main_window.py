import logging
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QGroupBox, QHBoxLayout, \
    QTableWidget, QTableWidgetItem, QMessageBox, QScrollArea, QLineEdit, QDialog, QStackedLayout, QListWidget
from PyQt5 import QtGui
from inventory.inventario_manager import InventarioManager
from ui.ui_manager import UIManager
from sales.sales_history_manager import SalesHistoryManager
from auth.auth_manager import AuthManager
from auth.login_dialog import LoginDialog
from auth.register_dialog import RegisterDialog
from auth.admin_panel import AdminPanel
from inventory.add_producto_dialog import AddProductoDialog
from logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Inventario")
        self.setGeometry(100, 100, 1200, 600)

        self.inventario_manager = InventarioManager()
        self.ui_manager = UIManager(self)
        self.sales_history_manager = SalesHistoryManager(self)
        self.auth_manager = AuthManager()

        self.current_section = 0
        self.sections = []

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.section_container = QWidget()
        self.section_layout = QStackedLayout()
        self.section_container.setLayout(self.section_layout)
        main_layout.addWidget(self.section_container)

        self.init_sections()

        nav_layout = QHBoxLayout()
        self.prev_button = self.create_button("Anterior", self.show_previous_section)
        nav_layout.addWidget(self.prev_button)

        self.next_button = self.create_button("Siguiente", self.show_next_section)
        nav_layout.addWidget(self.next_button)

        self.username_label = QLabel("")
        self.username_label.setStyleSheet("font-size: 16px; color: #333;")
        nav_layout.addWidget(self.username_label)

        main_layout.addLayout(nav_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.show_section(0)

    def init_sections(self):
        self.sections.append(self.create_inventory_section())
        self.sections.append(self.create_sales_section())
        self.sections.append(self.create_auth_section())
        self.sections.append(self.create_accounting_section())
        for section in self.sections:
            self.section_layout.addWidget(section)

    def create_inventory_section(self):
        section = QWidget()
        layout = QHBoxLayout()

        inventory_layout = QVBoxLayout()

        self.label = QLabel("Bienvenido a la Gestión de Inventario")
        self.label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #6A0DAD;
            margin-bottom: 20px;
        """)
        inventory_layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Producto", "Cantidad", "Precio"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #6A0DAD;
                color: white;
                padding: 4px;
                border: 1px solid #ddd;
            }
            QTableWidget::item {
                padding: 4px;
                border: 1px solid #ddd;
            }
        """)
        self.update_inventory_table()

        table_scroll_area = QScrollArea()
        table_scroll_area.setWidgetResizable(True)
        table_scroll_area.setWidget(self.table)
        inventory_layout.addWidget(table_scroll_area)

        self.update_inventory_table()

        inventory_group = QGroupBox("Inventario")
        inventory_group_layout = QVBoxLayout()

        self.btn_add_producto = self.create_button("Añadir Producto", self.mostrar_add_producto_dialog)
        self.btn_add_producto.setEnabled(False)
        inventory_group_layout.addWidget(self.btn_add_producto)

        self.btn_guardar = self.create_button("Guardar Cambios", self.guardar_cambios)
        self.btn_guardar.setEnabled(False)
        inventory_group_layout.addWidget(self.btn_guardar)

        inventory_group.setLayout(inventory_group_layout)
        inventory_layout.addWidget(inventory_group)

        layout.addLayout(inventory_layout)

        right_layout = QVBoxLayout()

        self.sales_history = self.sales_history_manager.create_sales_history_list()
        right_layout.addWidget(QLabel("Historial de Ventas"))
        right_layout.addWidget(self.sales_history)

        self.btn_ver_contabilidad = self.create_button("Ver Contabilidad", self.mostrar_contabilidad)
        self.btn_ver_contabilidad.setEnabled(False)
        right_layout.addWidget(self.btn_ver_contabilidad)

        layout.addLayout(right_layout)

        section.setLayout(layout)
        return section

    def create_sales_section(self):
        section = QWidget()
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

        self.vender_button = self.create_button("Vender", self.realizar_venta)
        layout.addWidget(self.vender_button)

        section.setLayout(layout)
        return section

    def create_auth_section(self):
        section = QWidget()
        layout = QVBoxLayout()

        self.btn_login = self.create_button("Iniciar Sesión", self.mostrar_login_dialog)
        layout.addWidget(self.btn_login)

        self.btn_register = self.create_button("Registrarse", self.mostrar_register_dialog)
        layout.addWidget(self.btn_register)

        self.btn_logout = self.create_button("Cerrar Sesión", self.logout)
        self.btn_logout.setEnabled(False)
        layout.addWidget(self.btn_logout)

        self.username_label = QLabel("")
        layout.addWidget(self.username_label)

        self.btn_admin_panel = self.create_button("Panel de Administración", self.mostrar_admin_panel)
        self.btn_admin_panel.setEnabled(False)
        layout.addWidget(self.btn_admin_panel)

        section.setLayout(layout)
        return section

    def create_accounting_section(self):
        section = QWidget()
        layout = QVBoxLayout()

        self.btn_ver_contabilidad = self.create_button("Ver Contabilidad", self.mostrar_contabilidad)
        self.btn_ver_contabilidad.setEnabled(False)
        layout.addWidget(self.btn_ver_contabilidad)

        section.setLayout(layout)
        return section

    def show_section(self, index):
        self.current_section = index
        self.section_layout.setCurrentIndex(index)

    def show_previous_section(self):
        if self.current_section > 0:
            self.show_section(self.current_section - 1)

    def show_next_section(self):
        if self.current_section < len(self.sections) - 1:
            self.show_section(self.current_section + 1)

    def create_button(self, text, callback):
        button = QPushButton(text)
        button.setFont(QtGui.QFont("Arial", 12))
        button.setStyleSheet("""
            QPushButton {
                background-color: #6A0DAD; /* Purple */
                color: white;
                border: 2px solid #6A0DAD;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                transition: background-color 0.3s ease, color 0.3s ease;
            }
            QPushButton:hover {
                background-color: white;
                color: #6A0DAD;
            }
            QPushButton:pressed {
                background-color: #5A0C9A;
            }
        """)
        button.clicked.connect(callback)
        return button

    def update_inventory_table(self):
        self.table.setRowCount(0)
        inventario = self.inventario_manager.get_products()
        for row, (id, name, quantity, price) in enumerate(inventario):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(id)))
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(str(quantity)))
            self.table.setItem(row, 3, QTableWidgetItem(f"${price:.2f}"))

    def guardar_cambios(self):
        # Código para guardar los cambios realizados en el inventario
        pass

    def realizar_venta(self):
        producto = self.producto_input.text()
        cantidad = self.cantidad_input.text()
        importe = self.importe_input.text()
        if not producto or not cantidad or not importe:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            return

        try:
            cantidad = int(cantidad)
            importe = float(importe)
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingrese valores válidos.")
            return

        self.sales_history_manager.add_sale(producto, cantidad, importe)

    def mostrar_add_producto_dialog(self):
        dialog = AddProductoDialog(self)
        dialog.exec_()

    def mostrar_login_dialog(self):
        dialog = LoginDialog(self)
        if dialog.exec_():
            username = dialog.username_input.text()
            self.auth_manager.login(username)
            self.username_label.setText(f"Usuario: {username}")
            self.btn_add_producto.setEnabled(True)
            self.btn_guardar.setEnabled(True)
            self.btn_ver_contabilidad.setEnabled(True)
            self.btn_logout.setEnabled(True)
            self.btn_admin_panel.setEnabled(self.auth_manager.is_admin())

    def mostrar_register_dialog(self):
        dialog = RegisterDialog(self)
        dialog.exec_()

    def logout(self):
        self.auth_manager.logout()
        self.username_label.setText("")
        self.btn_add_producto.setEnabled(False)
        self.btn_guardar.setEnabled(False)
        self.btn_ver_contabilidad.setEnabled(False)
        self.btn_logout.setEnabled(False)
        self.btn_admin_panel.setEnabled(False)

    def mostrar_admin_panel(self):
        if self.auth_manager.is_admin():
            panel = AdminPanel(self)
            panel.exec_()

    def mostrar_contabilidad(self):
        try:
            if self.auth_manager.current_user_role == 'admin':
                # Show accounting information
                pass
            else:
                QMessageBox.warning(self, "Acceso Denegado", "No tienes permisos para ver la contabilidad.")
        except Exception as e:
            logger.error(f"Exception: {e}")
            QMessageBox.warning(self, "Error", f"Ha ocurrido un error inesperado: {e}")

    def closeEvent(self, event):
        self.inventario_manager.close()
        self.sales_history_manager.close()
        self.auth_manager.close()
