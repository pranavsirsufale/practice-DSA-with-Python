import struct
import math

def loadTemplate(filePath):
    points = []

    with open(filePath, "rb") as f:
        data = f.read()

        for i in range(0, len(data), 5):
            x, y, t = struct.unpack("HHB", data[i:i+5])
            points.append((x, y, t))

    return points

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def matchTemplates(template1, template2, distThresh=15):
    matched = 0
    used = set()

    for p1 in template1:
        for i, p2 in enumerate(template2):
            if i in used:
                continue

            # Match type (ending/bifurcation)
            if p1[2] != p2[2]:
                continue

            # Distance check
            if distance(p1, p2) < distThresh:
                matched += 1
                used.add(i)
                break

    return matched

def computeScore(matched, total1, total2):
    return (2 * matched) / (total1 + total2)

template1 = loadTemplate("fingerprint_template1.bin")
template2 = loadTemplate("fingerprint_template2.bin")

matchedPoints = matchTemplates(template1, template2)

score = computeScore(
    matchedPoints,
    len(template1),
    len(template2)
)

print(f"Matched Points: {matchedPoints}")
print(f"Similarity Score: {(score * 100):.2f}%")


THRESHOLD = 0.6  # tune this

if score > THRESHOLD:
    print("✅ MATCH")
else:
    print("❌ NOT MATCH")