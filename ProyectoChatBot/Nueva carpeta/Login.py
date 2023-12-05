import tkinter as tk
import getpass
from tkinter import PhotoImage, messagebox
from tkinter import font
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import hashlib
from registro import register_student
from bot import start_chatbot

def hash_password(password):
    # Función para generar el hash SHA-256 de la contraseña
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    user = user_entry.get()
    password = password_entry.get()

    if user == "" or password == "":
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
    else:
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='bd_certus',
                user='root',
                password='archipielagoM1',
                port=3306
            )

            # Obtener el hash almacenado en la base de datos para el usuario
            sql_select_password = f"SELECT con_estudiante FROM t_estudiantes WHERE cod_estudiante='{user}'"
            cursor = connection.cursor()
            cursor.execute(sql_select_password)
            stored_hash = cursor.fetchone()

            if stored_hash:
                stored_hash = stored_hash[0]

                # Comparar el hash de la contraseña ingresada con el hash almacenado
                if stored_hash == hash_password(password):
                    # Inicio de sesión exitoso, obtener el user_id del usuario
                    sql_select_user_id = f"SELECT cod_estudiante FROM t_estudiantes WHERE cod_estudiante='{user}'"
                    cursor.execute(sql_select_user_id)
                    user_id = cursor.fetchone()[0]

                    # Llama a la función start_chatbot con el user_id
                    start_chatbot(root, user_id)

                    # Oculta la ventana de inicio de sesión
                    root.withdraw()

                    # Muestra un mensaje de éxito adicional o realiza otras acciones necesarias
                else:
                    messagebox.showerror("Error", "Error en las credenciales")
            else:
                messagebox.showerror("Error", "Usuario no encontrado")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", "Error en la consulta: " + str(e))
        finally:
            if connection.is_connected():
                connection.close()


def validate_code_input(P):
    return P.isdigit() and len(P) <= 8

def is_valid_char(char):
    return char.isdigit()

def validate_user_input(P):
    if P == "" or (P and P[0] == "-" and P[1:].isdigit()):
        return True
    return all(is_valid_char(c) for c in P)

def open_registration_window():
    registration_window = tk.Toplevel(root, bg="#ffffff", padx=30, pady=30)
    registration_window.title("Registrar Estudiante")
    registration_window.geometry("400x400")

    registration_window.configure(bg='#232f59')
    center_window(registration_window, 400, 400)

    def validate_code(entry_value):
        # Verificar si la entrada es un número y tiene como máximo 8 dígitos
        return entry_value.isdigit() and len(entry_value) <= 8

    vcmd = (registration_window.register(validate_code), '%P')

    cod_label = tk.Label(registration_window, text="Código:", font=large_font, bg="#232f59", fg="#ffffff")
    cod_label.pack(pady=5)
    cod_entry = tk.Entry(registration_window, font=large_font, fg="#232f59", validate="key", validatecommand=vcmd)
    cod_entry.pack(pady=3)

    nom_label = tk.Label(registration_window, text="Nombre:", font=large_font, bg="#232f59", fg="#ffffff")
    nom_label.pack(pady=5)
    nom_entry = tk.Entry(registration_window, font=large_font, fg="#232f59")
    nom_entry.pack(pady=3)

    ape_label = tk.Label(registration_window, text="Apellidos:", font=large_font, bg="#232f59", fg="#ffffff")
    ape_label.pack(pady=5)
    ape_entry = tk.Entry(registration_window, font=large_font, fg="#232f59")
    ape_entry.pack(pady=3)

    con_label = tk.Label(registration_window, text="Contraseña:", font=large_font, bg="#232f59", fg="#ffffff")
    con_label.pack(pady=5)
    con_entry = tk.Entry(registration_window, font=large_font, fg="#232f59", show="*")
    con_entry.pack(pady=3)

    def register_student1():
        cod = cod_entry.get()
        nom = nom_entry.get()
        ape = ape_entry.get()
        con = con_entry.get()

        # Check if any field is empty
        if not cod or not nom or not ape or not con:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
        else:
            register_student(cod, nom, ape, con)

    register_button = tk.Button(registration_window, text="Registrar", font=large_font, command=register_student1,
                                fg="#232f59", bg="#ffffff")
    register_button.pack(pady=10)


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def toggle_password_visibility():
    if show_password.get() == 1:
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

root = tk.Tk()
root.title("Inicio de sesión")
root.configure(bg="#232f59")
window_width = 650
window_height = 500
center_window(root, window_width, window_height)

image = Image.open("Nueva carpeta\logo-white-certus-peru.png")
image = image.resize((400, 130))

img = ImageTk.PhotoImage(image)
lbl_img = tk.Label(root, image=img, bd=0)
lbl_img.pack(pady=12)

login_frame = tk.Frame(root, bg="#ffffff", padx=30, pady=30)
login_frame.pack(expand=True)

large_font = font.Font(size=14)

user_label = tk.Label(login_frame, text="Usuario:", font=large_font, bg="#ffffff", fg="#232f59")
user_label.pack(pady=5)

user_entry = tk.Entry(login_frame, font=large_font, validate="key", fg="#ffffff", bg="#232f59")
user_entry['validatecommand'] = (user_entry.register(validate_code_input), '%P')
user_entry.pack(pady=5)

password_label = tk.Label(login_frame, text="Contraseña:", font=large_font, bg="#ffffff", fg="#232f59")
password_label.pack(pady=5)

password_entry = tk.Entry(login_frame, show="*", font=large_font, fg="#ffffff", bg="#232f59")
password_entry.pack(pady=5)

show_password = tk.IntVar()
show_password_checkbox = tk.Checkbutton(login_frame, text="Mostrar contraseña", variable=show_password, command=toggle_password_visibility, font=large_font, bg="#ffffff", fg="#232f59")
show_password_checkbox.pack(pady=5)

login_button = tk.Button(login_frame, text="Iniciar sesión", command=login, font=large_font, fg="#ffffff", bg="#232f59")
login_button.pack(pady=10)

register_label = tk.Label(login_frame, text="Registrar estudiante", cursor="hand2", font=large_font, bg="#ffffff", fg="#232f59")
register_label.pack()

def on_register_click(event):
    open_registration_window()

register_label.bind("<Button-1>", on_register_click)

root.mainloop()
