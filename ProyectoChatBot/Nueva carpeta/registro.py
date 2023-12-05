import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import hashlib
from tkinter import messagebox

def register_student(cod, nom, ape, con):
    try:
        # Hash de la contraseña utilizando SHA-256
        hashed_password = hashlib.sha256(con.encode()).hexdigest()

        connection = mysql.connector.connect(
            host='localhost',
            database='bd_certus',
            user='root',
            password='archipielagoM1',
            port=3306
        )

        cursor = connection.cursor()

        # Verificar si el estudiante ya existe
        select_query = "SELECT 1 FROM t_estudiantes WHERE cod_estudiante = %s"
        cursor.execute(select_query, (cod,))
        student_exists = cursor.fetchone() is not None

        if student_exists:
            messagebox.showerror("Error", "El estudiante ya existe.")
        else:
            # Insertar el estudiante en la base de datos con la contraseña hasheada
            insert_query = "INSERT INTO t_estudiantes (cod_estudiante, nom_estudiante, ape_estudiante, con_estudiante) VALUES (%s, %s, %s, %s)"
            data = (cod, nom, ape, hashed_password)
            cursor.execute(insert_query, data)
            connection.commit()
            messagebox.showinfo("Registro exitoso", "Estudiante registrado con éxito.")
        
    except Error as e:
        messagebox.showerror("Error", f"Error al registrar estudiante: {e}")
    
    finally:
        if connection.is_connected():
            connection.close()

 

