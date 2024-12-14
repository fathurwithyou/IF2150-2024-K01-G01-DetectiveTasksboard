import pandas as pd

class Victims:
    def __init__(self):
        self.victims_path = "data/victims.csv"
        self.cases_path = "data/victim_cases.csv"
        self.victims_df = pd.read_csv(self.victims_path)
        self.cases_df = pd.read_csv(self.cases_path)
        
    def get_victim_by_id(self, victim_id) -> dict:
        _df = self.victims_df.loc[self.victims_df["id"] == victim_id]
        return _df.to_dict(orient="records")[0] if not _df.empty else {}


    def get_victims(self):
        merged_df = self.victims_df.merge(self.cases_df, left_on='id', right_on='id_victim', how='left')
        merged_df['id_kasus'] = merged_df['id_kasus'].fillna(0).astype(int)
        merged_df = merged_df.fillna("not provided")
        grouped_df = merged_df.groupby(['id', 'nama', 'foto', 'nik', 'usia', 'jk', 'hasil_forensik'])['id_kasus'].apply(list).reset_index()
        return grouped_df
    
    def search_victims(self, term):
        term = term.lower()
        return self.get_victims()[
            self.get_victims().apply(
                lambda row: term in str(row.values).lower(), axis=1
            )
        ]

    def sort_victims(self):
        self.victims_df = self.victims_df.sort_values(by=["id"], ascending=True)

    def write_victims(self):
        self.victims_df.to_csv(self.victims_path, index=False)

    def add_victim(self, victim):
        new_victim_df = pd.DataFrame([victim])
        self.victims_df = pd.concat([self.victims_df, new_victim_df], ignore_index=True)
        self.sort_victims()
        self.write_victims()

    def delete_victim(self, victim_id):
        self.victims_df = self.victims_df[self.victims_df["id"] != victim_id]
        self.write_victims()

    def update_victim(self, updated_victim):
        updated_row = pd.DataFrame([updated_victim], index=[0])

        for i in range(len(updated_row.columns)):
            self.victims_df.loc[
                self.victims_df["id"] == updated_row["id"].values[0], updated_row.columns[i]
            ] = updated_row[updated_row.columns[i]].values[0]

        self.sort_victims()
        self.write_victims()


    def get_last_victim_id(self):
        if not self.victims_df.empty:
            return self.victims_df["id"].max()
        return 0 