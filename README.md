# Bike Rentals - Final Project Data Analytics

Proyek ini merupakan tugas akhir dari course *Data Analysis using Python* yang memanfaatkan *Bike Sharing Dataset* untuk melakukan analisis data secara menyeluruh. Prosesnya mencakup pengumpulan data, penilaian kualitas data, pembersihan data, eksplorasi, serta visualisasi untuk mendapatkan wawasan lebih lanjut. Visualisasi dan konklusi kemudian ditampilkan melalui *Streamlit*, sehingga pengguna dapat memprediksi jumlah penyewaan sepeda berdasarkan faktor cuaca secara interaktif.

## Daftar Isi
1. [Persiapan Lingkungan (Setup Virtual Environment)](#1-persiapan-lingkungan-setup-virtual-environment)  
2. [Instalasi Dependensi](#2-instalasi-dependensi)  
3. [Siklus Pengerjaan Proyek](#3-siklus-pengerjaan-proyek)  
4. [Menjalankan Dashboard](#4-menjalankan-dashboard)  
5. [Referensi Tambahan](#5-referensi-tambahan)

---

## 1. Persiapan Lingkungan (Setup Virtual Environment)

1. **Clone atau Download Repository**  
   Silakan *clone* atau *download* zip repository ini:
   
   bike-rentals-final-project.git
   
2. **Masuk ke Folder Proyek**  
   ```bash
   cd bike-rentals-final-project
   ```

3. **Membuat Virtual Environment**  
   Buat *virtual environment* untuk memisahkan dependensi proyek ini dari sistem global. \\
   ```bash
   python -m venv venv
   ```

4. **Aktivasi Virtual Environment**  
   ```bash
   venv\Scripts\activate
   ```

## 2. Instalasi Dependensi

**Pastikan berada pada virtual environment** yang telah Anda buat dan aktifkan sebelumnya.  

- Instal semua dependensi dengan menggunakan `requirements.txt`:  
  ```bash
  pip install -r requirements.txt
  ```

## 3. Project Work Cycle

1. **Data Wrangling**  
   - *Gathering data*  
   - *Assessing data*  
   - *Cleaning data*

2. **Exploratory Data Analysis (EDA)**  
   - Membuat pertanyaan bisnis dan analisis  
   - Mengeksplorasi data untuk menjawab pertanyaan tersebut

3. **Data Visualization**  
   - Membuat visualisasi data untuk menjawab pertanyaan bisnis

4. **Dashboard**  
   - Mempersiapkan *DataFrame* yang siap untuk digunakan  
   - Membuat *filter* pada dashboard  
   - Melengkapi dashboard dengan berbagai visualisasi

---

## 4. Menjalankan Dashboard

Untuk menjalankan *dashboard* Streamlit:

1. **Pastikan Virtual Environment aktif**  
   Sebelum menjalankan perintah berikut, pastikan **venv** telah diaktifkan.

2. **Jalankan perintah berikut**  
   ```bash
   streamlit run dashboard.py
   ```
   atau sesuaikan dengan path / folder tempat Anda menyimpan berkas `dashboard.py`, misalnya:
   ```bash
   streamlit run source/dashboard.py
   ```
