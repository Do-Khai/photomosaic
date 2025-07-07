import streamlit as st
from PIL import Image
from io import BytesIO
from photomosaic import generate_photomosaic

st.title("📸 Photomosaic")

input_img = st.file_uploader("Em upload ảnh gốc ở đây nhé", type=["jpg", "jpeg", "png"])
pool_imgs = st.file_uploader("Em upload ảnh con ở đây nhé, em có bấm Upload rồi bôi đen kéo thả nhé", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
cell_size = st.slider("Em chọn kích cỡ ảnh của mỗi ảnh con trong ảnh gốc nhé", min_value=5, max_value=1000, value=25)

if st.button("Em bấm vào đây để tạo ảnh nè"):
    if input_img and pool_imgs:
        input_pil = Image.open(input_img).convert("RGB")
        st.image(input_pil, caption="Original Image", use_column_width=True)

        with st.spinner("Generating photomosaic..."):
            mosaic_img = generate_photomosaic(input_pil, pool_imgs, cell_size)
            buf = BytesIO()
            mosaic_img.save(buf, format="JPEG")
            byte_im = buf.getvalue()

        st.image(mosaic_img, caption="Kết quả của em nè", use_column_width=True)
        st.download_button("Download Result", data=byte_im, file_name="output.jpg", mime="image/jpeg")
    else:
        st.warning("Please upload both an input image and multiple mosaic tile images.")
