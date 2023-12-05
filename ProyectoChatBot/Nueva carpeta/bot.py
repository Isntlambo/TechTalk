import tkinter as tk
import pymysql
from datetime import datetime
import tkinter as tk
from datetime import datetime
import pymysql

def start_chatbot(root, user_id):
    def load_chat_history():
        try:
            cursor = db.cursor()
            select_data_query = f"SELECT message, timestamp, is_user_message FROM chat_messages WHERE user_id = {user_id} ORDER BY timestamp"
            cursor.execute(select_data_query)
            rows = cursor.fetchall()

            chat_text.config(state='normal')

            for row in rows:
                message, timestamp, is_user_message = row
                formatted_time = timestamp.strftime("%I:%M %p")
                sender = "User" if is_user_message else "Chatbot"
                chat_input = f'{sender}: {message}\n{formatted_time}\n'
                chat_text.insert("end", chat_input, (sender.lower(), "message"))

            chat_text.config(state='disabled')
            chat_text.insert("end", "\n")
            chat_text.see("end")

        except Exception as e:
            print("Error loading chat history:", e)

    def send_message(event=None):
        user_message = user_entry.get()
        user_input = f'User: {user_message}\n{get_current_time()}\n'
        chat_text.config(state='normal')
        chat_text.insert("end", user_input, ("user", "message"))

        cursor = db.cursor()
        insert_query_user = f"INSERT INTO chat_messages (user_id, message, timestamp, is_user_message) VALUES ({user_id}, '{user_message}', NOW(), TRUE)"
        cursor.execute(insert_query_user)
        db.commit()

        chatbot_response = get_chatbot_response(user_message)
        insert_query_chatbot = f"INSERT INTO chat_messages (user_id, message, timestamp, is_user_message) VALUES ({user_id}, '{chatbot_response}', NOW(), FALSE)"
        cursor.execute(insert_query_chatbot)
        db.commit()

        chatbot_input = f'Chatbot: {chatbot_response}\n{get_current_time()}\n'
        chat_text.insert("end", chatbot_input, ("chatbot", "message"))

        chat_text.see("end")
        user_entry.delete(0, 'end')
        chat_text.see("end")

    def get_current_time():
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        return current_time

    def get_chatbot_response(user_message):
        try:
            cursor = db.cursor()
            select_query = "SELECT response, keywords FROM chatbot_responses"
            cursor.execute(select_query)
            responses = cursor.fetchall()

            user_message = user_message.lower()

            for response, keywords in responses:
                keyword_list = keywords.split(',')
                for keyword in keyword_list:
                    if keyword.strip().lower() in user_message:
                        return response

            return "Lo siento, no entiendo ese mensaje."

        except Exception as e:
            print("Error getting chatbot response:", e)
            return "Ocurrió un error al procesar tu mensaje."
        

        
    def logout():
        chatbot_window.destroy()
        root.deiconify()


    db = pymysql.connect(host="localhost", user="root", password="archipielagoM1", db="bd_certus", port=3306)

    chatbot_window = tk.Toplevel(root)
    chatbot_window.title('ChatBot')

    window_width = 850
    window_height = 600
    screen_width = chatbot_window.winfo_screenwidth()
    screen_height = chatbot_window.winfo_screenheight()
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)
    chatbot_window.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')

    chatbot_window.configure(bg='#232f59')

    title_frame = tk.Frame(chatbot_window, bg='#1e2b42', relief=tk.FLAT, bd=2)
    title_frame.pack(expand=1, fill="x")

    hcb_text = tk.Label(title_frame, height=2, width=14, bg='#952d98', text='TechTalk', font=('Impact', 20), fg='white')
    hcb_text.pack(side="left", padx=(5, 0))

    logout_button = tk.Button(title_frame, text="Cerrar Sesión", font=('Helvetica', 12),
                              command=logout, fg='white', bg='#f44336')
    logout_button.pack(side="right", padx=(0, 5))

    chat_text = tk.Text(chatbot_window, height=20, width=63, font=('Helvetica', 14), wrap="word")
    chat_text.tag_configure("user", justify="right", foreground="white", background="#005c4b")
    chat_text.tag_configure("chatbot", justify="left", foreground="white", background="#1e2b42")
    chat_text.tag_configure("message", lmargin1=10, lmargin2=10, rmargin=10)
    chat_text.pack(fill=tk.BOTH, expand=True)
    chat_text.config(state='disabled')

    user_entry = tk.Entry(chatbot_window, width=50, bg='white', font=('Helvetica', 20), relief=tk.FLAT, border=0)
    user_entry.pack(pady=(10, 10), side="left", fill=tk.BOTH, expand=True)
    user_entry.config(fg='#5c5a5a')

    user_entry.bind("<Return>", send_message)  # Evento "Enter"

    send_button = tk.Button(chatbot_window, height=1, width=3, bg='#0084ff', text='➤', font=('Helvetica', 20),
                            activeforeground='white', fg='white', relief=tk.FLAT, border=0,
                            activebackground='#0084ff', command=send_message)
    send_button.pack(pady=(10, 10), padx=(10, 0), side="right")

    chatbot_window.after(100, load_chat_history)

    root.withdraw()

    chatbot_window.mainloop()

 