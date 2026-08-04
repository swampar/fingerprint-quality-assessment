import cv2


# -----------------------------
# Blur Detection
# -----------------------------
def check_blur(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    return blur_score, blur_score >= 10


# -----------------------------
# Brightness Detection
# -----------------------------
def check_brightness(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    brightness = gray.mean()

    if brightness < 50:
        status = "Too Dark"
    elif brightness > 210:
        status = "Too Bright"
    else:
        status = "Good"

    return brightness, status


# -----------------------------
# Glare Detection
# -----------------------------
def check_glare(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    glare_pixels = (gray > 240).sum()
    total_pixels = gray.shape[0] * gray.shape[1]

    glare = glare_pixels / total_pixels

    return glare, glare <= 0.05


# -----------------------------
# ROI Detection
# -----------------------------
def check_roi(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    white_pixels = cv2.countNonZero(binary)
    total_pixels = gray.shape[0] * gray.shape[1]

    roi = white_pixels / total_pixels

    return roi, roi >= 0.15


# -----------------------------
# Ridge Clarity
# -----------------------------
def check_ridge_clarity(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150)

    edge_pixels = cv2.countNonZero(edges)
    total_pixels = gray.shape[0] * gray.shape[1]

    ridge = edge_pixels / total_pixels

    return ridge, ridge >= 0.03


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    image = "images/sample.jpg"

    blur_score, blur_ok = check_blur(image)
    brightness_score, brightness_status = check_brightness(image)
    glare_score, glare_ok = check_glare(image)
    roi_score, roi_ok = check_roi(image)
    ridge_score, ridge_ok = check_ridge_clarity(image)

    score = 0

    if blur_ok:
        score += 20

    if brightness_status == "Good":
        score += 20

    if glare_ok:
        score += 20

    if roi_ok:
        score += 20

    if ridge_ok:
        score += 20

    print("\n========== Fingerprint Quality Report ==========\n")

    print(f"Blur Score        : {blur_score:.2f}")
    print(f"Brightness        : {brightness_score:.2f}")
    print(f"Glare Fraction    : {glare_score:.4f}")
    print(f"ROI Fraction      : {roi_score:.4f}")
    print(f"Ridge Score       : {ridge_score:.4f}")

    print("\n--------------------------------------")

    print(f"Composite Score : {score}/100")

    if score >= 80:
        print("Final Result    : PASS")
    else:
        print("Final Result    : FAIL")