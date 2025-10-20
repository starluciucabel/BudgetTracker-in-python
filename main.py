"""
BudgetTracker - Applicazione Principale
Gestione Spese Personali

Studente: Cattano Lorenzo
Anno scolastico: 2025/2026
Scuola: Istituto Tecnico Superiore "ITS ICT"
Materia: Informatica
Docente: Prof. Papa Massimo

Descrizione:
Applicazione desktop per la gestione delle finanze personali.
Permette di registrare entrate e uscite, visualizzare il saldo mensile,
analizzare le spese per categoria e consultare lo storico delle transazioni.
"""

import sys
import tkinter as tk
from tkinter import messagebox


def main():
    """
    Funzione principale dell'applicazione
    """
    try:
        # Importa il modulo GUI
        from gui import avvia_applicazione

        # Avvia l'applicazione
        avvia_applicazione()

    except ImportError as e:
        print(f"Errore nell'importazione dei moduli: {e}")
        print("\nAssicurati di aver installato tutte le dipendenze:")
        print("  pip install matplotlib")
        sys.exit(1)

    except Exception as e:
        print(f"Errore nell'avvio dell'applicazione: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Intestazione
    print("=" * 60)
    print("BudgetTracker - Gestione Spese Personali")
    print("Studente: Cattano Lorenzo")
    print("Anno: 2025/2026")
    print("=" * 60)
    print("\nAvvio dell'applicazione...\n")

    # Avvia l'applicazione
    main()
