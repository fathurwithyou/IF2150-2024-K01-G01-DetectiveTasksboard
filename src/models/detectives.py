import pandas as pd

class Detective:
    def __init__(self):
        self.detective_df = pd.read_csv("data/detectives.csv")
        
    def get_detectives(self):
        return self.detective_df
    