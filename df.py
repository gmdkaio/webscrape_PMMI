from scrape import data_list
import pandas as pd

df = pd.DataFrame(data_list)

df.to_csv('dados_pmmi.csv', index=True)