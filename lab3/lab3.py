import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def color_quantization_kmeans(rgb_img, k=8, seed=42):
    h, w, _ = rgb_img.shape
    pixels = rgb_img.reshape((-1, 3)).astype(np.float32)
    kmeans = KMeans(n_clusters=k, random_state=seed, n_init=10)
    labels = kmeans.fit_predict(pixels)
    centers = kmeans.cluster_centers_
    quant_pixels = centers[labels].reshape((h, w, 3)).astype(np.uint8)
    return quant_pixels


def enhance_contrast_brightness(rgb_img, alpha=1.3, beta=20):
    return cv2.convertScaleAbs(rgb_img, alpha=alpha, beta=beta)


def enhance_lightness_lab(rgb_img):
    lab = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    l_eq = cv2.equalizeHist(l)
    lab_eq = cv2.merge((l_eq, a, b))
    out = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2RGB)
    return out


def main():
    input_path = "image.jpg"
    k = 8
    alpha = 1.3
    beta = 20

    bgr = cv2.imread(input_path)
    if bgr is None:
        raise FileNotFoundError(input_path)

    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    reduced = color_quantization_kmeans(rgb, k=k)
    enhanced_rgb = enhance_contrast_brightness(reduced, alpha=alpha, beta=beta)
    enhanced_lab = enhance_lightness_lab(reduced)

    cv2.imwrite("out_color_reduced.png", cv2.cvtColor(reduced, cv2.COLOR_RGB2BGR))
    cv2.imwrite("out_enhanced_rgb.png", cv2.cvtColor(enhanced_rgb, cv2.COLOR_RGB2BGR))
    cv2.imwrite("out_enhanced_lab.png", cv2.cvtColor(enhanced_lab, cv2.COLOR_RGB2BGR))

    plt.figure(figsize=(14, 5))

    plt.subplot(1, 4, 1)
    plt.title("Original")
    plt.imshow(rgb)
    plt.axis("off")

    plt.subplot(1, 4, 2)
    plt.title(f"Color Reduced (K={k})")
    plt.imshow(reduced)
    plt.axis("off")

    plt.subplot(1, 4, 3)
    plt.title(f"Enhanced RGB")
    plt.imshow(enhanced_rgb)
    plt.axis("off")

    plt.subplot(1, 4, 4)
    plt.title("Enhanced LAB")
    plt.imshow(enhanced_lab)
    plt.axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()