import tkinter as tk

class MenuBar:
    def __init__(self, root, controller):
        self.controller = controller
        self.menubar = tk.Menu(root)

        # --- Menu Arquivo ---
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Abrir", command=controller.open_image)
        file_menu.add_command(label="Salvar como...", command=controller.save_image)
        file_menu.add_command(label="Resetar Imagem", command=controller.reset_image) 
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=root.quit)
        self.menubar.add_cascade(label="Arquivo", menu=file_menu)

        # --- Menu: Editar (Rotação) ---
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        edit_menu.add_command(label="Rotacionar 90° (Horário)", command=controller.apply_rotate_clockwise)
        edit_menu.add_command(label="Rotacionar 90° (Anti-horário)", command=controller.apply_rotate_counter_clockwise)
        
        # --- NOVA OPÇÃO DE ROTAÇÃO LIVRE ---
        edit_menu.add_separator()
        edit_menu.add_command(label="Rotação Livre...", command=controller.open_rotation_window)
        
        self.menubar.add_cascade(label="Editar", menu=edit_menu)
        # --- Fim do Menu Editar ---

        # --- Menu: Filtros Básicos (Um clique) ---
        basic_filter_menu = tk.Menu(self.menubar, tearoff=0)
        
        basic_filter_menu.add_command(label="Converter para tons de cinza", command=controller.apply_gray)
        basic_filter_menu.add_command(label="Equalizar histograma", command=controller.apply_equalization)
        
        basic_filter_menu.add_separator()
        basic_filter_menu.add_command(label="Aplicar Blur (Média)", command=controller.apply_blur)
        basic_filter_menu.add_command(label="Aplicar Nitidez (Sharpen)", command=controller.apply_sharpen)
        basic_filter_menu.add_command(label="Detectar Bordas (Sobel)", command=controller.apply_sobel)
        
        # --- SUB-MENU: Canais de Cor (Visualização Isolada) ---
        basic_filter_menu.add_separator()
        
        color_channel_menu = tk.Menu(basic_filter_menu, tearoff=0)
        color_channel_menu.add_command(label="Visualizar Canal Azul", command=controller.apply_color_channel_blue)
        color_channel_menu.add_command(label="Visualizar Canal Verde", command=controller.apply_color_channel_green)
        color_channel_menu.add_command(label="Visualizar Canal Vermelho", command=controller.apply_color_channel_red)
        
        basic_filter_menu.add_cascade(label="Canais de Cor (Isolado)", menu=color_channel_menu)
        
        # --- OPÇÕES DE LIMIARIZAÇÃO BÁSICA ---
        basic_filter_menu.add_separator()
        basic_filter_menu.add_command(label="Limiarização (Otsu)", command=controller.apply_otsu_threshold)
        basic_filter_menu.add_command(label="Limiarização (Adaptativa)", command=controller.apply_adaptive_threshold)
        
        self.menubar.add_cascade(label="Filtros Básicos", menu=basic_filter_menu)

        # --- Menu: Filtros Avançados (Com Sliders ou Janelas Separadas) ---
        advanced_filter_menu = tk.Menu(self.menubar, tearoff=0)
        
        advanced_filter_menu.add_command(label="Limiarização (Global)...", command=controller.open_threshold_window) 
        advanced_filter_menu.add_command(label="Brilho e Contraste...", command=controller.open_brightness_window)
        
        advanced_filter_menu.add_separator()
        advanced_filter_menu.add_command(label="Dividir Canais (BGR Lado a Lado)...", command=controller.open_split_channels_window)
        
        self.menubar.add_cascade(label="Filtros Avançados", menu=advanced_filter_menu)