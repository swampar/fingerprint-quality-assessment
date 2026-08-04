import cv2

def check_blur(image_path):
    image = cv2.imread(image_path)

    if image is None:
        print("Image not found!")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    print(f"Blur Score: {blur_score:.2f}")

    if blur_score < 10:
        print("❌ Image is Blurry")
    else:
        print("✅ Image is Sharp")


check_blur("images/sample.jpg")