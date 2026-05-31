import socket, threading, protocol
import secrets
import sqlite3
import json
import hashlib, uuid

ADDRESS = ("127.0.0.1", 5555)
OK =  b"\1\2\1"
BAD = b"\2\1\2"

clients = {}

def db_handle():
    return sqlite3.connect("db.sqlite3")

def new_client_identifier() -> bytes:
    while True:
        secret = secrets.token_bytes(32)
        if secret in clients: continue
        return secret

def answer(connection, data, token):
    if token not in clients:
        connection.send(BAD)
        return
    connection.send(data)

def validate_token(token):
    if token not in clients: return False
    return clients[token]

def hash_password(password, salt) -> bytes:
    return hashlib.sha512((password + salt).encode("utf-8")).hexdigest()

def serialize_channel_messages(client, gte = 0):
    channel = client[2]
    db = db_handle()
    print(f"CHANNEL {channel}")
    msgs = db.execute("SELECT id, person, message FROM messages WHERE channel = ? AND id > ? ORDER BY id DESC", (channel, gte)).fetchall()
    print(msgs)
    db.close()
    data = []

    if len(msgs) > 0:
        client[3] = msgs[0][0]
        
    for msg in msgs:
        data.append({"id": msg[0], "user": msg[1], "content": msg[2]})
    return bytes(json.dumps(data), "utf_8")

def update_client(client):
    return serialize_channel_messages(client, client[3])

def server():
    s_socket = socket.create_server(ADDRESS)

    while True:
        connection, _ = s_socket.accept()
        data = connection.recv(10240)
        request_kind = protocol.get_request_id(data)
        match request_kind:
            case protocol.LoginRequest.ID:
                (name, password, key) = protocol.LoginRequest.unpack(data)

                db = db_handle()
                user = db.cursor().execute("SELECT password_hash, salt FROM accounts WHERE login = ?", (name,));
                user = user.fetchall()
                print(user)
                db.close()
                if len(user) == 0:
                    connection.send(BAD)
                    continue
                (hash, salt) = user[0]
                hashed_password = hash_password(password, salt)
                if hash == hashed_password:
                    identifier = new_client_identifier()
                    clients[identifier] = [ name, key, "/", 0 ]
                    connection.send(OK + identifier)
                else:
                    connection.send(BAD)
            case protocol.RegisterRequest.ID:
                (name, password) = protocol.RegisterRequest.unpack(data)
                db = db_handle()
                users = db.cursor().execute("SELECT login FROM accounts")
                users = users.fetchall()

                do_insert = True
                for user in users:
                    if user[0] == name:
                        connection.send(BAD)
                        do_insert = False
                        break
                if not do_insert: continue
                
                salt = uuid.uuid4().hex
                hashed_password = hash_password(password, salt)
                print(salt, hashed_password)
                db.cursor().execute("INSERT INTO accounts VALUES (?, ?, ?)", (name, hashed_password, salt))
                db.commit()
                db.close()
                print(users)
                connection.send(BAD)
            case protocol.MessageRequest.ID:
                (message, token) = protocol.MessageRequest.unpack(data)
                client = validate_token(token)
                if not client: continue
                db = db_handle()
                db.cursor().execute("INSERT INTO messages (person, message, channel) VALUES (?, ?, ?)", (client[0], message, client[2]))
                db.commit()
                db.close()
                # print(message, token)
                connection.send(OK + update_client(client))
            case protocol.JoinRequest.ID:
                (channel, token) = protocol.JoinRequest.unpack(data)
                client = validate_token(token)
                if not client: continue
                client[2] = channel
                # print(f"Channel: {channel}!", token)

                connection.send(OK + serialize_channel_messages(client))
            case _:
                connection.send(BAD)
        # connection.shutdown(socket.SHUT_RD)
            
def main():
    con = db_handle()
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, person, message, channel)");
    cur.execute("CREATE TABLE IF NOT EXISTS accounts (login PRIMARY KEY, password_hash, salt)");
    con.close()
    print("Server")
    threading.Thread(target=server).start()
