import cv2
import numpy as np


# ---------------------------------
# Blur Detection
# ---------------------------------
def check_blur(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Cannot load image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    return {
        "blur_score": round(float(blur_score), 2),
        "is_blurry": blur_score < 10
    }


# ---------------------------------
# Brightness Detection
# ---------------------------------
def check_brightness(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Cannot load image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    brightness = gray.mean()

    return {
        "brightness": round(float(brightness), 2),
        "too_dark": brightness < 50,
        "too_bright": brightness > 210
    }


# ---------------------------------
# Glare Detection
# ---------------------------------
def check_glare(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Cannot load image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    glare_pixels = (gray > 240).sum()

    total_pixels = gray.shape[0] * gray.shape[1]

    glare_fraction = glare_pixels / total_pixels

    return {
        "glare_fraction": round(float(glare_fraction), 4),
        "has_glare": glare_fraction > 0.05
    }


# ---------------------------------
# ROI Detection
# ---------------------------------
def check_roi(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Cannot load image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binary threshold
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    white_pixels = cv2.countNonZero(binary)

    total_pixels = gray.shape[0] * gray.shape[1]

    roi_fraction = white_pixels / total_pixels

    return {
        "roi_fraction": round(float(roi_fraction), 4),
        "roi_complete": roi_fraction > 0.15
    }


# =================================
# MAIN PROGRAM
# =================================

if __name__ == "__main__":

    image_path = "images/sample.jpg"

    blur = check_blur(image_path)
    brightness = check_brightness(image_path)
    glare = check_glare(image_path)
    roi = check_roi(image_path)

    print("\n========== Fingerprint Quality Report ==========\n")

    # Blur
    print("1. Blur Detection")
    print("----------------------------")
    print("Blur Score :", blur["blur_score"])
    print("Status     :", "❌ Blurry" if blur["is_blurry"] else "✅ Sharp")

    print()

    # Brightness
    print("2. Brightness Detection")
    print("----------------------------")
    print("Brightness :", brightness["brightness"])

    if brightness["too_dark"]:
        print("Status     : ❌ Too Dark")
    elif brightness["too_bright"]:
        print("Status     : ❌ Too Bright")
    else:
        print("Status     : ✅ Good Brightness")

    print()

    # Glare
    print("3. Glare Detection")
    print("----------------------------")
    print("Glare Fraction :", glare["glare_fraction"])
    print("Status          :", "❌ Glare Detected" if glare["has_glare"] else "✅ No Glare")

    print()

    # ROI
    print("4. ROI Detection")
    print("----------------------------")
    print("ROI Fraction :", roi["roi_fraction"])
    print("Status       :", "✅ Finger Detected" if roi["roi_complete"] else "❌ Finger Too Small")

    print("\n===============================================\n")