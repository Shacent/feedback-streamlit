# Import Library
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import string
from sqlalchemy import create_engine
import nltk
from nltk.corpus import stopwords

# Mengunduh stopwords jika belum tersedia
nltk.download('stopwords')

# Import Data from Supabase
SUPABASE_DATABASE_URL = (
    "postgresql://postgres.jpsxgdhvmdfgqbhvyhpo:SayangLabti.123@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
)

engine = create_engine(SUPABASE_DATABASE_URL)

# Menambahkan styling kustom menggunakan Markdown dan HTML
@st.cache_data
def style_average_score_section():
    st.markdown("""
    <style>
    .average-score-title {
        font-size: 22px;
        font-weight: bold;
        color: #ffff; /* Consistent White color for titles */
        text-align: center;
        margin-bottom: 10px;
    }
    .average-score {
        font-size: 50px;
        font-weight: 900;
        color: #4CAF50; /* Green for positive emphasis */
        text-align: center;
        padding: 15px;
        background-color: #f9f9f9; /* Light gray for contrast */
        border-radius: 10px;
        width: fit-content;
        margin: 0 auto;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
    }
    .divider {
        margin: 20px 0;
        border-top: 2px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# Menampilkan rata-rata skor dengan styling
@st.cache_data
def display_average_score(category, selected_matprak, overall_average_score):
    st.markdown(f'''
    <div class="average-score-title">Skor Rata-rata {category} {selected_matprak} Semua Kelas</div>
    <div class="average-score" style="color: black;">{overall_average_score:.2f} / 5</div>
    ''', unsafe_allow_html=True)

# Tambahkan logo ke sidebar
logo_url = "https://raw.githubusercontent.com/Shacent/feedback-streamlit/main/image/Logo%20Labti%20With%20BG.png"
st.sidebar.markdown(
    f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="{logo_url}" alt="Logo LabTI" style="width: 150px; border-radius: 5px;">
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
page = st.sidebar.selectbox(
    "Pilih Halaman",
    ["Pendahuluan", "Tata Cara Pemakaian", "Score", "Tentang Pembuat"]
)


if page == "Pendahuluan":
    # Centered Title
    st.markdown("""
    <h1 style="text-align: center; color: #ffff;">
        🌟 Selamat Datang di Aplikasi Feedback LabTI 🌟
    </h1>
    """, unsafe_allow_html=True)
    
    # Content Section
    st.markdown("""
    ## Mengapa Aplikasi Ini Dibuat?
    Praktikum adalah bagian penting dari pengalaman belajar. Melalui aplikasi ini, kami ingin memastikan:
    - **Pengajar (PJ)** dapat memahami efektivitas pengajaran mereka.
    - **Asisten** dapat meningkatkan kualitas bantuan teknis mereka.
    - **Materi** yang diberikan sesuai dan relevan dengan tujuan pembelajaran.
    - **Fasilitas** mendukung suasana belajar yang nyaman.

    ## Fitur Utama
    - 📊 **Visualisasi Interaktif**: Analisis skor dengan grafik dan tabel.
    - 💬 **Feedback Terfokus**: Lihat komentar dari praktikan berdasarkan kelas dan matprak yang dipilih.
    - ⚙️ **Kemudahan Penggunaan**: UX yang sudah disesuaikan untuk informasi yang relevan.

    ## Apa yang Bisa Anda Lakukan?
    - ✅ Mendapatkan Insight dari praktikan melalui form feedback
    - ✅ Pilih aspek seperti Pengajar, Asisten, Materi, atau Fasilitas.
    - ✅ Lihat hasil analisis skor dan komentar untuk meningkatkan kualitas praktikum Anda.

    ---
    """)


elif page == "Tata Cara Pemakaian":
    st.title("Tata Cara Pemakaian")
    st.markdown("""
    **Langkah-langkah penggunaan aplikasi:**
    1. **Navigasi Halaman**: Gunakan sidebar untuk berpindah antar halaman (Pendahuluan, Tata Cara, Score, dan Tentang Pembuat).
    2. **Analisis Data**: Pilih matprak atau kelas tertentu untuk melihat skor PJ/Asisten/Materi/Fasilitas dan komentar praktikan.
    3. **Unduh Hasil**: Gunakan fitur bawaan untuk menyimpan hasil table maupun visualisasi.
    """)
elif page == "Score":
    # Judul aplikasi
    st.title("Informasi Feedback Terhadap Praktikum Labti PTA 24/25")
    st.title("Informasi Skor Praktikum")

    # For PJ
    if True:
        try:
            # Membaca file CSV
            df_raw = pd.read_sql_table(table_name="ratings", con=engine.connect())

            # Daftar nama kolom untuk rata-rata penilaian
            PJ_columns = [
                'Bagaimana penilaian Anda terhadap komunikasi pengajar dalam men',
                'Seberapa baik pengajar dalam menjelaskan materi yang dibahas da',
                'Sejauh mana pengajar terlibat dan memberikan perhatian kepada p',
                'Seberapa terbuka pengajar terhadap pertanyaan dan klarifikasi d',
                'Bagaimana pengajar mengelola waktu dan diskusi di kelas praktik'
            ]

            # Menambahkan kolom rata-rata hanya dari kolom yang dipilih
            df_raw['average_pj'] = df_raw[PJ_columns].mean(axis=1)

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
            if 'Mata Praktikum yang Diikuti' in df_raw.columns:
                df['Matprak'] = (
                    df_raw['Mata Praktikum yang Diikuti']
                    .combine_first(df_raw['Mata Praktikum yang Diikuti.1'])
                    .combine_first(df_raw['Mata Praktikum yang Diikuti.2'])
                    .combine_first(df_raw['Mata Praktikum yang Diikuti.3'])
                )
            else:
                st.error("Kolom 'Matprak' tidak ditemukan dalam dataset. Harap periksa nama kolom.")
                st.stop()

            # Menambahkan kolom Score
            df['score_pj'] = df_raw['average_pj']

            # Menghitung rata-rata skor per Matprak dan Kelas
            average_score_pj = (
                df.groupby(['Matprak', 'Kelas'])['score_pj']
                .mean()
                .reset_index()
                .rename(columns={'score_pj': 'Average Score'})
            )

            # Tab Layout
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["PJ Score", "Assistant Score", "Materi Score", "Fasilitas Score", "Summary"])

            with tab1:
                st.title("Informasi Peforma PJ")

                # Menampilkan tabel rata-rata skor
                st.subheader("Rata-rata Score PJ per Matprak dan Kelas")
                st.dataframe(average_score_pj, use_container_width=True)

                # Input pengguna untuk memilih Matprak dan Kelas
                matprak_list = df['Matprak'].dropna().unique()
                selected_matprak_pj = st.selectbox("Pilih Matprak:", matprak_list)

                # Menaplikan informasi peforma PJ per matprak masing-masing kelas
                if selected_matprak_pj:
                    result = average_score_pj[average_score_pj['Matprak'] == selected_matprak_pj]

                    if result.empty:
                        st.warning(f"Tidak ada data untuk Matprak '{selected_matprak_pj}'.")
                    else:
                        st.subheader(f"Visualisasi Rata-rata Skor PJ untuk Matprak {selected_matprak_pj}")

                        # Membuat visualisasi barplot
                        result_sorted = result.sort_values(by="Average Score", ascending=False)
                        plt.figure(figsize=(10, 6))
                        sns.barplot(
                            data=result_sorted, 
                            x="Average Score", 
                            y="Kelas", 
                            palette="coolwarm"
                        )
                        plt.title(f"Rata-rata Skor PJ untuk Matprak '{selected_matprak_pj}'", fontsize=14)
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

                # Menampilkan trend average per matprak seluruh kelas
                if selected_matprak_pj:
                    # Menghitung rata-rata skor untuk Matprak yang dipilih dari gabungan seluruh kelas
                    result_pj_all_classes = average_score_pj[average_score_pj['Matprak'] == selected_matprak_pj]

                    if result_pj_all_classes.empty:
                        st.warning(f"Tidak ada data untuk Matprak '{selected_matprak_pj}'.")
                    else:
                        # Menghitung rata-rata dari seluruh kelas untuk Matprak yang dipilih
                        overall_average_score_pj = result_pj_all_classes['Average Score'].mean()

                        # Styling dan menampilkan rata-rata skor
                        style_average_score_section()
                        display_average_score("PJ", selected_matprak_pj, overall_average_score_pj)

                # Menampilkan komentar / saran dari praktikan dengan wordcloud dan tabel
                if selected_matprak_pj:
                    kelas_list = df[df['Matprak'] == selected_matprak_pj]['Kelas'].dropna().unique()
                    selected_kelas = st.selectbox("Pilih Kelas:", kelas_list)

                    if selected_kelas:
                        st.subheader(f"Ragam Komentar untuk Matprak {selected_matprak_pj} di Kelas {selected_kelas}")

                        # Filter data berdasarkan Matprak dan Kelas yang dipilih
                        filtered_data = df_raw[
                            (df['Matprak'] == selected_matprak_pj) &
                            (df['Kelas'] == selected_kelas)
                        ]

                        if 'Komentar atau Saran untuk Pengajar (PJ) ' in filtered_data.columns:
                            # Menggabungkan semua komentar
                            comments = filtered_data['Komentar atau Saran untuk Pengajar (PJ) '].dropna().str.cat(sep=' ')

                            # Menghapus kata-kata umum (stopwords) dan tanda baca
                            stop_words = set(stopwords.words('indonesian')).union({"bagus","nya","e", "sih", "f8", "udh", "ga", "ini"})  # Stopwords bahasa Indonesia
                            words = [
                                word.lower()
                                for word in comments.split()
                                if word.lower() not in stop_words and word not in string.punctuation
                            ]

                            if len(words) > 0:
                                # Membuat WordCloud
                                wordcloud = WordCloud(
                                    width=800, height=400,
                                    background_color="white",
                                    colormap="viridis",
                                    max_words=400
                                ).generate(' '.join(words))

                                # Menampilkan WordCloud
                                st.image(wordcloud.to_array(), caption=f"Wordcloud dari Komentar atau Saran untuk {selected_matprak_pj} - {selected_kelas}")
                            else:
                                st.warning("Tidak ada kata yang tersedia untuk membuat WordCloud.")
                        else:
                            st.warning("Kolom 'Komentar atau Saran untuk Pengajar (PJ)' tidak ditemukan di dataset.")

                        if 'Komentar atau Saran untuk Pengajar (PJ) ' in filtered_data.columns:

                            comments_data = filtered_data[['Komentar atau Saran untuk Pengajar (PJ) ']].dropna()

                            # Menambahkan kolom panjang komentar
                            comments_data['Panjang Komentar'] = comments_data['Komentar atau Saran untuk Pengajar (PJ) '].apply(len)

                            # Input pengguna untuk memilih jumlah komentar yang akan ditampilkan
                            jumlah_komentar = st.selectbox(
                                "Pilih jumlah komentar yang akan ditampilkan:", 
                                [5, 10, 15, 20, "Tampilkan Semua"], 
                                index=0  # Default adalah 5
                            )

                            # Menentukan jumlah komentar yang akan ditampilkan
                            if jumlah_komentar == "Tampilkan Semua":
                                top_comments_to_display = comments_data  # Menampilkan semua data
                            else:
                                # Mendapatkan komentar terpanjang sesuai pilihan jumlah
                                top_comments_to_display = comments_data.nlargest(jumlah_komentar, 'Panjang Komentar')

                            # Menampilkan tabel hanya dengan kolom komentar
                            st.subheader(f"Pesan Untuk PJ {selected_matprak_pj} Kelas {selected_kelas}")
                            if not top_comments_to_display.empty:
                                # Reset index dan mulai dari 1
                                top_comments_reset = top_comments_to_display.reset_index(drop=True)
                                top_comments_reset.index = top_comments_reset.index + 1

                                # Menampilkan hanya kolom komentar dengan index yang dimulai dari 1
                                st.table(top_comments_reset[['Komentar atau Saran untuk Pengajar (PJ) ']])
                            else:
                                st.warning("Tidak ada komentar untuk ditampilkan.")
                        else:
                            st.warning("Kolom 'Komentar atau Saran untuk Pengajar (PJ)' tidak ditemukan di dataset.")

                        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            with tab2:
                # For Assistance    
                st.title("Informasi Peforma Assisten")  

                ast_columns = [
                   'Sejauh mana asisten tersedia untuk membantu selama praktikum?  ',
                   'Bagaimana kemampuan asisten dalam memberikan bantuan teknis dan',
                   'Sejauh mana asisten memiliki pengetahuan yang memadai tentang m',
                   'Seberapa aktif asisten dalam memberikan bantuan dan mendukung k',
                   'Bagaimana sikap profesional asisten selama praktikum berlangsun'
                ]

                df_raw['average_ast'] = df_raw[ast_columns].mean(axis=1)
                df['score_asisten'] = df_raw['average_ast']

                # Menghitung rata-rata skor per Matprak dan Kelas untuk Asisten
                average_score_asisten = (
                    df.groupby(['Matprak', 'Kelas'])['score_asisten']
                    .mean()
                    .reset_index()
                    .rename(columns={'score_asisten': 'Average Score Asisten'})
                )

                # Menampilkan tabel rata-rata skor Asisten
                st.subheader("Rata-rata Score Asisten per Matprak dan Kelas")
                st.dataframe(average_score_asisten, use_container_width=True)

                # Input pengguna untuk memilih Matprak dan Kelas
                selected_matprak_asisten = st.selectbox("Pilih Matprak untuk Asisten:", matprak_list, key="matprak_asisten_selectbox")

                if selected_matprak_asisten:
                    result_asisten = average_score_asisten[average_score_asisten['Matprak'] == selected_matprak_asisten]

                    if result_asisten.empty:
                        st.warning(f"Tidak ada data untuk Matprak '{selected_matprak_asisten}'.")
                    else:
                        st.subheader(f"Visualisasi Rata-rata Skor Asisten untuk Matprak {selected_matprak_asisten}")

                        # Membuat visualisasi barplot
                        result_asisten_sorted = result_asisten.sort_values(by="Average Score Asisten", ascending=False)
                        plt.figure(figsize=(10, 6))
                        sns.barplot(
                            data=result_asisten_sorted, 
                            x="Average Score Asisten", 
                            y="Kelas", 
                            palette="coolwarm"
                        )
                        plt.title(f"Rata-rata Skor Asisten untuk Matprak '{selected_matprak_asisten}'", fontsize=14)
                        plt.xlabel("Average Score Asisten", fontsize=12)
                        plt.ylabel("Kelas", fontsize=12)

                        # Menambahkan nilai di setiap bar
                        for index, value in enumerate(result_asisten_sorted["Average Score Asisten"]):
                            plt.text(
                                value + 0.02, 
                                index, 
                                f"{value:.2f}", 
                                color="black", 
                                va="center"
                            )

                        st.pyplot(plt)

                        if selected_matprak_asisten:
                            # Menghitung rata-rata skor Asisten untuk Matprak yang dipilih dari gabungan seluruh kelas
                            result_asisten_all_classes = average_score_asisten[average_score_asisten['Matprak'] == selected_matprak_asisten]

                            if result_asisten_all_classes.empty:
                                st.warning(f"Tidak ada data untuk Matprak '{selected_matprak_asisten}'.")
                            else:
                                # Menghitung rata-rata dari seluruh kelas untuk Asisten yang dipilih
                                overall_average_score_asisten = result_asisten_all_classes['Average Score Asisten'].mean()
                                # Styling dan menampilkan rata-rata skor untuk Pengajar dan Asisten
                                style_average_score_section()
                                display_average_score("Asisten", selected_matprak_asisten, overall_average_score_asisten)

                if selected_matprak_asisten:
                    kelas_list_asisten = df[df['Matprak'] == selected_matprak_asisten]['Kelas'].dropna().unique()
                    selected_kelas_asisten = st.selectbox("Pilih Kelas untuk Asisten:", kelas_list_asisten, key="kelas_asisten_selectbox")

                    if selected_kelas_asisten:
                        st.subheader(f"Ragam Komentar untuk Asisten pada Matprak {selected_matprak_asisten} di Kelas {selected_kelas_asisten}")

                        # Filter data berdasarkan Matprak dan Kelas yang dipilih
                        filtered_data_asisten = df_raw[
                            (df['Matprak'] == selected_matprak_asisten) &
                            (df['Kelas'] == selected_kelas_asisten)
                        ]

                        # Menampilkan komentar untuk Asisten
                        if 'Komentar atau Saran untuk Asisten' in filtered_data_asisten.columns:
                            # Menggabungkan semua komentar Asisten
                            comments_asisten = filtered_data_asisten['Komentar atau Saran untuk Asisten'].dropna().str.cat(sep=' ')

                            # Menghapus kata-kata umum (stopwords) dan tanda baca untuk Asisten
                            words_asisten = [
                                word.lower()
                                for word in comments_asisten.split()
                                if word.lower() not in stop_words and word not in string.punctuation
                            ]

                            if len(words_asisten) > 0:
                                # Membuat WordCloud untuk komentar Asisten
                                wordcloud_asisten = WordCloud(
                                    width=800, height=400,
                                    background_color="white",
                                    colormap="viridis",
                                    max_words=400
                                ).generate(' '.join(words_asisten))

                                # Menampilkan WordCloud untuk Asisten
                                st.image(wordcloud_asisten.to_array(), caption=f"Wordcloud dari Komentar atau Saran untuk Asisten pada {selected_matprak_asisten} - {selected_kelas_asisten}")
                            else:
                                st.warning("Tidak ada kata yang tersedia untuk membuat WordCloud untuk Asisten.")
                        else:
                            st.warning("Kolom 'Komentar atau Saran untuk Asisten' tidak ditemukan di dataset.")

                        if 'Komentar atau Saran untuk Asisten' in filtered_data_asisten.columns:
                        
                            comments_data_asisten = filtered_data_asisten[['Komentar atau Saran untuk Asisten']].dropna()

                            # Menambahkan kolom panjang komentar Asisten
                            comments_data_asisten['Panjang Komentar'] = comments_data_asisten['Komentar atau Saran untuk Asisten'].apply(len)

                            # Input pengguna untuk memilih jumlah komentar yang akan ditampilkan
                            jumlah_komentar_asisten = st.selectbox(
                                "Pilih jumlah komentar yang akan ditampilkan untuk Asisten:", 
                                [5, 10, 15, 20, "Tampilkan Semua"], 
                                index=0  # Default adalah 5
                            )

                            # Menentukan jumlah komentar yang akan ditampilkan
                            if jumlah_komentar_asisten == "Tampilkan Semua":
                                top_comments_asisten_to_display = comments_data_asisten  # Menampilkan semua data
                            else:
                                # Mendapatkan komentar terpanjang sesuai pilihan jumlah
                                top_comments_asisten_to_display = comments_data_asisten.nlargest(jumlah_komentar_asisten, 'Panjang Komentar')

                            # Menampilkan tabel hanya dengan kolom komentar Asisten
                            st.subheader(f"Pesan Untuk Asisten {selected_matprak_asisten} Kelas {selected_kelas_asisten}")
                            if not top_comments_asisten_to_display.empty:
                                # Reset index dan mulai dari 1
                                top_comments_asisten_reset = top_comments_asisten_to_display.reset_index(drop=True)
                                top_comments_asisten_reset.index = top_comments_asisten_reset.index + 1

                                # Menampilkan hanya kolom komentar Asisten dengan index yang dimulai dari 1
                                st.table(top_comments_asisten_reset[['Komentar atau Saran untuk Asisten']])
                            else:
                                st.warning("Tidak ada komentar untuk ditampilkan untuk Asisten.")
                        else:
                            st.warning("Kolom 'Komentar atau Saran untuk Asisten' tidak ditemukan di dataset.")

                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            with tab3:
                # For Materials
                st.title("Informasi Peforma Materi")  

                # Kolom yang digunakan untuk menghitung rata-rata skor materi
                materi_columns = [
                    'Sejauh mana materi praktikum yang disampaikan mudah dipahami da',
                    'Seberapa lengkap materi yang diberikan selama praktikum dalam m',
                    'Sejauh mana materi yang diajarkan sesuai dengan tujuan dan hasi',
                    'Sejauh mana materi praktikum yang diberikan relevan dan menduku',
                    'Sejauh mana materi praktikum dapat membantu dalam pengembangan '
                ]

                # Menambahkan kolom rata-rata skor materi ke dataset
                df_raw['average_mat'] = df_raw[materi_columns].mean(axis=1)
                df['score_materi'] = df_raw['average_mat']

                # Menghitung rata-rata skor per Matprak dan Kelas untuk Materi
                average_score_materi = (
                    df.groupby(['Matprak', 'Kelas'])['score_materi']
                    .mean()
                    .reset_index()
                    .rename(columns={'score_materi': 'Average Score Materi'})
                )

                # Menampilkan tabel rata-rata skor Materi
                st.subheader("Rata-rata Score Materi per Matprak dan Kelas")
                st.dataframe(average_score_materi, use_container_width=True)

                # Input pengguna untuk memilih Matprak
                selected_matprak_materi = st.selectbox("Pilih Matprak untuk Materi:", matprak_list, key="matprak_materi_selectbox")

                if selected_matprak_materi:
                    result_materi = average_score_materi[average_score_materi['Matprak'] == selected_matprak_materi]

                    if result_materi.empty:
                        st.warning(f"Tidak ada data untuk Matprak '{selected_matprak_materi}'.")
                    else:
                        st.subheader(f"Visualisasi Rata-rata Skor Materi untuk Matprak {selected_matprak_materi}")

                        # Membuat visualisasi barplot
                        result_materi_sorted = result_materi.sort_values(by="Average Score Materi", ascending=False)
                        plt.figure(figsize=(10, 6))
                        sns.barplot(
                            data=result_materi_sorted, 
                            x="Average Score Materi", 
                            y="Kelas", 
                            palette="coolwarm"
                        )
                        plt.title(f"Rata-rata Skor Materi untuk Matprak '{selected_matprak_materi}'", fontsize=14)
                        plt.xlabel("Average Score Materi", fontsize=12)
                        plt.ylabel("Kelas", fontsize=12)

                        # Menambahkan nilai di setiap bar
                        for index, value in enumerate(result_materi_sorted["Average Score Materi"]):
                            plt.text(
                                value + 0.02, 
                                index, 
                                f"{value:.2f}", 
                                color="black", 
                                va="center"
                            )

                        st.pyplot(plt)

                        # Menghitung rata-rata skor Materi untuk Matprak yang dipilih dari semua kelas
                        overall_average_score_materi = result_materi['Average Score Materi'].mean()
                        style_average_score_section()
                        display_average_score("Materi",selected_matprak_materi, overall_average_score_materi)

                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

                if selected_matprak_materi:
                    kelas_list_materi = df[df['Matprak'] == selected_matprak_materi]['Kelas'].dropna().unique()
                    st.title("Saran Perbaikan Oleh Pratikan")
                    selected_kelas_materi = st.selectbox("Pilih Kelas untuk Informasi Hal yang Bisa Ditingkatkan Kedepannya:", kelas_list_materi, key="kelas_materi_selectbox")

                    if selected_kelas_materi:
                        st.subheader(f"Ragam Komentar untuk Materi pada Matprak {selected_matprak_materi} di Kelas {selected_kelas_materi}")

                        # Filter data berdasarkan Matprak dan Kelas yang dipilih
                        filtered_data_materi = df_raw[
                            (df['Matprak'] == selected_matprak_materi) &
                            (df['Kelas'] == selected_kelas_materi)
                        ]

                        # Menampilkan komentar untuk Materi
                        if 'Apa yang dapat diperbaiki atau ditingkatkan untuk praktikum?' in filtered_data_materi.columns:
                            comments_materi = filtered_data_materi['Apa yang dapat diperbaiki atau ditingkatkan untuk praktikum?'].dropna().str.cat(sep=' ')

                            # Menghapus kata-kata umum (stopwords) dan tanda baca untuk Materi
                            words_materi = [
                                word.lower()
                                for word in comments_materi.split()
                                if word.lower() not in stop_words and word not in string.punctuation
                            ]

                            if len(words_materi) > 0:
                                # Membuat WordCloud untuk komentar Materi
                                wordcloud_materi = WordCloud(
                                    width=800, height=400,
                                    background_color="white",
                                    colormap="viridis",
                                    max_words=50
                                ).generate(' '.join(words_materi))

                                # Menampilkan WordCloud untuk Materi
                                st.image(wordcloud_materi.to_array(), caption=f"Wordcloud dari Komentar atau Saran untuk Materi pada {selected_matprak_materi} - {selected_kelas_materi}")
                            else:
                                st.warning("Tidak ada kata yang tersedia untuk membuat WordCloud untuk Materi.")
                        else:
                            st.warning("Kolom 'Apa yang dapat diperbaiki atau ditingkatkan untuk praktikum?' tidak ditemukan di dataset.")

                        # Menampilkan komentar terperinci untuk Materi
                        if 'Apa yang dapat diperbaiki atau ditingkatkan untuk praktikum?' in filtered_data_materi.columns:
                            comments_data_materi = filtered_data_materi[['Apa yang dapat diperbaiki atau ditingkatkan untuk praktikum?']].dropna()

                            # Menambahkan kolom panjang komentar Materi
                            comments_data_materi['Panjang Komentar'] = comments_data_materi['Apa yang dapat diperbaiki atau ditingkatkan untuk praktikum?'].apply(len)

                            # Input pengguna untuk memilih jumlah komentar yang akan ditampilkan
                            jumlah_komentar_materi = st.selectbox(
                                "Pilih jumlah komentar yang akan ditampilkan untuk Materi:", 
                                [5, 10, 15, 20, "Tampilkan Semua"], 
                                index=0
                            )

                            # Menentukan jumlah komentar yang akan ditampilkan
                            if jumlah_komentar_materi == "Tampilkan Semua":
                                top_comments_materi_to_display = comments_data_materi
                            else:
                                top_comments_materi_to_display = comments_data_materi.nlargest(jumlah_komentar_materi, 'Panjang Komentar')

                            # Menampilkan tabel hanya dengan kolom komentar Materi
                            st.subheader(f"Pesan Untuk {selected_matprak_materi} Kelas {selected_kelas_materi}")
                            if not top_comments_materi_to_display.empty:
                                top_comments_materi_reset = top_comments_materi_to_display.reset_index(drop=True)
                                top_comments_materi_reset.index = top_comments_materi_reset.index + 1

                                st.table(top_comments_materi_reset[['Apa yang dapat diperbaiki atau ditingkatkan untuk praktikum?']])
                            else:
                                st.warning("Tidak ada komentar untuk ditampilkan untuk Materi.")
                        else:
                            st.warning("Kolom 'Apa yang dapat diperbaiki atau ditingkatkan untuk praktikum?' tidak ditemukan di dataset.")

                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)   

            with tab4:
                st.title("Informasi Performa Fasilitas")  

                    # Kolom yang digunakan untuk menghitung rata-rata skor fasilitas
                fasilitas_columns = [
                    'Sejauh mana ruang praktikum nyaman dan mendukung aktivitas sela',
                    'Sejauh mana perangkat dan peralatan yang disediakan cukup untuk',
                    'Bagaimana penilaian Anda terhadap kebersihan laboratorium selam',
                    'Bagaimana penilaian Anda terhadap keteraturan dan kerapian fasi',
                    'Sejauh mana jaringan internet dan perangkat lunak yang disediak',
                ]

                # Menambahkan kolom rata-rata skor fasilitas ke dataset
                df_raw['average_fasilitas'] = df_raw[fasilitas_columns].mean(axis=1)
                df['score_fasilitas'] = df_raw['average_fasilitas']

                # Menghitung rata-rata skor per Matprak untuk Fasilitas
                average_score_fasilitas = (
                    df.groupby(['Matprak'])['score_fasilitas']
                    .mean()
                    .reset_index()
                    .rename(columns={'score_fasilitas': 'Average Score Fasilitas'})
                )

                # Menampilkan tabel rata-rata skor Fasilitas
                st.subheader("Rata-rata Score Fasilitas per Matprak")
                st.dataframe(average_score_fasilitas, use_container_width=True)

                # Input pengguna untuk memilih Matprak
                selected_matprak_fasilitas = st.selectbox("Pilih Matprak untuk Fasilitas:", matprak_list, key="matprak_fasilitas_selectbox")

                if selected_matprak_fasilitas:
                    result_fasilitas = average_score_fasilitas[average_score_fasilitas['Matprak'] == selected_matprak_fasilitas]

                    if result_fasilitas.empty:
                        st.warning(f"Tidak ada data untuk Matprak '{selected_matprak_fasilitas}'.")
                    else:
                        overall_average_score_fasilitas = result_fasilitas["Average Score Fasilitas"].mean()  # Menghitung rata-rata dari kolom
                        
                        st.markdown("")
                        display_average_score("Fasilitas", selected_matprak_fasilitas, overall_average_score_fasilitas)

                        # Komentar dan WordCloud untuk semua kelas pada Matprak yang dipilih
                        st.subheader(f"Ragam Komentar untuk Fasilitas pada Matprak {selected_matprak_fasilitas}")

                        # Filter data berdasarkan Matprak yang dipilih
                        filtered_data_fasilitas = df_raw[df['Matprak'] == selected_matprak_fasilitas]

                        # Menggabungkan semua komentar untuk Matprak yang dipilih
                        if 'Masukkan untuk Fasilitas LabTI' in filtered_data_fasilitas.columns:
                            comments_fasilitas = filtered_data_fasilitas['Masukkan untuk Fasilitas LabTI'].dropna().str.cat(sep=' ')

                            # Menambahkan kata "bagus" ke dalam daftar stop words
                            custom_stop_words = stop_words.union({"bagus","nya","e", "sih", "f8", "udh", "ga", "ini"})

                            # Menghapus kata-kata umum (stopwords) dan tanda baca untuk Fasilitas
                            words_fasilitas = [
                                word.lower()
                                for word in comments_fasilitas.split()
                                if word.lower() not in custom_stop_words and word not in string.punctuation
                            ]

                            if len(words_fasilitas) > 0:
                                # Membuat WordCloud untuk komentar Fasilitas
                                wordcloud_fasilitas = WordCloud(
                                    width=800, height=400,
                                    background_color="white",
                                    colormap="viridis",
                                    max_words=400
                                ).generate(' '.join(words_fasilitas))

                                # Menampilkan WordCloud untuk Fasilitas
                                st.image(wordcloud_fasilitas.to_array(), caption=f"Wordcloud dari Komentar atau Saran untuk Fasilitas pada Matprak {selected_matprak_fasilitas}")
                            else:
                                st.warning("Tidak ada kata yang tersedia untuk membuat WordCloud untuk Fasilitas.")
                        else:
                            st.warning("Kolom 'Masukkan untuk Fasilitas LabTI' tidak ditemukan di dataset.")

                        # Menampilkan komentar terperinci untuk Fasilitas
                        if 'Masukkan untuk Fasilitas LabTI' in filtered_data_fasilitas.columns:
                            comments_data_fasilitas = filtered_data_fasilitas[['Masukkan untuk Fasilitas LabTI']].dropna()

                            # Menambahkan kolom panjang komentar Fasilitas
                            comments_data_fasilitas['Panjang Komentar'] = comments_data_fasilitas['Masukkan untuk Fasilitas LabTI'].apply(len)

                            # Input pengguna untuk memilih jumlah komentar yang akan ditampilkan
                            jumlah_komentar_fasilitas = st.selectbox(
                                "Pilih jumlah komentar yang akan ditampilkan untuk Fasilitas:", 
                                [5, 10, 15, 20, "Tampilkan Semua"], 
                                index=0
                            )

                            # Menentukan jumlah komentar yang akan ditampilkan
                            if jumlah_komentar_fasilitas == "Tampilkan Semua":
                                top_comments_fasilitas_to_display = comments_data_fasilitas
                            else:
                                top_comments_fasilitas_to_display = comments_data_fasilitas.nlargest(jumlah_komentar_fasilitas, 'Panjang Komentar')

                            # Menampilkan tabel hanya dengan kolom komentar Fasilitas
                            st.subheader(f"Pesan Untuk Fasilitas {selected_matprak_fasilitas}")
                            if not top_comments_fasilitas_to_display.empty:
                                top_comments_fasilitas_reset = top_comments_fasilitas_to_display.reset_index(drop=True)
                                top_comments_fasilitas_reset.index = top_comments_fasilitas_reset.index + 1

                                st.table(top_comments_fasilitas_reset[['Masukkan untuk Fasilitas LabTI']])
                            else:
                                st.warning("Tidak ada komentar untuk ditampilkan untuk Fasilitas.")
                        else:
                            st.warning("Kolom 'Masukkan untuk Fasilitas LabTI' tidak ditemukan di dataset.")

                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                # Section: Summary
                # Menambahkan CSS untuk menempatkan title di tengah halaman
                st.markdown("""
                    <style>
                        .centered-title {
                            font-size: 40px;
                            font-weight: 900;
                            color:;
                            text-align: center;
                            margin-top: 20px;  /* Menambahkan sedikit ruang di atas */
                        }
                    </style>
                """, unsafe_allow_html=True)

            with tab5:
                # Menampilkan title di tengah halaman menggunakan HTML
                st.markdown('<div class="centered-title">Data Summary 📊</div>', unsafe_allow_html=True)

                st.markdown("")
                st.markdown("")

                # Menghitung jumlah data
                jumlah_data = len(df)

                st.markdown(f'<div class="average-score" style="color: black;"> Total Data: {jumlah_data:,}</div>', unsafe_allow_html=True)
                # Divider
                st.markdown("---")

                # 2. Menampilkan rata-rata skor overall untuk PJ, Asisten, dan Materi
                st.markdown('<div class="centered-title">Overall Average Score</div>', unsafe_allow_html=True)
                st.markdown("")

                # Membuat 3 kolom untuk menampilkan nilai
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="PJ Average Score", value=f"{overall_average_score_pj:.2f} / 5")
                with col2:
                    st.metric(label="Asisten Average Score", value=f"{overall_average_score_asisten:.2f} / 5")
                with col3:
                    st.metric(label="Materi Average Score", value=f"{overall_average_score_materi:.2f} / 5")

                # Divider
                st.markdown("---")

            # 3. Menampilkan informasi pembuat
            st.markdown('<div class="centered-title">Disclaimer</div>', unsafe_allow_html=True)
            st.markdown("")
            st.markdown("""
            <style>
            .creator-box {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                font-size: 18px;
                text-align: center;
                color: #555;
            }
            .signature {
                    font-size: 14px;
                    font-style: italic;
                    color: #B0B0B0;  /* Warna abu-abu */
                    text-align: center;
                    margin-top: 10px;  /* Menambahkan sedikit ruang di atas signature */
                }
            </style>
            <div class="creator-box">
                <strong>This Data Only Based on LabTI Feedback Form !</strong>
            </div>
            """, unsafe_allow_html=True)

            # Menambahkan signature "Made by Shacent" di bawah judul
            st.markdown('<div class="signature">Made by Shacent & Wardiansyah</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Kesalahan saat membaca atau memproses file: {e}")
    else:
        st.info("Unggah file CSV untuk melanjutkan analisis.")

elif page == "Tentang Pembuat":
    st.title("Tentang Pembuat")
    st.markdown("""
    ### Pembuat dan Kontributor

    **Pembuat**:  
    - **Nama**: Muhammad Hauzan Dini Fakhri
    - **Email**: hauzandini@gmail.com  
    - **LinkedIn**: [linkedin.com/in/muhammad-hauzan-dini-fakhri/](https://www.linkedin.com/in/muhammad-hauzan-dini-fakhri/)
    - **GitHub**: [Shacent](https://github.com/Shacent)  

    **Kontributor**:  
    - **Nama**: Wardiansyah Fauzi Abdillah  
    - **Email**: ardi.dl738@gmail.com  
    - **LinkedIn**: [linkedin.com/in/wardiansyah-fauzi-abdillah](https://linkedin.com/in/wardiansyah-fauzi-abdillah)  
    - **GitHub**: [github.com/WardiansyahF](https://github.com/WardiansyahF)  

    ### Tujuan Aplikasi
    Aplikasi ini dirancang untuk membantu LabTI menganalisis feedback dari praktikan secara interaktif, dengan visualisasi dan analisis yang mudah dipahami.  

    ### Hak Cipta
    © 2025 Shacent & Wardiansyah Fauzi Abdillah. All rights reserved.
    """)
