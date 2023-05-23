import streamlit as st
from streamlit_option_menu import option_menu
import hydralit_components as hc

from datetime import datetime
import time
import openpyxl

import pandas as pd
from deta import Deta

from be import db_functions as db
from be import fuzzyMamdani as fz
# import fuzzyMamdani as fz

import math


page_title = "Rekomendasi Merek Masker"
page_icon = ":money_with_wings:"
layout = "wide"
# layout = "centered"

file_path = 'tamplate.xlsx'


st.set_page_config(page_title=page_title,
                   page_icon=page_icon, layout=layout, initial_sidebar_state='collapsed')

# ===================== navbar mengunakan hydralit

# menu_data = [
#     {'icon': "far fa-copy", 'label': "Data Masker"},
#     {'id': 'Rekomendasi', 'icon': "🐙", 'label': "Rekomendasi"},
# ]

# over_theme = {'txc_inactive': '#FFFFFF'}
# menu_id = hc.nav_bar(
#     menu_definition=menu_data,
#     override_theme=over_theme,
#     home_name='Upload Data',
#     login_name='Logout',
#     # will show the st hamburger as well as the navbar now!
#     hide_streamlit_markers=True,
#     sticky_nav=True,  # at the top or not
#     sticky_mode='sticky',  # jumpy or not-jumpy, but sticky or pinned
# )

# ================= Akhir Navbar Hydralit

# ================== Style

# with open('style.py') as style:
#     st.markdown(f'<style>{style.read}</style>', unsafe_allow_html=True)

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
                <style>
                # MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                .css-15zrgzn {display: none}
                .css-eczf16 {display: none}
                .css-jn99sy {display: none}
                div.css-82vsbp.e1tzin5v0{
                    /*background-color: #eee ;
                    border: 1px solid #dcdcdc !important;
                    /* padding: 20px 20px 20px 70px; */
                    padding: 5% 5% 5% 10%;
                    border-radius: 10px;*/
                }

                .card {
                    background-color: rgb(14, 17, 23);
                    border :1px solid white;
                    border-radius: 8px;
                    padding: 16px;
                    margin-bottom: 16px;
                    /*text-align: center;*/
                }

                .card .title {
                    font-size: 20px;
                    color:#FF4B4B;
                    font-weight: bold;
                    margin-bottom: 8px;
                }

                .card .content {
                    font-size: 14px;
                    margin-bottom: 8px;
                }
                .card .content span{
                    color:#FF4B4B;
                }

                .card .edit-button {
                    background-color: #ffcc00;
                    color: #fff;
                    padding: 4px 8px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }

                .card .edit-button:hover {
                    background-color: #ffbb00;
                }

                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)


# ================================================ akhir style


# =========== Navbar Menggunakan Streamlit_option_menu
# --- NAVIGATION MENU ---
# NOTE : Terdapat bug tidak bisa menggunakan posisi sticky ketika orientation horizontal dan tidak didalam st.sidebar
# selected = option_menu(
#     menu_title=None,
#     options=["Upload Data", "Data Masker", "Rekomendasi"],
#     # https://icons.getbootstrap.com/
#     icons=["pencil-fill", "pencil-fill", "bar-chart-fill"],
#     orientation="horizontal",
#     styles={
#         "container": {"position": "sticky !important"}
#     }
# )
with st.sidebar:
    selected = option_menu(
        menu_title='Sistem Rekomendasi',
        options=["Dashboard", "Upload Data",
                 "Data Masker", "Rekomendasi", "Logout"],
        # https://icons.getbootstrap.com/
        icons=["bi-house-door-fill", "bi-cloud-upload-fill  ", "pencil-fill",
               "bar-chart-fill", "bi-box-arrow-left"]
    )


st.title(page_title + " " + page_icon)


@st.cache_data
def fetch_masker_data():
    return db.fetch_data_masker()


# Membuat session state untuk menyimpan data masker
if 'masker_data' not in st.session_state:
    st.session_state.masker_data = fetch_masker_data()


if selected == "Dashboard":
    st.title("Penggunaan Sistem")
    st.write("Selamat datang di sistem kami!")
    st.write("Berikut adalah langkah-langkah penggunaan sistem:")
    st.markdown(
        "1. User perlu mengedit data stok pada halaman **Data Masker** setelah melakukan pembelian stok.")
    st.markdown("2. Untuk mendapatkan rekomendasi, user perlu mengupload data penjualan selama 2 minggu terakhir pada halaman **Upload Data Penjualan** sesuai dengan template yang ada.")
    st.markdown("3. Setelah melakukan upload, user dapat masuk ke halaman **Rekomendasi** dan memilih tanggal upload untuk mendapatkan rekomendasi.")

# input data
if selected == "Upload Data":
    # if menu_id == "Upload Data":
    st.header(f"Upload File")

    def file_download_link(file_path, file_name):
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
        st.download_button(
            label='Download Tamplate', data=file_bytes, file_name=file_name)

    # Memanggil fungsi download button
    file_path = 'tamplate.xlsx'
    file_name = 'tamplate.xlsx'
    file_download_link(file_path, file_name)

    with st.form("entry_from"):
        # data = st.file_uploader(
        #     "Upload File Excel Sesuai Dengan Tamplate", type=["xlsx"])

        # if data:
        #     # Buka file Excel dengan openpyxl
        #     wb = openpyxl.load_workbook(data)
        #     # Cek apakah sheet "Hasil" ada dalam file Excel
        #     if "Transaksi" not in wb.sheetnames:
        #         data = "Salah"
        #     else:
        #         # Tampilkan tampilan loading ketika file di-upload
        #         with st.spinner("Uploading file..."):
        #             df = pd.read_excel(data, sheet_name="Transaksi")
        #             time.sleep(2)

        # submitted = st.form_submit_button("Simpan Data")

        data = st.file_uploader(
            "Upload File Excel Sesuai Dengan Template", type=["xlsx"])

        if data:
            # Buka file Excel dengan openpyxl
            wb = openpyxl.load_workbook(data)

            # Baca sheet pertama
            sheet = wb.active
            df = pd.DataFrame(sheet.values)

            # Cek apakah ada kolom "merek" dan "banyak"
            if "merek" not in df.iloc[0].values or "banyak" not in df.iloc[0].values:
                data = "Salah"
            else:
                # Tampilkan tampilan loading ketika file di-upload
                with st.spinner("Uploading file..."):
                    # Baca sheet "Transaksi" menjadi dataframe
                    df = pd.read_excel(data, sheet_name="Transaksi")
                    time.sleep(2)

        submitted = st.form_submit_button("Simpan Data")

        # Jika tombol "Simpan Data" diklik
        if submitted:
            # Jika file belum di-upload
            if not data:
                st.warning(
                    "Silakan upload file Excel terlebih dahulu. Pastikan Sesuai Dengan Tamplate")
            elif data == "Salah":
                st.warning(
                    "File Yang Anda Upload Tidak Sesuai Tamplate. Pastikan file yang diupload sesuai dengan template.")
            else:
                # Tampilkan tampilan loading ketika data di-push ke database
                with st.spinner("Menyimpan Data, Harap Bersabar..."):
                    # Tambahkan kolom tanggal upload
                    df["tanggal_upload"] = datetime.now().strftime(
                        # "%Y-%m-%d")
                        "%Y-%m-%d %H:%M:%S")
                    # Push data ke database
                    for index, row in df.iterrows():
                        db.insert_period(
                            row["tanggal"], row["merek"], row["banyak"], row["tanggal_upload"])
                        time.sleep(0.5)
                st.success("Data berhasil diupload ke database Deta.sh")


if selected == "Data Masker":
    # if menu_id == "Data Masker":
    st.title('Data Barang')
    st.write('Isi Form Di Bawah Ini Jika Ingin Menambahkan Merek Baru')

    col1, col2 = st.columns(2)

    with col1:
        merek = st.text_input('Merek')

    with col2:
        stok_awal = st.number_input('Stok Awal', min_value=0, max_value=120)

    with col1:
        harga_awal = st.number_input('Harga Awal (Modal)', min_value=0)

    with col2:
        keuntungan = st.number_input(
            'Keuntungan', min_value=0, max_value=14000)

    if st.button('Tambah Data'):
        with st.spinner('Sedang memuat...'):
            time.sleep(2)  # Contoh penundaan simulasi loading data
            try:
                db.insert_data(merek, stok_awal, harga_awal, keuntungan)
                st.success('Data berhasil ditambahkan')
            except ValueError as e:
                st.error(str(e))

    # edit data

    st.write('Pilih Data Dibawah Jika Ingin Di Edit')

    # dropdown merek
    merek_list = [item.get('merek') for item in db.fetch_data_masker()]
    selected_merek = st.selectbox('Pilih merek', options=merek_list)

    # mengambil data masker yang dipilih
    selected_data = db.fetch_data_masker_by_merek(selected_merek)

    col3, col4 = st.columns(2)
    # mengisi form input dengan data masker yang dipilih
    with col3:
        edit_merek = st.text_input(
            'Merek', value=selected_data.get('merek', ""))
        harga_awal = st.number_input(
            'Harga Awal(Modal)', value=selected_data.get('harga_awal', 0))
    with col4:
        stok_awal = st.number_input('Stok Awal', value=selected_data.get(
            'stok_awal', 0), min_value=0, max_value=120)
        keuntungan = st.number_input('Keuntungan', value=selected_data.get(
            'keuntungan', 0), min_value=0, max_value=14000)

    if st.button('Simpan Perubahan'):
        with st.spinner('Sedang memuat...'):
            time.sleep(2)  # Contoh penundaan simulasi loading data
            try:
                db.edit_data(selected_data.get('key'), edit_merek,
                             stok_awal, harga_awal, keuntungan)
                st.success('Data berhasil diedit')

                # Update session state dengan data masker yang sudah diedit
                for i, masker in enumerate(st.session_state.masker_data):
                    if masker.get('key') == selected_data.get('key'):
                        st.session_state.masker_data[i]['merek'] = edit_merek
                        st.session_state.masker_data[i]['harga_awal'] = harga_awal
                        st.session_state.masker_data[i]['stok_awal'] = stok_awal
                        st.session_state.masker_data[i]['keuntungan'] = keuntungan
                        break
            except ValueError as e:
                st.error(str(e))

    with st.form(key='search_masker'):
        search_input = st.text_input('Cari masker')
        search_button = st.form_submit_button('Cari')

    # Menampilkan data dalam bentuk card
    st.write('Daftar Masker')

    # Mengatur jumlah kolom yang diinginkan
    num_cols = 2
    cols = st.columns(num_cols)

    # Menghitung jumlah card yang akan ditampilkan pada setiap kolom
    num_items_per_col = (len(st.session_state.masker_data) // num_cols) + 1

    with st.spinner('Sedang memuat...'):
        time.sleep(1)  # Contoh penundaan simulasi loading data

        # for i in range(num_cols):
        #     with cols[i]:
        #         for j in range(i*num_items_per_col, min((i+1)*num_items_per_col, len(st.session_state.masker_data))):
        #             item = st.session_state.masker_data[j]
        #             key = item.get('key')
        #             merek = item.get('merek')
        #             stok_awal = item.get('stok_awal')
        #             harga_awal = item.get('harga_awal')
        #             keuntungan = item.get('keuntungan')
        #             harga_jual = item.get('harga_jual')

        #             # Filter data berdasarkan input pencarian
        #             if search_input and search_input.lower() not in merek.lower():
        #                 continue

        #             with st.container():
        #                 st.write(f"## {merek}")
        #                 st.write(f"Stok awal: {stok_awal}")
        #                 st.write(f"Harga awal: {harga_awal}")
        #                 st.write(f"Keuntungan: {keuntungan}")
        #                 st.write(f"Harga jual: {harga_jual}")
        #                 if st.button(f'Hapus', key=f'hapus-{merek}'):
        #                     db.delete_data(key)
        #                     st.success(f'Data {merek} berhasil dihapus')
        #                     # Menghapus data dari session state setelah dihapus dari database
        #                     st.session_state.masker_data = [
        #                         d for d in st.session_state.masker_data if d['key'] != key]
        for i in range(num_cols):
            with cols[i]:
                for j in range(i * num_items_per_col, min((i + 1) * num_items_per_col, len(st.session_state.masker_data))):
                    item = st.session_state.masker_data[j]
                    key = item.get('key')
                    merek = item.get('merek')
                    stok_awal = item.get('stok_awal')
                    harga_awal = item.get('harga_awal')
                    keuntungan = item.get('keuntungan')
                    harga_jual = item.get('harga_jual')

                    if search_input and search_input.lower() not in merek.lower():
                        continue

                    # Menampilkan elemen kustom dalam bentuk HTML
                    card_html = f'''
                    <div class="card">
                        <div class="title">{merek}</div>
                        <div class="content">Stok awal: <span>{stok_awal}</span></div>
                        <div class="content">Harga awal: <span>{harga_awal}</span></div>
                        <div class="content">Keuntungan: <span>{keuntungan}</span></div>
                        <div class="content">Harga jual: <span>{harga_jual}</span></div>
                        <!--- <button class="edit-button" onclick="editItem('{merek}')">Edit</button> -->
                        <!--- <button class="edit-button" onclick="deleteItem('{key}')">Hapus</button> -->
                    </div>
                    '''

                    st.markdown(card_html, unsafe_allow_html=True)

                    # Fungsi untuk menghapus item
                    # def delete_item(item_key):
                    #     db.delete_data(item_key)
                    #     st.success(f'Data {merek} berhasil dihapus')
                    #     st.session_state.masker_data = [
                    #         d for d in st.session_state.masker_data if d['key'] != item_key]

                    # if st.button(f'Hapus', key=f'hapus-{merek}'):
                    #     delete_item(key)

                    if st.button(f'Hapus', key=f'hapus-{merek}'):
                        db.delete_data(key)
                        st.success(f'Data {merek} berhasil dihapus')
                        st.session_state.masker_data = [
                            d for d in st.session_state.masker_data if d['key'] != key]


# if selected == "Data Masker":
#     st.title('Data Barang')
#     st.write('Isi Form Di Bawah Ini Jika Ingin Menambahkan Merek Baru')

#     col1, col2 = st.columns(2)

#     with col1:
#         merek = st.text_input('Merek')

#     with col2:
#         stok_awal = st.number_input('Stok Awal', min_value=0, max_value=120)

#     with col1:
#         harga_awal = st.number_input('Harga Awal', min_value=0)

#     with col2:
#         keuntungan = st.number_input(
#             'Keuntungan', min_value=0, max_value=14000)

#     if st.button('Tambah Data'):
#         try:
#             db.insert_data(merek, stok_awal, harga_awal, keuntungan)
#             st.success('Data berhasil ditambahkan')
#         except ValueError as e:
#             st.error(str(e))

#     # edit data

#     st.write('Pilih Data Dibawah Jika Ingin Di Edit')

#     # dropdown merek
#     merek_list = [item.get('merek') for item in db.fetch_data_masker()]
#     # merek_list = [item.get('merek') for item in fetch_masker_data()]
#     selected_merek = st.selectbox('Pilih merek', options=merek_list)

#     # mengambil data masker yang dipilih
#     selected_data = db.fetch_data_masker_by_merek(selected_merek)

#     col3, col4 = st.columns(2)
#     # mengisi form input dengan data masker yang dipilih
#     with col3:
#         edit_merek = st.text_input(
#             'Merek', value=selected_data.get('merek', ""))
#         harga_awal = st.number_input(
#             'Edit Harga Awal', value=selected_data.get('harga_awal', 0))
#     with col4:
#         stok_awal = st.number_input('Stok Awal', value=selected_data.get(
#             'stok_awal', 0), min_value=0, max_value=120)
#         keuntungan = st.number_input('Keuntungan', value=selected_data.get(
#             'keuntungan', 0), min_value=0, max_value=14000)

#     if st.button('Simpan Perubahan'):
#         try:
#             # simpan data masker yang diedit
#             db.edit_data(selected_data.get('key'), edit_merek,
#                          stok_awal, harga_awal, keuntungan)
#             st.success('Data berhasil diedit')

#             # Update session state dengan data masker yang sudah diedit
#             for i, masker in enumerate(st.session_state.masker_data):
#                 if masker.get('key') == selected_data.get('key'):
#                     st.session_state.masker_data[i]['merek'] = edit_merek
#                     st.session_state.masker_data[i]['harga_awal'] = harga_awal
#                     st.session_state.masker_data[i]['stok_awal'] = stok_awal
#                     st.session_state.masker_data[i]['keuntungan'] = keuntungan
#                     break
#         except ValueError as e:
#             st.error(str(e))
#     # ================================================= akhir tampilan tambah dan edit
#     # ================================================= 14

#     # def show_masker_data(masker_data):
#     #     st.write('Daftar Masker')

#     #     # Mengatur jumlah kolom yang diinginkan
#     #     num_cols = 3
#     #     cols = st.beta_columns(num_cols)

#     #     # Menghitung jumlah card yang akan ditampilkan pada setiap kolom
#     #     num_items_per_col = (len(masker_data) // num_cols) + 1

#     #     for i in range(num_cols):
#     #         with cols[i]:
#     #             for j in range(i*num_items_per_col, min((i+1)*num_items_per_col, len(masker_data))):
#     #                 item = masker_data[j]
#     #                 key = item.get('key')
#     #                 merek = item.get('merek')
#     #                 stok_awal = item.get('stok_awal')
#     #                 harga_awal = item.get('harga_awal')
#     #                 keuntungan = item.get('keuntungan')
#     #                 harga_jual = item.get('harga_jual')

#     #                 # Tambahkan border pada kontainer kartu
#     #                 with st.beta_container():
#     #                     st.write(
#     #                         f'<style>.card {{border: 1px solid #ccc; border-radius: 5px; padding: 10px;}}</style>', unsafe_allow_html=True)
#     #                     st.write(f"<div class='card'>")
#     #                     st.write(f"## {merek}")
#     #                     st.write(f"Stok awal: {stok_awal}")
#     #                     st.write(f"Harga awal: {harga_awal}")
#     #                     st.write(f"Keuntungan: {keuntungan}")
#     #                     st.write(f"Harga jual: {harga_jual}")
#     #                     if st.button(f'Hapus', key=f'hapus-{merek}'):
#     #                         db.delete_data(key)
#     #                         st.success(f'Data {merek} berhasil dihapus')
#     #                         # Menghapus data dari cache setelah dihapus dari database
#     #                         masker_data.pop(j)
#     #                     st.write("</div>")

#     # # Membatasi jumlah data yang ditampilkan pada setiap halaman menjadi 9
#     # PAGE_SIZE = 9

#     # # Mengambil data masker dengan caching
#     # masker_data = fetch_masker_data()

#     # # Membagi data menjadi beberapa halaman dengan teknik lazy loading
#     # num_pages = (len(masker_data) // PAGE_SIZE) + 1
#     # page_number = st.sidebar.number_input(
#     #     'Halaman', min_value=1, max_value=num_pages, value=1, step=1)
#     # start_idx = (page_number - 1) * PAGE_SIZE
#     # end_idx = start_idx + PAGE_SIZE
#     # masker_data = masker_data[start_idx:end_idx]

#     # # Menampilkan data masker pada halaman yang dipilih
#     # show_masker_data(masker_data)

#     # # Menambahkan fitur pagination
#     # st_pagination(masker_data, page_number, num_pages, PAGE_SIZE)
#     # ================================================= 13

#     with st.form(key='search_masker'):
#         search_input = st.text_input('Cari masker')
#         search_button = st.form_submit_button('Cari')

#     # Menampilkan data dalam bentuk card
#     st.write('Daftar Masker')

#     # Mengatur jumlah kolom yang diinginkan
#     num_cols = 2
#     cols = st.columns(num_cols)

#     # Menghitung jumlah card yang akan ditampilkan pada setiap kolom
#     num_items_per_col = (len(st.session_state.masker_data) // num_cols) + 1

#     for i in range(num_cols):
#         with cols[i]:
#             for j in range(i*num_items_per_col, min((i+1)*num_items_per_col, len(st.session_state.masker_data))):
#                 item = st.session_state.masker_data[j]
#                 key = item.get('key')
#                 merek = item.get('merek')
#                 stok_awal = item.get('stok_awal')
#                 harga_awal = item.get('harga_awal')
#                 keuntungan = item.get('keuntungan')
#                 harga_jual = item.get('harga_jual')

#                 # Filter data berdasarkan input pencarian
#                 if search_input and search_input.lower() not in merek.lower():
#                     continue

#                 with st.container():
#                     st.write(f"## {merek}")
#                     st.write(f"Stok awal: {stok_awal}")
#                     st.write(f"Harga awal: {harga_awal}")
#                     st.write(f"Keuntungan: {keuntungan}")
#                     st.write(f"Harga jual: {harga_jual}")
#                     if st.button(f'Hapus', key=f'hapus-{merek}'):
#                         db.delete_data(key)
#                         st.success(f'Data {merek} berhasil dihapus')
#                         # Menghapus data dari session state setelah dihapus dari database
#                         st.session_state.masker_data = [
#                             d for d in st.session_state.masker_data if d['key'] != key]
    # ================================================= 12


if selected == "Rekomendasi":
    # if menu_id == "Rekomendasi":
    # Inisialisasi state
    if "list_data" not in st.session_state:
        st.session_state["list_data"] = []

    st.header(f"Hasil Rekomendasi")
    with st.form("saved_periods"):
        period = st.selectbox("Select Waktu Upload :",
                              db.fetch_all_tanggal_upload())
        submitted = st.form_submit_button(
            "Dapatkan Rekomendasi")
        deleted = st.form_submit_button(
            "Hapus Data")
        if deleted:
            with st.spinner("Sedang Menghapus Data"):
                db.delete_data_by_date(period)
                st.success(
                    f"All data for upload date {period} has been deleted.")
                st.session_state["list_data"] = []
        if submitted:
            with st.spinner("Sedang menghitung, pastikan jangan keluar dari tab ini..."):
                # pertama
                # period_data = db.fetch_periods_by_date(period)
                # kedua
                period_data = db.merge_data(period)

                for record in period_data:
                    # stock = record['stock']
                    stock = record['stok']
                    total_penjualan = record['total_penjualan']
                    # pertama
                    # total_pendapatan = record['total_pendapatan']
                    # kedua
                    total_pendapatan = record['keuntungan']

                    priority, quantity = fz.fuzzyMamdani(
                        stock, total_penjualan, total_pendapatan)

                    record['priority'] = priority
                    # membulatkan nilai quantity ke atas
                    record['quantity'] = math.ceil(quantity)

                sorted_data = sorted(
                    period_data, key=lambda x: x['priority'], reverse=True)

                st.session_state["list_data"] = sorted_data

                # # Tampilkan data hasil fuzzy Mamdani
                # st.write("Hasil rekomendasi: ")

                # # Tampilkan data dalam bentuk list
                # for i, record in enumerate(sorted_data):
                #     no = i+1
                #     merek = record['merek']
                #     quantity = record['quantity']
                #     priority = record['priority']
                #     st.write(
                #         f"{no}. | {merek} | {quantity:.0f} | {priority:.2f}")
    # Tampilkan data dalam bentuk list
    if st.session_state["list_data"]:
        st.write("Hasil rekomendasi: ")
        sorted_data = st.session_state["list_data"]
        for i, record in enumerate(sorted_data):
            no = i+1
            merek = record['merek']
            quantity = record['quantity']
            priority = record['priority']
            st.write(f"{no}. | {merek} | {quantity:.0f} | {priority:.2f}")

if selected == "Logout":
    st.header(f"Tampilan Logout")
