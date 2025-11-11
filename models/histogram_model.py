import cv2
import numpy as np

class HistogramModel:

    def calculate_histogram_data(self, image):
        """
        Calcula os dados do histograma para uma imagem (que pode ser BGR ou Cinza).
        Retorna uma lista de tuplas: (canal, dados_do_histograma, cor_do_grafico)
        """
        if image is None:
            return []

        if len(image.shape) == 2:
            # 1. Imagem em Tons de Cinza
            hist = cv2.calcHist([image], [0], None, [256], [0, 256])
            return [(hist, 'gray')]
        
        elif len(image.shape) == 3:
            # 2. Imagem Colorida (BGR)
            colors = ('b', 'g', 'r')
            results = []
            
            for i, color in enumerate(colors):
                # Calcula o histograma para o canal B, G e R
                hist = cv2.calcHist([image], [i], None, [256], [0, 256])
                results.append((hist, color))
            
            return results
        
        return []