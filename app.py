import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Kalkulator Kesehatan & BMI", page_icon="✨")

st.title("✨ Kalkulator Kesehatan & BMI")
st.write("Cek apakah berat badanmu ideal atau tidak!")

nama = st.text_input("Masukkan nama kamu:")
tinggi = st.number_input("Tinggi badan (cm):", min_value=50, max_value=250)
berat = st.number_input("Berat badan (kg):", min_value=10, max_value=300)
foto = st.camera_input("Ambil foto kamu:")

if st.button("Hitung BMI"):
    if tinggi > 0 and berat > 0:
        tinggi_meter = tinggi / 100
        bmi = berat / (tinggi_meter ** 2)

        # Tentukan kategori & nasehat
        if bmi < 18.5:
            kategori = "Kurus"
            nasihat = "Perbanyak asupan bergizi agar berat badan lebih seimbang."
        elif 18.5 <= bmi < 25:
            kategori = "Normal"
            nasihat = "Selamat! Berat badanmu ideal. Tetap jaga pola makan & olahraga."
        elif 25 <= bmi < 30:
            kategori = "Gemuk"
            nasihat = "Mulailah rutin olahraga dan kurangi makanan tinggi kalori."
        else:
            kategori = "Obesitas"
            nasihat = "Segera atur pola makan dan olahraga, konsultasikan ke dokter bila perlu."

        st.success(f"Halo {nama}, BMI kamu adalah **{bmi:.2f}** ({kategori})")
        st.info(nasihat)

        # Buat laporan gambar
        if foto:
            foto_img = Image.open(foto).resize((200, 200))
        else:
            foto_img = Image.new("RGB", (200, 200), color="gray")

        img = Image.new("RGB", (500, 400), color="white")
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        # Tempel foto
        img.paste(foto_img, (30, 100))

        # Tambah teks
        draw.text((250, 50), f"Nama: {nama}", fill="black", font=font)
        draw.text((250, 80), f"Tinggi: {tinggi} cm", fill="black", font=font)
        draw.text((250, 110), f"Berat: {berat} kg", fill="black", font=font)
        draw.text((250, 140), f"BMI: {bmi:.2f}", fill="black", font=font)
        draw.text((250, 170), f"Kategori: {kategori}", fill="red" if kategori != "Normal" else "green", font=font)
        draw.text((30, 320), f"Pesan: {nasihat}", fill="black", font=font)

        # Simpan ke buffer
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.image(img, caption="Laporan BMI")
        st.download_button(
            label="📥 Download Laporan PNG",
            data=byte_im,
            file_name=f"Laporan_BMI_{nama}.png",
            mime="image/png"
        )
    else:
        st.error("Isi data tinggi dan berat dengan benar.")
