import os
import sqlite3
from datetime import datetime

# Nombre del archivo de la base de datos
DB_FILE = "gestion_clientes.db"

# Conectar o crear la base de datos SQLite
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Crear la tabla clientes
cursor.execute('''
CREATE TABLE clientes (
    DNI CHAR(9) NOT NULL PRIMARY KEY, -- 8 números y 1 letra
    Nombre CHAR(15) NOT NULL,         -- Nombre limitado a 15 caracteres
    Apellidos CHAR(50) NOT NULL,      -- Apellidos limitado a 50 caracteres
    Edad INTEGER NOT NULL,            -- Edad como entero
    Debe DECIMAL(9, 2) NOT NULL,      -- Monto debe con 7 enteros y 2 decimales
    Pagado DECIMAL(9, 2) NOT NULL,    -- Monto pagado con 7 enteros y 2 decimales
    TimestampActualizacion DATETIME NOT NULL -- Fecha y hora de la última actualización
)
''')
print("Tabla 'clientes' creada exitosamente.")

# Cerrar la conexión
conn.close()