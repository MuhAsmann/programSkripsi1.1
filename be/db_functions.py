import os

from deta import Deta
# from dotenv import load_dotenv

# load_dotenv(".env")


# DETA_KEY = os.getenv("DETA_KEY")
DETA_KEY = os.environ("DETA_KEY")


deta = Deta(DETA_KEY)

db_transaksi = deta.Base("dataTransaksi")
db_data_masker = deta.Base("dataMasker")
db_user = deta.Base("user")
db_hasil = deta.Base("dataHasil")


# =============================== login


def insert_user(username, name, password):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db_user.put({"key": username, "name": name, "password": password})


def fetch_all_users():
    """Returns a dict of all users"""
    res = db_user.fetch()
    return res.items


# print(fetch_all_users())

def get_user(username):
    """If not found, the function will return none"""
    return db_user.get(username)


def update_user(username, updates):
    """If the item is updated, returns None. Otherwise, an exception is raised"""
    return db_user.update(updates, username)


def delete_user(username):
    """Always returns None, even if the key does not exist"""
    return db_user.delete(username)


# ======================================= upload produk


def insert_period(tanggal, merek, banyak, tanggal_upload):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db_transaksi.put({"tanggal": tanggal, "merek": merek, "banyak": banyak, "tanggal_upload": tanggal_upload})


def fetch_all_tanggal_upload():
    """Returns a list of all unique values in the tanggal_upload column"""
    all_data = db_transaksi.fetch().items
    unique_tanggal_upload = list(
        set([item['tanggal_upload'] for item in all_data]))
    return unique_tanggal_upload


def fetch_periods_by_date(tanggal_upload):
    """Returns a list of all periods with the specified upload date"""
    all_data = db_transaksi.fetch().items
    filtered_data = [
        item for item in all_data if item['tanggal_upload'] == tanggal_upload]
    return filtered_data


def fetch_data_masker_by_merek(selected_merek):
    all_data = db_data_masker.fetch().items
    filtered_data = [
        item for item in all_data if item['merek'] == selected_merek]
    return filtered_data[0] if filtered_data else {}


def delete_data_by_date(tanggal_upload):
    """Deletes all data with the specified tanggal_upload"""
    data = db_transaksi.fetch({"tanggal_upload": tanggal_upload})
    for item in data.items:
        db_transaksi.delete(item["key"])


def merge_data(tanggal_upload):
    # Fetch data from both tables
    data_masker = db_data_masker.fetch().items
    data_transaksi = db_transaksi.fetch().items

    # Get total banyak for each mask brand from transaksi table
    total_banyak_by_merek = {}
    for item in data_transaksi:
        if item['tanggal_upload'] == tanggal_upload:
            if item['merek'] in total_banyak_by_merek:
                total_banyak_by_merek[item['merek']] += item['banyak']
            else:
                total_banyak_by_merek[item['merek']] = item['banyak']

    # Merge data from both tables by mask brand
    result = []
    for item_masker in data_masker:
        merek = item_masker['merek']
        stok = item_masker['stok_awal'] - total_banyak_by_merek.get(merek, 0)
        total_penjualan = total_banyak_by_merek.get(merek, 0)
        keuntungan = total_banyak_by_merek.get(
            merek, 0) * item_masker['keuntungan']

        result.append({
            'merek': merek,
            'stok': stok,
            'total_penjualan': total_penjualan,
            'keuntungan': keuntungan
        })

    return result


# =================================  Data Masker
def fetch_data_masker():
    return db_data_masker.fetch().items


def insert_data(merek, stok_awal, harga_awal, keuntungan):
    """Returns the report on a successful creation, otherwise raises an error"""
    existing_data = db_data_masker.fetch({"merek": merek}).items
    if existing_data:
        raise ValueError(
            f"Data dengan merek {merek} sudah ada, Silahkan Edit Data Dibawah")
    else:
        return db_data_masker.put({
            'merek': merek,
            'stok_awal': stok_awal,
            'harga_awal': harga_awal,
            'keuntungan': keuntungan,
            'harga_jual': harga_awal + keuntungan
        })


def edit_data(key, merek, stok_awal, harga_awal, keuntungan):
    return db_data_masker.update({
        'merek': merek,
        'stok_awal': stok_awal,
        'harga_awal': harga_awal,
        'keuntungan': keuntungan,
        'harga_jual': harga_awal+keuntungan
    }, key)


# belum digunakan
def update_data(key, merek, stok_awal, harga_awal, keuntungan):
    """Updates an existing masker data in the database"""
    existing_data = db_data_masker.fetch({'merek': merek})
    if existing_data and existing_data[0]['key'] != key:
        raise ValueError(
            f"Data dengan merek {merek} sudah ada, hapus terlebih dahulu jika ingin diganti")
    else:
        db_data_masker.update({
            'merek': merek,
            'stok_awal': stok_awal,
            'harga_awal': harga_awal,
            'keuntungan': keuntungan,
            'harga_jual': harga_awal + keuntungan
        }, key=key)


def delete_data(key):
    return db_data_masker.delete(key)


#  ============================== Hasil Perhitungan
def inputHasil(hasil):
    return db_hasil.put(hasil)


def cekHasil(period):
    existing_data = db_hasil.fetch({"tanggal_upload": period}).items

    if existing_data:
        return existing_data
    else:
        return 0
