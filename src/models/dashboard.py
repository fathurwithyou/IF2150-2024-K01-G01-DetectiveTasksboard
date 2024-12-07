import pandas as pd

def get_not_done_cases(csv_file):
    cases_df = pd.read_csv(csv_file)

    not_done_cases = cases_df[~cases_df['status'].isin(['Selesai'])]

    case_data = []
    for _, row in not_done_cases.iterrows():
        case_data.append({
            'id': row['id'],
            'judul': row['judul'],
            'status': row['status'],
            'tanggal_mulai': row['tanggal_mulai'],
            'tanggal_selesai': row['tanggal_selesai'] if pd.notna(row['tanggal_selesai']) else "Ongoing",
        })
    
    return case_data
