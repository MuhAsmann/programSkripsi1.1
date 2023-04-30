import streamlit as st
from streamlit_option_menu import option_menu

from datetime import datetime
import time
import openpyxl

import pandas as pd
from deta import Deta

import database as db
import fuzzyMamdani as fz

import math


page_title = "Rekomendasi Merek Masker"
page_icon = ":money_with_wings:"
layout = "wide"
# layout = "centered"

file_path = 'tamplate.xlsx'


st.set_page_config(page_title=page_title,
                   page_icon=page_icon, layout=layout)

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
                <style>
                # MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)


# ================================================ akhir style

st.title(page_title + " " + page_icon)

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Upload Data", "Data Masker", "Rekomendasi"],
    # https://icons.getbootstrap.com/
    icons=["pencil-fill", "pencil-fill", "bar-chart-fill"],
    orientation="horizontal",
)


# input data
if selected == "Upload Data":
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
    st.title('Data Barang')
    st.write('Isi Form Di Bawah Ini Jika Ingin Menambahkan Merek Baru')

    col1, col2 = st.columns(2)

    with col1:
        merek = st.text_input('Merek')

    with col2:
        stok_awal = st.number_input('Stok Awal', min_value=0, max_value=120)

    with col1:
        harga_awal = st.number_input('Harga Awal', min_value=0)

    with col2:
        keuntungan = st.number_input(
            'Keuntungan', min_value=0, max_value=14000)

    if st.button('Tambah Data'):
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
        merek = st.text_input('Merek', value=selected_data.get('merek', ""))
        harga_awal = st.number_input(
            'Edit Harga Awal', value=selected_data.get('harga_awal', 0))
    with col4:
        stok_awal = st.number_input('Stok Awal', value=selected_data.get(
            'stok_awal', 0), min_value=0, max_value=120)
        keuntungan = st.number_input('Keuntungan', value=selected_data.get(
            'keuntungan', 0), min_value=0, max_value=14000)

    if st.button('Simpan Perubahan'):
        try:
            # simpan data masker yang diedit
            db.edit_data(selected_data.get('key'), merek,
                         stok_awal, harga_awal, keuntungan)
            st.success('Data berhasil diedit')
        except ValueError as e:
            st.error(str(e))

    # with col3:
    #     edit_merek = st.text_input('Merek ')

    # with col4:
    #     edit_stok_awal = st.number_input(
    #         'Edit Stok Awal', min_value=0, max_value=120)

    # with col3:
    #     edit_harga_awal = st.number_input('Edit Harga Awal', min_value=0)

    # with col4:
    #     edit_keuntungan = st.number_input(
    #         'Edit Keuntungan', min_value=0, max_value=14000)

    # if st.button('Simpan Data'):
    #     try:
    #         db.insert_data(merek, stok_awal, harga_awal, keuntungan)
    #         st.success('Data berhasil diedit')
    #     except ValueError as e:
    #         st.error(str(e))

    # fungsi edit data menggunakan table

    # st.write('Berikut adalah data barang yang tersedia:')
    # st.caption(
    #     "Untuk Edit Data Cukup Langsung Klik Data Pada Kolom Edit, Lalu Klik Tombol Simpan")

    # data = db.fetch_data_masker()

    # st.write('Edit Data')
    # df = pd.DataFrame(
    #     data, columns=['merek', 'stok_awal', 'harga_awal', 'keuntungan'])

    # edited_df = st.experimental_data_editor(
    #     df, use_container_width=True)

    # if st.button('Simpan Perubahan'):
    #     if edited_df is not None:
    #         for i, row in edited_df.iterrows():
    #             merek = row['merek']
    #             stok_awal = row['stok_awal']
    #             harga_awal = row['harga_awal']
    #             keuntungan = row['keuntungan']
    #             key = data[i]['key']

    #             db.edit_data(key, merek, stok_awal, harga_awal,
    #                          keuntungan)
    #         st.success(f'Data {merek} berhasil diedit')

    # =================================== Membuat judul tabel

    # Inisialisasi variabel
    data = None

    with st.form(key='search_masker'):
        search_input = st.text_input('Cari masker')
        search_button = st.form_submit_button('Cari')
        st.empty()  # Untuk menambahkan spasi antara input search dan tombol "Tampilkan Data"

        if st.form_submit_button('Tampilkan Data'):
            data = db.fetch_data_masker()

    # Menampilkan data dalam bentuk tabel
    if data:
        st.write('Daftar Masker')
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.write('No')
        with col2:
            st.write('Merek')
        with col3:
            st.write('Stok Awal')
        with col4:
            st.write('Harga Awal')
        with col5:
            st.write('Keuntungan')
        with col6:
            st.write('Harga Jual')
        with col7:
            st.write('')

        for i, item in enumerate(data):
            key = item.get('key')
            merek = item.get('merek')
            stok_awal = item.get('stok_awal')
            harga_awal = item.get('harga_awal')
            keuntungan = item.get('keuntungan')
            harga_jual = item.get('harga_jual')

            # Filter data berdasarkan input pencarian
            if search_input and search_input.lower() not in merek.lower():
                continue

            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
            with col1:
                st.write(i+1)
            with col2:
                st.write(merek)
            with col3:
                st.write(stok_awal)
            with col4:
                st.write(harga_awal)
            with col5:
                st.write(keuntungan)
            with col6:
                st.write(harga_jual)
            with col7:
                if st.button(f'Hapus', key=f'hapus-{merek}'):
                    db.delete_data(key)
                    st.success(f'Data {merek} berhasil dihapus')
    else:
        st.write('Silakan klik tombol "Tampilkan Data" untuk melihat daftar masker.')

    # data = db.fetch_data_masker()

    # with st.form(key='search_masker'):
    #     search_input = st.text_input('Cari masker')
    #     search_button = st.form_submit_button('Cari')

    # # Menampilkan data dalam bentuk tabel
    # st.write('Daftar Masker')
    # col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    # with col1:
    #     st.write('No')
    # with col2:
    #     st.write('Merek')
    # with col3:
    #     st.write('Stok Awal')
    # with col4:
    #     st.write('Harga Awal')
    # with col5:
    #     st.write('Keuntungan')
    # with col6:
    #     st.write('Harga Jual')
    # with col7:
    #     st.write('')

    # for i, item in enumerate(data):
    #     key = item.get('key')
    #     merek = item.get('merek')
    #     stok_awal = item.get('stok_awal')
    #     harga_awal = item.get('harga_awal')
    #     keuntungan = item.get('keuntungan')
    #     harga_jual = item.get('harga_jual')

    #     # Filter data berdasarkan input pencarian
    #     if search_input and search_input.lower() not in merek.lower():
    #         continue

    #     col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    #     with col1:
    #         st.write(i+1)
    #     with col2:
    #         st.write(merek)
    #     with col3:
    #         st.write(stok_awal)
    #     with col4:
    #         st.write(harga_awal)
    #     with col5:
    #         st.write(keuntungan)
    #     with col6:
    #         st.write(harga_jual)
    #     with col7:
    #         if st.button(f'Hapus', key=f'hapus-{merek}'):
    #             db.delete_data(key)
    #             st.success(f'Data {merek} berhasil dihapus')


if selected == "Rekomendasi":
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
            with st.spinner("Sedang menghitung..."):
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
