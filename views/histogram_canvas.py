import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HistogramCanvas:
    def __init__(self, root):
        """
        Cria um Canvas Tkinter gerenciado pelo Matplotlib.
        'root' deve ser o frame onde o gráfico será embutido.
        """
        
        # 1. Cria a Figura do Matplotlib (fundo escuro para combinar)
        self.figure = Figure(figsize=(3, 2), dpi=100, facecolor="#333")
        self.figure.subplots_adjust(left=0.15, right=0.95, bottom=0.2, top=0.9)

        # 2. Cria o 'eixo' (o gráfico em si)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("#222")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['top'].set_color('none')
        self.ax.spines['right'].set_color('none')
        self.ax.set_xlabel('Intensidade', color='white', fontsize=8)
        self.ax.set_ylabel('Nº Pixels', color='white', fontsize=8)
        self.ax.set_xlim([0, 256])

        # 3. Embutindo a figura no Tkinter (esta é a mágica)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas.draw()

    def plot_histogram(self, histogram_data):
        """
        Recebe os dados calculados pelo HistogramModel e plota no gráfico.
        'histogram_data' é a lista: [(hist, color), (hist, color), ...]
        """
        # 1. Limpa o gráfico anterior
        self.ax.clear()

        # 2. Redefine os limites e estilos (pois o clear() apaga tudo)
        self.ax.set_xlabel('Intensidade', color='white', fontsize=8)
        self.ax.set_ylabel('Nº Pixels', color='white', fontsize=8)
        self.ax.set_xlim([0, 256])
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        if not histogram_data:
            self.ax.text(0.5, 0.5, 'Sem dados', color='white', 
                         horizontalalignment='center', verticalalignment='center', 
                         transform=self.ax.transAxes)
            self.canvas.draw()
            return

        # 3. Plota os novos dados (B, G, R ou Cinza)
        for (hist_channel, color) in histogram_data:
            self.ax.plot(hist_channel, color=color, linewidth=1.0)

        # 4. Redesenha o canvas Tkinter
        self.canvas.draw()