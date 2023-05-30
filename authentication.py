import hashlib
import sqlite3
import pyotp
import qrcode

def auth(c):
    c.send("Username ".encode())
    username = c.recv(1024).decode()
    c.send("Password ".encode())
    password = c.recv(1024)

    if username.strip().lower() == "register":
        register(c)
        return

    password = hashlib.sha256(password).hexdigest()
    # Authenticate the user using the provided username and password
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))
    result = cur.fetchone()

    if result:
        c.send("Username and password correct! Now you need to verify your MFA code. Look on your phone, please.".encode())
        totp = result[2]  # MFA key stored in the third column of the table
        if not totp:
            key = pyotp.random_base32()
            totp = pyotp.TOTP(key)
            cur.execute("UPDATE userdata SET totp = ? WHERE username = ?", (key, username))
            conn.commit()

        c.send("Enter MFA Code: ".encode())
        mfa_code = c.recv(1024).decode().strip()
        verify = totp.verify(mfa_code)

        if verify:
            c.send("MFA Code valid. Login successful!".encode())
            # Perform any additional actions for successful login
            loginsuccessful(c)
        else:
            c.send("MFA Code invalid. Please try again.".encode())
    else:
        c.send("Login failed! Please try again.".encode())

    conn.close()
    c.close()

def loginsuccessful(c):
    c.send("MFA Code valid. Login successful!".encode())
    # Perform any actions after successful login
    # ...

def register(c):
    c.send("Enter username for registration: ".encode())
    username = c.recv(1024).decode().strip()

    c.send("Enter password for registration: ".encode())
    password = c.recv(1024).strip()
    password = hashlib.sha256(password).hexdigest()

    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM userdata WHERE username = ?", (username,))
    result = cur.fetchone()

    if result:
        c.send("Username already exists. Please choose a different username.".encode())
    else:
        key = pyotp.random_base32()
        totp = pyotp.TOTP(key)
        uri = totp.provisioning_uri(name=username, issuer_name="Online Banking")
        uri += "&period=30"
        qrcode.make(uri).save("totp.png")
        cur.execute("INSERT INTO userdata (username, password, totp) VALUES (?, ?, ?)", (username, password, key))
        conn.commit()
        c.send("Registration successful. You can now log in with your new account.".encode())

    conn.close()
