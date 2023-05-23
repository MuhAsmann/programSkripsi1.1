# Fungsi keanggotaan triangular
def trimf(x, a, b, c):
    return max(0, min((x - a) / (b - a), (c - x) / (c - b)))

# Fungsi implikasi minimum


def impl_min(a, b):
    return min(a, b)

# Fungsi implikasi maksimum


def impl_max(a, b):
    return max(a, b)

# Fungsi defuzzifikasi centroid


def defuzz_centroid(x, membership):
    numerator = sum([x[i] * membership[i] for i in range(len(x))])
    denominator = sum(membership)
    return numerator / denominator if denominator != 0 else 0

# Fuzzifikasi variabel input


def fuzzify_input(x, sets):
    membership = []
    for set_range in sets:
        a, b, c = set_range
        membership.append(trimf(x, a, b, c))
    return membership

# Fuzzifikasi variabel output


def fuzzify_output(x, sets):
    membership = []
    for set_range in sets:
        a, b, c = set_range
        membership.append(trimf(x, a, b, c))
    return membership

# Inferensi dengan aturan-aturan fuzzy


def fuzzy_inference(stok, penjualan, pendapatan):
    # Fuzzifikasi input
    stok_membership = fuzzify_input(
        stok, [(0, 10, 20), (10, 20, 30), (20, 30, 40)])
    penjualan_membership = fuzzify_input(
        penjualan, [(0, 50, 100), (50, 100, 150), (100, 150, 200)])
    pendapatan_membership = fuzzify_input(
        pendapatan, [(0, 500, 1000), (500, 1000, 1500), (1000, 1500, 2000)])

    # Aturan fuzzy
    rule1 = impl_min(stok_membership[0], penjualan_membership[0])
    rule2 = impl_min(stok_membership[1], pendapatan_membership[1])
    rule3 = impl_min(penjualan_membership[2], pendapatan_membership[2])

    # Aggregasi aturan
    kuantitas_membership = [impl_max(rule1, 0.5), impl_max(
        rule2, rule3), impl_max(rule3, 0.5)]
    prioritas_membership = [impl_max(rule1, 0.7), impl_max(
        rule2, rule3), impl_max(rule3, 0.3)]

    return kuantitas_membership, prioritas_membership


# Defuzzifikasi
kuantitas_values = [0, 1, 2]  # Nilai-nilai kuantitas yang mungkin
prioritas_values = [0, 1, 2]  # Nilai-nilai prioritas yang mungkin
defuzzy_kuantitas = defuzz_centroid(
    kuantitas_values, fuzzy_inference(15, 80, 1200)[0])
defuzzy_prioritas = defuzz_centroid(
    prioritas_values, fuzzy_inference(15, 80, 1200)[1])

print("Kuantitas:", defuzzy_kuantitas)
print("Prioritas:", defuzzy_prioritas)
