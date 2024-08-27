import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import io


# Function to convert image to grayscale
def convert_to_grayscale(image):
    return image.convert("L")


# Function to convert image to green
def convert_to_green(image):
    rgb_image = image.convert("RGB")
    pixels = rgb_image.load()
    for i in range(rgb_image.width):
        for j in range(rgb_image.height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (0, g, 0)
    return rgb_image


# Function to apply a stylized filter (e.g., edge enhancement)
def apply_stylized_filter(image):
    return image.filter(ImageFilter.EDGE_ENHANCE)


# Function to apply a comic oil paint effect
def apply_comic_oil_paint(image):
    oil_paint_image = image.filter(ImageFilter.SMOOTH_MORE)  # Apply a smoothing filter
    oil_paint_image = oil_paint_image.filter(ImageFilter.CONTOUR)  # Add contour to simulate comic effect
    oil_paint_image = oil_paint_image.filter(ImageFilter.EDGE_ENHANCE)  # Enhance edges for more pronounced effect
    return oil_paint_image


# Function to apply a colored comic oil paint effect
def apply_colored_comic_oil_paint(image):
    # Convert to RGB if not already
    rgb_image = image.convert("RGB")

    # Apply a smoothing filter
    smoothed_image = rgb_image.filter(ImageFilter.SMOOTH_MORE)

    # Apply contour and edge enhancement
    contour_image = smoothed_image.filter(ImageFilter.CONTOUR)
    colored_comic_image = contour_image.filter(ImageFilter.EDGE_ENHANCE)

    # Enhance the colors to make them more vivid
    enhancer = ImageEnhance.Color(colored_comic_image)
    vivid_image = enhancer.enhance(2.0)  # Increase color saturation

    return vivid_image


# Start the camera with an expander
with st.expander("Start Camera"):
    camera_image = st.camera_input("Camera")

if camera_image:
    # Create a Pillow instance
    img = Image.open(camera_image)

    # Dropdown menu for color conversion or stylized filter
    conversion_option = st.selectbox(
        "Select image transformation",
        ["Grayscale", "Green", "Stylized Filter", "Comic Oil Paint", "Colored Comic Oil Paint"]
    )

    # Apply the selected transformation
    if conversion_option == "Grayscale":
        transformed_img = convert_to_grayscale(img)
    elif conversion_option == "Green":
        transformed_img = convert_to_green(img)
    elif conversion_option == "Stylized Filter":
        transformed_img = apply_stylized_filter(img)
    elif conversion_option == "Comic Oil Paint":
        transformed_img = apply_comic_oil_paint(img)
    elif conversion_option == "Colored Comic Oil Paint":
        transformed_img = apply_colored_comic_oil_paint(img)

    # Display the transformed image
    st.image(transformed_img, caption=f"{conversion_option} Image", use_column_width=True)

    # Save the transformed image to an in-memory buffer
    buf = io.BytesIO()
    transformed_img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    # Create a downloadable link for the image
    st.download_button(
        label=f"Download {conversion_option} Image",
        data=byte_im,
        file_name=f"{conversion_option.lower().replace(' ', '_')}_image.png",
        mime="image/png"
    )
