import streamlit as st
from PIL import Image
import io

# Start the camera with an expander
with st.expander("Start Camera"):
    camera_image = st.camera_input("Camera")

if camera_image:
    # Create a Pillow instance
    img = Image.open(camera_image)

    # Convert the Pillow image to grayscale
    gray_img = img.convert("L")

    # Display the grayscale image
    st.image(gray_img, caption="Grayscale Image", use_column_width=True)

    # Save the grayscale image to an in-memory buffer
    buf = io.BytesIO()
    gray_img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    # Create a downloadable link for the image
    st.download_button(
        label="Download Grayscale Image",
        data=byte_im,
        file_name="gray_image.png",
        mime="image/png"
    )
