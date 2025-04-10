import mariadb
import tkinter as tk
from tkinter import ttk, messagebox

class AnredeManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Anredeverwaltung")
        
        # Datenbankverbindung
        self.conn = mariadb.connect(
            user="sven",
            password="sven",
            host="localhost",
            port=3306,
            database="schlumpfshop3"
        )
        self.cur = self.conn.cursor()
        
        # GUI aufbauen
        self.setup_ui()
        
        # Theme (wie in deinem vorherigen Code)
        self.setup_theme()

    def setup_theme(self):
        self.root.option_add("*tearOff", False)
        style = ttk.Style(self.root)
        self.root.tk.call("source", r"C:\Users\svent\Documents\Phyton_Projekte\tkinter_oberfläche.py\Forest-ttk-theme-master\Forest-ttk-theme-master\forest-dark.tcl")
        style.theme_use("forest-dark")

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Eingabefeld für neue Anrede
        input_frame = ttk.LabelFrame(main_frame, text="Neue Anrede hinzufügen", padding="10")
        input_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(input_frame, text="Anrede:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.anrede_entry = ttk.Entry(input_frame, width=15)
        self.anrede_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        add_button = ttk.Button(input_frame, text="Hinzufügen", command=self.anrede_hinzufuegen)
        add_button.grid(row=0, column=2, padx=(15, 5), pady=5)
        
        # Liste der vorhandenen Anreden
        list_frame = ttk.LabelFrame(main_frame, text="Vorhandene Anreden", padding="10")
        list_frame.pack(fill="both", expand=True)
        
        columns = ("ID", "Anrede")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=5)
        
        # Spalten konfigurieren
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Anrede", width=150, anchor="w")
        
        # Überschriften
        self.tree.heading("ID", text="ID")
        self.tree.heading("Anrede", text="Anrede")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Vorhandene Anreden laden
        self.lade_anreden()
        
        # Event-Binding für Enter-Taste
        self.anrede_entry.bind("<Return>", lambda event: self.anrede_hinzufuegen())

    def lade_anreden(self):
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("SELECT * FROM anrede ORDER BY ID_Anrede")
        for row in self.cur.fetchall():
            self.tree.insert("", "end", values=row)

    def anrede_hinzufuegen(self):
        neue_anrede = self.anrede_entry.get().strip()
        
        if not neue_anrede:
            messagebox.showwarning("Eingabefehler", "Bitte eine Anrede eingeben!")
            return
            
        if len(neue_anrede) > 10:
            messagebox.showwarning("Eingabefehler", "Anrede darf maximal 10 Zeichen lang sein!")
            return
            
        try:
            # Nächste ID finden
            self.cur.execute("SELECT MAX(ID_Anrede) FROM anrede")
            max_id = self.cur.fetchone()[0] or 0
            neue_id = max_id + 1
            
            # Anrede einfügen
            self.cur.execute("INSERT INTO anrede (ID_Anrede, Anrede) VALUES (?, ?)", 
                           (neue_id, neue_anrede))
            self.conn.commit()
            
            messagebox.showinfo("Erfolg", f"Anrede '{neue_anrede}' wurde hinzugefügt!")
            self.anrede_entry.delete(0, tk.END)
            self.lade_anreden()
            
        except mariadb.Error as e:
            messagebox.showerror("Datenbankfehler", f"Fehler: {e}")
            self.conn.rollback()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AnredeManager(root)
    
    # Fenster zentrieren
    root.update()
    root.minsize(400, 300)
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()