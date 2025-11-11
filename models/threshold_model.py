import cv2
import numpy as np

class ThresholdModel:
    def __init__(self):
        pass # Não precisamos de estado aqui

    def apply_threshold(self, image, threshold_value, threshold_type=cv2.THRESH_BINARY):
        """
        Aplica a limiarização global (usada pelo slider).
        """
        if image is None:
            return None

        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image
        
        ret_val, thresh_image = cv2.threshold(gray_image, threshold_value, 255, threshold_type)
        
        return thresh_image

    # --- NOVO MÉTODO: Limiarização de Otsu ---
    def apply_otsu_threshold(self, image):
        """
        Aplica a limiarização de Otsu, que encontra o limiar ideal automaticamente.
        """
        if image is None:
            return None
        
        # 1. Converter para tons de cinza
        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image
        
        # 2. Aplicar o threshold com a flag THRESH_OTSU
        # O valor 0 (primeiro argumento) é ignorado por causa da flag Otsu
        ret_val, thresh_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 3. Converter de volta para BGR para consistência
        return cv2.cvtColor(thresh_image, cv2.COLOR_GRAY2BGR)

    # --- NOVO MÉTODO: Limiarização Adaptativa ---
    def apply_adaptive_threshold(self, image):
        """
        Aplica a limiarização adaptativa, ideal para iluminação irregular.
        """
        if image is None:
            return None
        
        # 1. Converter para tons de cinza
        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image

        # 2. Aplicar o threshold adaptativo
        # cv2.ADAPTIVE_THRESH_MEAN_C: O limiar é a média da área do bloco (11x11).
        # C (2): Uma constante subtraída da média.
        adaptive_thresh_image = cv2.adaptiveThreshold(
            gray_image, 
            255, 
            cv2.ADAPTIVE_THRESH_MEAN_C, 
            cv2.THRESH_BINARY, 
            11, # Tamanho do bloco (block size), deve ser ímpar
            2   # Constante C
        )

        # 3. Converter de volta para BGR para consistência
        return cv2.cvtColor(adaptive_thresh_image, cv2.COLOR_GRAY2BGR)