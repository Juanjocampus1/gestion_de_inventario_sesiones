# auth/register_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
import logging

logger = logging.getLogger(__name__)

class RegisterDialog(QDialog):
    def __init__(self, auth_manager, parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.setWindowTitle("Registrarse")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.register_button = QPushButton("Registrarse")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            self.auth_manager.register(username, password)
            QMessageBox.information(self, "Éxito", "Usuario registrado con éxito")
            self.accept()
        except Exception as e:
            logger.error(f"Error during registration: {e}")
            QMessageBox.critical(self, "Error", f"Error al registrar el usuario: {e}")