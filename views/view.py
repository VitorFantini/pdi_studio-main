import tkinter as tk
from views.menu_bar import MenuBar
from views.image_panel import ImagePanel
from views.control_panel import ControlPanel

class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.menu = MenuBar(self.root, controller)
        self.root.config(menu=self.menu.menubar)

        self.control_panel = ControlPanel(self.root)
        self.control_panel.frame.pack(side="right", fill="y", padx=10, pady=10)

        # --- NOVOS PARÂMETROS NO ImagePanel ---
        # Passa um callback para o Controller que será chamado quando o painel for redimensionado
        self.original_panel = ImagePanel(self.root, title="Imagem Original", 
                                         on_resize_callback=self.controller.on_original_panel_resize)
        self.original_panel.frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        self.processed_panel = ImagePanel(self.root, title="Imagem Processada",
                                          on_resize_callback=self.controller.on_processed_panel_resize)
        self.processed_panel.frame.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

    def display_new_image(self, original_tk, processed_tk):
        self.original_panel.show_image(original_tk)
        self.processed_panel.show_image(processed_tk)

    def display_processed_image(self, processed_tk):
        self.processed_panel.show_image(processed_tk)

    def log_action(self, text):
        self.control_panel.add_log(text)