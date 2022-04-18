from operator import index
import pandas as pd
def clean_data(df_raw):
   #Eliminar películas que se encuentran en producción
   indexes_no_released = df_raw[df_raw["status"]=='In Production'].index
   df = df_raw.drop(index = indexes_no_released)

   #ELiminar budget 0
   indexes_budget_0 = df[df["budget"]<10000].index
   df = df.drop(index = indexes_budget_0)
      
   #Eliminar filas con revenue 0
   indexes_0_re = df[df["revenue"]==0].index
   df = df.drop(index = indexes_0_re)

   #Eliminar películas sin género
   indexes_no_genres = df[df["genres"]=="[]"].index
   df = df.drop(index = indexes_no_genres)

   #Eliminar películas sin cast, crew, keywords
   indexes_no_cck = df[(df["cast"]=="[]") | (df["crew"]=="[]") | (df["keywords"]=="[]")].index
   df = df.drop(index = indexes_no_cck)

   #Peliculas con runtime 0
   indexes_no_runtime = df[(df["runtime"]==0) | (df["runtime"].isna()) | (df["runtime"]<40)].index
   df = df.drop(index = indexes_no_runtime)

   #Peliculas_no_com_coun
   indexes_no_country = df[(df["production_countries"]=="[]") | (df["production_companies"]=="[]")].index
   df = df.drop(index = indexes_no_country)

   return df