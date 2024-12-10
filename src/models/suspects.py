import pandas as pd

class Suspects:
    def __init__(self):
        self.suspects_path = "data/suspects.csv"
        self.cases_path = "data/suspects_cases.csv"
        self.suspects_df = pd.read_csv(self.suspects_path)
        self.cases_df = pd.read_csv(self.cases_path)

    def get_suspects(self):
        merged_df = self.suspects_df.merge(self.cases_df, left_on='id', right_on='id_suspect', how='left')
        merged_df['id_kasus'] = merged_df['id_kasus'].fillna(0).astype(int)
        merged_df = merged_df.fillna("not provided")
        grouped_df = merged_df.groupby(['id','nama','foto','nik','usia','jk','catatan_kriminal'])['id_kasus'].apply(list).reset_index()
        return grouped_df

    def search_suspects(self, term):
        term = term.lower()
        return self.suspects_df[
            self.suspects_df.apply(
                lambda row: term in str(row.values).lower(), axis=1
            )
        ]

    def sort_suspects(self):
        self.suspects_df = self.suspects_df.sort_values(by=["id"], ascending=True)

    def write_suspects(self):
        self.suspects_df.to_csv(self.suspects_path, index=False)

    def add_suspect(self, suspect):
        new_suspect_df = pd.DataFrame([suspect])
        self.suspects_df = pd.concat([self.suspects_df, new_suspect_df], ignore_index=True)
        self.sort_suspects()
        self.write_suspects()

    def delete_suspect(self, suspect_id):
        self.suspects_df = self.suspects_df[self.suspects_df["id"] != suspect_id]
        self.write_suspects()

    def update_suspect(self, updated_suspect):
        updated_row = pd.DataFrame([updated_suspect], index=[0])

        for i in range(len(updated_row.columns)):
            self.suspects_df.loc[
                self.suspects_df["id"] == updated_row["id"].values[0], updated_row.columns[i]
            ] = updated_row[updated_row.columns[i]].values[0]

        self.sort_suspects()
        self.write_suspects()

    def get_last_suspect_id(self):
        if not self.suspects_df.empty:
            return self.suspects_df["id"].max()
        return 0