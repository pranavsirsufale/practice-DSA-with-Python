import cv2
import base64
import numpy as np

def get_fingerprint_template(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
        
    orb = cv2.ORB_create(nfeatures=500)
    keypoints, descriptors = orb.detectAndCompute(img, None)
    
    if descriptors is not None:
        template_bytes = descriptors.tobytes()
        template_string = base64.b64encode(template_bytes).decode('utf-8')
        return template_string
    return None

template = get_fingerprint_template("fingerprint_capture.bmp")
if template:
    print(template)