import pandas as pd
from models.dashboard import Dashboard
from models.suspects import Suspects
from models.victims import Victims
from models.detectives import Detectives

class Cases:
    def __init__(self):
        self.cases_df = pd.read_csv("data/cases.csv")

    def get_cases(self):
        return self.cases_df

    def sort_cases(self):
        # sort by status, then by tanggal_mulai
        self.cases_df = self.cases_df.sort_values(by=['status', 'tanggal_mulai'], ascending=[False, True])
    
    def write_cases(self):
        self.cases_df.to_csv(self.path, index=False)
    
    def add_case(self, case):
        self.cases_df = self.cases_df.append(case, ignore_index=True)
        self.sort_cases()
        self.write_cases()
    
    
        
    
    