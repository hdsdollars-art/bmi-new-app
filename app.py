import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Kalkulator Kesehatan & BMI", page_icon="✨")

st.title("✨ Kalkulator Kesehatan & BMI")
st.write("Cek apakah berat badanmu ideal atau tidak!")

# Input data
nama = st.text_input("Masukkan nama kamu:")
tinggi = st.number_input("Tinggi badan (cm):", min_value=50, max_value=250)
berat = st.number_input("Berat badan (kg):", min_value=10, max_value=300)
foto = st.camera_input("📸 Ambil foto kamu:")

if st.button("Hitung BMI"):
    if tinggi > 0 and berat > 0:
        tinggi_meter = tinggi / 100
        bmi = berat / (tinggi_meter ** 2)

        # Tentukan kategori + warna + nasihat
        if bmi < 18.5:
            kategori = "Kurus"
            warna = "red"
            nasihat = "Perbanyak asupan bergizi agar berat badan lebih seimbang."
        elif 18.5 <= bmi < 25:
            kategori = "Normal"
            warna = "green"
            nasihat = "Selamat! Berat badanmu ideal. Tetap jaga pola makan & olahraga."
        elif 25 <= bmi < 30:
            kategori = "Gemuk"
            warna = "orange"
            nasihat = "Mulailah rutin olahraga dan kurangi makanan tinggi kalori."
        else:
            kategori = "Obesitas"
            warna = "red"
            nasihat = "Segera atur pola makan dan olahraga, konsultasikan ke dokter bila perlu."

        st.success(f"Halo {nama}, BMI kamu adalah **{bmi:.2f}** ({kategori})")
        st.info(nasihat)

        # --- Buat laporan PNG ---
        if foto:
            foto_img = Image.open(foto).resize((200, 200))
        else:
            foto_img = Image.new("RGB", (200, 200), color="gray")

        # Background
        img = Image.new("RGB", (600, 450), color="#E6F7FF")  # biru muda
        draw = ImageDraw.Draw(img)

        # Font (default PIL)
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()

        # Header / Judul
        draw.rectangle([(0, 0), (600, 60)], fill="#1890FF")  # biru tua header
        draw.text((200, 20), "LAPORAN BMI", fill="white", font=font_title)

        # Tempel foto
        img.paste(foto_img, (30, 100))

        # Info teks
        draw.text((260, 100), f"Nama     : {nama}", fill="black", font=font_text)
        draw.text((260, 130), f"Tinggi   : {tinggi} cm", fill="black", font=font_text)
        draw.text((260, 160), f"Berat    : {berat} kg", fill="black", font=font_text)
        draw.text((260, 190), f"BMI      : {bmi:.2f}", fill="black", font=font_text)

        # Kategori dengan warna
        draw.text((260, 220), f"Kategori : {kategori}", fill=warna, font=font_text)

        # Pesan
        draw.text((30, 330), f"Pesan: {nasihat}", fill="black", font=font_text)

        # Footer
        draw.rectangle([(0, 400), (600, 450)], fill="#1890FF")
        draw.text((200, 420), "✨ Tetap jaga kesehatanmu ✨", fill="white", font=font_text)

        # Simpan ke buffer
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Tampilkan preview + download
        st.image(img, caption="📋 Laporan BMI")
        st.download_button(
            label="📥 Download Laporan PNG",
            data=byte_im,
            file_name=f"Laporan_BMI_{nama}.png",
            mime="image/png"
        )

    else:
        st.error("Isi data tinggi dan berat dengan benar.")
