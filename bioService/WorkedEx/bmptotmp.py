import struct, zlib, base64
import cv2
import numpy as np
from skimage.morphology import skeletonize


img = cv2.imread("fingerprint_capture.bmp", cv2.IMREAD_GRAYSCALE)

if img is None:
    raise Exception("Image not found!")

img = cv2.equalizeHist(img)
img = cv2.GaussianBlur(img, (5, 5), 0)

thresh = cv2.adaptiveThreshold(
    img, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    11, 2
)

binary = thresh // 255
skeleton = skeletonize(binary).astype(np.uint8)


def getMinutiae(skel):
    minutiae = []
    rows, cols = skel.shape

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if skel[i, j] == 1:
                neighbors = [
                    skel[i-1, j-1], skel[i-1, j], skel[i-1, j+1],
                    skel[i, j+1], skel[i+1, j+1], skel[i+1, j],
                    skel[i+1, j-1], skel[i, j-1]
                ]

                transitions = sum(
                    (neighbors[k] == 0 and neighbors[(k+1) % 8] == 1)
                    for k in range(8)
                )

                if transitions == 1:
                    minutiae.append((i, j, 1))  # ending
                elif transitions == 3:
                    minutiae.append((i, j, 2))  # bifurcation

    return minutiae

minutiaePoints = getMinutiae(skeleton)

# -----------------------------
# Step 5: Remove Border Noise
# -----------------------------
def removeBorderPoints(points, margin, shape):
    filtered = []
    rows, cols = shape

    for (x, y, t) in points:
        if margin < x < rows - margin and margin < y < cols - margin:
            filtered.append((x, y, t))

    return filtered

minutiaePoints = removeBorderPoints(minutiaePoints, margin=10, shape=skeleton.shape)

# -----------------------------
# Step 6: Limit Points (IMPORTANT)
# -----------------------------
# Keep only top N points
MAX_POINTS = 80
minutiaePoints = minutiaePoints[:MAX_POINTS]

print(f"Final minutiae count: {len(minutiaePoints)}")

# -----------------------------
# Step 7: Save Binary Template
# -----------------------------
with open("fingerprint_template.bin", "wb") as f:
    for (x, y, t) in minutiaePoints:
        f.write(struct.pack("HHB", x, y, t))

# -----------------------------
# Step 8: Compress Template
# -----------------------------
with open("fingerprint_template.bin", "rb") as f:
    raw_data = f.read()

compressed_data = zlib.compress(raw_data)

with open("fingerprint_template_compressed.bin", "wb") as f:
    f.write(compressed_data)

# -----------------------------
# Step 9: Convert to Base64 (for DB storage)
# -----------------------------
encoded = base64.b64encode(compressed_data).decode()

with open("fingerprint_template_base64.txt", "w") as f:
    f.write(encoded)

print("Template saved successfully!")