import tkinter as tk
from tkinter import scrolledtext
from views.histogram_canvas import HistogramCanvas # Importa o novo canvas

class ControlPanel:
    def __init__(self, root):
        self.frame = tk.Frame(root, bg="#333", width=300) # Aumentei a largura
        self.frame.pack_propagate(False)

        # --- 1. Histórico de Ações ---
        tk.Label(self.frame, text="Histórico de Ações", fg="white", bg="#333").pack(pady=5)
        self.log_area = scrolledtext.ScrolledText(self.frame, height=15, bg="#111", fg="white", width=38)
        self.log_area.pack(padx=5, pady=5)

        # --- 2. Canvas do Histograma ---
        tk.Label(self.frame, text="Histograma (Processada)", fg="white", bg="#333").pack(pady=(10, 5))
        
        # Cria um frame para conter o gráfico
        hist_frame = tk.Frame(self.frame, bg="#333", height=250)
        hist_frame.pack_propagate(False)
        hist_frame.pack(fill=tk.X, padx=5, pady=5)

        # Instancia o nosso novo HistogramCanvas dentro do frame
        self.histogram_canvas = HistogramCanvas(hist_frame)


    def add_log(self, text):
        self.log_area.insert(tk.END, f"> {text}\n")
        self.log_area.see(tk.END)
    
    def update_histogram(self, histogram_data):
        """Método de atalho para atualizar o gráfico."""
        self.histogram_canvas.plot_histogram(histogram_data)