import requests
import pandas as pd

def get_id_movie_by_year(years, api_key):
    id_movies = []
    release_date = []
    title = []
    for i in years:
        print("year:", i )
        for j in range(1,501):
            response = requests.get(f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&page={j}&primary_release_year={i}&sort_by=primary_release_date.asc')
            highest_revenue = response.json()

            first_results = highest_revenue["results"]
        
            for k in first_results:
                        
                try:                
                    release_date.append(k["release_date"])
                    title.append(k["title"])
                    print(k["release_date"])
                    print(k["title"])
                    id_movies.append(k["id"])
                    print(k["id"])   
                except:
                    release_date.append("000")
                    title.append("000")
                    id_movies.append(k["000"])
                    continue

    df_years_id_movie = pd.DataFrame(id_movies, columns=["id"])
    df_years_id_movie["date"] = release_date
    df_years_id_movie["title"] = title
    return df_years_id_movie
    

def get_info_movie_according_id(df_total, api_key):
    id_m_4 = []
    cast = []
    crew = []
    keywords = []
    adult = []
    budget = []
    genres = []
    original_langu = []
    original_title = []
    popularity = []
    production_companies = []
    production_countries = []
    release_date = []
    revenue = []
    runtime = []
    spoken_language = []
    status = []
    tagline = []
    vote_average = []
    vote_count = []
    video =[]
    title = []
    belongs_to_collection = []
    overview = []
    homepage = []
    imdb_id = []
    poster_path = []
    for q in df_total["id"].values[300001:]:
        
        response = requests.get(f'https://api.themoviedb.org/3/movie/{q}?api_key=' +  api_key + "&append_to_response=keywords,credits")
        highest_revenue = response.json()
        try:        
            id_minf = q
            cast_v = highest_revenue["credits"]["cast"]
            crew_v = highest_revenue["credits"]["crew"]
            keywords_v = highest_revenue["keywords"]["keywords"]
            adult_v = highest_revenue["adult"]
            budget_v = highest_revenue["budget"]
            genres_v = highest_revenue["genres"]
            original_langu_v = highest_revenue["original_language"]
            original_title_v = highest_revenue['original_title']
            popularity_v = highest_revenue['popularity']
            production_companies_v = highest_revenue['production_companies']
            production_countries_v = highest_revenue['production_countries']
            release_date_v = highest_revenue['release_date']
            revenue_v = highest_revenue['revenue']
            runtime_v = highest_revenue['runtime']
            spoken_language_v = highest_revenue['spoken_languages']
            status_v = highest_revenue['status']
            tagline_v = highest_revenue['tagline']
            vote_average_v = highest_revenue['vote_average']
            vote_count_v = highest_revenue['vote_count']
            video_v = highest_revenue['video']
            title_v = highest_revenue['title']
            belongs_to_collection_v = highest_revenue['belongs_to_collection']
            overview_v = highest_revenue['overview']
            homepage_v = highest_revenue['homepage']
            imdb_id_v = highest_revenue['imdb_id']
            poster_path_v = highest_revenue['poster_path']
            
        except:
            continue
        print(id_minf)
        id_m_4.append(id_minf)
        adult.append(adult_v)
        budget.append(budget_v)
        genres.append(genres_v)
        original_langu.append(original_langu_v)
        original_title.append(original_title_v)
        popularity.append(popularity_v)
        production_companies.append(production_companies_v)
        production_countries.append(production_countries_v)
        release_date.append(release_date_v)
        revenue.append(revenue_v)
        runtime.append(runtime_v)
        spoken_language.append(spoken_language_v)
        status.append(status_v)
        tagline.append(tagline_v)
        vote_average.append(vote_average_v)
        vote_count.append(vote_count_v)
        video.append(video_v)
        title.append(title_v)
        belongs_to_collection.append(belongs_to_collection_v)
        overview.append(overview_v)
        homepage.append(homepage_v)
        imdb_id.append(imdb_id_v)
        poster_path.append(poster_path_v)
        keywords.append(keywords_v)
        cast.append(cast_v)
        crew.append(crew_v)
    
    df_years_info_movie = pd.DataFrame(id_m_4, columns=["id"])
    df_years_info_movie["adult"] = adult
    df_years_info_movie["budget"] = budget
    df_years_info_movie["genres"] = genres
    df_years_info_movie["original_language"] = original_langu
    df_years_info_movie["original_title"] = original_title
    df_years_info_movie["popularity"] = popularity
    df_years_info_movie["production_companies"] = production_companies
    df_years_info_movie["production_countries"] = production_countries
    df_years_info_movie["release_date"] = release_date
    df_years_info_movie["revenue"] = revenue
    df_years_info_movie["runtime"] = runtime
    df_years_info_movie["spoken_languages"] = spoken_language
    df_years_info_movie["status"] = status
    df_years_info_movie["tagline"] = tagline
    df_years_info_movie["vote_average"] = vote_average
    df_years_info_movie["vote_count"] = vote_count
    df_years_info_movie["video"] = video
    df_years_info_movie["title"] = title
    df_years_info_movie["belongs_to_collection"] = belongs_to_collection
    df_years_info_movie["overview"] = overview
    df_years_info_movie["homepage"] = homepage
    df_years_info_movie["imdb_id"] = imdb_id
    df_years_info_movie["poster_path"] = poster_path
    df_years_info_movie["crew"] = crew
    df_years_info_movie["cast"] = cast
    df_years_info_movie["keywords"] = keywords

    return df_years_info_movie