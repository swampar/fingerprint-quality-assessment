import cv2


# ---------------------------------
# Blur Detection
# ---------------------------------
def check_blur(image_path):
    """
    Check whether the image is blurry using Laplacian Variance.
    """

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
    """
    Check whether the image is too dark or too bright.
    """

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
    """
    Detect glare (overexposed white pixels).
    """

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


# =================================
# MAIN PROGRAM
# =================================
if __name__ == "__main__":

    image_path = "images/sample.jpg"

    # Run all quality checks
    blur_result = check_blur(image_path)
    brightness_result = check_brightness(image_path)
    glare_result = check_glare(image_path)

    # Display Report
    print("\n========== Fingerprint Quality Report ==========\n")

    # Blur
    print("1. Blur Detection")
    print("----------------------------")
    print(f"Blur Score : {blur_result['blur_score']}")

    if blur_result["is_blurry"]:
        print("Status     : ❌ Blurry")
    else:
        print("Status     : ✅ Sharp")

    print()

    # Brightness
    print("2. Brightness Detection")
    print("----------------------------")
    print(f"Brightness : {brightness_result['brightness']}")

    if brightness_result["too_dark"]:
        print("Status     : ❌ Too Dark")

    elif brightness_result["too_bright"]:
        print("Status     : ❌ Too Bright")

    else:
        print("Status     : ✅ Good Brightness")

    print()

    # Glare
    print("3. Glare Detection")
    print("----------------------------")
    print(f"Glare Fraction : {glare_result['glare_fraction']}")

    if glare_result["has_glare"]:
        print("Status         : ❌ Glare Detected")
    else:
        print("Status         : ✅ No Glare")

    print("\n===============================================\n")