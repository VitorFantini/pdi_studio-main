import cv2
from PIL import Image, ImageTk
import numpy as np

class Model:
    def __init__(self):
        self.image = None
        self.original = None

    def load_image(self, path):
        self.image = cv2.imread(path)
        self.original = self.image.copy()

    def save_image(self, path):
        if self.image is not None:
            cv2.imwrite(path, self.image)

    def reset_image(self):
        """
        Reseta a imagem processada (self.image) de volta para a
        imagem original (self.original), que nunca deve ser modificada.
        """
        if self.original is not None:
            self.image = self.original.copy()
            return self.image 

    def resize_image_proportional(self, cv_image, max_width, max_height):
        if cv_image is None:
            return None

        h, w = cv_image.shape[:2]
        
        if w <= max_width and h <= max_height:
            return cv_image

        ratio_w = max_width / w
        ratio_h = max_height / h
        ratio = min(ratio_w, ratio_h)
        
        new_w = int(w * ratio)
        new_h = int(h * ratio)
        
        return cv2.resize(cv_image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # ========== Operações de PDI ==========
    
    def convert_to_gray(self, image_to_process):
        if image_to_process is None:
            return None
        if len(image_to_process.shape) == 2:
            return cv2.cvtColor(image_to_process, cv2.COLOR_GRAY2BGR)
        gray = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY) 
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def equalize_histogram(self, image_to_process):
        if image_to_process is None:
            return None
        if len(image_to_process.shape) == 3:
            gray = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY)
        else:
            gray = image_to_process
        equalized = cv2.equalizeHist(gray)
        return cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)

    # ========== Conversão ==========
    def to_tk_image(self, cv_image):
        if cv_image is None:
            return None
        if len(cv_image.shape) == 2:
             cv_image = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2BGR)
        rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        return ImageTk.PhotoImage(img)

    # --- MÉTODOS DE ROTAÇÃO GEOMÉTRICA (CORRIGIDOS) ---
    def rotate_image_clockwise(self):
        """Rotaciona APENAS self.image em 90 graus (horário)."""
        if self.image is None:
            return
        # self.original NÃO é modificado
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)

    def rotate_image_counter_clockwise(self):
        """Rotaciona APENAS self.image em 90 graus (anti-horário)."""
        if self.image is None:
            return
        # self.original NÃO é modificado
        self.image = cv2.rotate(self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # --- MÉTODO: Rotação Livre (Helper) ---
    def apply_free_rotation(self, image_to_rotate, angle):
        """
        Rotaciona uma imagem por um ângulo livre.
        Esta função NÃO modifica o estado do modelo (self.image),
        ela apenas retorna a imagem rotacionada.
        """
        if image_to_rotate is None:
            return None
        
        (h, w) = image_to_rotate.shape[:2]
        (cX, cY) = (w // 2, h // 2)

        M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
        
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))

        M[0, 2] += (new_w / 2) - cX
        M[1, 2] += (new_h / 2) - cY

        rotated_image = cv2.warpAffine(
            image_to_rotate, 
            M, 
            (new_w, new_h), 
            borderValue=(0, 0, 0)
        )
        
        return rotated_image