import pandas as pd
import regex as re
import os

os.chdir(os.path.dirname(__file__))

path_o = str(os.getcwd()).split("\\")
path_o = "\\".join(path_o[:-1])
os.chdir(path_o+"\\data\\raw")
print(os.getcwd())

def clean_data_2(df):
   path_o = str(os.getcwd()).split("\\")
   path_o = "\\".join(path_o[:-1])
   os.chdir(path_o+"\\data\\raw")
   print(os.getcwd())
   copy_df = df.copy()
   #Type fecha columna release date
   copy_df[['year', 'month', 'day']] = copy_df['release_date'].str.split('-', expand=True)
   copy_df["release_date"] = pd.to_datetime(copy_df["release_date"])
   copy_df['year'] = copy_df['year'].astype(int)
   copy_df['month'] = copy_df['month'].astype(int)
   copy_df['day'] = copy_df['day'].astype(int)

    #Extrar informacion genres por película
   list_genres_principal = []
   list_genres = []
   for k in copy_df["genres"].values:
      r1 = re.findall(r"'name':\s'([.\w\s]+)\'", k)
      list_genres_principal.append(r1[0])
      list_genres.append(r1)
   copy_df["genres"] = list_genres_principal
   copy_df["genres_all"] = list_genres

    #Extrar informacion de las compañias en produccion
   list_companies = []
   list_companies_principal = []
   for l in copy_df["production_companies"].values:
      r2 = re.findall(r"'name':\s[\'|\"]([.\w\d\s-&()'\.,\|/\"+–]*)[\"|\'], 'or", l)
      list_companies.append(r2)
      list_companies_principal.append(r2[0])
   copy_df["production_companies"] = list_companies_principal
   copy_df["production_companies_all"] = list_companies
   #print(list_companies)

    #Extrar informacion de los países en produccion
   list_countries = []
   list_countries_principal = []
   for m in copy_df["production_countries"].values:
      r3 = re.findall(r"'name':\s'([.\w\s]+)\'", m)
      list_countries.append(r3)
      list_countries_principal.append(r3[0])      
   copy_df["production_countries"] = list_countries_principal
   copy_df["production_countries_all"] = list_countries
   #print(list_countries)

     #Extrar informacion de los lenguajes hablados en la película
   list_spoken_languages = []
   list_spoken_languages_principal = []
   for p in copy_df["spoken_languages"].values:
      r4 = re.findall(r"'english_name':\s'([.\w\s]+)\'", p)
      list_spoken_languages.append(r4)
      try:
         list_spoken_languages_principal.append(r4[0])
      except:
         list_spoken_languages_principal.append("Cambiar")
   copy_df["spoken_languages"] = list_spoken_languages_principal
   copy_df["spoken_languages_all"] = list_spoken_languages

    #Crear columna market share por genero
   market_share = copy_df.groupby(["year","genres"]).sum().reset_index().copy()
   market_share = market_share.merge(copy_df.groupby(["year"]).sum()[["revenue"]].reset_index().rename(columns={"revenue":"revenue_year"}), on="year")
   market_share["market_share_genres"] = market_share["revenue"] / market_share["revenue_year"]
   market_share = market_share[["year","genres", "market_share_genres"]]
   copy_df = copy_df.merge(market_share, on=["genres", "year"], how="right")

   copy_df.loc[697, "spoken_languages"] = "Turkish"
   copy_df.loc[2707, "spoken_languages"] = "English"
   copy_df.loc[2874, "spoken_languages"] = "English"
   copy_df.loc[5139, "spoken_languages"] = "English"
   copy_df.loc[5236, "spoken_languages"] = "English"
   copy_df.loc[5273, "spoken_languages"] = "English"

   copy_df.loc[697, "spoken_languages_all"] = "[Turkish]"
   copy_df.loc[2707, "spoken_languages_all"] = "[English]"
   copy_df.loc[2874, "spoken_languages_all"] = "[English]"
   copy_df.loc[5139, "spoken_languages_all"] = "[English]"
   copy_df.loc[5236, "spoken_languages_all"] = "[English]"
   copy_df.loc[5273, "spoken_languages_all"] = "[English]"

     #Extrar informacion de las palabras claves por película
   list_keywords = []
   list_keywords_principal = []
   for o in copy_df["keywords"].values:
      r5 = re.findall(r"'name':\s[\'|\"]([.\w\s-,()\']+)[\'|\"]", o)
      list_keywords_principal.append(r5[0])
      list_keywords.append(r5)
   copy_df["keywords"] = list_keywords_principal
   copy_df["keywords_all"] = list_keywords

     #Extrar informacion del reparto por película
   list_cast = []
   list_cast_principal = []
   for q in copy_df["cast"].values:
      r6 = re.findall(r"\'original_name\': \'([.\w\s-]+)\'", q)
      list_cast_principal.append(r6[0])
      list_cast.append(r6)
   copy_df["cast"] = list_cast_principal
   copy_df["cast_all"] = list_cast 

   #ELiminar registros con no director
   index_no_director = copy_df[~copy_df["crew"].str.contains("'Director'")].index
   copy_df.drop(index = index_no_director, inplace = True)

     #Extrar informacion del director de cada película
   list_director = []
   count = 0
   count_l = []
   for r in copy_df["crew"].values:
      str_crew = str(r)
      count += 1      
      for s in str_crew.split("}, {'"):                  
         if "'job': 'Director'" in s:            
               count_l.append(count)              
               r7 = re.findall(r"'original_name': [\'|\"]([.\w\s'“”,-]+)[\'|\"], 'po", s)
               list_director.append(r7[0]) 
   df = pd.DataFrame(count_l, columns=["counts"])
   df["director"] = list_director
   df.drop_duplicates(subset=['counts'], inplace=True)
   copy_df["crew"] = df["director"].values  

    #Agregar información sobre la vacunación Covid a nivel mundial
   df_vacunas = pd.read_csv("data_vaccination_covid.csv", parse_dates=["date"])[1:]
   df_vacunas = df_vacunas.groupby("date").sum().reset_index()
   df_vacunas["date"] = pd.to_datetime(df_vacunas["date"])
   copy_df = copy_df.merge(df_vacunas, left_on="release_date", right_on="date", how="left").fillna(0)

    #Agregar reporte Covid a nivel mundial
   df_report_covid = pd.read_csv("COVID_19_global_data.csv", parse_dates=["Date_reported"])
   df_report_covid = df_report_covid.groupby("Date_reported").sum().reset_index()
   df_report_covid["Date_reported"] = pd.to_datetime(df_report_covid["Date_reported"])
   copy_df = copy_df.merge(df_report_covid, left_on="release_date", right_on="Date_reported", how="left").fillna(0)

     #Inflar los valores de revenue y budget al año 2022
   df_CPI = pd.read_csv("CPI_by_year.csv").rename(columns={"CPIAUCNS":"CPI"})
   df_CPI[["year", "month", "day"]] = df_CPI["DATE"].str.split("-", expand=True)
   df_CPI = df_CPI.groupby("year").mean().loc["1970":,].reset_index()
   df_CPI.iloc[-1,1] = 287.504
   df_CPI["year"] = df_CPI["year"].astype(int)
   array_CPI = df_CPI["CPI"].values
   CPI_actual_before = []
   for p in range(len(array_CPI)):
      division = array_CPI[-1] / array_CPI[p]
      CPI_actual_before.append(division)
   df_CPI["CPI_now/before"] = CPI_actual_before
   copy_df = copy_df.merge(df_CPI, left_on="year", right_on="year")
   copy_df["revenue"] = (copy_df["CPI_now/before"]) * copy_df["revenue"]
   copy_df["budget"] =   (copy_df["CPI_now/before"]) * copy_df["budget"]
            
   #Eliminar columnas
   copy_df = copy_df[['budget', 'genres', 'popularity', 'production_companies',
      'production_countries', 'release_date', 'revenue', 'runtime',
      'spoken_languages', 'crew', 'cast', 'keywords', 'title', "year", "month", "day", "market_share_genres",
      "genres_all", "production_companies_all", "production_countries_all", "spoken_languages_all", "keywords_all", "cast_all",
      'people_vaccinated', 'people_fully_vaccinated', 'total_boosters', 'New_cases', 'New_deaths']]    

   return copy_df 