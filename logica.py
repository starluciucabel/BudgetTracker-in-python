"""
BudgetTracker - Modulo Logica
Gestisce la logica di business, validazione e calcoli

Studente: Cattano Lorenzo
Anno: 2025/2026
"""

from datetime import datetime
from typing import Tuple, Optional
import re


class Transazione:
    """Classe che rappresenta una singola transazione"""

    def __init__(self, tipo: str, importo: float, categoria: str,
                 descrizione: str = "", data: Optional[str] = None):
        """
        Inizializza una transazione

        Args:
            tipo: 'entrata' o 'uscita'
            importo: Importo della transazione
            categoria: Categoria della transazione
            descrizione: Descrizione opzionale
            data: Data in formato YYYY-MM-DD (default: oggi)
        """
        self.tipo = tipo
        self.importo = importo
        self.categoria = categoria
        self.descrizione = descrizione
        self.data = data if data else datetime.now().strftime("%Y-%m-%d")

    def __str__(self) -> str:
        return f"{self.tipo.upper()}: {self.importo}€ - {self.categoria} ({self.data})"


class Bilancio:
    """Classe per la gestione del bilancio"""

    def __init__(self, entrate: float = 0.0, uscite: float = 0.0):
        """
        Inizializza il bilancio

        Args:
            entrate: Totale entrate
            uscite: Totale uscite
        """
        self.entrate = entrate
        self.uscite = uscite

    @property
    def saldo(self) -> float:
        """Calcola il saldo corrente"""
        return self.entrate - self.uscite

    def aggiungi_entrata(self, importo: float) -> None:
        """Aggiunge un'entrata al bilancio"""
        self.entrate += importo

    def aggiungi_uscita(self, importo: float) -> None:
        """Aggiunge un'uscita al bilancio"""
        self.uscite += importo

    def percentuale_risparmio(self) -> float:
        """Calcola la percentuale di risparmio"""
        if self.entrate == 0:
            return 0.0
        return (self.saldo / self.entrate) * 100

    def __str__(self) -> str:
        return f"Entrate: {self.entrate}€ | Uscite: {self.uscite}€ | Saldo: {self.saldo}€"


class Validatore:
    """Classe per la validazione degli input utente"""

    @staticmethod
    def valida_importo(importo_str: str) -> Tuple[bool, Optional[float], str]:
        """
        Valida un importo inserito dall'utente

        Args:
            importo_str: Stringa contenente l'importo

        Returns:
            Tupla (valido, importo_float, messaggio_errore)
        """
        if not importo_str or importo_str.strip() == "":
            return False, None, "L'importo non può essere vuoto"

        # Sostituisci virgola con punto
        importo_str = importo_str.replace(',', '.')

        try:
            importo = float(importo_str)
            if importo <= 0:
                return False, None, "L'importo deve essere maggiore di zero"
            if importo > 1000000000:
                return False, None, "L'importo è troppo grande"
            # Arrotonda a 2 decimali
            importo = round(importo, 2)
            return True, importo, ""
        except ValueError:
            return False, None, "L'importo deve essere un numero valido"

    @staticmethod
    def valida_data(data_str: str) -> Tuple[bool, Optional[str], str]:
        """
        Valida una data inserita dall'utente

        Args:
            data_str: Stringa contenente la data (formato YYYY-MM-DD)

        Returns:
            Tupla (valido, data_formattata, messaggio_errore)
        """
        if not data_str or data_str.strip() == "":
            return False, None, "La data non può essere vuota"

        # Prova diversi formati
        formati = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"]

        for formato in formati:
            try:
                data_obj = datetime.strptime(data_str, formato)
                # Verifica che la data non sia futura
                if data_obj > datetime.now():
                    return False, None, "La data non può essere futura"
                # Verifica che la data non sia troppo vecchia (es. oltre 100 anni)
                if data_obj.year < datetime.now().year - 100:
                    return False, None, "La data è troppo vecchia"
                # Restituisci in formato standard
                return True, data_obj.strftime("%Y-%m-%d"), ""
            except ValueError:
                continue

        return False, None, "Formato data non valido. Usa YYYY-MM-DD o DD/MM/YYYY"

    @staticmethod
    def valida_categoria(categoria: str, categorie_disponibili: list) -> Tuple[bool, str]:
        """
        Valida una categoria

        Args:
            categoria: Nome della categoria
            categorie_disponibili: Lista delle categorie valide

        Returns:
            Tupla (valido, messaggio_errore)
        """
        if not categoria or categoria.strip() == "":
            return False, "Seleziona una categoria"
        if categoria not in categorie_disponibili:
            return False, "Categoria non valida"
        return True, ""

    @staticmethod
    def valida_tipo(tipo: str) -> Tuple[bool, str]:
        """
        Valida il tipo di transazione

        Args:
            tipo: 'entrata' o 'uscita'

        Returns:
            Tupla (valido, messaggio_errore)
        """
        if tipo not in ['entrata', 'uscita']:
            return False, "Il tipo deve essere 'entrata' o 'uscita'"
        return True, ""

    @staticmethod
    def valida_descrizione(descrizione: str, max_lunghezza: int = 200) -> Tuple[bool, str, str]:
        """
        Valida e pulisce una descrizione

        Args:
            descrizione: Testo della descrizione
            max_lunghezza: Lunghezza massima permessa

        Returns:
            Tupla (valido, descrizione_pulita, messaggio_errore)
        """
        if descrizione is None:
            return True, "", ""

        descrizione = descrizione.strip()

        if len(descrizione) > max_lunghezza:
            return False, descrizione, f"La descrizione non può superare {max_lunghezza} caratteri"

        return True, descrizione, ""


class Formattatore:
    """Classe per la formattazione dei dati"""

    @staticmethod
    def formatta_valuta(importo: float) -> str:
        """
        Formatta un importo come valuta

        Args:
            importo: Importo da formattare

        Returns:
            Stringa formattata (es. "1.234,56 €")
        """
        return f"{importo:,.2f} €".replace(',', 'X').replace('.', ',').replace('X', '.')

    @staticmethod
    def formatta_data(data_str: str, formato_output: str = "%d/%m/%Y") -> str:
        """
        Formatta una data per la visualizzazione

        Args:
            data_str: Data in formato YYYY-MM-DD
            formato_output: Formato desiderato

        Returns:
            Data formattata
        """
        try:
            data_obj = datetime.strptime(data_str, "%Y-%m-%d")
            return data_obj.strftime(formato_output)
        except ValueError:
            return data_str

    @staticmethod
    def formatta_percentuale(valore: float) -> str:
        """
        Formatta una percentuale

        Args:
            valore: Valore percentuale

        Returns:
            Stringa formattata (es. "25,5%")
        """
        return f"{valore:.1f}%".replace('.', ',')

    @staticmethod
    def ottieni_nome_mese(mese_str: str) -> str:
        """
        Converte un mese in formato YYYY-MM nel nome del mese

        Args:
            mese_str: Stringa nel formato YYYY-MM

        Returns:
            Nome del mese (es. "Gennaio 2025")
        """
        try:
            data_obj = datetime.strptime(mese_str, "%Y-%m")
            mesi = [
                "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
                "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"
            ]
            return f"{mesi[data_obj.month - 1]} {data_obj.year}"
        except ValueError:
            return mese_str


class CalcolatoreStatistiche:
    """Classe per il calcolo di statistiche avanzate"""

    @staticmethod
    def media_giornaliera(totale: float, giorni: int) -> float:
        """Calcola la media giornaliera"""
        if giorni == 0:
            return 0.0
        return totale / giorni

    @staticmethod
    def categoria_piu_costosa(spese_per_categoria: dict) -> Tuple[str, float]:
        """
        Trova la categoria con spesa maggiore

        Args:
            spese_per_categoria: Dizionario {categoria: importo}

        Returns:
            Tupla (categoria, importo)
        """
        if not spese_per_categoria:
            return ("Nessuna", 0.0)
        categoria = max(spese_per_categoria, key=spese_per_categoria.get)
        return (categoria, spese_per_categoria[categoria])

    @staticmethod
    def percentuale_categoria(importo_categoria: float, totale: float) -> float:
        """
        Calcola la percentuale di una categoria sul totale

        Args:
            importo_categoria: Importo della categoria
            totale: Totale delle spese

        Returns:
            Percentuale
        """
        if totale == 0:
            return 0.0
        return (importo_categoria / totale) * 100
