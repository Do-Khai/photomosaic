import cv2
import numpy as np
from PIL import Image

def get_images(files, cell_size):
    result = []
    images = []
    for file in files:
        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        image = cv2.resize(image, (cell_size, cell_size))
        avg_color = np.mean(image, axis=(0, 1))
        result.append(avg_color)
        images.append(image)
    return images, result

def generate_photomosaic(input_pil_image, pool_images_files, cell_size):
    image_np = np.array(input_pil_image)
    height, width, _ = image_np.shape
    num_cols = width // cell_size
    num_rows = height // cell_size

    pool_images, sub_image_avg_colors = get_images(pool_images_files, cell_size)
    output_image = np.zeros((num_rows * cell_size, num_cols * cell_size, 3), dtype=np.uint8)

    for i in range(num_cols):
        for j in range(num_rows):
            sub_image = image_np[j*cell_size:(j+1)*cell_size, i*cell_size:(i+1)*cell_size, :]
            avg_color = np.mean(sub_image, axis=(0, 1))
            result = np.sqrt(np.sum((avg_color - sub_image_avg_colors) ** 2, axis=1))
            idx = np.argmin(result)
            output_image[j*cell_size:(j+1)*cell_size, i*cell_size:(i+1)*cell_size, :] = pool_images[idx]

    return Image.fromarray(output_image)
