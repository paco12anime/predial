import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QCheckBox)
from PyQt5.QtGui import QIntValidator
import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('usuarios.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nombre TEXT, apellido TEXT, telefono TEXT UNIQUE, correo TEXT, contrasena TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS adeudos (cuenta TEXT PRIMARY KEY, adeudo REAL)''')
c.execute('''INSERT OR IGNORE INTO adeudos (cuenta, adeudo) VALUES ('UA009999001', 1500.50)''')
conn.commit()

class PredialApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Sistema de Predial')
        self.setGeometry(100, 100, 400, 300)
        
        # Layout principal
        self.main_layout = QVBoxLayout()
        
        # Mostrar ventana de registro al inicio
        self.show_registration()
        
        self.setLayout(self.main_layout)
    
    def show_registration(self):
        # Limpiar el layout principal
        self.clear_layout(self.main_layout)
        
        # Layout de registro
        registration_layout = QVBoxLayout()
        
        # Campos de registro
        self.first_name = QLineEdit(self)
        self.first_name.setPlaceholderText('Nombres')
        self.last_name = QLineEdit(self)
        self.last_name.setPlaceholderText('Apellidos')
        self.phone = QLineEdit(self)
        self.phone.setPlaceholderText('Número de teléfono')
        self.email = QLineEdit(self)
        self.email.setPlaceholderText('Correo electrónico')
        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Contraseña')
        self.password.setEchoMode(QLineEdit.Password)
        
        # Botón de registro
        register_button = QPushButton('Regístrate', self)
        register_button.clicked.connect(self.register)
        
        # Añadir campos al layout de registro
        registration_layout.addWidget(self.first_name)
        registration_layout.addWidget(self.last_name)
        registration_layout.addWidget(self.phone)
        registration_layout.addWidget(self.email)
        registration_layout.addWidget(self.password)
        registration_layout.addWidget(register_button)
        
        # Campos de inicio de sesión
        self.login_phone = QLineEdit(self)
        self.login_phone.setPlaceholderText('Teléfono')
        self.login_password = QLineEdit(self)
        self.login_password.setPlaceholderText('Contraseña')
        self.login_password.setEchoMode(QLineEdit.Password)
        self.terms_checkbox = QCheckBox('Aceptar términos', self)
        
        # Botón de inicio de sesión
        login_button = QPushButton('Entrar', self)
        login_button.clicked.connect(self.login)
        
        # Añadir campos al layout de inicio de sesión
        registration_layout.addWidget(self.login_phone)
        registration_layout.addWidget(self.login_password)
        registration_layout.addWidget(self.terms_checkbox)
        registration_layout.addWidget(login_button)
        
        self.main_layout.addLayout(registration_layout)
    
    def register(self):
        nombre = self.first_name.text()
        apellido = self.last_name.text()
        telefono = self.phone.text()
        correo = self.email.text()
        contrasena = self.password.text()
        if nombre and apellido and telefono and correo and contrasena:
            try:
                c.execute("INSERT INTO usuarios (nombre, apellido, telefono, correo, contrasena) VALUES (?, ?, ?, ?, ?)", 
                          (nombre, apellido, telefono, correo, contrasena))
                conn.commit()
                QMessageBox.information(self, 'Registro', 'Usuario registrado con éxito!')
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, 'Error', 'El teléfono ya está registrado')
        else:
            QMessageBox.warning(self, 'Error', 'Todos los campos son obligatorios')
    
    def login(self):
        telefono = self.login_phone.text()
        contrasena = self.login_password.text()
        aceptar_terminos = self.terms_checkbox.isChecked()
        
        if telefono and contrasena and aceptar_terminos:
            c.execute("SELECT * FROM usuarios WHERE telefono = ? AND contrasena = ?", (telefono, contrasena))
            usuario = c.fetchone()
            if usuario:
                QMessageBox.information(self, 'Inicio de sesión', 'Sesión iniciada con éxito!')
                self.show_debt_query()
            else:
                QMessageBox.warning(self, 'Error', 'Teléfono o contraseña incorrectos')
        else:
            QMessageBox.warning(self, 'Error', 'Todos los campos son obligatorios y debe aceptar los términos')
    
    def show_debt_query(self):
        # Limpiar el layout principal
        self.clear_layout(self.main_layout)
        
        # Layout de consulta de adeudo
        debt_layout = QVBoxLayout()
        
        # Campo de cuenta predial
        self.account_number = QLineEdit(self)
        self.account_number.setPlaceholderText('Cuenta predial (ej. UA009999001)')
        
        # Botón de consulta
        query_button = QPushButton('Consultar', self)
        query_button.clicked.connect(self.query_debt)
        
        # Añadir campos al layout de consulta
        debt_layout.addWidget(self.account_number)
        debt_layout.addWidget(query_button)
        
        self.main_layout.addLayout(debt_layout)
    
    def query_debt(self):
        cuenta = self.account_number.text()
        c.execute("SELECT adeudo FROM adeudos WHERE cuenta = ?", (cuenta,))
        resultado = c.fetchone()
        if resultado:
            QMessageBox.information(self, 'Consulta de adeudo', f'Adeudo: ${resultado[0]:.2f}')
            self.show_payment_process()
        else:
            QMessageBox.warning(self, 'Error', 'Cuenta no encontrada')
    
    def show_payment_process(self):
        # Limpiar el layout principal
        self.clear_layout(self.main_layout)
        
        # Layout de proceso de pago
        payment_layout = QVBoxLayout()
        
        # Campos de tarjeta
        self.card_number = QLineEdit(self)
        self.card_number.setPlaceholderText('Número de tarjeta')
        self.expiry_date = QLineEdit(self)
        self.expiry_date.setPlaceholderText('Fecha de expiración (MM/AA)')
        self.cvv = QLineEdit(self)
        self.cvv.setPlaceholderText('CVV')
        
        # Botón de pago
        pay_button = QPushButton('Pagar', self)
        pay_button.clicked.connect(self.process_payment)
        
        # Añadir campos al layout de pago
        payment_layout.addWidget(self.card_number)
        payment_layout.addWidget(self.expiry_date)
        payment_layout.addWidget(self.cvv)
        payment_layout.addWidget(pay_button)
        
        self.main_layout.addLayout(payment_layout)
    
    def process_payment(self):
        # Aquí iría la lógica para procesar el pago
        QMessageBox.information(self, 'Pago', 'Pago realizado con éxito!')
    
    def clear_layout(self, layout):
        # Limpiar layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PredialApp()
    ex.show()
    sys.exit(app.exec_())

# Cerrar la conexión a la base de datos
conn.close()
