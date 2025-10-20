"""
BudgetTracker - Modulo Grafici
Gestisce la generazione di grafici con matplotlib

Studente: Cattano Lorenzo
Anno: 2025/2026
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from typing import Dict, Optional, Tuple

# Configura matplotlib per usare un backend compatibile con tkinter
matplotlib.use('TkAgg')


class GeneratoreGrafici:
    """Classe per la generazione di grafici statistici"""

    def __init__(self):
        """Inizializza il generatore di grafici"""
        # Configura lo stile dei grafici
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colori = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A',
            '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2',
            '#F8B195', '#C06C84'
        ]

    def crea_grafico_torta(self, spese_per_categoria: Dict[str, float],
                          titolo: str = "Distribuzione Spese per Categoria",
                          dimensione: Tuple[int, int] = (10, 8)) -> Figure:
        """
        Crea un grafico a torta delle spese per categoria

        Args:
            spese_per_categoria: Dizionario {categoria: importo}
            titolo: Titolo del grafico
            dimensione: Tupla (larghezza, altezza) in pollici

        Returns:
            Figure matplotlib
        """
        fig = Figure(figsize=dimensione, dpi=100)
        ax = fig.add_subplot(111)

        if not spese_per_categoria or sum(spese_per_categoria.values()) == 0:
            ax.text(0.5, 0.5, 'Nessun dato disponibile',
                   horizontalalignment='center',
                   verticalalignment='center',
                   fontsize=14,
                   color='gray')
            ax.set_title(titolo, fontsize=16, fontweight='bold', pad=20)
            return fig

        # Ordina per importo decrescente
        categorie = list(spese_per_categoria.keys())
        importi = list(spese_per_categoria.values())

        # Crea il grafico a torta
        wedges, texts, autotexts = ax.pie(
            importi,
            labels=categorie,
            autopct=lambda pct: f'{pct:.1f}%' if pct > 5 else '',
            startangle=90,
            colors=self.colori[:len(categorie)],
            textprops={'fontsize': 10}
        )

        # Migliora l'aspetto delle etichette
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)

        # Aggiungi una legenda con gli importi
        legenda_labels = [f'{cat}: {imp:,.2f} €' for cat, imp in zip(categorie, importi)]
        ax.legend(legenda_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1),
                 fontsize=9)

        ax.set_title(titolo, fontsize=16, fontweight='bold', pad=20)

        fig.tight_layout()
        return fig

    def crea_grafico_barre(self, dati: Dict[str, float], titolo: str = "Confronto",
                          xlabel: str = "Categoria", ylabel: str = "Importo (€)",
                          dimensione: Tuple[int, int] = (12, 6),
                          orizzontale: bool = False) -> Figure:
        """
        Crea un grafico a barre

        Args:
            dati: Dizionario con i dati da visualizzare
            titolo: Titolo del grafico
            xlabel: Etichetta asse X
            ylabel: Etichetta asse Y
            dimensione: Tupla (larghezza, altezza) in pollici
            orizzontale: Se True, crea barre orizzontali

        Returns:
            Figure matplotlib
        """
        fig = Figure(figsize=dimensione, dpi=100)
        ax = fig.add_subplot(111)

        if not dati or sum(dati.values()) == 0:
            ax.text(0.5, 0.5, 'Nessun dato disponibile',
                   horizontalalignment='center',
                   verticalalignment='center',
                   fontsize=14,
                   color='gray')
            ax.set_title(titolo, fontsize=16, fontweight='bold', pad=20)
            return fig

        categorie = list(dati.keys())
        valori = list(dati.values())

        if orizzontale:
            bars = ax.barh(categorie, valori, color=self.colori[:len(categorie)])
            ax.set_xlabel(ylabel, fontsize=12)
            ax.set_ylabel(xlabel, fontsize=12)
        else:
            bars = ax.bar(categorie, valori, color=self.colori[:len(categorie)])
            ax.set_xlabel(xlabel, fontsize=12)
            ax.set_ylabel(ylabel, fontsize=12)
            # Ruota le etichette se ci sono molte categorie
            if len(categorie) > 5:
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # Aggiungi valori sopra le barre
        for i, (bar, valore) in enumerate(zip(bars, valori)):
            if orizzontale:
                ax.text(valore, i, f' {valore:,.2f}€',
                       va='center', fontsize=9)
            else:
                ax.text(i, valore, f'{valore:,.2f}€',
                       ha='center', va='bottom', fontsize=9)

        ax.set_title(titolo, fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)

        fig.tight_layout()
        return fig

    def crea_grafico_confronto_entrate_uscite(self, entrate: float, uscite: float,
                                              dimensione: Tuple[int, int] = (8, 6)) -> Figure:
        """
        Crea un grafico a barre per confrontare entrate e uscite

        Args:
            entrate: Totale entrate
            uscite: Totale uscite
            dimensione: Tupla (larghezza, altezza) in pollici

        Returns:
            Figure matplotlib
        """
        fig = Figure(figsize=dimensione, dpi=100)
        ax = fig.add_subplot(111)

        categorie = ['Entrate', 'Uscite', 'Saldo']
        valori = [entrate, uscite, entrate - uscite]
        colori_custom = ['#2ECC71', '#E74C3C', '#3498DB' if valori[2] >= 0 else '#E74C3C']

        bars = ax.bar(categorie, valori, color=colori_custom, width=0.6)

        # Aggiungi valori sopra le barre
        for i, (bar, valore) in enumerate(zip(bars, valori)):
            ax.text(i, valore if valore >= 0 else 0,
                   f'{valore:,.2f}€',
                   ha='center',
                   va='bottom' if valore >= 0 else 'top',
                   fontsize=12,
                   fontweight='bold')

        ax.set_ylabel('Importo (€)', fontsize=12)
        ax.set_title('Riepilogo Finanziario', fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, axis='y', alpha=0.3)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

        fig.tight_layout()
        return fig

    def crea_grafico_andamento_mensile(self, dati_mensili: Dict[str, Tuple[float, float]],
                                      dimensione: Tuple[int, int] = (12, 6)) -> Figure:
        """
        Crea un grafico dell'andamento mensile di entrate e uscite

        Args:
            dati_mensili: Dizionario {mese: (entrate, uscite)}
            dimensione: Tupla (larghezza, altezza) in pollici

        Returns:
            Figure matplotlib
        """
        fig = Figure(figsize=dimensione, dpi=100)
        ax = fig.add_subplot(111)

        if not dati_mensili:
            ax.text(0.5, 0.5, 'Nessun dato disponibile',
                   horizontalalignment='center',
                   verticalalignment='center',
                   fontsize=14,
                   color='gray')
            ax.set_title('Andamento Mensile', fontsize=16, fontweight='bold', pad=20)
            return fig

        mesi = list(dati_mensili.keys())
        entrate = [dati[0] for dati in dati_mensili.values()]
        uscite = [dati[1] for dati in dati_mensili.values()]
        saldi = [e - u for e, u in zip(entrate, uscite)]

        x = range(len(mesi))

        # Crea linee per entrate, uscite e saldo
        ax.plot(x, entrate, marker='o', label='Entrate', color='#2ECC71',
               linewidth=2, markersize=8)
        ax.plot(x, uscite, marker='s', label='Uscite', color='#E74C3C',
               linewidth=2, markersize=8)
        ax.plot(x, saldi, marker='^', label='Saldo', color='#3498DB',
               linewidth=2, markersize=8, linestyle='--')

        ax.set_xticks(x)
        ax.set_xticklabels(mesi, rotation=45, ha='right')
        ax.set_xlabel('Mese', fontsize=12)
        ax.set_ylabel('Importo (€)', fontsize=12)
        ax.set_title('Andamento Mensile', fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

        fig.tight_layout()
        return fig

    @staticmethod
    def incorpora_grafico_in_tkinter(figura: Figure, container) -> FigureCanvasTkAgg:
        """
        Incorpora un grafico matplotlib in un widget tkinter

        Args:
            figura: Figure matplotlib da incorporare
            container: Widget tkinter contenitore

        Returns:
            Canvas del grafico
        """
        canvas = FigureCanvasTkAgg(figura, master=container)
        canvas.draw()
        return canvas

    @staticmethod
    def salva_grafico(figura: Figure, percorso: str, dpi: int = 300) -> bool:
        """
        Salva un grafico su file

        Args:
            figura: Figure matplotlib da salvare
            percorso: Percorso del file di output
            dpi: Risoluzione in DPI

        Returns:
            True se il salvataggio è riuscito
        """
        try:
            figura.savefig(percorso, dpi=dpi, bbox_inches='tight')
            return True
        except Exception as e:
            print(f"Errore nel salvataggio del grafico: {e}")
            return False
