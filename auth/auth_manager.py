# auth/auth_manager.py
import mysql.connector
import logging

logger = logging.getLogger(__name__)

class AuthManager:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="curso",
                database="usuarios"
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            logger.error(f"Error connecting to database: {err}")
            raise

        self.current_user = None
        self.current_user_role = None

    def login(self, username, password):
        try:
            self.cursor.execute("SELECT id, rol FROM usuario WHERE username=%s AND contraseña=%s", (username, password))
            result = self.cursor.fetchone()
            if result:
                self.current_user, self.current_user_role = result
                return True
            return False
        except mysql.connector.Error as err:
            logger.error(f"Error during login: {err}")
            return False

    def register(self, username, password, role="empleado"):
        try:
            self.cursor.execute("INSERT INTO usuario (username, contraseña, rol) VALUES (%s, %s, %s)", (username, password, role))
            self.connection.commit()
            logger.info(f"User {username} registered successfully")
        except mysql.connector.Error as err:
            logger.error(f"Error during registration: {err}")
            raise

    def logout(self):
        self.current_user = None
        self.current_user_role = None

    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()