import pandas as pd

def save(pprompt, nprompt, filter):
    idx=len(pd.read_csv("stdlist.csv"))
    new_df=pd.DataFrame({"pprompt" : pprompt,
                         "nprompt" : nprompt,
                         "filter" : filter},
                         index=[idx])
    new_df.to_csv("stdlist.csv",mode="a", header=False)
    return None

def load_list():
    data_list = []
    df = pd.read_csv("stdlist.csv")
    for i in range(len(df)):
        data_list.append(df.iloc[i].tolist())
    return data_list

def Now_idx():
    df=pd.read_csv("stdlist.csv")
    return len(df)

def load_std(idx):
    df=pd.read_csv("stdlist.csv")
    data_info=df.iloc[idx]
    return data_info

if __name__ =="__main__":
    load_list()