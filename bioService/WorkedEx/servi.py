from flask import Flask, request, jsonify
import struct, zlib, base64, math, ctypes, os
import cv2
import numpy as np
from skimage.morphology import skeletonize

app = Flask(__name__)

# -----------------------------
# 🔹 Device Setup (Futronic FS88)
# -----------------------------
workingDir = os.getcwd()
scanApi = ctypes.WinDLL(os.path.join(workingDir, "ftrScanAPI.dll"))
ftrApi = ctypes.WinDLL(os.path.join(workingDir, "FTRAPI.dll"))

successCode = 1

# -----------------------------
# 🔹 Template From Device
# -----------------------------
def getTemplateFromDevice():
    handleDevice = scanApi.ftrScanOpenDevice()
    if not handleDevice:
        return None, "deviceNotFound"

    width, height = 320, 480
    imageSize = width * height
    imageBuffer = ctypes.create_string_buffer(imageSize)

    result = scanApi.ftrScanGetFrame(ctypes.c_void_p(handleDevice), imageBuffer, None)

    if result == successCode:
        templateBuffer = ctypes.create_string_buffer(2048)
        templateSize = ctypes.c_int(0)

        res = ftrApi.ftrEnroll(
            ctypes.c_void_p(handleDevice),
            imageBuffer,
            templateBuffer,
            ctypes.byref(templateSize)
        )

        if res == 0:
            templateBase64 = base64.b64encode(templateBuffer[:templateSize.value]).decode()
            scanApi.ftrScanCloseDevice(ctypes.c_void_p(handleDevice))
            return templateBase64, None

    scanApi.ftrScanCloseDevice(ctypes.c_void_p(handleDevice))
    return None, "captureFailed"

# -----------------------------
# 🔹 Template From Image
# -----------------------------
def generateTemplateFromImage(imagePath):
    image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return None

    image = cv2.equalizeHist(image)
    image = cv2.GaussianBlur(image, (5, 5), 0)

    threshold = cv2.adaptiveThreshold(
        image, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    binary = threshold // 255
    skeleton = skeletonize(binary).astype(np.uint8)

    minutiaePoints = extractMinutiae(skeleton)
    minutiaePoints = removeBorderPoints(minutiaePoints, 10, skeleton.shape)
    minutiaePoints = minutiaePoints[:80]

    rawData = b''.join([struct.pack("HHB", x, y, t) for x, y, t in minutiaePoints])
    compressedData = zlib.compress(rawData)
    encodedTemplate = base64.b64encode(compressedData).decode()

    return encodedTemplate

# -----------------------------
# 🔹 Minutiae Functions
# -----------------------------
def extractMinutiae(skeleton):
    points = []
    rows, cols = skeleton.shape

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if skeleton[i, j] == 1:
                neighbors = [
                    skeleton[i-1,j-1], skeleton[i-1,j], skeleton[i-1,j+1],
                    skeleton[i,j+1], skeleton[i+1,j+1], skeleton[i+1,j],
                    skeleton[i+1,j-1], skeleton[i,j-1]
                ]

                transitions = sum((neighbors[k] == 0 and neighbors[(k+1) % 8] == 1) for k in range(8))

                if transitions == 1:
                    points.append((i, j, 1))
                elif transitions == 3:
                    points.append((i, j, 2))

    return points


def removeBorderPoints(points, margin, shape):
    rows, cols = shape
    return [(x, y, t) for x, y, t in points if margin < x < rows - margin and margin < y < cols - margin]

# -----------------------------
# 🔹 Template Matching
# -----------------------------
def decodeTemplate(base64Template):
    compressedData = base64.b64decode(base64Template)
    rawData = zlib.decompress(compressedData)

    points = []
    for i in range(0, len(rawData), 5):
        x, y, t = struct.unpack("HHB", rawData[i:i+5])
        points.append((x, y, t))

    return points


def matchTemplates(template1, template2, distanceThreshold=15):
    matched = 0
    usedIndexes = set()

    for p1 in template1:
        for i, p2 in enumerate(template2):
            if i in usedIndexes:
                continue
            if p1[2] != p2[2]:
                continue
            if math.dist(p1[:2], p2[:2]) < distanceThreshold:
                matched += 1
                usedIndexes.add(i)
                break

    score = (2 * matched) / (len(template1) + len(template2))
    return score, matched

# -----------------------------
# 🔹 API Routes
# -----------------------------

@app.route("/capture", methods=["GET"])
def capture():
    template, error = getTemplateFromDevice()
    if error:
        return jsonify({"error": error}), 500

    return jsonify({"template": template})


@app.route("/generateTemplateFromImage", methods=["POST"])
def generateTemplateFromImageRoute():
    file = request.files["image"]
    tempPath = "temp.bmp"
    file.save(tempPath)

    template = generateTemplateFromImage(tempPath)
    if not template:
        return jsonify({"error": "processingFailed"}), 500

    return jsonify({"template": template})


@app.route("/verify", methods=["POST"])
def verify():
    data = request.json

    dbTemplate = data.get("dbTemplate")
    source = data.get("source")

    if source == "device":
        liveTemplate, error = getTemplateFromDevice()
        if error:
            return jsonify({"error": error}), 500

    elif source == "image":
        imagePath = data.get("imagePath")
        liveTemplate = generateTemplateFromImage(imagePath)

    else:
        return jsonify({"error": "invalidSource"}), 400

    template1 = decodeTemplate(dbTemplate)
    template2 = decodeTemplate(liveTemplate)

    score, matchedPoints = matchTemplates(template1, template2)

    return jsonify({
        "matchedPoints": matchedPoints,
        "score": score,
        "isMatch": score > 0.6
    })


# -----------------------------
# 🔹 Run Service
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)