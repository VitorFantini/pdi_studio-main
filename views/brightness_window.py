import tkinter as tk
from tkinter import Scale, HORIZONTAL, Frame, Button, Label

class BrightnessWindow:
    def __init__(self, master, controller, image_to_show):
        self.master = master
        self.controller = controller
        self.image_to_show = image_to_show 

        self.window = tk.Toplevel(master)
        self.window.title("Ajuste de Brilho e Contraste")
        self.window.geometry("500x750") # Um pouco mais alta para 2 sliders
        self.window.resizable(False, False) 
        self.window.grab_set() 
        self.window.protocol("WM_DELETE_WINDOW", self._on_cancel) 
        self.window.configure(bg="#2a2a2a") 

        # Frame principal
        main_frame = Frame(self.window, bg="#2a2a2a") 
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- SLIDER 1: CONTRASTE (Alpha) ---
        self.contrast_label = Label(
            main_frame, 
            text="Contraste: 1.0",
            bg="#2a2a2a",
            fg="white"
        )
        self.contrast_label.pack(pady=(5, 5))

        self.contrast_slider = Scale(
            main_frame,
            from_=0.1, # Contraste mínimo
            to=3.0,    # Contraste máximo
            orient=HORIZONTAL,
            length=400,
            resolution=0.1, # Incremento
            command=self._on_slider_change,
            bg="#444", fg="white", troughcolor="#555",
            highlightthickness=0, relief=tk.FLAT, activebackground="#55aaff"
        )
        self.contrast_slider.set(1.0) # Valor inicial neutro
        self.contrast_slider.pack(pady=5)

        # --- SLIDER 2: BRILHO (Beta) ---
        self.brightness_label = Label(
            main_frame, 
            text="Brilho: 0",
            bg="#2a2a2a",
            fg="white"
        )
        self.brightness_label.pack(pady=(10, 5))

        self.brightness_slider = Scale(
            main_frame,
            from_=-100, # Brilho mínimo
            to=100,     # Brilho máximo
            orient=HORIZONTAL,
            length=400,
            command=self._on_slider_change,
            bg="#444", fg="white", troughcolor="#555",
            highlightthickness=0, relief=tk.FLAT, activebackground="#55aaff"
        )
        self.brightness_slider.set(0) # Valor inicial neutro
        self.brightness_slider.pack(pady=5)

        # Label para exibir a imagem
        self.image_label = Label(main_frame, bg="#222")
        self.image_label.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # --- FRAME DE BOTÕES ---
        button_frame = Frame(main_frame, bg="#2a2a2a")
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.cancel_button = Button(
            button_frame, text="Cancelar", bg="#555", fg="white",
            relief=tk.FLAT, highlightthickness=0, command=self._on_cancel
        )
        self.cancel_button.grid(row=0, column=0, sticky=tk.E, padx=5)

        self.apply_button = Button(
            button_frame, text="Aplicar", bg="#007acc", fg="white",
            relief=tk.FLAT, highlightthickness=0, command=self._on_apply
        )
        self.apply_button.grid(row=0, column=1, sticky=tk.W, padx=5)

        # Exibe a imagem inicial
        self.update_display_image()

    def _on_slider_change(self, value=None):
        """Chamado quando QUALQUER slider é movido."""
        # Atualiza os textos
        contrast_val = self.contrast_slider.get()
        brightness_val = self.brightness_slider.get()
        self.contrast_label.config(text=f"Contraste: {contrast_val:.1f}")
        self.brightness_label.config(text=f"Brilho: {brightness_val}")
        
        # Atualiza a pré-visualização
        self.update_display_image()

    def update_display_image(self):
        """ Pede ao controlador para aplicar o filtro de pré-visualização. """
        if self.image_to_show is None:
            return

        alpha = self.contrast_slider.get()
        beta = self.brightness_slider.get()

        tk_image = self.controller.apply_brightness_preview(self.image_to_show, alpha, beta)
        
        if tk_image:
            self.image_label.config(image=tk_image)
            self.image_label.image = tk_image 
        else:
            self.image_label.config(image=None)
            self.image_label.image = None

    def _on_apply(self):
        """ Aplica o filtro na imagem principal e fecha a janela. """
        alpha = self.contrast_slider.get()
        beta = self.brightness_slider.get()
        self.controller.apply_final_brightness(alpha, beta)
        self.window.destroy()

    def _on_cancel(self):
        """ Apenas fecha a janela sem aplicar nada. """
        self.controller.on_brightness_window_closed()
        self.window.destroy()