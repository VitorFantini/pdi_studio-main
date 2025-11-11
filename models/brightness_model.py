import cv2
import numpy as np

class BrightnessModel:
    
    def apply_brightness_contrast(self, image, alpha, beta):
        """
        Ajusta o brilho e contraste da imagem.
        alpha: Contraste (float, 1.0 é neutro)
        beta: Brilho (int, 0 é neutro)
        """
        if image is None:
            return None
        
        # A função convertScaleAbs aplica a fórmula: G(x,y) = alpha * F(x,y) + beta
        # np.clip garante que os valores permaneçam dentro de 0-255
        new_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        
        return new_image