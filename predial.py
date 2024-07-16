import sys
import hashlib
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QCheckBox, QStackedWidget, QTabWidget, QLabel, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sqlite3
import re

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            QMessageBox.critical(None, "Database Error", f"Error connecting to database: {e}")

    def setup(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                apellido TEXT,
                telefono TEXT UNIQUE,
                correo TEXT,
                contrasena TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS adeudos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cuenta TEXT UNIQUE,
                adeudo REAL
            )
        ''')
        self.conn.commit()

    def register_user(self, nombre, apellido, telefono, correo, contrasena):
        hashed_password = hashlib.sha256(contrasena.encode()).hexdigest()
        self.cursor.execute('''
            INSERT INTO usuarios (nombre, apellido, telefono, correo, contrasena)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, apellido, telefono, correo, hashed_password))
        self.conn.commit()

    def login_user(self, telefono, contrasena):
        hashed_password = hashlib.sha256(contrasena.encode()).hexdigest()
        self.cursor.execute('''
            SELECT * FROM usuarios WHERE telefono = ? AND contrasena = ?
        ''', (telefono, hashed_password))
        return self.cursor.fetchone()

    def query_debt(self, cuenta):
        self.cursor.execute('SELECT adeudo FROM adeudos WHERE cuenta = ?', (cuenta,))
        return self.cursor.fetchone()

    def add_debt(self, cuenta, adeudo):
        self.cursor.execute('''
            INSERT INTO adeudos (cuenta, adeudo)
            VALUES (?, ?)
        ''', (cuenta, adeudo))
        self.conn.commit()

    def close(self):
        self.conn.close()


class AuthWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header_label = QLabel("Predial")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(header_label)
        
        self.tab_widget = QTabWidget()
        self.login_tab = QWidget()
        self.register_tab = QWidget()
        
        self.tab_widget.addTab(self.login_tab, "Iniciar sesión")
        self.tab_widget.addTab(self.register_tab, "Registrarse")
        
        login_layout = QVBoxLayout(self.login_tab)
        self.login_phone = QLineEdit()
        self.login_phone.setPlaceholderText('Teléfono')
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText('Contraseña')
        self.login_password.setEchoMode(QLineEdit.Password)
        self.terms_checkbox = QCheckBox('Aceptar términos')
        self.login_button = QPushButton('Entrar')
        self.login_button.setStyleSheet("background-color: #4CAF50; color: black; padding: 10px;")
        
        login_layout.addWidget(self.login_phone)
        login_layout.addWidget(self.login_password)
        login_layout.addWidget(self.terms_checkbox)
        login_layout.addWidget(self.login_button)
        login_layout.setSpacing(10)
        
        register_layout = QVBoxLayout(self.register_tab)
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText('Nombres')
        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText('Apellidos')
        self.register_phone = QLineEdit()
        self.register_phone.setPlaceholderText('Número de teléfono')
        self.email = QLineEdit()
        self.email.setPlaceholderText('Correo electrónico')
        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText('Contraseña')
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_button = QPushButton('Regístrate')
        self.register_button.setStyleSheet("background-color: #008CBA; color: black; padding: 10px;")
        
        register_layout.addWidget(self.first_name)
        register_layout.addWidget(self.last_name)
        register_layout.addWidget(self.register_phone)
        register_layout.addWidget(self.email)
        register_layout.addWidget(self.register_password)
        register_layout.addWidget(self.register_button)
        register_layout.setSpacing(10)
        
        layout.addWidget(self.tab_widget)


class DebtQueryWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header_label = QLabel("Predial")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(header_label)
        
        self.account_number = QLineEdit()
        self.account_number.setPlaceholderText('Cuenta predial (ej. UA009999001)')
        
        self.query_button = QPushButton('Consultar')
        self.query_button.setStyleSheet("background-color: #008CBA; color: black; padding: 10px;")
        
        self.logout_button = QPushButton('Cerrar sesión')
        self.logout_button.setStyleSheet("background-color: #f44336; color: black; padding: 10px;")
        
        layout.addWidget(self.account_number)
        layout.addWidget(self.query_button)
        layout.addWidget(self.logout_button)
        layout.setSpacing(10)


class PaymentWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header_label = QLabel("Predial")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(header_label)
        
        self.pay_button = QPushButton('Pagar')
        self.pay_button.setStyleSheet("background-color: #4CAF50; color: black; padding: 10px;")
        layout.addWidget(self.pay_button)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)


class AddDebtWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header_label = QLabel("Añadir Adeudo")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(header_label)
        
        self.account_number = QLineEdit()
        self.account_number.setPlaceholderText('Cuenta predial')
        
        self.debt_amount = QLineEdit()
        self.debt_amount.setPlaceholderText('Monto de adeudo')
        
        self.add_button = QPushButton('Añadir')
        self.add_button.setStyleSheet("background-color: #4CAF50; color: black; padding: 10px;")
        
        layout.addWidget(self.account_number)
        layout.addWidget(self.debt_amount)
        layout.addWidget(self.add_button)
        layout.setSpacing(10)


class PredialApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager('usuarios.db')
        self.db.setup()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Sistema de Predial')
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet("background-color: #f0f0f0; font-family: Arial; color: black;")

        self.stack = QStackedWidget()
        self.auth_window = AuthWindow()
        self.debt_query_window = DebtQueryWindow(self)
        self.payment_window = PaymentWindow(self)
        self.add_debt_window = AddDebtWindow(self)

        self.stack.addWidget(self.auth_window)
        self.stack.addWidget(self.debt_query_window)
        self.stack.addWidget(self.payment_window)
        self.stack.addWidget(self.add_debt_window)

        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

        self.auth_window.login_button.clicked.connect(self.login)
        self.auth_window.register_button.clicked.connect(self.register)
        self.debt_query_window.query_button.clicked.connect(self.query_debt)
        self.debt_query_window.logout_button.clicked.connect(self.logout)
        self.payment_window.pay_button.clicked.connect(self.process_payment)
        self.add_debt_window.add_button.clicked.connect(self.add_debt)

    def login(self):
        telefono = self.auth_window.login_phone.text()
        contrasena = self.auth_window.login_password.text()
        aceptar_terminos = self.auth_window.terms_checkbox.isChecked()

        if telefono and contrasena and aceptar_terminos:
            usuario = self.db.login_user(telefono, contrasena)
            if usuario:
                QMessageBox.information(self, 'Inicio de sesión', 'Sesión iniciada con éxito!')
                self.stack.setCurrentWidget(self.debt_query_window)
            else:
                QMessageBox.warning(self, 'Error', 'Teléfono o contraseña incorrectos')
        else:
            QMessageBox.warning(self, 'Error', 'Todos los campos son obligatorios y debe aceptar los términos')

    def register(self):
        nombre = self.auth_window.first_name.text()
        apellido = self.auth_window.last_name.text()
        telefono = self.auth_window.register_phone.text()
        correo = self.auth_window.email.text()
        contrasena = self.auth_window.register_password.text()

        if nombre and apellido and telefono and correo and contrasena:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
                QMessageBox.warning(self, 'Error', 'Formato de correo incorrecto')
                return
            if len(contrasena) < 6:
                QMessageBox.warning(self, 'Error', 'La contraseña debe tener al menos 6 caracteres')
                return
            try:
                self.db.register_user(nombre, apellido, telefono, correo, contrasena)
                QMessageBox.information(self, 'Registro', 'Usuario registrado con éxito!')
                self.auth_window.tab_widget.setCurrentIndex(0)
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, 'Error', 'El teléfono ya está registrado')
        else:
            QMessageBox.warning(self, 'Error', 'Todos los campos son obligatorios')

    def query_debt(self):
        cuenta = self.debt_query_window.account_number.text()
        if cuenta:
            resultado = self.db.query_debt(cuenta)
            if resultado:
                adeudo = resultado[0]
                QMessageBox.information(self, 'Adeudo', f'Su adeudo es de ${adeudo:.2f}')
                self.stack.setCurrentWidget(self.payment_window)
            else:
                QMessageBox.warning(self, 'Error', 'Cuenta no encontrada')
        else:
            QMessageBox.warning(self, 'Error', 'Debe ingresar una cuenta')

    def logout(self):
        self.stack.setCurrentWidget(self.auth_window)

    def process_payment(self):
        self.payment_window.status_label.setText("Procesando pago...")
        QMessageBox.information(self, 'Pago', 'Pago procesado con éxito!')
        self.payment_window.status_label.setText("")

    def add_debt(self):
        cuenta = self.add_debt_window.account_number.text()
        adeudo = self.add_debt_window.debt_amount.text()

        try:
            adeudo = float(adeudo)
            self.db.add_debt(cuenta, adeudo)
            QMessageBox.information(self, 'Añadir Adeudo', 'Adeudo añadido con éxito!')
        except ValueError:
            QMessageBox.warning(self, 'Error', 'El monto del adeudo debe ser un número válido')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PredialApp()
    ex.show()
    sys.exit(app.exec_())
