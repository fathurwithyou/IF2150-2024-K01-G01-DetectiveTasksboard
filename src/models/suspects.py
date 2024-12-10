import pandas as pd

class Suspects:
    def __init__(self):
        self.path = "data/suspects.csv"
        self.suspects_df = pd.read_csv(self.path)

    def get_suspects(self):
        return self.suspects_df

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
        self.suspects_df.to_csv(self.path, index=False)

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