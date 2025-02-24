import streamlit as st
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes  # Importamos funciones para cifrado AES

# Definimos el título de la aplicación
st.title("Cifrado Adrián PyCryptography - Codificación y Decodificación")

# Inicializamos variables de sesión si aún no existen
if "texto_cifrado" not in st.session_state:
    st.session_state.texto_cifrado = ""  # Almacena el texto cifrado

if "clave" not in st.session_state:
    st.session_state.clave = get_random_bytes(16)  # Generamos una clave de 16 bytes

if "nonce" not in st.session_state:
    st.session_state.nonce = None  # Inicializamos el nonce

if "tag" not in st.session_state:
    st.session_state.tag = None  # Inicializamos el tag

# Permite la subida de un archivo TXT
archivo = st.file_uploader("Sube un archivo TXT", type=["txt"], key="file_uploader_2")

if archivo:
    # Leemos y mostramos el contenido del archivo
    texto = archivo.read().decode("utf-8")
    st.text_area("Contenido del archivo:", texto, height=200)
    st.session_state.texto_cifrado = texto

    # Botón para cifrar el texto
    if st.button("Cifrar"):
        st.session_state.cipher = AES.new(st.session_state.clave, AES.MODE_EAX)  # Configuramos cifrado AES
        st.session_state.texto_cifrado = texto.encode()  # Convertimos texto a bytes
        st.session_state.cifrado, st.session_state.tag = st.session_state.cipher.encrypt_and_digest(st.session_state.texto_cifrado)  # Ciframos y generamos tag
        st.session_state.nonce = st.session_state.cipher.nonce  # Guardamos el nonce

        # Creamos la carpeta 'archivos' si no existe
        os.makedirs("archivos", exist_ok=True)

        # Guardamos el texto cifrado en un archivo
        with open("archivos/cifrado.txt", "wb") as f:
            f.write(st.session_state.cifrado)
        
        st.markdown(f"**Texto cifrado:** `{st.session_state.cifrado}`")

    # Botón para descifrar el texto
    if st.button("Descifrar"):
        if st.session_state.texto_cifrado and st.session_state.nonce and st.session_state.tag:
            cipher_dec = AES.new(st.session_state.clave, AES.MODE_EAX, st.session_state.nonce)  # Configuramos descifrado
            try:
                # Intentamos descifrar el texto
                st.session_state.texto_descifrado = cipher_dec.decrypt(st.session_state.cifrado).decode()
                
                # Guardamos el texto descifrado en un archivo
                with open("archivos/descifrado.txt", "w") as f:
                    f.write(st.session_state.texto_descifrado)
                
                st.markdown(f"**Texto descifrado:** `{st.session_state.texto_descifrado}`")
            
            except:
                st.error("Error: El texto cifrado no es válido o la clave es incorrecta")
        else:
            st.warning("No hay un texto cifrado válido para descifrar. Cifra un texto primero")
