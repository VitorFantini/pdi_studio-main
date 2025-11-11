import tkinter as tk
from tkinter import Scale, HORIZONTAL, Frame, Button, Label

class RotationWindow:
    def __init__(self, master, controller, image_to_show):
        self.master = master
        self.controller = controller
        self.image_to_show = image_to_show 

        self.window = tk.Toplevel(master)
        self.window.title("Rotação Livre")
        self.window.geometry("500x670") 
        self.window.resizable(False, False) 
        self.window.grab_set() 
        self.window.protocol("WM_DELETE_WINDOW", self._on_cancel) 
        self.window.configure(bg="#2a2a2a") 

        # Frame principal
        main_frame = Frame(self.window, bg="#2a2a2a") 
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Slider para o ângulo
        self.angle_label = Label(
            main_frame, 
            text="Ângulo: 0°",
            bg="#2a2a2a",
            fg="white"
        )
        self.angle_label.pack(pady=(0, 5))

        self.angle_slider = Scale(
            main_frame,
            from_=-180,
            to=180,
            orient=HORIZONTAL,
            length=400,
            command=self._on_slider_change,
            resolution=1, # Incremento de 1 grau
            bg="#444",
            fg="white",
            troughcolor="#555",
            highlightthickness=0,
            relief=tk.FLAT,
            activebackground="#55aaff"
        )
        self.angle_slider.set(0) 
        self.angle_slider.pack(pady=5)

        # Label para exibir a imagem rotacionada
        self.image_label = Label(
            main_frame, 
            bg="#222"
        )
        self.image_label.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Frame de botões
        button_frame = Frame(main_frame, bg="#2a2a2a")
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        button_frame.columnconfigure(0, weight=1) 
        button_frame.columnconfigure(1, weight=1)

        self.cancel_button = Button(
            button_frame,
            text="Cancelar",
            bg="#555", fg="white", relief=tk.FLAT,
            highlightthickness=0, command=self._on_cancel
        )
        self.cancel_button.grid(row=0, column=0, sticky=tk.E, padx=5)

        self.apply_button = Button(
            button_frame,
            text="Aplicar",
            bg="#007acc", fg="white", relief=tk.FLAT,
            highlightthickness=0, command=self._on_apply
        )
        self.apply_button.grid(row=0, column=1, sticky=tk.W, padx=5)

        # Exibe a imagem inicial
        self.update_display_image(0)

    def _on_slider_change(self, value):
        angle = int(value)
        self.angle_label.config(text=f"Ângulo: {angle}°")
        self.update_display_image(angle)

    def update_display_image(self, angle):
        if self.image_to_show is None:
            return

        tk_image = self.controller.apply_rotation_preview(self.image_to_show, angle)
        
        if tk_image:
            self.image_label.config(image=tk_image)
            self.image_label.image = tk_image 
        else:
            self.image_label.config(image=None)
            self.image_label.image = None

    def _on_apply(self):
        final_angle = self.angle_slider.get()
        self.controller.apply_final_rotation(final_angle)
        self.window.destroy()

    def _on_cancel(self):
        self.controller.on_rotation_window_closed()
        self.window.destroy()