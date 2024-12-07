import pandas as pd

class Detective:
    def __init__(self):
        self.path = "data/detectives.csv"
        self.detective_df = pd.read_csv(self.path)

    def get_detectives(self):
        return self.detective_df

    def search_detectives(self, term):
        term = term.lower()
        return self.detective_df[
            self.detective_df.apply(
                lambda row: term in str(row.values).lower(), axis=1
            )
        ]

    def sort_detectives(self):
        self.detective_df = self.detective_df.sort_values(by=["id"], ascending=True)

    def write_detectives(self):
        self.detective_df.to_csv(self.path, index=False)

    def add_detective(self, detective):
        new_detective_df = pd.DataFrame([detective])
        self.detective_df = pd.concat([self.detective_df, new_detective_df], ignore_index=True)
        self.sort_detectives()
        self.write_detectives()

    def delete_detective(self, detective_id):
        self.detective_df = self.detective_df[self.detective_df["id"] != detective_id]
        self.write_detectives()

    def update_detective(self, updated_detective):
        updated_row = pd.DataFrame([updated_detective], index=[0])

        for i in range(len(updated_row.columns)):
            self.detective_df.loc[
                self.detective_df["id"] == updated_row["id"].values[0], updated_row.columns[i]
            ] = updated_row[updated_row.columns[i]].values[0]

        self.sort_detectives()
        self.write_detectives()

    def get_last_detective_id(self):
        if not self.detective_df.empty:
            return self.detective_df["id"].max()
        return 0