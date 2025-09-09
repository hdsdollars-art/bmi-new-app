import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="✨ Kalkulator Kesehatan & BMI", page_icon="💪")

st.title("✨ Kalkulator Kesehatan & BMI")

# Input data pengguna
nama = st.text_input("Masukkan nama kamu:")
usia = st.number_input("Usia:", min_value=5, max_value=120, step=1)
gender = st.selectbox("Jenis Kelamin:", ["Laki-laki", "Perempuan"])
tinggi = st.number_input("Tinggi badan (cm):", min_value=50, max_value=250)
berat = st.number_input("Berat badan (kg):", min_value=10, max_value=300)
aktivitas = st.selectbox(
    "Tingkat Aktivitas Harian:",
    ["Sedentary (minim olahraga)", "Ringan", "Sedang", "Berat", "Sangat Berat"]
)

foto = st.camera_input("📸 Ambil foto kamu:")

# Hitung BMI + BMR + TDEE
if st.button("Hitung BMI & Kalori"):
    if tinggi > 0 and berat > 0 and usia > 0:
        tinggi_meter = tinggi / 100
        bmi = berat / (tinggi_meter ** 2)

        # Kategori
        if bmi < 18.5:
            kategori = "Kurus ❌"
            warna = "red"
            nasehat = "Perbanyak makanan bergizi, tidur cukup, dan olahraga ringan."
            makanan = "🍗 Daging ayam, 🥛 susu, 🥑 alpukat, 🥜 kacang-kacangan"
            olahraga = "🏋️ Latihan beban ringan, yoga"
        elif 18.5 <= bmi < 25:
            kategori = "Normal ✅"
            warna = "green"
            nasehat = "Pertahankan pola makan sehat dan olahraga teratur."
            makanan = "🥗 Sayur segar, 🍎 buah, 🍚 nasi merah, 🐟 ikan"
            olahraga = "🏃 Jogging, 🚴 bersepeda, 🏊 berenang"
        elif 25 <= bmi < 30:
            kategori = "Gemuk ⚠️"
            warna = "orange"
            nasehat = "Kurangi makanan berlemak, perbanyak aktivitas fisik."
            makanan = "🥦 Sayuran hijau, 🍊 buah rendah kalori, 🍵 teh hijau"
            olahraga = "🏃 Jalan cepat, aerobik, skipping"
        else:
            kategori = "Obesitas ❌"
            warna = "red"
            nasehat = "Segera perhatikan pola makan & konsultasi ke dokter."
            makanan = "🥗 Salad, 🍵 sup, 🥒 timun, 🍊 jeruk"
            olahraga = "🚶 Jalan kaki rutin, 🧘 yoga, 🏊 renang ringan"

        st.markdown(f"<h3 style='color:{warna}'>Kategori: {kategori}</h3>", unsafe_allow_html=True)
        st.info(f"💡 Nasehat: {nasehat}")
        st.write(f"🍴 Rekomendasi makanan: {makanan}")
        st.write(f"🤸 Rekomendasi olahraga: {olahraga}")

        # Berat ideal
        ideal_min = 18.5 * (tinggi_meter ** 2)
        ideal_max = 24.9 * (tinggi_meter ** 2)
        st.write(f"📊 Berat ideal untuk tinggi kamu: **{ideal_min:.1f} – {ideal_max:.1f} kg**")

        # Hitung BMR
        if gender == "Laki-laki":
            bmr = 88.362 + (13.397 * berat) + (4.799 * tinggi) - (5.677 * usia)
        else:
            bmr = 447.593 + (9.247 * berat) + (3.098 * tinggi) - (4.330 * usia)

        faktor = {
            "Sedentary (minim olahraga)": 1.2,
            "Ringan": 1.375,
            "Sedang": 1.55,
            "Berat": 1.725,
            "Sangat Berat": 1.9
        }
        tdee = bmr * faktor[aktivitas]
        st.write(f"🔥 Kebutuhan kalori harian (TDEE): **{tdee:.0f} kcal**")

        # --- Buat laporan PNG ---
        if foto:
            foto_img = Image.open(foto).resize((200, 200))
        else:
            foto_img = Image.new("RGB", (200, 200), color="gray")

        img = Image.new("RGB", (650, 500), color="#E6F7FF")
        draw = ImageDraw.Draw(img)

        font = ImageFont.load_default()

        # Header
        draw.rectangle([(0, 0), (650, 60)], fill="#1890FF")
        draw.text((250, 20), "LAPORAN BMI & KALORI", fill="white", font=font)

        # Foto
        img.paste(foto_img, (30, 100))

        # Info teks
        draw.text((260, 100), f"Nama   : {nama}", fill="black", font=font)
        draw.text((260, 130), f"Usia   : {usia} tahun", fill="black", font=font)
        draw.text((260, 160), f"Gender : {gender}", fill="black", font=font)
        draw.text((260, 190), f"Tinggi : {tinggi} cm", fill="black", font=font)
        draw.text((260, 220), f"Berat  : {berat} kg", fill="black", font=font)
        draw.text((260, 250), f"BMI    : {bmi:.2f} ({kategori})", fill=warna, font=font)
        draw.text((260, 280), f"Ideal  : {ideal_min:.1f}-{ideal_max:.1f} kg", fill="black", font=font)
        draw.text((260, 310), f"TDEE   : {tdee:.0f} kcal", fill="black", font=font)

        # Pesan
        draw.text((30, 350), f"Nasehat: {nasehat}", fill="black", font=font)

        # Footer
        draw.rectangle([(0, 460), (650, 500)], fill="#1890FF")
        draw.text((200, 470), "✨ Tetap jaga kesehatanmu ✨", fill="white", font=font)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.image(img, caption="📋 Laporan BMI & Kalori")
        st.download_button(
            label="📥 Download Laporan PNG",
            data=byte_im,
            file_name=f"Laporan_BMI_{nama}.png",
            mime="image/png"
        )
    else:
        st.error("Isi data dengan benar.")
