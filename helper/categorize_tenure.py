def categorize_tenure(tenure):
    if 1 <= tenure <= 12:
        return 'Pelanggan 1 Tahun'
    elif 13 <= tenure <= 24:
        return 'Pelanggan 2 Tahun'
    elif 25 <= tenure <= 36:
        return 'Pelanggan 3 Tahun'
    elif 37 <= tenure <= 48:
        return 'Pelanggan 4 Tahun'
    elif 49 <= tenure <= 60:
        return 'Pelanggan 5 Tahun'
    else:
        return 'Pelanggan lebih dari 5 Tahun'