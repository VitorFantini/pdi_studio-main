import cv2
import numpy as np

class ConvolutionModel:

    def apply_blur(self, image):
        """Aplica um filtro de média (blur) simples."""
        if image is None:
            return None
        
        # Usa um kernel de 5x5 para o blur
        blurred_image = cv2.blur(image, (5, 5))
        return blurred_image

    def apply_sharpen(self, image):
        """Aplica um filtro de nitidez (sharpen)."""
        if image is None:
            return None
        
        # Kernel de nitidez
        kernel = np.array([
            [ 0, -1,  0],
            [-1,  5, -1],
            [ 0, -1,  0]
        ])
        
        # cv2.filter2D aplica o kernel na imagem
        sharpened_image = cv2.filter2D(image, -1, kernel)
        return sharpened_image

    def apply_sobel(self, image):
        """Aplica o filtro de detecção de bordas de Sobel."""
        if image is None:
            return None

        # 1. Converter para tons de cinza (Sobel funciona melhor em 1 canal)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 2. Calcular os gradientes X e Y
        # Usamos CV_16S (inteiro de 16 bits) para evitar perda de dados nas bordas
        grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1, ksize=3)

        # 3. Converter de volta para 8-bit (unsigned)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)

        # 4. Combinar os gradientes X e Y
        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        
        # 5. Converter de volta para BGR para consistência com o resto do app
        sobel_bgr = cv2.cvtColor(grad, cv2.COLOR_GRAY2BGR)
        return sobel_bgr