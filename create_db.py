import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('usuarios.db')
c = conn.cursor()

# Crear tablas
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    apellido TEXT,
    telefono TEXT UNIQUE,
    correo TEXT,
    contrasena TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS adeudos (
    cuenta TEXT PRIMARY KEY,
    adeudo REAL
)''')

# Insertar datos iniciales
c.execute('''INSERT OR IGNORE INTO adeudos (cuenta, adeudo) VALUES ('UA009999001', 1500.50)''')

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("Base de datos creada con éxito.")
