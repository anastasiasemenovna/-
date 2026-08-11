import tkinter as tk
from tkinter import ttk

def atbash(text):
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr(base + (25 - (ord(char) - base))))
        else:
            result.append(char)
    return ''.join(result)

def caesar(text, shift, mode='encrypt'):
    shift = shift % 26
    if mode == 'decrypt':
        shift = -shift
    
    result = []
    for char in text:
        if 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        elif 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(char)
    
    return ''.join(result)

def pigpen(text, mode):
    dictionary = {
        'a': '⌐', 'b': '¬', 'c': '⌡',
        'd': '┌', 'e': '┬', 'f': '┐',
        'g': '├', 'h': '┼', 'i': '┤',
        'j': '└', 'k': '┴', 'l': '┘',
        'm': '▌', 'n': '▐', 'o': '▀',
        'p': '▄', 'q': '■', 'r': '□',
        's': '▪', 't': '▫', 'u': '▬',
        'v': '▭', 'w': '▮', 'x': '▯',
        'y': '◘', 'z': '◙'
    }
    reverse_dict = {v: k for k, v in dictionary.items()}
    
    result = []
    if mode == "decrypt":
        for char in text:
            result.append(reverse_dict.get(char, char))
    else:
        for char in text.lower():
            result.append(dictionary.get(char, char))
    
    return ''.join(result)

def vigenere(text, key, mode='encrypt'):
    key_index = 0
    t = []
    for char in text:
        if char.isalpha():
            t.append(key[key_index % len(key)])
            key_index += 1
        else:
            t.append(char)
    t = ''.join(t)
    
    result = []
    sign = 1 if mode == 'encrypt' else -1  # + для шифровки, - для дешифровки
    
    for i, char in enumerate(text):
        if 'A' <= char <= 'Z':
            shift = (ord(char) - ord('A') + sign * (ord(t[i].upper()) - ord('A'))) % 26
            result.append(chr(shift + ord('A')))
        elif 'a' <= char <= 'z':
            shift = (ord(char) - ord('a') + sign * (ord(t[i].lower()) - ord('a'))) % 26
            result.append(chr(shift + ord('a')))
        else:
            result.append(char)
    
    return ''.join(result)

def KSA(S, key_bytes):
    j = 0
    for i in range(0, 256):
        j = (j + S[i] + key_bytes[i % len(key_bytes)]) % 256
        g = S[i]
        S[i] = S[j]
        S[j] = g
    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        g = S[i]
        S[i] = S[j]
        S[j] = g
        t = (S[i] + S[j]) % 256
        yield S[t]

def rc4(data, key):
    S = list(range(256))
    key_bytes = key.encode('utf-8')
    S = KSA(S, key_bytes)
    gen = PRGA(S)
    
    result = []
    for byte in data:
        result.append(byte ^ next(gen))
    
    return bytes(result)

def on_encrypt():
    text = input_text.get("1.0", tk.END).strip()
    cipher = cipher_var.get()
    key = key_entry.get()
    
    if cipher == "Цезарь":
        shift = int(key)
        result = caesar(text, shift)
    elif cipher == "Атбаш":
        result = atbash(text)
    elif cipher == "Пигпен":
        result = pigpen(text, 'encrypt')
    elif cipher == "Виженер":
        result = vigenere(text, key)
    elif cipher == "RC4":
        encrypted_bytes = rc4(text.encode('utf-8'), key)
        result = encrypted_bytes.hex()
    else:
        result = "Неизвестный шифр"
    
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", result)

def on_decrypt():
    text = input_text.get("1.0", tk.END).strip()
    cipher = cipher_var.get()
    key = key_entry.get()

    if cipher == "Цезарь":
        shift = int(key)
        result = caesar(text, shift, 'decrypt')
    elif cipher == "Атбаш":
        result = atbash(text)
    elif cipher == "Пигпен":
        result = pigpen(text, 'decrypt')
    elif cipher == "Виженер":
        result = vigenere(text, key, "decrypt")
    elif cipher == "RC4":
        encrypted_bytes = bytes.fromhex(text)
        decrypted_bytes = rc4(encrypted_bytes, key)
        result = decrypted_bytes.decode('utf-8')
    else:
        result = "Неизвестный шифр"

    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", result)

# --- Окно ---
root = tk.Tk()
root.title("Шифровальщик для масона")
root.geometry("500x500")
root.configure(bg='#2c2c2c')

# --- Поле ввода ---
tk.Label(root, text="Введите текст:", bg='#2c2c2c', fg='white').pack()
input_text = tk.Text(root, height=5, width=50)
input_text.pack()

# --- Выбор шифра ---
tk.Label(root, text="Выберите шифр:", bg='#2c2c2c', fg='white').pack()
cipher_var = tk.StringVar(value="Цезарь")
cipher_menu = ttk.Combobox(root, textvariable=cipher_var, 
                           values=["Цезарь", "Атбаш", "Пигпен", "Виженер", "RC4"])
cipher_menu.pack()

# --- Поле для ключа ---
tk.Label(root, text="Ключ (если нужен):", bg='#2c2c2c', fg='white').pack()
key_entry = tk.Entry(root)
key_entry.pack()

# --- Кнопки ---
btn_frame = tk.Frame(root, bg='#2c2c2c')
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="✠ Зашифровать", command=on_encrypt).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="🗝 Расшифровать", command=on_decrypt).pack(side=tk.LEFT, padx=5)

# --- Поле результата ---
tk.Label(root, text="Результат:", bg='#2c2c2c', fg='white').pack()
output_text = tk.Text(root, height=5, width=50)
output_text.pack()

root.mainloop()