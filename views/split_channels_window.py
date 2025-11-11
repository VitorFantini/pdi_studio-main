import tkinter as tk
from tkinter import Frame, Label
from PIL import ImageTk, Image

class SplitChannelsWindow:
    def __init__(self, master, controller, image_to_show):
        self.master = master
        self.controller = controller
        self.image_to_show = image_to_show # A imagem BGR que será exibida

        self.window = tk.Toplevel(master)
        self.window.title("Visualização de Canais BGR Separados")
        
        # O tamanho da janela pode ser dinâmico ou fixo, vamos começar fixo
        # E.g., para uma imagem de 450px de largura, 3 canais = 1350px de largura + margens
        # Altura: 450px + margens
        self.window.geometry("1400x550") 
        self.window.resizable(False, False) 
        self.window.grab_set() 
        self.window.protocol("WM_DELETE_WINDOW", self._on_closing) # Apenas fecha a janela

        # Estilo da janela
        self.window.configure(bg="#2a2a2a") 

        # Frame principal
        main_frame = Frame(self.window, bg="#2a2a2a") 
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Label para exibir a imagem combinada dos canais
        self.image_label = Label(main_frame, bg="#222") # Cor de fundo igual aos painéis
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # Atualiza a imagem imediatamente
        self._display_split_channels()

    def _display_split_channels(self):
        """
        Pede ao controlador para gerar a imagem combinada dos canais 
        e a exibe na label.
        """
        if self.image_to_show is None:
            return

        # O controlador chama o ColorModel e converte para Tkinter
        tk_image = self.controller.get_split_channels_tk_image(self.image_to_show)
        
        if tk_image:
            self.image_label.config(image=tk_image)
            self.image_label.image = tk_image 
        else:
            self.image_label.config(image=None)
            self.image_label.image = None

    def _on_closing(self):
        """
        Lida com o fechamento da janela.
        """
        # Notifica o controlador que a janela foi fechada
        self.controller.on_split_channels_window_closed()
        self.window.destroy()