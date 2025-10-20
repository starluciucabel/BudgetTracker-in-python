"""
BudgetTracker - Modulo Database
Gestisce la connessione e le operazioni sul database SQLite

Studente: Cattano Lorenzo
Anno: 2025/2026
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class Database:
    """Classe per la gestione del database SQLite delle transazioni"""

    def __init__(self, db_name: str = "budgettracker.db"):
        """
        Inizializza la connessione al database

        Args:
            db_name: Nome del file database
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables()

    def _connect(self) -> None:
        """Crea la connessione al database"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            raise Exception(f"Errore nella connessione al database: {e}")

    def _create_tables(self) -> None:
        """Crea le tabelle del database se non esistono"""
        try:
            # Tabella transazioni
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS transazioni (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL CHECK(tipo IN ('entrata', 'uscita')),
                    importo REAL NOT NULL CHECK(importo > 0),
                    categoria TEXT NOT NULL,
                    descrizione TEXT,
                    data TEXT NOT NULL,
                    data_inserimento TEXT NOT NULL
                )
            """)

            # Tabella categorie predefinite
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS categorie (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    tipo TEXT NOT NULL CHECK(tipo IN ('entrata', 'uscita')),
                    UNIQUE(nome, tipo)
                )
            """)

            # Inserisci categorie predefinite se la tabella è vuota
            self.cursor.execute("SELECT COUNT(*) FROM categorie")
            if self.cursor.fetchone()[0] == 0:
                categorie_default = [
                    ('Alimentari', 'uscita'),
                    ('Trasporti', 'uscita'),
                    ('Svago', 'uscita'),
                    ('Bollette', 'uscita'),
                    ('Salute', 'uscita'),
                    ('Abbigliamento', 'uscita'),
                    ('Istruzione', 'uscita'),
                    ('Casa', 'uscita'),
                    ('Altro', 'uscita'),
                    ('Stipendio', 'entrata'),
                    ('Bonus', 'entrata'),
                    ('Investimenti', 'entrata'),
                    ('Altro', 'entrata')
                ]
                self.cursor.executemany(
                    "INSERT INTO categorie (nome, tipo) VALUES (?, ?)",
                    categorie_default
                )

            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Errore nella creazione delle tabelle: {e}")

    def aggiungi_transazione(self, tipo: str, importo: float, categoria: str,
                           descrizione: str, data: str) -> bool:
        """
        Aggiunge una nuova transazione al database

        Args:
            tipo: 'entrata' o 'uscita'
            importo: Importo della transazione
            categoria: Categoria della transazione
            descrizione: Descrizione opzionale
            data: Data della transazione (formato YYYY-MM-DD)

        Returns:
            True se l'inserimento è avvenuto con successo
        """
        try:
            data_inserimento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("""
                INSERT INTO transazioni (tipo, importo, categoria, descrizione, data, data_inserimento)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tipo, importo, categoria, descrizione, data, data_inserimento))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Errore nell'inserimento della transazione: {e}")
            return False

    def ottieni_transazioni(self, mese: Optional[str] = None,
                           categoria: Optional[str] = None) -> List[Dict]:
        """
        Recupera le transazioni dal database con filtri opzionali

        Args:
            mese: Filtro per mese (formato YYYY-MM)
            categoria: Filtro per categoria

        Returns:
            Lista di dizionari con le transazioni
        """
        try:
            query = "SELECT * FROM transazioni WHERE 1=1"
            params = []

            if mese:
                query += " AND strftime('%Y-%m', data) = ?"
                params.append(mese)

            if categoria and categoria != "Tutte":
                query += " AND categoria = ?"
                params.append(categoria)

            query += " ORDER BY data DESC, data_inserimento DESC"

            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()

            transazioni = []
            for row in rows:
                transazioni.append({
                    'id': row[0],
                    'tipo': row[1],
                    'importo': row[2],
                    'categoria': row[3],
                    'descrizione': row[4],
                    'data': row[5],
                    'data_inserimento': row[6]
                })

            return transazioni
        except sqlite3.Error as e:
            print(f"Errore nel recupero delle transazioni: {e}")
            return []

    def elimina_transazione(self, id_transazione: int) -> bool:
        """
        Elimina una transazione dal database

        Args:
            id_transazione: ID della transazione da eliminare

        Returns:
            True se l'eliminazione è avvenuta con successo
        """
        try:
            self.cursor.execute("DELETE FROM transazioni WHERE id = ?", (id_transazione,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Errore nell'eliminazione della transazione: {e}")
            return False

    def ottieni_categorie(self, tipo: Optional[str] = None) -> List[str]:
        """
        Recupera le categorie dal database

        Args:
            tipo: Filtro per tipo ('entrata' o 'uscita')

        Returns:
            Lista di nomi delle categorie
        """
        try:
            if tipo:
                self.cursor.execute("SELECT nome FROM categorie WHERE tipo = ? ORDER BY nome", (tipo,))
            else:
                self.cursor.execute("SELECT nome FROM categorie ORDER BY nome")

            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Errore nel recupero delle categorie: {e}")
            return []

    def ottieni_saldo(self, mese: Optional[str] = None) -> Tuple[float, float, float]:
        """
        Calcola il saldo per un determinato mese

        Args:
            mese: Mese da analizzare (formato YYYY-MM)

        Returns:
            Tupla (entrate_totali, uscite_totali, saldo)
        """
        try:
            query_base = "SELECT tipo, SUM(importo) FROM transazioni WHERE 1=1"
            params = []

            if mese:
                query_base += " AND strftime('%Y-%m', data) = ?"
                params.append(mese)

            query_base += " GROUP BY tipo"

            self.cursor.execute(query_base, params)
            risultati = self.cursor.fetchall()

            entrate = 0.0
            uscite = 0.0

            for row in risultati:
                if row[0] == 'entrata':
                    entrate = row[1]
                elif row[0] == 'uscita':
                    uscite = row[1]

            saldo = entrate - uscite
            return (entrate, uscite, saldo)
        except sqlite3.Error as e:
            print(f"Errore nel calcolo del saldo: {e}")
            return (0.0, 0.0, 0.0)

    def ottieni_spese_per_categoria(self, mese: Optional[str] = None) -> Dict[str, float]:
        """
        Calcola le spese totali per categoria

        Args:
            mese: Mese da analizzare (formato YYYY-MM)

        Returns:
            Dizionario {categoria: importo_totale}
        """
        try:
            query = "SELECT categoria, SUM(importo) FROM transazioni WHERE tipo = 'uscita'"
            params = []

            if mese:
                query += " AND strftime('%Y-%m', data) = ?"
                params.append(mese)

            query += " GROUP BY categoria ORDER BY SUM(importo) DESC"

            self.cursor.execute(query, params)
            risultati = self.cursor.fetchall()

            return {row[0]: row[1] for row in risultati}
        except sqlite3.Error as e:
            print(f"Errore nel calcolo delle spese per categoria: {e}")
            return {}

    def chiudi(self) -> None:
        """Chiude la connessione al database"""
        if self.conn:
            self.conn.close()

    def backup(self, percorso_backup: str) -> bool:
        """
        Crea un backup del database

        Args:
            percorso_backup: Percorso del file di backup

        Returns:
            True se il backup è stato creato con successo
        """
        try:
            import shutil
            shutil.copy2(self.db_name, percorso_backup)
            return True
        except Exception as e:
            print(f"Errore nel backup del database: {e}")
            return False
