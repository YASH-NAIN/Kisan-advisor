"""Classical image features: HSV colour histograms + simple texture stats."""
import numpy as np
from PIL import Image

def extract(img):
    """img: PIL image -> 1-D feature vector."""
    a = np.array(img.convert("RGB").resize((128, 128)))
    import cv2
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
    feats = []
    for ch, bins, rng in [(0, 16, 180), (1, 8, 256), (2, 8, 256)]:
        h = cv2.calcHist([hsv], [ch], None, [bins], [0, rng]).flatten()
        feats.extend(h / h.sum())
    g = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY).astype("float32")
    lap = cv2.Laplacian(g, cv2.CV_32F)
    gx, gy = cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1)
    feats += [lap.var() / 1000, np.abs(gx).mean() / 100, np.abs(gy).mean() / 100, g.std() / 100]
    # 4x4 grid mean colour (spatial layout of spots)
    for i in range(4):
        for j in range(4):
            blk = a[i*32:(i+1)*32, j*32:(j+1)*32].reshape(-1, 3).mean(0) / 255
            feats.extend(blk)
    return np.array(feats, dtype="float32")
