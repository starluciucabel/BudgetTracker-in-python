"""
BudgetTracker - Modulo GUI
Gestisce l'interfaccia grafica con tkinter

Studente: Cattano Lorenzo
Anno: 2025/2026
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from typing import Optional, Callable
from database import Database
from logica import Validatore, Formattatore, Bilancio, CalcolatoreStatistiche
from grafici import GeneratoreGrafici


class InterfacciaGrafica:
    """Classe principale per l'interfaccia grafica dell'applicazione"""

    def __init__(self, root: tk.Tk):
        """
        Inizializza l'interfaccia grafica

        Args:
            root: Finestra principale tkinter
        """
        self.root = root
        self.root.title("BudgetTracker - Gestione Spese Personali")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)

        # Inizializza i moduli
        self.db = Database()
        self.validatore = Validatore()
        self.formattatore = Formattatore()
        self.generatore_grafici = GeneratoreGrafici()
        self.statistiche = CalcolatoreStatistiche()

        # Variabili
        self.mese_corrente = datetime.now().strftime("%Y-%m")
        self.categoria_filtro = "Tutte"

        # Configura stile
        self._configura_stile()

        # Crea l'interfaccia
        self._crea_menu()
        self._crea_interfaccia()

        # Carica dati iniziali
        self.aggiorna_visualizzazione()

        # Gestisci chiusura
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _configura_stile(self) -> None:
        """Configura lo stile dell'interfaccia"""
        style = ttk.Style()
        style.theme_use('clam')

        # Colori personalizzati
        self.colore_primario = "#2C3E50"
        self.colore_secondario = "#34495E"
        self.colore_accento = "#3498DB"
        self.colore_successo = "#2ECC71"
        self.colore_errore = "#E74C3C"
        self.colore_sfondo = "#ECF0F1"

        # Configura widget
        style.configure('TFrame', background=self.colore_sfondo)
        style.configure('TLabel', background=self.colore_sfondo, font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'),
                       background=self.colore_sfondo, foreground=self.colore_primario)
        style.configure('Saldo.TLabel', font=('Segoe UI', 20, 'bold'),
                       background=self.colore_sfondo)

    def _crea_menu(self) -> None:
        """Crea la barra del menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Backup Database", command=self._backup_database)
        file_menu.add_separator()
        file_menu.add_command(label="Esci", command=self._on_closing)

        # Menu Visualizza
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Visualizza", menu=view_menu)
        view_menu.add_command(label="Aggiorna", command=self.aggiorna_visualizzazione)

        # Menu Aiuto
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aiuto", menu=help_menu)
        help_menu.add_command(label="Info", command=self._mostra_info)

    def _crea_interfaccia(self) -> None:
        """Crea l'interfaccia principale"""
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configura griglia
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Crea sezioni
        self._crea_pannello_sinistra(main_frame)
        self._crea_pannello_centrale(main_frame)

    def _crea_pannello_sinistra(self, parent) -> None:
        """Crea il pannello sinistro con input e riepilogo"""
        left_frame = ttk.Frame(parent, padding="5")
        left_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Sezione inserimento transazione
        self._crea_sezione_inserimento(left_frame)

        # Sezione riepilogo
        self._crea_sezione_riepilogo(left_frame)

    def _crea_sezione_inserimento(self, parent) -> None:
        """Crea la sezione per inserire nuove transazioni"""
        frame = ttk.LabelFrame(parent, text="Nuova Transazione", padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N), pady=(0, 10))

        # Tipo transazione
        ttk.Label(frame, text="Tipo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.tipo_var = tk.StringVar(value="uscita")
        tipo_frame = ttk.Frame(frame)
        tipo_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Radiobutton(tipo_frame, text="Entrata", variable=self.tipo_var,
                       value="entrata", command=self._on_tipo_changed).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(tipo_frame, text="Uscita", variable=self.tipo_var,
                       value="uscita", command=self._on_tipo_changed).pack(side=tk.LEFT)

        # Importo
        ttk.Label(frame, text="Importo (€):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.importo_entry = ttk.Entry(frame, width=20)
        self.importo_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        # Categoria
        ttk.Label(frame, text="Categoria:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.categoria_var = tk.StringVar()
        self.categoria_combo = ttk.Combobox(frame, textvariable=self.categoria_var,
                                           state="readonly", width=18)
        self.categoria_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        self._aggiorna_categorie()

        # Data
        ttk.Label(frame, text="Data:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.data_entry = ttk.Entry(frame, width=20)
        self.data_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.data_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)

        # Descrizione
        ttk.Label(frame, text="Descrizione:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.descrizione_entry = ttk.Entry(frame, width=20)
        self.descrizione_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)

        # Pulsante aggiungi
        btn_aggiungi = ttk.Button(frame, text="Aggiungi Transazione",
                                 command=self._aggiungi_transazione)
        btn_aggiungi.grid(row=5, column=0, columnspan=2, pady=10)

        frame.columnconfigure(1, weight=1)

    def _crea_sezione_riepilogo(self, parent) -> None:
        """Crea la sezione riepilogo con saldo"""
        frame = ttk.LabelFrame(parent, text="Riepilogo Mensile", padding="10")
        frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), pady=(0, 10))

        # Selettore mese
        mese_frame = ttk.Frame(frame)
        mese_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        ttk.Label(mese_frame, text="Mese:").pack(side=tk.LEFT, padx=5)
        self.mese_var = tk.StringVar(value=self.mese_corrente)
        self.mese_combo = ttk.Combobox(mese_frame, textvariable=self.mese_var,
                                      state="readonly", width=15)
        self.mese_combo.pack(side=tk.LEFT, padx=5)
        self.mese_combo.bind("<<ComboboxSelected>>", lambda e: self.aggiorna_visualizzazione())
        self._aggiorna_mesi()

        # Entrate
        ttk.Label(frame, text="Entrate:", font=('Segoe UI', 11)).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.entrate_label = ttk.Label(frame, text="0,00 €", font=('Segoe UI', 11, 'bold'),
                                       foreground=self.colore_successo)
        self.entrate_label.grid(row=1, column=1, sticky=tk.E, pady=5)

        # Uscite
        ttk.Label(frame, text="Uscite:", font=('Segoe UI', 11)).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.uscite_label = ttk.Label(frame, text="0,00 €", font=('Segoe UI', 11, 'bold'),
                                     foreground=self.colore_errore)
        self.uscite_label.grid(row=2, column=1, sticky=tk.E, pady=5)

        # Separatore
        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Saldo
        ttk.Label(frame, text="Saldo:", font=('Segoe UI', 14, 'bold')).grid(
            row=4, column=0, sticky=tk.W, pady=5)
        self.saldo_label = ttk.Label(frame, text="0,00 €", style='Saldo.TLabel')
        self.saldo_label.grid(row=4, column=1, sticky=tk.E, pady=5)

        frame.columnconfigure(1, weight=1)

    def _crea_pannello_centrale(self, parent) -> None:
        """Crea il pannello centrale con tabs"""
        # Notebook per tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))

        # Tab Transazioni
        self._crea_tab_transazioni()

        # Tab Grafici
        self._crea_tab_grafici()

    def _crea_tab_transazioni(self) -> None:
        """Crea il tab delle transazioni"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="Transazioni")

        # Frame filtri
        filtri_frame = ttk.Frame(tab)
        filtri_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(filtri_frame, text="Filtra per categoria:").pack(side=tk.LEFT, padx=5)
        self.filtro_categoria_var = tk.StringVar(value="Tutte")
        filtro_combo = ttk.Combobox(filtri_frame, textvariable=self.filtro_categoria_var,
                                   state="readonly", width=15)
        filtro_combo.pack(side=tk.LEFT, padx=5)
        filtro_combo.bind("<<ComboboxSelected>>", lambda e: self.aggiorna_visualizzazione())

        # Aggiorna combo categorie per filtro
        categorie = ["Tutte"] + self.db.ottieni_categorie()
        filtro_combo['values'] = categorie

        ttk.Button(filtri_frame, text="Elimina Selezionata",
                  command=self._elimina_transazione_selezionata).pack(side=tk.RIGHT, padx=5)

        # Treeview transazioni
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview
        columns = ('Data', 'Tipo', 'Categoria', 'Descrizione', 'Importo')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        # Configura colonne
        self.tree.heading('Data', text='Data')
        self.tree.heading('Tipo', text='Tipo')
        self.tree.heading('Categoria', text='Categoria')
        self.tree.heading('Descrizione', text='Descrizione')
        self.tree.heading('Importo', text='Importo')

        self.tree.column('Data', width=100)
        self.tree.column('Tipo', width=80)
        self.tree.column('Categoria', width=120)
        self.tree.column('Descrizione', width=250)
        self.tree.column('Importo', width=100)

        # Tag per colori
        self.tree.tag_configure('entrata', foreground=self.colore_successo)
        self.tree.tag_configure('uscita', foreground=self.colore_errore)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def _crea_tab_grafici(self) -> None:
        """Crea il tab dei grafici"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="Grafici")

        # Frame controlli
        controlli_frame = ttk.Frame(tab)
        controlli_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(controlli_frame, text="Tipo grafico:").pack(side=tk.LEFT, padx=5)
        self.tipo_grafico_var = tk.StringVar(value="torta")
        ttk.Radiobutton(controlli_frame, text="Torta", variable=self.tipo_grafico_var,
                       value="torta", command=self._aggiorna_grafico).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(controlli_frame, text="Barre", variable=self.tipo_grafico_var,
                       value="barre", command=self._aggiorna_grafico).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(controlli_frame, text="Confronto", variable=self.tipo_grafico_var,
                       value="confronto", command=self._aggiorna_grafico).pack(side=tk.LEFT, padx=5)

        ttk.Button(controlli_frame, text="Salva Grafico",
                  command=self._salva_grafico).pack(side=tk.RIGHT, padx=5)

        # Frame grafico
        self.grafico_frame = ttk.Frame(tab)
        self.grafico_frame.pack(fill=tk.BOTH, expand=True)

    def _on_tipo_changed(self) -> None:
        """Gestisce il cambio di tipo transazione"""
        self._aggiorna_categorie()

    def _aggiorna_categorie(self) -> None:
        """Aggiorna la lista delle categorie in base al tipo"""
        tipo = self.tipo_var.get()
        categorie = self.db.ottieni_categorie(tipo)
        self.categoria_combo['values'] = categorie
        if categorie:
            self.categoria_combo.current(0)

    def _aggiorna_mesi(self) -> None:
        """Aggiorna la lista dei mesi disponibili"""
        # Genera ultimi 12 mesi
        mesi = []
        data_corrente = datetime.now()
        for i in range(12):
            anno = data_corrente.year
            mese = data_corrente.month - i
            if mese <= 0:
                mese += 12
                anno -= 1
            mesi.append(f"{anno}-{mese:02d}")

        self.mese_combo['values'] = mesi

    def _aggiungi_transazione(self) -> None:
        """Aggiunge una nuova transazione al database"""
        # Valida input
        tipo = self.tipo_var.get()
        importo_str = self.importo_entry.get()
        categoria = self.categoria_var.get()
        data_str = self.data_entry.get()
        descrizione = self.descrizione_entry.get()

        # Validazione tipo
        valido, msg = self.validatore.valida_tipo(tipo)
        if not valido:
            messagebox.showerror("Errore", msg)
            return

        # Validazione importo
        valido, importo, msg = self.validatore.valida_importo(importo_str)
        if not valido:
            messagebox.showerror("Errore", msg)
            self.importo_entry.focus()
            return

        # Validazione categoria
        categorie = self.db.ottieni_categorie(tipo)
        valido, msg = self.validatore.valida_categoria(categoria, categorie)
        if not valido:
            messagebox.showerror("Errore", msg)
            return

        # Validazione data
        valido, data, msg = self.validatore.valida_data(data_str)
        if not valido:
            messagebox.showerror("Errore", msg)
            self.data_entry.focus()
            return

        # Validazione descrizione
        valido, descrizione, msg = self.validatore.valida_descrizione(descrizione)
        if not valido:
            messagebox.showerror("Errore", msg)
            self.descrizione_entry.focus()
            return

        # Inserisci nel database
        if self.db.aggiungi_transazione(tipo, importo, categoria, descrizione, data):
            messagebox.showinfo("Successo", "Transazione aggiunta con successo!")
            # Pulisci campi
            self.importo_entry.delete(0, tk.END)
            self.descrizione_entry.delete(0, tk.END)
            self.data_entry.delete(0, tk.END)
            self.data_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            # Aggiorna visualizzazione
            self.aggiorna_visualizzazione()
        else:
            messagebox.showerror("Errore", "Errore nell'aggiunta della transazione")

    def _elimina_transazione_selezionata(self) -> None:
        """Elimina la transazione selezionata"""
        selezione = self.tree.selection()
        if not selezione:
            messagebox.showwarning("Attenzione", "Seleziona una transazione da eliminare")
            return

        # Conferma
        risposta = messagebox.askyesno("Conferma",
                                      "Sei sicuro di voler eliminare la transazione selezionata?")
        if not risposta:
            return

        # Ottieni ID dalla selezione
        item = self.tree.item(selezione[0])
        # L'ID è memorizzato come tag
        tags = self.tree.item(selezione[0], 'tags')
        if len(tags) > 1:
            id_transazione = int(tags[1])
            if self.db.elimina_transazione(id_transazione):
                messagebox.showinfo("Successo", "Transazione eliminata con successo!")
                self.aggiorna_visualizzazione()
            else:
                messagebox.showerror("Errore", "Errore nell'eliminazione della transazione")

    def aggiorna_visualizzazione(self) -> None:
        """Aggiorna tutti i dati visualizzati"""
        mese = self.mese_var.get()
        filtro_cat = self.filtro_categoria_var.get() if hasattr(self, 'filtro_categoria_var') else None

        # Aggiorna riepilogo
        entrate, uscite, saldo = self.db.ottieni_saldo(mese)
        self.entrate_label.config(text=self.formattatore.formatta_valuta(entrate))
        self.uscite_label.config(text=self.formattatore.formatta_valuta(uscite))
        self.saldo_label.config(text=self.formattatore.formatta_valuta(saldo))

        # Colora saldo
        if saldo >= 0:
            self.saldo_label.config(foreground=self.colore_successo)
        else:
            self.saldo_label.config(foreground=self.colore_errore)

        # Aggiorna lista transazioni
        self._aggiorna_lista_transazioni(mese, filtro_cat)

        # Aggiorna grafico
        self._aggiorna_grafico()

    def _aggiorna_lista_transazioni(self, mese: str, categoria: Optional[str]) -> None:
        """Aggiorna la lista delle transazioni"""
        # Pulisci treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Ottieni transazioni
        cat_filtro = None if categoria == "Tutte" else categoria
        transazioni = self.db.ottieni_transazioni(mese, cat_filtro)

        # Popola treeview
        for trans in transazioni:
            data_formattata = self.formattatore.formatta_data(trans['data'])
            importo_formattato = self.formattatore.formatta_valuta(trans['importo'])
            tipo_label = trans['tipo'].capitalize()

            # Inserisci con tag per colore e ID
            self.tree.insert('', tk.END,
                           values=(data_formattata, tipo_label, trans['categoria'],
                                 trans['descrizione'], importo_formattato),
                           tags=(trans['tipo'], str(trans['id'])))

    def _aggiorna_grafico(self) -> None:
        """Aggiorna il grafico visualizzato"""
        # Pulisci frame
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        mese = self.mese_var.get()
        tipo_grafico = self.tipo_grafico_var.get()

        try:
            if tipo_grafico == "torta":
                spese = self.db.ottieni_spese_per_categoria(mese)
                figura = self.generatore_grafici.crea_grafico_torta(
                    spese, f"Spese per Categoria - {self.formattatore.ottieni_nome_mese(mese)}")
            elif tipo_grafico == "barre":
                spese = self.db.ottieni_spese_per_categoria(mese)
                figura = self.generatore_grafici.crea_grafico_barre(
                    spese, f"Spese per Categoria - {self.formattatore.ottieni_nome_mese(mese)}",
                    "Categoria", "Importo (€)", orizzontale=True)
            else:  # confronto
                entrate, uscite, saldo = self.db.ottieni_saldo(mese)
                figura = self.generatore_grafici.crea_grafico_confronto_entrate_uscite(
                    entrate, uscite)

            # Incorpora in tkinter
            canvas = self.generatore_grafici.incorpora_grafico_in_tkinter(
                figura, self.grafico_frame)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            ttk.Label(self.grafico_frame, text=f"Errore nella generazione del grafico: {e}").pack()

    def _salva_grafico(self) -> None:
        """Salva il grafico corrente su file"""
        percorso = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), ("Tutti i file", "*.*")]
        )
        if percorso:
            mese = self.mese_var.get()
            tipo_grafico = self.tipo_grafico_var.get()

            try:
                if tipo_grafico == "torta":
                    spese = self.db.ottieni_spese_per_categoria(mese)
                    figura = self.generatore_grafici.crea_grafico_torta(spese)
                elif tipo_grafico == "barre":
                    spese = self.db.ottieni_spese_per_categoria(mese)
                    figura = self.generatore_grafici.crea_grafico_barre(spese, orizzontale=True)
                else:
                    entrate, uscite, saldo = self.db.ottieni_saldo(mese)
                    figura = self.generatore_grafici.crea_grafico_confronto_entrate_uscite(
                        entrate, uscite)

                if self.generatore_grafici.salva_grafico(figura, percorso):
                    messagebox.showinfo("Successo", "Grafico salvato con successo!")
                else:
                    messagebox.showerror("Errore", "Errore nel salvataggio del grafico")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore: {e}")

    def _backup_database(self) -> None:
        """Crea un backup del database"""
        percorso = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("Database SQLite", "*.db"), ("Tutti i file", "*.*")],
            initialfile=f"backup_budgettracker_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        )
        if percorso:
            if self.db.backup(percorso):
                messagebox.showinfo("Successo", "Backup creato con successo!")
            else:
                messagebox.showerror("Errore", "Errore nella creazione del backup")

    def _mostra_info(self) -> None:
        """Mostra informazioni sull'applicazione"""
        info = """BudgetTracker - Gestione Spese Personali

Versione: 1.0
Anno: 2025/2026

Studente: Cattano Lorenzo
Scuola: ITS ICT
Docente: Prof. Papa Massimo

Applicazione per la gestione delle finanze personali
con supporto per entrate, uscite e analisi statistiche."""
        messagebox.showinfo("Informazioni", info)

    def _on_closing(self) -> None:
        """Gestisce la chiusura dell'applicazione"""
        if messagebox.askokcancel("Uscita", "Vuoi uscire dall'applicazione?"):
            self.db.chiudi()
            self.root.destroy()


def avvia_applicazione():
    """Funzione per avviare l'applicazione"""
    root = tk.Tk()
    app = InterfacciaGrafica(root)
    root.mainloop()
