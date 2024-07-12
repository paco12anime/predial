import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QCheckBox
import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('usuarios.db')
c = conn.cursor()

# Creación de la tabla de usuarios
c.execute('''CREATE TABLE IF NOT EXISTS usuarios
             (id INTEGER PRIMARY KEY, 
              nombre TEXT, 
              apellido TEXT, 
              telefono TEXT UNIQUE, 
              correo TEXT, 
              contrasena TEXT)''')

# Creación de la tabla de adeudos
c.execute('''CREATE TABLE IF NOT EXISTS adeudos
             (cuenta TEXT PRIMARY KEY, 
              adeudo REAL)''')

# Insertar un adeudo de ejemplo
c.execute('''INSERT OR IGNORE INTO adeudos (cuenta, adeudo) VALUES ('UA009999001', 1500.50)''')

conn.commit()

class SistemaPredial(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Sistema Predial')
        self.setGeometry(100, 100, 400, 300)
        
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Ventana principal
        self.label_cuenta = QLabel('Cuenta Predial:')
        self.entry_cuenta = QLineEdit()

        self.btn_consultar_adeudo = QPushButton('Consultar Adeudo')
        self.btn_consultar_adeudo.clicked.connect(self.consultar_adeudo)

        self.label_tarjeta = QLabel('Tarjeta de Crédito/Débito:')
        self.entry_tarjeta = QLineEdit()

        self.label_cvv = QLabel('CVV:')
        self.entry_cvv = QLineEdit()

        self.label_fecha_expiracion = QLabel('Fecha de Expiración (MM/AA):')
        self.entry_fecha_expiracion = QLineEdit()

        self.btn_iniciar_pago = QPushButton('Iniciar Pago')
        self.btn_iniciar_pago.clicked.connect(self.iniciar_pago)

        self.layout.addWidget(self.label_cuenta)
        self.layout.addWidget(self.entry_cuenta)
        self.layout.addWidget(self.btn_consultar_adeudo)
        self.layout.addWidget(self.label_tarjeta)
        self.layout.addWidget(self.entry_tarjeta)
        self.layout.addWidget(self.label_cvv)
        self.layout.addWidget(self.entry_cvv)
        self.layout.addWidget(self.label_fecha_expiracion)
        self.layout.addWidget(self.entry_fecha_expiracion)
        self.layout.addWidget(self.btn_iniciar_pago)

        self.setLayout(self.layout)

    def consultar_adeudo(self):
        cuenta = self.entry_cuenta.text()
        c.execute("SELECT adeudo FROM adeudos WHERE cuenta = ?", (cuenta,))
        resultado = c.fetchone()
        if resultado:
            QMessageBox.information(self, "Consulta de Adeudo", f"El adeudo de la cuenta {cuenta} es: ${resultado[0]:.2f}")
        else:
            QMessageBox.warning(self, "Error", "Cuenta no encontrada")

    def iniciar_pago(self):
        tarjeta = self.entry_tarjeta.text()
        cvv = self.entry_cvv.text()
        fecha_expiracion = self.entry_fecha_expiracion.text()
        if tarjeta and cvv and fecha_expiracion:
            QMessageBox.information(self, "Pago", "Pago realizado exitosamente")
        else:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")

class Login(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Iniciar Sesión')
        self.setGeometry(100, 60, 1000, 800) 
        
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.label_telefono = QLabel('Teléfono:')
        self.entry_login_telefono = QLineEdit()

        self.label_contrasena = QLabel('Contraseña:')
        self.entry_login_contrasena = QLineEdit()
        self.entry_login_contrasena.setEchoMode(QLineEdit.Password)

        self.var_aceptar = QCheckBox('Aceptar términos y condiciones')

        self.btn_entrar = QPushButton('Entrar')
        self.btn_entrar.clicked.connect(self.iniciar_sesion)

        self.layout.addWidget(self.label_telefono)
        self.layout.addWidget(self.entry_login_telefono)
        self.layout.addWidget(self.label_contrasena)
        self.layout.addWidget(self.entry_login_contrasena)
        self.layout.addWidget(self.var_aceptar)
        self.layout.addWidget(self.btn_entrar)

        self.setLayout(self.layout)

    def iniciar_sesion(self):
        telefono = self.entry_login_telefono.text()
        contrasena = self.entry_login_contrasena.text()
        aceptar_terminos = self.var_aceptar.isChecked()

        if telefono and contrasena and aceptar_terminos:
            c.execute("SELECT * FROM usuarios WHERE telefono = ? AND contrasena = ?", (telefono, contrasena))
            usuario = c.fetchone()
            if usuario:
                QMessageBox.information(self, "Inicio de sesión", "Inicio de sesión exitoso")
                self.hide()
                self.main_window = SistemaPredial()
                self.main_window.show()
            else:
                QMessageBox.warning(self, "Error", "Teléfono o contraseña incorrectos")
        else:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios y debe aceptar los términos")

class Registro(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Registrar')
        self.setGeometry(100, 60, 1000, 800) 
        
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.label_nombre = QLabel('Nombres:')
        self.entry_nombre = QLineEdit()

        self.label_apellido = QLabel('Apellidos:')
        self.entry_apellido = QLineEdit()

        self.label_telefono = QLabel('Teléfono:')
        self.entry_telefono = QLineEdit()

        self.label_correo = QLabel('Correo Electrónico:')
        self.entry_correo = QLineEdit()

        self.label_contrasena = QLabel('Contraseña:')
        self.entry_contrasena = QLineEdit()
        self.entry_contrasena.setEchoMode(QLineEdit.Password)

        self.btn_registrar = QPushButton('Registrar')
        self.btn_registrar.clicked.connect(self.registrar)

        self.layout.addWidget(self.label_nombre)
        self.layout.addWidget(self.entry_nombre)
        self.layout.addWidget(self.label_apellido)
        self.layout.addWidget(self.entry_apellido)
        self.layout.addWidget(self.label_telefono)
        self.layout.addWidget(self.entry_telefono)
        self.layout.addWidget(self.label_correo)
        self.layout.addWidget(self.entry_correo)
        self.layout.addWidget(self.label_contrasena)
        self.layout.addWidget(self.entry_contrasena)
        self.layout.addWidget(self.btn_registrar)

        self.setLayout(self.layout)

    def registrar(self):
        nombre = self.entry_nombre.text()
        apellido = self.entry_apellido.text()
        telefono = self.entry_telefono.text()
        correo = self.entry_correo.text()
        contrasena = self.entry_contrasena.text()

        if nombre and apellido and telefono and correo and contrasena:
            try:
                c.execute("INSERT INTO usuarios (nombre, apellido, telefono, correo, contrasena) VALUES (?, ?, ?, ?, ?)",
                          (nombre, apellido, telefono, correo, contrasena))
                conn.commit()
                QMessageBox.information(self, "Registro", "Usuario registrado exitosamente")
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Error", "El teléfono ya está registrado")
        else:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    login = Login()
    registro = Registro()

    login.show()
    registro.show()

    sys.exit(app.exec_())

# Cerrar la conexión a la base de datos
conn.close()
