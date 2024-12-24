import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Analisis Rata-rata Skor PJ Praktikum berdasarkan Matprak dan Kelas")

# Upload file
uploaded_file = st.file_uploader("Unggah file CSV data mentah:", type="csv")

if uploaded_file is not None:
    # Membaca file CSV
    df_raw = pd.read_csv(uploaded_file)

    # Daftar nama kolom untuk rata-rata penilaian
    PJ_columns = [
        'Bagaimana penilaian Anda terhadap komunikasi pengajar dalam menyampaikan materi praktikum? ',
        'Seberapa baik pengajar dalam menjelaskan materi yang dibahas dalam praktikum? ',
        'Sejauh mana pengajar terlibat dan memberikan perhatian kepada praktikan selama praktikum? ',
        'Seberapa terbuka pengajar terhadap pertanyaan dan klarifikasi dari praktikan? ',
        'Bagaimana pengajar mengelola waktu dan diskusi di kelas praktikum?  '
    ]

    # Menambahkan kolom rata-rata hanya dari kolom yang dipilih
    df_raw['Average_pj'] = df_raw[PJ_columns].mean(axis=1)

    # Membuat DataFrame utama
    df = df_raw[['Timestamp', 'Email Address']]

    # Mengisi kolom Tingkat
    df['Tingkat'] = (
        df_raw['Pilih tingkat kelas Anda pada periode PTA 2024/2025.  ']
        .combine_first(df_raw['Pilih tingkat kelas Anda pada periode PTA 2024/2025.  .1'])
        .combine_first(df_raw['Pilih tingkat kelas Anda pada periode PTA 2024/2025.  .2'])
    )

    # Mengisi kolom Kelas
    df['Kelas'] = (
        df_raw['Pilih kelas Anda']
        .combine_first(df_raw['Pilih kelas Anda.1'])
        .combine_first(df_raw['Pilih kelas Anda.2'])
        .combine_first(df_raw['Pilih kelas Anda.3'])
    )

    # Mengisi kolom Matprak
    df['Matprak'] = (
        df_raw['Mata Praktikum yang Diikuti']
        .combine_first(df_raw['Mata Praktikum yang Diikuti.1'])
        .combine_first(df_raw['Mata Praktikum yang Diikuti.2'])
        .combine_first(df_raw['Mata Praktikum yang Diikuti.3'])
    )

    # Menambahkan kolom Score
    df['Score'] = df_raw['Average_pj']

    # Menghitung rata-rata skor per Matprak dan Kelas
    average_score = (
        df.groupby(['Matprak', 'Kelas'])['Score']
        .mean()
        .reset_index()
        .rename(columns={'Score': 'Average Score'})
    )

    # Menampilkan tabel rata-rata skor
    st.subheader("Rata-rata Score per Matprak dan Kelas")
    st.dataframe(average_score, use_container_width=True)

    # Input pengguna untuk memilih Matprak
    matprak_list = average_score['Matprak'].unique()
    selected_matprak = st.selectbox("Pilih Matprak:", matprak_list)

    # Filter data berdasarkan Matprak yang dipilih
    if selected_matprak:
        result = average_score[average_score['Matprak'] == selected_matprak]

        if result.empty:
            st.warning(f"Tidak ada data untuk Matprak '{selected_matprak}'.")
        else:
            st.subheader(f"Visualisasi Rata-rata Skor untuk Matprak '{selected_matprak}'")

            # Membuat visualisasi barplot
            result_sorted = result.sort_values(by="Average Score", ascending=False)
            plt.figure(figsize=(10, 6))
            sns.barplot(
                data=result_sorted, 
                x="Average Score", 
                y="Kelas", 
                palette="coolwarm"
            )
            plt.title(f"Rata-rata Skor untuk Matprak '{selected_matprak}'", fontsize=14)
            plt.xlabel("Average Score", fontsize=12)
            plt.ylabel("Kelas", fontsize=12)

            # Menambahkan nilai di setiap bar
            for index, value in enumerate(result_sorted["Average Score"]):
                plt.text(
                    value + 0.02, 
                    index, 
                    f"{value:.2f}", 
                    color="black", 
                    va="center"
                )
        
            st.pyplot(plt)
