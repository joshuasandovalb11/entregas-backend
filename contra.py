import bcrypt

# Lista de contraseñas que quieres hashear
passwords = [
    'Carlos2025',
    'Maria2025',
    'Jose2025',
    'Ana2025',
    'Pedro2025'
]

print("--- Hashes Bcrypt Generados ---")

# Genera un hash para cada contraseña de la lista
for pwd in passwords:
    # Codifica la contraseña a bytes
    password_bytes = pwd.encode('utf-8')
    
    # Genera el salt y el hash
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    
    # Decodifica el hash a string para poder copiarlo
    hashed_string = hashed_bytes.decode('utf-8')
    
    print(f"Contraseña: {pwd}  ->  Hash: {hashed_string}")

print("\nCopia y pega estos hashes en tu script de INSERT.")