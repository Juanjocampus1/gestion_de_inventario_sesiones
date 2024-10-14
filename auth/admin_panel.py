from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QMessageBox


class AdminPanel(QDialog):
    def __init__(self, auth_manager, parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.setWindowTitle("Panel de Administración")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Contraseña")
        layout.addWidget(self.password_input)

        self.role_combobox = QComboBox()
        self.role_combobox.addItems(["admin", "empleado", "cliente"])
        layout.addWidget(self.role_combobox)

        self.create_button = QPushButton("Crear Usuario")
        self.create_button.clicked.connect(self.create_user)
        layout.addWidget(self.create_button)

        self.update_button = QPushButton("Actualizar Rol")
        self.update_button.clicked.connect(self.update_role)
        layout.addWidget(self.update_button)

        self.setLayout(layout)

    def create_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_combobox.currentText()
        if self.auth_manager.create_user(username, password, role):
            QMessageBox.information(self, "Éxito", "Usuario creado exitosamente.")
        else:
            QMessageBox.warning(self, "Error", "Usuario ya registrado.")

    def update_role(self):
        username = self.username_input.text()
        role = self.role_combobox.currentText()
        if self.auth_manager.update_user_role(username, role):
            QMessageBox.information(self, "Éxito", "Rol actualizado exitosamente.")
        else:
            QMessageBox.warning(self, "Error", "Usuario no encontrado.")