import tkinter as tk
from tkinter import Scale, HORIZONTAL, Frame, Button

class ThresholdWindow:
    def __init__(self, master, controller, image_to_show):
        self.master = master
        self.controller = controller
        self.image_to_show = image_to_show # Imagem OpenCV que será exibida na janela

        self.window = tk.Toplevel(master)
        self.window.title("Ajuste de Limiarização")
        self.window.geometry("500x670") # Aumentei a altura para caber os botões
        self.window.resizable(False, False) 
        self.window.grab_set() 
        
        # --- MUDANÇA NA LÓGICA DO 'X' ---
        # Agora o 'X' chama _on_cancel (igual ao botão Cancelar)
        self.window.protocol("WM_DELETE_WINDOW", self._on_cancel) 
        
        self.window.configure(bg="#2a2a2a") 

        # Frame principal
        main_frame = tk.Frame(self.window, bg="#2a2a2a") 
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Slider para o valor do limiar
        self.threshold_label = tk.Label(
            main_frame, 
            text="Limiar: 125",
            bg="#2a2a2a",
            fg="white"
        )
        self.threshold_label.pack(pady=(0, 5))

        self.threshold_slider = Scale(
            main_frame,
            from_=0,
            to=255,
            orient=HORIZONTAL,
            length=400,
            command=self._on_slider_change,
            bg="#444",
            fg="white",
            troughcolor="#555",
            highlightthickness=0,
            relief=tk.FLAT,
            activebackground="#55aaff"
        )
        self.threshold_slider.set(125) 
        self.threshold_slider.pack(pady=5)

        # Label para exibir a imagem limiarizada
        self.image_label = tk.Label(
            main_frame, 
            bg="#222"
        )
        self.image_label.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # --- NOVO FRAME DE BOTÕES ---
        button_frame = Frame(main_frame, bg="#2a2a2a")
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        button_frame.columnconfigure(0, weight=1) # Faz o botão centralizar
        button_frame.columnconfigure(1, weight=1)

        self.cancel_button = Button(
            button_frame,
            text="Cancelar",
            bg="#555",
            fg="white",
            relief=tk.FLAT,
            highlightthickness=0,
            command=self._on_cancel # Chama a nova função de cancelar
        )
        self.cancel_button.grid(row=0, column=0, sticky=tk.E, padx=5)

        self.apply_button = Button(
            button_frame,
            text="Aplicar",
            bg="#007acc", # Cor de destaque
            fg="white",
            relief=tk.FLAT,
            highlightthickness=0,
            command=self._on_apply # Chama a nova função de aplicar
        )
        self.apply_button.grid(row=0, column=1, sticky=tk.W, padx=5)


        # Exibe a imagem inicial (com limiar 125)
        self.update_display_image(self.threshold_slider.get())

    def _on_slider_change(self, value):
        """Chamado quando o slider é movido."""
        threshold_value = int(value)
        self.threshold_label.config(text=f"Limiar: {threshold_value}")
        self.update_display_image(threshold_value)

    def update_display_image(self, threshold_value):
        """
        Pede ao controlador para aplicar o limiar e atualiza a imagem exibida.
        """
        if self.image_to_show is None:
            return

        tk_image = self.controller.apply_threshold_preview(self.image_to_show, threshold_value)
        
        if tk_image:
            self.image_label.config(image=tk_image)
            self.image_label.image = tk_image 
        else:
            self.image_label.config(image=None)
            self.image_label.image = None

    # --- NOVOS MÉTODOS PARA OS BOTÕES ---

    def _on_apply(self):
        """
        Lida com o clique no botão 'Aplicar'.
        Aplica o filtro na imagem principal e fecha a janela.
        """
        final_threshold_value = self.threshold_slider.get()
        # Notifica o controlador para aplicar este valor na imagem principal
        self.controller.apply_final_threshold(final_threshold_value)
        self.window.destroy() # Fecha a janela

    def _on_cancel(self):
        """
        Lida com o clique no botão 'Cancelar' ou no 'X' da janela.
        Apenas fecha a janela sem aplicar nada.
        """
        # Notifica o controlador que a janela foi fechada
        self.controller.on_threshold_window_closed()
        self.window.destroy() # Fecha a janela