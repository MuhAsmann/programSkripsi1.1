def trimf(x, a, b, c):
    if x <= a or x >= c:
        return 0
    if a < x <= b:
        return (x - a) / (b - a)
    if b < x < c:
        return (c - x) / (c - b)
    else:
        return 0


def stok_membership(x):
    return {
        'sedikit': trimf(x, 0, 25, 50),
        'cukup': trimf(x, 30, 60, 90),
        'banyak': trimf(x, 70, 95, 120)
    }


def penjualan_membership(x):
    return {
        'sedikit': trimf(x, 0, 25, 50),
        'sedang': trimf(x, 30, 60, 90),
        'banyak': trimf(x, 70, 95, 120)
    }


def pendapatan_membership(x):
    return {
        'sangat rendah': trimf(x, 0, 225000, 450000),
        'rendah': trimf(x, 200000, 500000, 800000),
        'sedang': trimf(x, 500000, 850000, 1200000),
        'tinggi': trimf(x, 900000, 1200000, 1500000),
        'sangat tinggi': trimf(x, 1250000, 1470000, 1700000)
    }


def fuzzy_inference(stok, penjualan, pendapatan):
    prioritas_output = {
        'sangat rendah': [],
        'rendah': [],
        'sedang': [],
        'tinggi': [],
        'sangat tinggi': []
    }
    jumlah_output = {
        'sangat sedikit': [],
        'sedikit': [],
        'sedang': [],
        'banyak': [],
        'sangat banyak': []
    }

    # inference min (Rule)
    # Rule 1
    if 0 <= stok <= 50 and 0 <= penjualan <= 50 and 0 <= pendapatan <= 450000:
        prioritas_output['sangat rendah'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sangat rendah'])])
        jumlah_output['sangat sedikit'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sangat rendah'])])
    # Rule 2
    if 0 <= stok <= 50 and 0 <= penjualan <= 50 and 50000 <= pendapatan <= 850000:
        prioritas_output['sangat rendah'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['rendah'])])
        jumlah_output['sangat sedikit'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['rendah'])])
    # Rule 3
    if 0 <= stok <= 50 and 0 <= penjualan <= 50 and 450000 <= pendapatan <= 1250000:
        prioritas_output['rendah'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sedang'])])
        jumlah_output['sangat sedikit'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sedang'])])
    # Rule 4
    if 0 <= stok <= 50 and 0 <= penjualan <= 50 and 850000 <= pendapatan <= 1650000:
        prioritas_output['rendah'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['tinggi'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['tinggi'])])
    # Rule 5
    if 0 <= stok <= 50 and 0 <= penjualan <= 50 and 1250000 <= pendapatan <= 1700000:
        prioritas_output['rendah'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])
    # Rule 6
    if 0 <= stok <= 50 and 30 <= penjualan <= 90 and 0 <= pendapatan <= 450000:
        prioritas_output['rendah'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sangat rendah'])])
        jumlah_output['sangat sedikit'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sangat rendah'])])

    # Rule 7
    if 0 <= stok <= 50 and 30 <= penjualan <= 90 and 50000 <= pendapatan <= 850000:
        prioritas_output['rendah'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['rendah'])])
        jumlah_output['sangat sedikit'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['rendah'])])

    # Rule 8
    if 0 <= stok <= 50 and 30 <= penjualan <= 90 and 450000 <= pendapatan <= 1250000:
        prioritas_output['sedang'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sedang'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sedang'])])

    # Rule 9
    if 0 <= stok <= 50 and 30 <= penjualan <= 90 and 850000 <= pendapatan <= 1650000:
        prioritas_output['tinggi'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['tinggi'])])
        jumlah_output['sedang'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['tinggi'])])

    # Rule 10
    if 0 <= stok <= 50 and 30 <= penjualan <= 90 and 1250000 <= pendapatan <= 1700000:
        prioritas_output['sangat tinggi'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])
        jumlah_output['banyak'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])

    # Rule 11
    if 0 <= stok <= 50 and 70 <= penjualan <= 120 and 0 <= pendapatan <= 450000:
        prioritas_output['sedang'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['sangat rendah'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['sangat rendah'])])

    # Rule 12
    if 0 <= stok <= 50 and 70 <= penjualan <= 120 and 50000 <= pendapatan <= 850000:
        prioritas_output['sedang'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['rendah'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['rendah'])])

    # Rule 13
    if 0 <= stok <= 50 and 70 <= penjualan <= 120 and 450000 <= pendapatan <= 1250000:
        prioritas_output['tinggi'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['sedang'])])
        jumlah_output['sedang'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['sedang'])])

    # Rule 14
    if 0 <= stok <= 50 and 70 <= penjualan <= 120 and 850000 <= pendapatan <= 1650000:
        prioritas_output['sangat tinggi'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['tinggi'])])
        jumlah_output['banyak'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['tinggi'])])

    # Rule 15
    if 0 <= stok <= 50 and 70 <= penjualan <= 120 and 1250000 <= pendapatan <= 1700000:
        prioritas_output['sangat tinggi'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])
        jumlah_output['sangat banyak'].extend([min(stok_membership(float(stok))['sedikit'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])

    # Rule 16
    if 30 <= stok <= 90 and 0 <= penjualan <= 50 and 0 <= pendapatan <= 450000:
        prioritas_output['sangat rendah'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sangat rendah'])])
        jumlah_output['sangat sedikit'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sangat rendah'])])

    # Rule 17
    if 30 <= stok <= 90 and 0 <= penjualan <= 50 and 50000 <= pendapatan <= 850000:
        prioritas_output['sangat rendah'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['rendah'])])
        jumlah_output['sangat sedikit'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['rendah'])])

    # Rule 18
    if 30 <= stok <= 90 and 0 <= penjualan <= 50 and 450000 <= pendapatan <= 1250000:
        prioritas_output['rendah'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sedang'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sedang'])])

    # Rule 19
    if 30 <= stok <= 90 and 0 <= penjualan <= 50 and 850000 <= pendapatan <= 1650000:
        prioritas_output['rendah'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['tinggi'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['tinggi'])])

    # Rule 20
    if 30 <= stok <= 90 and 0 <= penjualan <= 50 and 1250000 <= pendapatan <= 1700000:
        prioritas_output['sedang'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])

    # Rule 21
    if 30 <= stok <= 90 and 30 <= penjualan <= 90 and 0 <= pendapatan <= 450000:
        prioritas_output['sangat rendah'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sangat rendah'])])
        jumlah_output['sangat sedikit'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sangat rendah'])])

    # Rule 22
    if 30 <= stok <= 90 and 30 <= penjualan <= 90 and 50000 <= pendapatan <= 850000:
        prioritas_output['rendah'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['rendah'])])
        jumlah_output['sangat sedikit'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['rendah'])])
        print("Prioritas sebelum:", prioritas_output)

    # Rule 23
    if 30 <= stok <= 90 and 30 <= penjualan <= 90 and 450000 <= pendapatan <= 1250000:
        prioritas_output['sedang'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sedang'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sedang'])])

    # Rule 24
    if 30 <= stok <= 90 and 30 <= penjualan <= 90 and 850000 <= pendapatan <= 1650000:
        prioritas_output['tinggi'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['tinggi'])])
        jumlah_output['sedang'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['tinggi'])])

    # Rule 25
    if 30 <= stok <= 90 and 30 <= penjualan <= 90 and 1250000 <= pendapatan <= 1700000:
        prioritas_output['sangat tinggi'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])
        jumlah_output['banyak'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])

    # Rule 26
    if 30 <= stok <= 90 and 70 <= penjualan <= 120 and 0 <= pendapatan <= 450000:
        prioritas_output['sedang'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['sangat rendah'])])
        jumlah_output['sangat sedikit'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['sangat rendah'])])

    # Rule 27
    if 30 <= stok <= 90 and 70 <= penjualan <= 120 and 50000 <= pendapatan <= 850000:
        prioritas_output['sedang'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['rendah'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['rendah'])])

    # Rule 28
    if 30 <= stok <= 90 and 70 <= penjualan <= 120 and 450000 <= pendapatan <= 1250000:
        prioritas_output['tinggi'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['sedang'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['sedang'])])

    # Rule 29
    if 30 <= stok <= 90 and 70 <= penjualan <= 120 and 850000 <= pendapatan <= 1650000:
        prioritas_output['tinggi'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['tinggi'])])
        jumlah_output['sedang'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['tinggi'])])

    # Rule 30
    if 30 <= stok <= 90 and 70 <= penjualan <= 120 and 1250000 <= pendapatan <= 1700000:
        prioritas_output['sangat tinggi'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])
        jumlah_output['banyak'].extend([min(stok_membership(float(stok))['cukup'], penjualan_membership(
            float(penjualan))['banyak'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])

    # Rule 31
    if 70 <= stok <= 120 and 0 <= penjualan <= 50 and 0 <= pendapatan <= 450000:
        prioritas_output['sangat rendah'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sangat rendah'])])
        jumlah_output['sangat sedikit'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sangat rendah'])])

    # Rule 32
    if 70 <= stok <= 120 and 0 <= penjualan <= 50 and 50000 <= pendapatan <= 850000:
        prioritas_output['sangat rendah'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['rendah'])])
        jumlah_output['sangat sedikit'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['rendah'])])

    # Rule 33
    if 70 <= stok <= 120 and 0 <= penjualan <= 50 and 450000 <= pendapatan <= 1250000:
        prioritas_output['sangat rendah'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sedang'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sedang'])])

    # Rule 34
    if 70 <= stok <= 120 and 0 <= penjualan <= 50 and 850000 <= pendapatan <= 1650000:
        prioritas_output['sangat rendah'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['tinggi'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['tinggi'])])

    # Rule 35
    if 70 <= stok <= 120 and 0 <= penjualan <= 50 and 1250000 <= pendapatan <= 1700000:
        prioritas_output['rendah'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedikit'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])

    # Rule 36
    if 70 <= stok <= 120 and 30 <= penjualan <= 90 and 0 <= pendapatan <= 450000:
        prioritas_output['rendah'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sangat rendah'])])
        jumlah_output['sangat sedikit'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sangat rendah'])])

    # Rule 37
    if 70 <= stok <= 120 and 30 <= penjualan <= 90 and 50000 <= pendapatan <= 850000:
        prioritas_output['rendah'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['rendah'])])
        jumlah_output['sangat sedikit'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['rendah'])])

    # Rule 38
    if 70 <= stok <= 120 and 30 <= penjualan <= 90 and 450000 <= pendapatan <= 1250000:
        prioritas_output['sedang'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sedang'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sedang'])])

    # Rule 39
    if 70 <= stok <= 120 and 30 <= penjualan <= 90 and 850000 <= pendapatan <= 1650000:
        prioritas_output['tinggi'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['tinggi'])])
        jumlah_output['sedikit'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['tinggi'])])

    # Rule 40
    if 70 <= stok <= 120 and 30 <= penjualan <= 90 and 1250000 <= pendapatan <= 1700000:
        prioritas_output['sangat tinggi'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])
        jumlah_output['sedang'].extend([min(stok_membership(float(stok))['banyak'], penjualan_membership(
            float(penjualan))['sedang'], pendapatan_membership(float(pendapatan))['sangat tinggi'])])

    # inference max
    maksimum_sr = max(
        prioritas_output['sangat rendah']) if prioritas_output['sangat rendah'] else None
    maksimum_r = max(prioritas_output['rendah']
                     ) if prioritas_output['rendah'] else None
    maksimum_s = max(prioritas_output['sedang']
                     ) if prioritas_output['sedang'] else None
    maksimum_t = max(prioritas_output['tinggi']
                     ) if prioritas_output['tinggi'] else None
    maksimum_st = max(
        prioritas_output['sangat tinggi']) if prioritas_output['sangat tinggi'] else None

    prioritas_output['sangat rendah'] = [
        maksimum_sr] if maksimum_sr is not None else []
    prioritas_output['rendah'] = [maksimum_r] if maksimum_r is not None else []
    prioritas_output['sedang'] = [maksimum_s] if maksimum_s is not None else []
    prioritas_output['tinggi'] = [maksimum_t] if maksimum_t is not None else []
    prioritas_output['sangat tinggi'] = [
        maksimum_st] if maksimum_st is not None else []

    maksimum_ssd = max(jumlah_output['sangat sedikit']
                       ) if jumlah_output['sangat sedikit'] else None
    maksimum_sd = max(jumlah_output['sedikit']
                      ) if jumlah_output['sedikit'] else None
    maksimum_sg = max(jumlah_output['sedang']
                      ) if jumlah_output['sedang'] else None
    maksimum_b = max(jumlah_output['banyak']
                     ) if jumlah_output['banyak'] else None
    maksimum_sb = max(jumlah_output['sangat banyak']
                      ) if jumlah_output['sangat banyak'] else None

    jumlah_output['sangat sedikit'] = [
        maksimum_ssd] if maksimum_ssd is not None else []
    jumlah_output['sedikit'] = [maksimum_sd] if maksimum_sd is not None else []
    jumlah_output['sedang'] = [maksimum_sg] if maksimum_sg is not None else []
    jumlah_output['banyak'] = [maksimum_b] if maksimum_b is not None else []
    jumlah_output['sangat banyak'] = [
        maksimum_sb] if maksimum_sb is not None else []

    derajat_keanggotaan_prioritas = {
        'sangat rendah': [0, 1.5, 3],
        'rendah': [1, 3, 5],
        'sedang': [3, 5, 7],
        'tinggi': [5, 7, 9],
        'sangat tinggi': [7, 8.5, 10]
    }

    derajat_keanggotaan_kuantitas = {
        'sangat sedikit': [0, 10, 20],
        'sedikit': [15, 32.5, 50],
        'sedang': [40, 57.5, 75],
        'tinggi': [65, 82.5, 100],
        'sangat tinggi': [90, 105, 120]
    }

    total_sample_prioritas = 0
    numerator_sum_prioritas = 0
    denominator_sum_prioritas = 0
    total_sample_kuantitas = 0
    numerator_sum_kuantitas = 0
    denominator_sum_kuantitas = 0

    for prioritas, nilai_keanggotaan in prioritas_output.items():
        if nilai_keanggotaan:
            sample1 = derajat_keanggotaan_prioritas[prioritas][0]
            sample2 = derajat_keanggotaan_prioritas[prioritas][2]
            derajat_keanggotaan = nilai_keanggotaan[0]

            total_sample_prioritas += 2 * derajat_keanggotaan
            numerator_sum_prioritas += (sample1 +
                                        sample2) * derajat_keanggotaan
            denominator_sum_prioritas += 2 * derajat_keanggotaan

    for kuantitas, nilai_keanggotaan in jumlah_output.items():
        if nilai_keanggotaan:
            sample1 = derajat_keanggotaan_kuantitas[kuantitas][0]
            sample2 = derajat_keanggotaan_kuantitas[kuantitas][2]
            derajat_keanggotaan = nilai_keanggotaan[0]

            total_sample_kuantitas += 2 * derajat_keanggotaan
            numerator_sum_kuantitas += (sample1 +
                                        sample2) * derajat_keanggotaan
            denominator_sum_kuantitas += 2 * derajat_keanggotaan

    defuzzification_prioritas = 0
    defuzzification_kuantitas = 0

    if denominator_sum_prioritas != 0:
        defuzzification_prioritas = numerator_sum_prioritas / denominator_sum_prioritas

    if denominator_sum_kuantitas != 0:
        defuzzification_kuantitas = numerator_sum_kuantitas / denominator_sum_kuantitas

    return defuzzification_prioritas, defuzzification_kuantitas
