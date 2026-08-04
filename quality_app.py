import streamlit as st
from quality_assessment import (
    check_blur,
    check_brightness,
    check_glare,
    check_roi,
    check_ridge_clarity,
)
import tempfile

st.set_page_config(page_title="Fingerprint Quality Assessment")

st.title("Fingerprint Quality Assessment")

option = st.radio(
    "Choose Input Method",
    ["Upload Image", "Camera"]
)

if option == "Upload Image":
    uploaded_file = st.file_uploader(
        "Upload Fingerprint Image",
        type=["jpg", "jpeg", "png"]
    )
    camera_image = None

else:
    camera_image = st.camera_input("Capture Fingerprint")
    uploaded_file = None

if uploaded_file is not None or camera_image is not None:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:

        if uploaded_file is not None:
            tmp.write(uploaded_file.read())

        else:
            tmp.write(camera_image.getvalue())

        image_path = tmp.name

    st.image(image_path, caption="Uploaded Image", use_container_width=True)

    blur_score, blur_ok = check_blur(image_path)
    brightness_score, brightness_status = check_brightness(image_path)
    glare_score, glare_ok = check_glare(image_path)
    roi_score, roi_ok = check_roi(image_path)
    ridge_score, ridge_ok = check_ridge_clarity(image_path)

    st.subheader("Results")

    st.write(f"**Blur Score:** {blur_score:.2f}")
    st.write("✅ Sharp" if blur_ok else "❌ Blurry")

    st.write(f"**Brightness:** {brightness_score:.2f}")
    st.write(brightness_status)

    st.write(f"**Glare Fraction:** {glare_score:.4f}")
    st.write("✅ No Glare" if glare_ok else "❌ Glare Detected")

    st.write(f"**ROI Fraction:** {roi_score:.4f}")
    st.write("✅ Finger Detected" if roi_ok else "❌ Poor ROI")

    st.write(f"**Ridge Score:** {ridge_score:.4f}")
    st.write("✅ Clear Ridges" if ridge_ok else "❌ Poor Ridge Quality")