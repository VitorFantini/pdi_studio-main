import tkinter as tk
from tkinter import Label

class ImagePanel:
    def __init__(self, root, title, on_resize_callback=None): # Adicionado callback
        self.frame = tk.Frame(root, bg="#222", bd=2, relief="sunken")

        self.title_label = Label(self.frame, text=title, bg="#444", fg="white", height=1)
        self.title_label.pack(side="top", fill="x")

        self.image_label = Label(self.frame, bg="#222")
        self.image_label.pack(fill="both", expand=True)
        
        self.on_resize_callback = on_resize_callback

        # --- NOVA LÓGICA DE BIND PARA REDIMENSIONAMENTO ---
        # Vincula o evento de configuração (redimensionamento) do frame à função _on_frame_resize
        self.frame.bind("<Configure>", self._on_frame_resize)
        self._current_width = 0
        self._current_height = 0

    def _on_frame_resize(self, event):
        """
        Método chamado quando o frame do ImagePanel é redimensionado.
        Notifica o callback (geralmente no Controller) se o tamanho mudou.
        """
        # Verifica se as dimensões realmente mudaram para evitar chamadas desnecessárias
        if event.width != self._current_width or event.height != self._current_height:
            self._current_width = event.width
            self._current_height = event.height
            if self.on_resize_callback:
                # Chama o callback, passando o novo tamanho disponível para a imagem
                # Subtrai um pouco para dar margem ou considerar o título
                self.on_resize_callback(self._current_width - 10, self._current_height - 30)

    def show_image(self, image):
        if image:
            self.image_label.config(image=image)
            self.image_label.image = image  # mantém referência
        else:
            self.image_label.config(image=None)
            self.image_label.image = None