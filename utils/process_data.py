from sklearn.preprocessing import LabelEncoder

def process_data_ML(df_raw):
    df = df_raw[['budget', 'genres', 'popularity', 'production_companies',
       'production_countries', 'revenue', 'runtime',
       'spoken_languages', 'crew', 'cast', 'keywords',
       'month', 'day', 'market_share_genres', 'people_vaccinated',
       'people_fully_vaccinated', 'total_boosters', 'New_cases', 'New_deaths']]

    encode_col = ['genres', 'production_companies','production_countries', 'spoken_languages', 'crew', 'cast', 'keywords']
    en = LabelEncoder()
    for cols in encode_col:
        df[cols] = en.fit_transform(df[cols])    

    return df 