# run in Jupyter Notebook...
import pandas as pd
data = pd.read_json("yelp-restaurants-origin.json", lines=True)

df = pd.DataFrame()
df2 = pd.DataFrame()

for index, row in data.iterrows():   
    if not row.empty:
        for cate in ['Italian','Chinese', 'Japanese', 'Indian','Mexican']:
            if row["categories"] and cate in row["categories"]:
                df = df.append(row)

idx = [0] * 5
for index, row in df.iterrows():   
    if not row.empty:
        for cate in ['Italian','Chinese', 'Japanese', 'Indian','Mexican']:
            if row["categories"] and cate in row["categories"]:           
                if cate == 'Italian' and idx[0] < 1000:
                    idx[0] += 1
                    df2 = df2.append(row)
                if cate == 'Chinese' and idx[1] < 1000:
                    idx[1] += 1
                    df2 = df2.append(row)
                if cate == 'Japanese' and idx[2] < 1000:
                    idx[2] += 1
                    df2 = df2.append(row)
                if cate =='Indian' and idx[3] < 1000:
                    idx[3] += 1
                    df2 = df2.append(row)
                if cate == 'Mexican' and idx[4] < 1000:
                    idx[4] += 1
                    df2 = df2.append(row)

df2.to_json('Data_5k_table.json', orient='table', index=False)

df2 = pd.read_json("Data_5k_table_wo_schema.json", orient='table')

df3 = df2[["address", 'business_id', 'categories', 'city', 'hours', 'is_open', 'name', 'stars', 'state']]
df3.to_json("cleanData_5k_records.json", orient="records")
