import cv2

image = cv2.imread("images/sample.jpg")

if image is None:
    print("Image not found!")
else:
    print("Image loaded successfully!")
    print("Image Shape:", image.shape)

    cv2.imshow("Fingerprint", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()