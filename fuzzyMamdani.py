import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np


def fuzzyMamdani(stock, total_penjualan, total_pendapatan):
    # Deklarasi variabel input
    stok = ctrl.Antecedent(np.arange(0, 121, 1), 'stok')
    penjualan = ctrl.Antecedent(np.arange(0, 121, 1), 'penjualan')
    pendapatan = ctrl.Antecedent(np.arange(0, 1700001, 10000), 'pendapatan')

    # Deklarasi variabel output
    prioritas = ctrl.Consequent(np.arange(0, 11, 1), 'prioritas')
    jumlah = ctrl.Consequent(np.arange(0, 501, 1), 'jumlah')

    # Membership function untuk variabel input stok
    stok['sedikit'] = fuzz.trimf(stok.universe, [0, 0, 50])
    stok['cukup'] = fuzz.trimf(stok.universe, [30, 60, 90])
    stok['banyak'] = fuzz.trimf(stok.universe, [70, 120, 120])

    # Membership function untuk variabel input penjualan
    penjualan['sedikit'] = fuzz.trimf(penjualan.universe, [0, 0, 50])
    penjualan['sedang'] = fuzz.trimf(penjualan.universe, [30, 60, 90])
    penjualan['banyak'] = fuzz.trimf(penjualan.universe, [70, 120, 120])

    # Membership function untuk variabel input pendapatan
    pendapatan['sangat rendah'] = fuzz.trimf(
        pendapatan.universe, [0, 0, 450000])
    pendapatan['rendah'] = fuzz.trimf(
        pendapatan.universe, [50000, 450000, 850000])
    pendapatan['sedang'] = fuzz.trimf(
        pendapatan.universe, [450000, 850000, 1250000])
    pendapatan['tinggi'] = fuzz.trimf(
        pendapatan.universe, [850000, 1250000, 1650000])
    pendapatan['sangat tinggi'] = fuzz.trimf(
        pendapatan.universe, [1250000, 1700000, 1700000])

    # Membership function untuk variabel output prioritas
    prioritas['sangat rendah'] = fuzz.trimf(prioritas.universe, [0, 0, 2])
    prioritas['rendah'] = fuzz.trimf(prioritas.universe, [0, 2, 4])
    prioritas['sedang'] = fuzz.trimf(prioritas.universe, [2, 4, 6])
    prioritas['tinggi'] = fuzz.trimf(prioritas.universe, [4, 6, 8])
    prioritas['sangat tinggi'] = fuzz.trimf(prioritas.universe, [6, 8, 10])

    # Membership function untuk variabel output jumlah
    jumlah['sedikit'] = fuzz.trimf(jumlah.universe, [0, 0, 50])
    jumlah['sedang'] = fuzz.trimf(jumlah.universe, [30, 60, 90])
    jumlah['banyak'] = fuzz.trimf(jumlah.universe, [70, 120, 120])

    # Rules
    rule1 = ctrl.Rule(stok['sedikit'] & penjualan['sedikit'] &
                      pendapatan['sangat rendah'], (prioritas['sangat rendah'], jumlah['sedikit']))
    rule2 = ctrl.Rule(stok['sedikit'] & penjualan['sedikit'] &
                      pendapatan['rendah'], (prioritas['sangat rendah'], jumlah['sedikit']))
    rule3 = ctrl.Rule(stok['sedikit'] & penjualan['sedikit'] &
                      pendapatan['rendah'], (prioritas['rendah'], jumlah['sedikit']))
    rule4 = ctrl.Rule(stok['sedikit'] & penjualan['sedikit'] &
                      pendapatan['tinggi'], (prioritas['rendah'], jumlah['sedikit']))
    rule5 = ctrl.Rule(stok['sedikit'] & penjualan['sedikit'] &
                      pendapatan['sangat tinggi'], (prioritas['rendah'], jumlah['sedikit']))
    rule6 = ctrl.Rule(stok['sedikit'] & penjualan['sedang'] &
                      pendapatan['sangat rendah'], (prioritas['rendah'], jumlah['sedikit']))
    rule7 = ctrl.Rule(stok['sedikit'] & penjualan['sedang'] &
                      pendapatan['rendah'], (prioritas['rendah'], jumlah['sedikit']))
    rule8 = ctrl.Rule(stok['sedikit'] & penjualan['sedang'] &
                      pendapatan['sedang'], (prioritas['tinggi'], jumlah['banyak']))
    rule9 = ctrl.Rule(stok['sedikit'] & penjualan['sedang'] &
                      pendapatan['tinggi'], (prioritas['sangat tinggi'], jumlah['banyak']))
    rule10 = ctrl.Rule(stok['sedikit'] & penjualan['sedang'] &
                       pendapatan['sangat tinggi'], (prioritas['sangat tinggi'], jumlah['banyak']))
    rule11 = ctrl.Rule(stok['sedikit'] & penjualan['banyak'] &
                       pendapatan['sangat rendah'], (prioritas['sedang'], jumlah['sedang']))
    rule12 = ctrl.Rule(stok['sedikit'] & penjualan['banyak'] &
                       pendapatan['rendah'], (prioritas['sedang'], jumlah['sedang']))
    rule13 = ctrl.Rule(stok['sedikit'] & penjualan['banyak'] &
                       pendapatan['sedang'], (prioritas['tinggi'], jumlah['banyak']))
    rule14 = ctrl.Rule(stok['sedikit'] & penjualan['banyak'] &
                       pendapatan['tinggi'], (prioritas['sangat tinggi'], jumlah['banyak']))
    rule15 = ctrl.Rule(stok['sedikit'] & penjualan['banyak'] &
                       pendapatan['sangat tinggi'], (prioritas['sangat tinggi'], jumlah['banyak']))

    rule16 = ctrl.Rule(stok['cukup'] & penjualan['sedikit'] &
                       pendapatan['sangat rendah'], (prioritas['sangat rendah'], jumlah['sedikit']))
    rule17 = ctrl.Rule(stok['cukup'] & penjualan['sedikit'] &
                       pendapatan['rendah'], (prioritas['sangat rendah'], jumlah['sedikit']))
    rule18 = ctrl.Rule(stok['cukup'] & penjualan['sedikit'] &
                       pendapatan['sedang'], (prioritas['rendah'], jumlah['sedikit']))
    rule19 = ctrl.Rule(stok['cukup'] & penjualan['sedikit'] &
                       pendapatan['tinggi'], (prioritas['rendah'], jumlah['sedikit']))
    rule20 = ctrl.Rule(stok['cukup'] & penjualan['sedikit'] &
                       pendapatan['sangat tinggi'], (prioritas['sedang'], jumlah['sedikit']))
    rule21 = ctrl.Rule(stok['cukup'] & penjualan['sedang'] &
                       pendapatan['sangat rendah'], (prioritas['sangat rendah'], jumlah['sedikit']))
    rule22 = ctrl.Rule(stok['cukup'] & penjualan['sedang'] &
                       pendapatan['rendah'], (prioritas['rendah'], jumlah['sedikit']))
    rule23 = ctrl.Rule(stok['cukup'] & penjualan['sedang'] &
                       pendapatan['sedang'], (prioritas['sedang'], jumlah['sedikit']))
    rule24 = ctrl.Rule(stok['cukup'] & penjualan['sedang'] &
                       pendapatan['tinggi'], (prioritas['tinggi'], jumlah['sedang']))
    rule25 = ctrl.Rule(stok['cukup'] & penjualan['sedang'] &
                       pendapatan['sangat tinggi'], (prioritas['sangat tinggi'], jumlah['sedang']))
    rule26 = ctrl.Rule(stok['cukup'] & penjualan['banyak'] &
                       pendapatan['sangat rendah'], (prioritas['sedang'], jumlah['sedang']))
    rule27 = ctrl.Rule(stok['cukup'] & penjualan['banyak'] &
                       pendapatan['rendah'], (prioritas['sedang'], jumlah['sedang']))
    rule28 = ctrl.Rule(stok['cukup'] & penjualan['banyak'] &
                       pendapatan['sedang'], (prioritas['tinggi'], jumlah['sedang']))
    rule29 = ctrl.Rule(stok['cukup'] & penjualan['banyak'] &
                       pendapatan['tinggi'], (prioritas['tinggi'], jumlah['sedang']))
    rule30 = ctrl.Rule(stok['cukup'] & penjualan['banyak'] &
                       pendapatan['sangat tinggi'], (prioritas['sangat tinggi'], jumlah['sedang']))

    rule31 = ctrl.Rule(stok['banyak'] & penjualan['sedikit'] &
                       pendapatan['sangat rendah'], (prioritas['sangat rendah'], jumlah['sedikit']))
    rule32 = ctrl.Rule(stok['banyak'] & penjualan['sedikit'] &
                       pendapatan['rendah'], (prioritas['sangat rendah'], jumlah['sedikit']))
    rule33 = ctrl.Rule(stok['banyak'] & penjualan['sedikit'] &
                       pendapatan['sedang'], (prioritas['sangat rendah'], jumlah['sedikit']))
    rule34 = ctrl.Rule(stok['banyak'] & penjualan['sedikit'] &
                       pendapatan['tinggi'], (prioritas['sangat rendah'], jumlah['sedikit']))
    rule35 = ctrl.Rule(stok['banyak'] & penjualan['sedikit'] &
                       pendapatan['sangat tinggi'], (prioritas['sangat rendah'], jumlah['sedikit']))
    rule36 = ctrl.Rule(stok['banyak'] & penjualan['sedang'] &
                       pendapatan['sangat rendah'], (prioritas['rendah'], jumlah['sedikit']))
    rule37 = ctrl.Rule(stok['banyak'] & penjualan['sedang'] &
                       pendapatan['rendah'], (prioritas['rendah'], jumlah['sedikit']))
    rule38 = ctrl.Rule(stok['banyak'] & penjualan['sedang'] &
                       pendapatan['sedang'], (prioritas['sedang'], jumlah['sedikit']))
    rule39 = ctrl.Rule(stok['banyak'] & penjualan['sedang'] &
                       pendapatan['tinggi'], (prioritas['tinggi'], jumlah['sedikit']))
    rule40 = ctrl.Rule(stok['banyak'] & penjualan['sedang'] &
                       pendapatan['sangat tinggi'], (prioritas['sangat tinggi'], jumlah['sedikit']))

    # Pembuatan system kontrol
    prioritas_jumlah_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9,
                                                rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17,
                                                rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25,
                                                rule26, rule27, rule28, rule29, rule30, rule31, rule32, rule33, rule34, rule35, rule36, rule37, rule38, rule39, rule40])

    # Proses simulasi
    prioritas_jumlah = ctrl.ControlSystemSimulation(prioritas_jumlah_ctrl)

    # Mengisi nilai input
    prioritas_jumlah.input['stok'] = int(stock)
    prioritas_jumlah.input['penjualan'] = int(total_penjualan)
    prioritas_jumlah.input['pendapatan'] = int(total_pendapatan)

    # Perhitungan nilai output
    prioritas_jumlah.compute()

    hasil_Prioritas = prioritas_jumlah.output['prioritas']
    hasil_jumlah = prioritas_jumlah.output['jumlah']

    # Menampilkan hasil output
    # print('===============================================')
    # print('Masker Prioritas (0 - 10): ', prioritas_jumlah.output['prioritas'])
    # print('Jumlah Masker yang harus diberli (0 - 500) : ',
    #       prioritas_jumlah.output['jumlah'])
    return hasil_Prioritas, hasil_jumlah
