import streamlit as st
from PIL import Image
import io

def resize_and_compress_image(input_image_path, output_path, target_size, size_unit):
    with Image.open(input_image_path) as img:
        # Convert RGBA to RGB
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Resize to a reasonable display size while maintaining aspect ratio
        max_width, max_height = 800, 800
        img.thumbnail((max_width, max_height))

        # Convert target size to bytes
        target_size_bytes = target_size * 1024 if size_unit == 'KB' else target_size * 1024 * 1024
        
        # Attempt to compress and save the image
        quality = 95
        img.save(output_path, "JPEG", quality=quality, optimize=True)
        
        # Check the resulting file size
        while os.path.getsize(output_path) > target_size_bytes and quality > 10:
            # Reduce the quality by 5 units and try again
            quality -= 5
            img.save(output_path, "JPEG", quality=quality, optimize=True)
    
    return output_path

def main():
    st.title("Image Compressor")
    
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        size_unit_option = st.selectbox("Select Size Unit", ("KB", "MB"))
        target_size = st.number_input(f"Target File Size in {size_unit_option}", min_value=0.1, step=0.1, format="%.1f")
        
        if st.button("Compress Image"):
            input_path = "temp_uploaded_image.jpg"
            output_path = "compressed_image.jpg"
            
            # Save the uploaded file
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                compressed_image_path = resize_and_compress_image(input_path, output_path, target_size, size_unit_option)
                st.success("Image compressed successfully!")
                st.download_button(
                    label="Download Compressed Image",
                    data=open(compressed_image_path, "rb").read(),
                    file_name="compressed_image.jpg",
                    mime="image/jpeg"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
