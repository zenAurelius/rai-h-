import pandas as pd

datas = pd.read_csv("./data/plat.csv")
datas.LIEUX.value_counts().to_csv('./data/plat_lieux.csv', index=True)

