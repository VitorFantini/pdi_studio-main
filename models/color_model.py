import cv2
import numpy as np

class ColorModel:

    def get_color_channel(self, image, channel_index):
        """
        Isola um canal de cor (B=0, G=1, R=2).
        Retorna uma imagem BGR completa, mas apenas com o canal solicitado.
        """
        if image is None or len(image.shape) < 3:
            return image # Retorna a imagem como está se não for colorida

        # Cria uma imagem preta com as mesmas dimensões
        zeros = np.zeros(image.shape[:2], dtype="uint8")
        
        # Separa os canais B, G, R
        (B, G, R) = cv2.split(image)
        
        if channel_index == 0: # Azul
            return cv2.merge([B, zeros, zeros])
        elif channel_index == 1: # Verde
            return cv2.merge([zeros, G, zeros])
        elif channel_index == 2: # Vermelho
            return cv2.merge([zeros, zeros, R])
        else:
            return image # Caso de índice inválido

    def get_split_channels_view(self, image):
        """
        Divide os canais e os retorna como três imagens COLORIDAS
        combinadas lado a lado em uma única imagem BGR.
        """
        if image is None or len(image.shape) < 3:
            return image

        # 1. Cria uma imagem preta com as mesmas dimensões
        h, w = image.shape[:2]
        zeros = np.zeros((h, w), dtype="uint8")
        
        # 2. Separa os canais B, G, R
        (B, G, R) = cv2.split(image)
        
        # 3. Cria as 3 imagens BGR isoladas (ESTA É A CORREÇÃO)
        B_img = cv2.merge([B, zeros, zeros])
        G_img = cv2.merge([zeros, G, zeros])
        R_img = cv2.merge([zeros, zeros, R])
        
        # 4. Adiciona rótulos (como antes)
        cv2.putText(B_img, 'Azul (B)', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 100), 2)
        cv2.putText(G_img, 'Verde (G)', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 100), 2)
        cv2.putText(R_img, 'Red (R)', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 255), 2)

        # 5. Empilha as imagens horizontalmente
        split_view = np.hstack([B_img, G_img, R_img])
        
        return split_view