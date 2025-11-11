from tkinter import Tk, filedialog, messagebox
from models.model import Model
from models.histogram_model import HistogramModel
from models.threshold_model import ThresholdModel 
from models.brightness_model import BrightnessModel
from models.convolution_model import ConvolutionModel
from models.color_model import ColorModel 
from views.view import View
from views.threshold_window import ThresholdWindow 
from views.brightness_window import BrightnessWindow 
from views.split_channels_window import SplitChannelsWindow
from views.rotation_window import RotationWindow
import cv2 


class Controller:
    def __init__(self):
        self.root = Tk()
        self.root.title("PDI Studio - Sistema Interativo de Processamento de Imagens")
        self.root.geometry("1600x900")
        self.root.configure(bg="#2a2a2a")

        # Models
        self.model = Model()
        self.histogram_model = HistogramModel()
        self.threshold_model = ThresholdModel() 
        self.brightness_model = BrightnessModel()
        self.convolution_model = ConvolutionModel()
        self.color_model = ColorModel() 

        # Armazena as dimensões que os painéis de imagem devem ter
        self.original_panel_max_dims = {"width": 1, "height": 1} 
        self.processed_panel_max_dims = {"width": 1, "height": 1} 

        # View
        self.view = View(self.root, controller=self)
        
        # Estado para as janelas de filtro
        self.threshold_window_instance = None 
        self.brightness_window_instance = None 
        self.split_channels_window_instance = None
        self.rotation_window_instance = None
        
        self.update_histogram_display() 

    def on_original_panel_resize(self, width, height):
        self.original_panel_max_dims["width"] = width
        self.original_panel_max_dims["height"] = height
        self._display_images_in_panels() 

    def on_processed_panel_resize(self, width, height):
        self.processed_panel_max_dims["width"] = width
        self.processed_panel_max_dims["height"] = height
        self._display_images_in_panels() 

    def _display_images_in_panels(self):
        if self.model.original is None:
            self.view.display_new_image(None, None) 
            return

        # A Imagem Original (self.model.original) NUNCA muda
        resized_original_cv = self.model.resize_image_proportional(
            self.model.original, 
            self.original_panel_max_dims["width"], 
            self.original_panel_max_dims["height"]
        )
        tk_original = self.model.to_tk_image(resized_original_cv)

        # A Imagem Processada (self.model.image) é a que muda
        resized_processed_cv = self.model.resize_image_proportional(
            self.model.image, 
            self.processed_panel_max_dims["width"], 
            self.processed_panel_max_dims["height"]
        )
        tk_processed = self.model.to_tk_image(resized_processed_cv)

        self.view.display_new_image(tk_original, tk_processed)

    # ========== Métodos principais ==========
    def run(self):
        self.root.mainloop()

    def update_histogram_display(self):
        hist_data = self.histogram_model.calculate_histogram_data(self.model.image)
        self.view.control_panel.update_histogram(hist_data)

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Arquivos de imagem", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if path:
            self.model.load_image(path)
            self._display_images_in_panels() 
            self.view.log_action(f"Imagem carregada: {path}")
            self.update_histogram_display()

    def save_image(self):
        if self.model.image is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem processada para salvar.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", ".jpg"), ("BMP", ".bmp")]
        )
        if path:
            self.model.save_image(path) 
            self.view.log_action(f"Imagem salva em: {path}")

    def reset_image(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada para resetar.")
            return
        
        # O Reset agora funciona corretamente,
        # copiando a original (intocada) para a processada.
        self.model.reset_image() 
        self._display_images_in_panels() 
        self.view.log_action("Imagem resetada para o original.")
        self.update_histogram_display()

    # --- MÉTODOS DE ROTAÇÃO (EDITAR) ---
    def apply_rotate_clockwise(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return
        
        # Chama o método do modelo (que agora só mexe no self.image)
        self.model.rotate_image_clockwise() 
        self._display_images_in_panels() 
        self.view.log_action("Imagem rotacionada 90° (Horário).")
        self.update_histogram_display()

    def apply_rotate_counter_clockwise(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return
        
        # Chama o método do modelo (que agora só mexe no self.image)
        self.model.rotate_image_counter_clockwise() 
        self._display_images_in_panels() 
        self.view.log_action("Imagem rotacionada 90° (Anti-horário).")
        self.update_histogram_display()
        
    # --- MÉTODOS DE ROTAÇÃO LIVRE ---
    def open_rotation_window(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return
            
        if self.rotation_window_instance is None or not self.rotation_window_instance.window.winfo_exists():
            # A janela de preview opera na imagem processada atual
            image_for_rotation = self.model.image 
            self.rotation_window_instance = RotationWindow(self.root, self, image_for_rotation)
        else:
            self.rotation_window_instance.window.lift()

    def apply_rotation_preview(self, original_cv_image, angle):
        if original_cv_image is None:
            return None
        
        rotated_cv = self.model.apply_free_rotation(original_cv_image, angle)

        preview_max_width, preview_max_height = 450, 450
        resized_rotated_cv = self.model.resize_image_proportional(
            rotated_cv, preview_max_width, preview_max_height
        )
        
        if resized_rotated_cv is not None:
            return self.model.to_tk_image(resized_rotated_cv)
        return None

    def apply_final_rotation(self, angle):
        if self.model.original is None:
            return
        
        # --- CORREÇÃO PRINCIPAL ---
        # Aplica a rotação APENAS em self.model.image
        # self.model.original NÃO é modificado.
        self.model.image = self.model.apply_free_rotation(self.model.image, angle)

        self._display_images_in_panels()
        self.view.log_action(f"Rotação livre de {angle}° aplicada.")
        self.update_histogram_display()
        self.rotation_window_instance = None 

    def on_rotation_window_closed(self):
        self.rotation_window_instance = None
    # --- Fim Rotação Livre ---


    # --- MÉTODOS DE FILTROS BÁSICOS (Um clique) ---
    # --- TODOS FORAM ATUALIZADOS PARA USAR self.model.image ---

    def apply_gray(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return
        # Aplicar na imagem processada atual
        self.model.image = self.model.convert_to_gray(self.model.image) 
        self._display_images_in_panels() 
        self.view.log_action("Conversão para tons de cinza aplicada.")
        self.update_histogram_display()

    def apply_equalization(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return
        # Aplicar na imagem processada atual
        self.model.image = self.model.equalize_histogram(self.model.image) 
        self._display_images_in_panels() 
        self.view.log_action("Equalização de histograma aplicada.")
        self.update_histogram_display()

    def apply_blur(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return
        # Aplicar na imagem processada atual
        self.model.image = self.convolution_model.apply_blur(self.model.image)
        self._display_images_in_panels() 
        self.view.log_action("Filtro de Blur (Média) aplicado.")
        self.update_histogram_display()

    def apply_sharpen(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return
        # Aplicar na imagem processada atual
        self.model.image = self.convolution_model.apply_sharpen(self.model.image)
        self._display_images_in_panels() 
        self.view.log_action("Filtro de Nitidez (Sharpen) aplicado.")
        self.update_histogram_display()

    def apply_sobel(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return
        # Aplicar na imagem processada atual
        self.model.image = self.convolution_model.apply_sobel(self.model.image)
        self._display_images_in_panels() 
        self.view.log_action("Filtro de Detecção de Bordas (Sobel) aplicado.")
        self.update_histogram_display()

    def apply_otsu_threshold(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return
        # Aplicar na imagem processada atual
        self.model.image = self.threshold_model.apply_otsu_threshold(self.model.image)
        self._display_images_in_panels() 
        self.view.log_action("Limiarização de Otsu aplicada.")
        self.update_histogram_display()

    def apply_adaptive_threshold(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return
        # Aplicar na imagem processada atual
        self.model.image = self.threshold_model.apply_adaptive_threshold(self.model.image)
        self._display_images_in_panels() 
        self.view.log_action("Limiarização Adaptativa aplicada.")
        self.update_histogram_display()

    def apply_color_channel_blue(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return
        # Aplicar na imagem processada atual
        self.model.image = self.color_model.get_color_channel(self.model.image, 0)
        self._display_images_in_panels()
        self.view.log_action("Visualizando Canal Azul (B).")
        self.update_histogram_display()

    def apply_color_channel_green(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return
        # Aplicar na imagem processada atual
        self.model.image = self.color_model.get_color_channel(self.model.image, 1)
        self._display_images_in_panels()
        self.view.log_action("Visualizando Canal Verde (G).")
        self.update_histogram_display()
        
    def apply_color_channel_red(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return
        # Aplicar na imagem processada atual
        self.model.image = self.color_model.get_color_channel(self.model.image, 2)
        self._display_images_in_panels()
        self.view.log_action("Visualizando Canal Vermelho (R).")
        self.update_histogram_display()

    # --- MÉTODOS DE FILTROS AVANÇADOS (Janelas) ---
    # (Estes já funcionavam corretamente em self.model.image)
    
    def open_split_channels_window(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return
        if self.split_channels_window_instance is None or not self.split_channels_window_instance.window.winfo_exists():
            image_for_split = self.model.image 
            self.split_channels_window_instance = SplitChannelsWindow(self.root, self, image_for_split)
        else:
            self.split_channels_window_instance.window.lift()

    def get_split_channels_tk_image(self, image_cv):
        if image_cv is None:
            return None
        split_view_cv = self.color_model.get_split_channels_view(image_cv)
        preview_width, preview_height = 1350, 450
        resized_split_view_cv = self.model.resize_image_proportional(
            split_view_cv, preview_width, preview_height
        )
        if resized_split_view_cv is not None:
            return self.model.to_tk_image(resized_split_view_cv)
        return None

    def on_split_channels_window_closed(self):
        self.split_channels_window_instance = None
        
    def open_threshold_window(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return
        if self.threshold_window_instance is None or not self.threshold_window_instance.window.winfo_exists():
            image_for_threshold = self.model.image 
            self.threshold_window_instance = ThresholdWindow(self.root, self, image_for_threshold)
        else:
            self.threshold_window_instance.window.lift() 

    def apply_threshold_preview(self, original_cv_image, threshold_value):
        if original_cv_image is None:
            return None
        thresholded_cv = self.threshold_model.apply_threshold(original_cv_image, threshold_value)
        preview_max_width, preview_max_height = 450, 450
        resized_thresholded_cv = self.model.resize_image_proportional(
            thresholded_cv, preview_max_width, preview_max_height
        )
        if resized_thresholded_cv is not None:
            return self.model.to_tk_image(resized_thresholded_cv)
        return None

    def apply_final_threshold(self, final_threshold_value):
        if self.model.original is None:
            return
        final_thresholded_cv = self.threshold_model.apply_threshold(self.model.image, final_threshold_value)
        self.model.image = cv2.cvtColor(final_thresholded_cv, cv2.COLOR_GRAY2BGR) 
        self._display_images_in_panels()
        self.view.log_action(f"Limiarização global aplicada com valor: {final_threshold_value}.")
        self.update_histogram_display()
        self.threshold_window_instance = None 

    def on_threshold_window_closed(self):
        self.threshold_window_instance = None
    
    def open_brightness_window(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Carregando")
            return
        if self.brightness_window_instance is None or not self.brightness_window_instance.window.winfo_exists():
            image_for_brightness = self.model.image 
            self.brightness_window_instance = BrightnessWindow(self.root, self, image_for_brightness)
        else:
            self.brightness_window_instance.window.lift()

    def apply_brightness_preview(self, original_cv_image, alpha, beta):
        if original_cv_image is None:
            return None
        adjusted_cv = self.brightness_model.apply_brightness_contrast(original_cv_image, alpha, beta)
        preview_max_width, preview_max_height = 450, 450
        resized_adjusted_cv = self.model.resize_image_proportional(
            adjusted_cv, preview_max_width, preview_max_height
        )
        if resized_adjusted_cv is not None:
            return self.model.to_tk_image(resized_adjusted_cv)
        return None

    def apply_final_brightness(self, alpha, beta):
        if self.model.original is None:
            return
        final_adjusted_cv = self.brightness_model.apply_brightness_contrast(self.model.image, alpha, beta)
        self.model.image = final_adjusted_cv 
        self._display_images_in_panels()
        self.view.log_action(f"Brilho/Contraste aplicado (Alpha: {alpha:.1f}, Beta: {beta}).")
        self.update_histogram_display()
        self.brightness_window_instance = None 

    def on_brightness_window_closed(self):
        self.brightness_window_instance = None