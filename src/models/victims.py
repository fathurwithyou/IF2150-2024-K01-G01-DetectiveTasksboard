import pandas as pd

class Victims:
    def __init__(self):
        self.path = "data/victims.csv"
        self.victims_df = pd.read_csv(self.path)

    def get_victims(self):
        return self.victims_df

    def search_victims(self, term):
        term = term.lower()
        return self.victims_df[
            self.victims_df.apply(
                lambda row: term in str(row.values).lower(), axis=1
            )
        ]

    def sort_victims(self):
        self.victims_df = self.victims_df.sort_values(by=["id"], ascending=True)

    def write_victims(self):
        self.victims_df.to_csv(self.path, index=False)

    def add_victim(self, victim):
        new_victim_df = pd.DataFrame([victim])
        self.victims_df = pd.concat([self.victims_df, new_victim_df], ignore_index=True)
        self.sort_victims()
        self.write_victims()
