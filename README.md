# 📋 Automate Rating Feedback LabTI Procedure

> **Deskripsi Singkat**  
> Panduan ini berisi langkah-langkah detail untuk menggunakan tools Automate Rating Feedback untuk mendapatkan insight secara cepat perihal peforma pembelajaran melalui feedback form yang diisi oleh praktikan. Dokumentasi ini dirancang untuk memastikan proses berjalan secara konsisten dan efisien.

---

## 📂 Daftar Isi
1. [Pendahuluan](##pendahuluan)
2. [Persiapan](##persiapan)
3. [Proses Langkah-Langkah](##proses-langkah-langkah)
4. [Disclaimer](##disclaimer)

---

## 📝 Pendahuluan
**Tujuan:**  
Tujuan adanya Automate Rating Feedback LabTI Procedure ini untuk memberikan panduan ke siapa saja yang ingin memerlukan insight perihal peforma lab secara cepat dan tanpa harus mengelola data lebih lanjut.

**Peringatan:**  
Streamlit tidak akan bekerja jika form mengalami perubahan format kolom, sehingga akan diberikan update lebih lanjut jika mengalami perubahan form.

**Hasil Akhir**  
Automate Feedback from VALID dalam memberikan hasil score rata-rata setiap kelas dan mata praktikum yang dipilih sesuai dengan pengelolahan manual dan sudah di testing juga menggunakan data yang lain.

---

## ⚙️ Persiapan
**Google Account:**
- LabTI 1
- LabTI 3

**Prasyarat:**
- Internet

---

## 🛠️ Proses Langkah-Langkah
### 1. Langkah 1: Login Menggunakan Akun LabTI 1 / LabTI 3

![Langkah 1](https://github.com/Shacent/feedback-streamlit/blob/main/image/Accounts.png?raw=true)

### 2. Langkah 2: Kunjungi Feedback Form LabTI
Link Form: https://bit.ly/FeedbackLabTI

![Langkah 2](https://github.com/Shacent/feedback-streamlit/blob/main/image/2.png?raw=true)

### 3. Langkah 3: Buka Menu Edit Form

![Langkah 3](https://github.com/Shacent/feedback-streamlit/blob/main/image/3.png?raw=true)

### 4. Langkah 4: Pilih Jawaban

![Langkah 4](https://github.com/Shacent/feedback-streamlit/blob/main/image/4.png?raw=true)

### 5. Langkah 5: Buka Spreadsheet Form

![Langkah 5](https://github.com/Shacent/feedback-streamlit/blob/main/image/5.png?raw=true)

### 6. Langkah 6: Download Data as CSV
FYI: CSV adalah singkatan dari Comma Separated Value, yang merupakan format file untuk menyimpan data dalam bentuk teks biasa. File CSV menyimpan informasi yang dipisahkan oleh koma, bukan dalam kolom.

![Langkah 6](https://github.com/Shacent/feedback-streamlit/blob/main/image/6.png?raw=true)

### 7. Langkah 7: Data Berhasil di-Download

![Langkah 7](https://github.com/Shacent/feedback-streamlit/blob/main/image/7.png?raw=true)

### 8. Langkah 8: Membuka Automate Rating Feedback LabTI App
Link: https://feedback-labti.streamlit.app/

![Langkah 8](https://github.com/Shacent/feedback-streamlit/blob/main/image/8.png?raw=true)

### 9. Langkah 9: Upload Data
Upload data csv yang sudah didownload tadi

![Langkah 9](https://github.com/Shacent/feedback-streamlit/blob/main/image/9.png?raw=true)

### 10. Langkah 10: Pilih Data yang akan Diproses

![Langkah 10](https://github.com/Shacent/feedback-streamlit/blob/main/image/10.png?raw=true)

### 11. Langkah 11: Rata-rata Score Berhasil Dibuat
Jika form masih memiliki struktur yang sama, maka seharusnya akan muncul tabel yang sesuai dengan gambar di bawah ini

![Langkah 11](https://github.com/Shacent/feedback-streamlit/blob/main/image/11.png?raw=true)

### 12. Langkah 12: Pilih Mata Praktikum yang Diinginkan
Pilih mata praktikum yang akan dicari insightnya

![Langkah 12](https://github.com/Shacent/feedback-streamlit/blob/main/image/12.png?raw=true)

### 13. Langkah 13: Contoh Disini Memilih IMK

![Langkah 13](https://github.com/Shacent/feedback-streamlit/blob/main/image/13.png?raw=true)

### 14. Langkah 14: Insight Matprak Berhasil Terbuat
Disini muncul nilai rata-rata dari masing-masing matprak yang dipilih per kelas yang diikuti

![Langkah 14](https://github.com/Shacent/feedback-streamlit/blob/main/image/14.png?raw=true)

### 15. Langkah 15: Visualisasi Bar Plot
Barplot membantu dalam melihat lebih jelas terhadap detail perbandingan antar kelas

![Langkah 15](https://github.com/Shacent/feedback-streamlit/blob/main/image/15.png?raw=true)

---

## 📝 Disclaimer

> **Perbandingan Menggunakan Manual**  
> Hasil dari data yang diolah sudah dilakukan validasi menggunakan pengelolahan manual, sehingga apapun hasil yang ditampilkan pada app ini akan valid sesuai dengan prosedur yang dilakukan secara manual

### Hasil Average Menggunakan App: 
![app](https://github.com/Shacent/feedback-streamlit/blob/main/image/app.png?raw=true)

### Hasil Average Menggunakan Manual: 
![Manual](https://github.com/Shacent/feedback-streamlit/blob/main/image/manual.png?raw=true)

### Kesimpulan
Dari hasil tersebut terlihat bahwa terdapat kesamaan diantara data yang diolah menggunakan manual dengan app, sehingga app ini dapat digunakan dan dikembangkan lebih lanjut untuk keperluan mendatang.
