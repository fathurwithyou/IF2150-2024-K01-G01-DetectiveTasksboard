import pandas as pd
# from models.dashboard import Dashboard
from models.suspects import Suspects
from models.victims import Victims
from models.detectives import Detective
from typing import List, Tuple


class Cases:
    def __init__(self):
        # id,judul,status,tanggal_mulai,tanggal_selesai,perkembangan_kasus,catatan
        self.cases_df = pd.read_csv("data/cases.csv", index_col='id')
        # id_victim,id_kasus
        self.victim_id = pd.read_csv("data/victim_cases.csv")
        # id_suspect,id_kasus
        self.suspect_id = pd.read_csv("data/suspect_cases.csv")
        # id_detective,id_kasus
        self.detective_id = pd.read_csv("data/detective_cases.csv")
        # id,nama,foto,nik,usia,jk,hasil_forensik
        self.victims_df = pd.read_csv("data/victims.csv", index_col='id')
        # id,nama,foto,nik,usia,jk,catatan_kriminal
        self.suspects_df = pd.read_csv("data/suspects.csv", index_col='id')
        # id,nama,nik
        self.detectives_df = pd.read_csv("data/detectives.csv", index_col='id')
        self.path = "data/cases.csv"

    def get_suspects_by_id_kasus(self, id_kasus: int) -> pd.DataFrame:
        id_suspects = self.suspect_id.loc[self.suspect_id['id_kasus']
                                          == id_kasus]['id_suspect'].tolist()
        return self.suspects_df.loc[self.suspects_df.index.isin(id_suspects)]

    def get_victims_by_id_kasus(self, id_kasus: int) -> pd.DataFrame:
        id_victims = self.victim_id.loc[self.victim_id['id_kasus']
                                        == id_kasus]['id_victim'].tolist()
        return self.victims_df.loc[self.victims_df.index.isin(id_victims)]

    def get_detectives_by_id_kasus(self, id_kasus: int) -> pd.DataFrame:
        id_detectives = self.detective_id.loc[self.detective_id['id_kasus']
                                              == id_kasus]['id_detective'].tolist()
        return self.detectives_df.loc[self.detectives_df.index.isin(id_detectives)]

    def get_cases_info(self, id_kasus: int) -> Tuple[dict, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        case = self.cases_df.loc[self.cases_df.index == id_kasus]
        suspects = self.get_suspects_by_id_kasus(id_kasus)
        victims = self.get_victims_by_id_kasus(id_kasus)
        detectives = self.get_detectives_by_id_kasus(id_kasus)
        case = case.to_dict(orient='records')[0]
        return case, suspects, victims, detectives

    def sort_cases(self):
        self.cases_df = self.cases_df.sort_values(
            by=['status', 'tanggal_mulai'], ascending=[True, True])

    def get_cases(self):
        self.sort_cases()
        return self.cases_df

    def write_cases(self):
        self.cases_df.to_csv(self.path, index_label='id')
        
    def write_updated_case(self):
        self.suspect_id.to_csv("data/suspect_cases.csv", index=False)
        self.victim_id.to_csv("data/victim_cases.csv", index=False)
        self.detective_id.to_csv("data/detective_cases.csv", index=False)
        self.write_cases()

    def update_case(self, id_kasus, updated_case, list_of_suspect_id, list_of_victim_id, list_of_detective_id):
        """Dropping all the previous data and updating with the new one"""
        self.cases_df.drop(self.cases_df[self.cases_df.index == id_kasus].index, inplace=True)
        self.suspect_id.drop(self.suspect_id[self.suspect_id['id_kasus'] == id_kasus].index, inplace=True)
        self.victim_id.drop(self.victim_id[self.victim_id['id_kasus'] == id_kasus].index, inplace=True)
        self.detective_id.drop(self.detective_id[self.detective_id['id_kasus'] == id_kasus].index, inplace=True)
        
        for id_suspect in list_of_suspect_id:
            self.suspect_id = pd.concat([self.suspect_id, pd.DataFrame([[id_suspect, id_kasus]], columns=['id_suspect', 'id_kasus'])])
        
        for id_victim in list_of_victim_id:
            self.victim_id = pd.concat([self.victim_id, pd.DataFrame([[id_victim, id_kasus]], columns=['id_victim', 'id_kasus'])])
            
        for id_detective in list_of_detective_id:
            self.detective_id = pd.concat([self.detective_id, pd.DataFrame([[id_detective, id_kasus]], columns=['id_detective', 'id_kasus'])])
        
        self.cases_df = pd.concat([self.cases_df, pd.DataFrame([updated_case], index=[id_kasus])])
        
        self.write_updated_case()
        self.sort_cases()

    def add_case(self, case):
        new_case_df = pd.DataFrame(
            [case], index=[self.cases_df.index.max() + 1 if not self.cases_df.empty else 0])
        self.cases_df = pd.concat([self.cases_df, new_case_df])
        self.sort_cases()
        self.write_cases()
        
    def get_name_list(self, df: pd.DataFrame) -> List[str]:
        return df['nama'].tolist()

    def get_all_suspects_id(self) -> pd.DataFrame:
        return self.suspect_id
    
    def get_all_victims_id(self) -> pd.DataFrame:
        return self.victim_id
    
    def get_all_detectives_id(self) -> pd.DataFrame:
        return self.detective_id
    
    