# create_hash.py
from app.security import get_password_hash

# La contraseña que usaremos para las pruebas
plain_password = "password123"

# Generamos el hash
hashed_password = get_password_hash(plain_password)

print("\n--- HASH DE CONTRASEÑA GENERADO ---")
print("Copia la siguiente línea completa y pégala en el script de SQL:")
print(f"\n{hashed_password}\n")
print("------------------------------------")