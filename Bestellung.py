import mariadb
import tkinter as tk
from tkinter import ttk, messagebox

class Artikel:
    def __init__(self, nummer, name, preis, lagerbestand, lieferant):
        self.nummer = nummer
        self.name = name
        self.preis = preis
        self.lagerbestand = lagerbestand
        self.lieferant = lieferant

class LagerbestandsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lagerbestandsüberwachung")
        self.artikel_liste = []
        
        # Datenbankverbindung herstellen
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
        
        # Initiale Suche mit Standardwert 100
        self.entry.insert(0, "100")
        self.update_datenbank()

    def setup_ui(self):
        # Styling
        self.root.option_add("*tearOff", False)
        style = ttk.Style(self.root)
        self.root.tk.call("source", r"C:\Users\svent\Documents\Phyton_Projekte\tkinter_oberfläche.py\Forest-ttk-theme-master\Forest-ttk-theme-master\forest-dark.tcl")
        style.theme_use("forest-dark")

        # Hauptrahmen
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Suchbereich oben
        search_frame = ttk.LabelFrame(main_frame, text="Mindestlagerbestand", padding=(10, 5))
        search_frame.pack(fill="x", pady=(0, 10))
        
        self.entry = ttk.Entry(search_frame)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        search_btn = ttk.Button(search_frame, text="Suchen", command=self.update_datenbank)
        search_btn.pack(side="left")

        # Treeview für Ergebnisse
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True)

        self.treeview = ttk.Treeview(tree_frame, columns=("ID", "Artikel", "Preis", "Lagerbestand", "Lieferant"), 
                                   show="headings", height=15)
        
        # Spalten konfigurieren
        self.treeview.column("ID", width=80, anchor="center")
        self.treeview.column("Artikel", width=200)
        self.treeview.column("Preis", width=100, anchor="e")
        self.treeview.column("Lagerbestand", width=100, anchor="center")
        self.treeview.column("Lieferant", width=150)
        
        # Überschriften
        self.treeview.heading("ID", text="Artikelnummer")
        self.treeview.heading("Artikel", text="Artikelbezeichnung")
        self.treeview.heading("Preis", text="Preis (Netto)")
        self.treeview.heading("Lagerbestand", text="Lagerbestand")
        self.treeview.heading("Lieferant", text="Lieferant")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        
        self.treeview.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Event-Binding für Enter-Taste
        self.entry.bind("<Return>", lambda event: self.update_datenbank())

    def update_datenbank(self, *args):
        eingabe = self.entry.get()
        try:
            eingabe = int(eingabe)
            self.cur.execute("""
                SELECT `Artikelnummer`, `Artikelname`, `Preis_Netto`, `Lagerbestand`, lieferant.Lieferantenname
                FROM `artikel` 
                INNER JOIN lieferant ON artikel.Lieferant = lieferant.ID_Lieferant
                WHERE `Lagerbestand` < %s
                ORDER BY `Lagerbestand` ASC
                """, (eingabe,))
            
            # Alte Daten löschen
            self.artikel_liste.clear()
            self.treeview.delete(*self.treeview.get_children())
            
            # Ergebnisse verarbeiten
            for row in self.cur.fetchall():
                artikel = Artikel(*row)
                self.artikel_liste.append(artikel)
                self.treeview.insert("", "end", values=(
                    artikel.nummer,
                    artikel.name,
                    f"{artikel.preis:.2f} €",
                    artikel.lagerbestand,
                    artikel.lieferant
                ))
                
        except ValueError:
            messagebox.showerror("Fehler", "Bitte eine gültige Zahl eingeben!")
        except mariadb.Error as e:
            messagebox.showerror("Datenbankfehler", f"Fehler: {e}")

    def __del__(self):
        # Datenbankverbindung schließen
        if hasattr(self, 'conn'):
            self.conn.close()

# Hauptprogramm
if __name__ == "__main__":
    root = tk.Tk()
    app = LagerbestandsApp(root)
    
    # Fenster zentrieren
    root.update()
    root.minsize(800, 600)
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()