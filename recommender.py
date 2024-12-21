import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
 
import warnings
warnings.filterwarnings('ignore')


def get_similarities(song_name, data, song_vectorizer):
   
  # Getting vector for the input song.
  text_array1 = song_vectorizer[0].transform(data[data['track_name']==song_name]['genre']).toarray()
  num_array1 = data[data['track_name']==song_name].select_dtypes(include=np.number).to_numpy()
   
  # We will store similarity for each row of the dataset.
  sim = []
  for idx, row in data.iterrows():
    name = row['track_name']
     
    # Getting vector for current song.
    text_array2 = song_vectorizer.transform(data[data['track_name']==name]['genre']).toarray()
    num_array2 = data[data['track_name']==name].select_dtypes(include=np.number).to_numpy()
 
    # Calculating similarities for text as well as numeric features
    text_sim = cosine_similarity(text_array1, text_array2)[0][0]
    num_sim = cosine_similarity(num_array1, num_array2)[0][0]
    sim.append(text_sim + num_sim)
     
  return sim


def recommend_songs(song_name, songs_data):
  # Base case
  data = songs_data.copy()
  if data[data['track_name'] == song_name].shape[0] == 0:
    print('Вы ввели неизвестное название песни.')
    print('Вот другие песни, которые вам могут понравиться:\n')
     
    for song in data.sample(n=5)['track_name'].values:
      print(song)
    return
   
  data['similarity_factor'] = get_similarities(song_name, data)
 
  data.sort_values(by=['similarity_factor'],
                   ascending = [False],
                   inplace=True)
   
  # First song will be the input song itself as the similarity will be highest.
  return data[['track_name', 'artist_name', 'genre']][2:7].values.tolist()

def recommend_new_user(genres, songs_data):
  '''
  Рекомендации для новых пользователей (на основе жанров)
  '''
  data = songs_data.copy()
  data = data[data['genre'].isin(genres)]
  return data[['track_name', 'artist_name', 'genre']][:7].values.tolist()
