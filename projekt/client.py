# messaging
# chat rooms
# encryption/decryption
# register

import socket, server, protocol
import tkinter as tk
import json
from cryptography.hazmat.backends import default_backend  
from cryptography.hazmat.primitives import serialization  
from cryptography.hazmat.primitives.asymmetric import rsa 

def generate_key_pair() -> (bytes, bytes, bytes, bytes):
    priv = rsa.generate_private_key(public_exponent=65537, key_size=4096, backend=default_backend())
    priv_pem = priv.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
    )
    pub = priv.public_key()
    pub_pem = pub.public_bytes(  
        encoding=serialization.Encoding.PEM,  
        format=serialization.PublicFormat.SubjectPublicKeyInfo  
    )  
    return (pub, pub_pem, priv, priv_pem)


class Client:
    def __init__(self):
        self.identifier = None 

    def send_request(self, request):
        connection = socket.create_connection(server.ADDRESS)
        return protocol.send_request(connection, request, self.keys[0])
    
    def clear_window(self) -> None:
        for child in self.root.winfo_children():
            child.destroy()    

    def new_msg(self, msg):
            return tk.Label(self.message_window, text=f"{msg['user']}: {msg['content']}")

    def join_channel(self, channel):
        answer = self.send_request(protocol.JoinRequest(self.identifier, channel))
        data = answer[1]
        print(data)
        data = json.loads(data)
        for child in self.message_window.winfo_children():
            child.destroy()
        for message in data:
            self.new_msg(message).pack(anchor="nw")

    def run_logged_in(self, username: str) -> None:
        self.clear_window()
        self.message_window = tk.Frame(self.root, height=640)
        message_input = tk.Entry(self.root)
        self.message_window.grid(column=2, row=3, padx=5, pady=5)
        message = tk.Label(self.message_window, text="xx")
        message.pack()
        message2 = tk.Label(self.message_window, text="xx")
        message2.pack()
        message_input.grid(column=2, row=2, padx=5, pady=5)

        self.join_channel("/")

        connect_input = tk.Entry(self.root, text="/")
        connect_input.grid(column=0, row=0, padx=10, pady=10)
        tk.Button(self.root, text="Connect", command=lambda: self.join_channel(connect_input.get())).grid(column=0, row=1, padx=10, pady=5)
        

        def send_message():
            print(message_input.get())
            msg = message_input.get()
            answer = self.send_request(protocol.MessageRequest(self.identifier, msg))
            data = json.loads(answer[1])
            print(self.message_window.pack_slaves)
            for msg in data:
                label = self.new_msg(msg)
                label.pack(anchor="w", before=self.message_window.pack_slaves()[0])
            message_input.delete(0, tk.END)

        tk.Button(self.root, text="Send", command=send_message).grid(column=3, row=2, padx=5, pady=5)

    def login(self):
        self.keys = generate_key_pair()

        tk.Label(self.root, text="username:").grid(column=0, row=0, padx=20, pady=20)
        name = tk.Entry(self.root)
        name.grid(column=1, row=0, padx=5, pady=20)

        tk.Label(self.root, text="password:").grid(column=0, row=1, padx=20, pady=5)
        password = tk.Entry(self.root, show="*")
        password.grid(column=1, row=1, padx=5, pady=20)

        status_label = None

        def attempt_login():
            if self.attempt_login(name.get(), password.get()): 
                self.run_logged_in(name.get())
            else:
                status_label.config(text="Invalid username or password")

        def attempt_register():
            if self.attempt_register(name.get(), password.get()): 
                status_label.config(text="Registered!")
            else:
                status_label.config(text="Register failed")

        button = tk.Button(self.root, text="login", command=attempt_login)
        button.grid(padx=20, pady=0, column=0, row=3)
        button = tk.Button(self.root, text="register", command=attempt_register)
        button.grid(padx=20, pady=0, column=1, row=3)

        status_label = tk.Label(self.root)
        status_label.grid(column=0, row=2, padx=20, pady=0)


    def attempt_login(self, name, password) -> bool:
        print(f"Name: {name}")
        answer = self.send_request(protocol.LoginRequest(name, password, self.keys[1]))
        print(answer)
        self.identifier = answer[1]
        return answer[0]

    def attempt_register(self, name, password) -> bool:
        print(f"Name: {name}")
        answer = self.send_request(protocol.RegisterRequest(name, password))
        return answer[0]

    def run(self): 
        self.root = tk.Tk()
        self.login()
        self.root.mainloop()
