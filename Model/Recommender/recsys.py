import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def recommendation(city, category_preferences, days):
    # Load DataFrame 
    df = pd.read_csv("./Model/Recommender/data.csv")
    df["Category"] = df["Category"].str.replace("'", "")
    df['Category'] = df['Category'].str.strip('[]')
    df.drop("Unnamed: 0", axis=1, inplace=True)

    # Filter data by city
    data = df[df['City'] == city]
    if data.empty:
        return "Tidak ada tempat wisata dalam kategori yang dicari di kota ini."
    
    # Split categories and preferences
    categories = [category for category, score in category_preferences]
    
    # Filter data by categories
    data = data[data['Category'].str.contains('|'.join(categories), case=False, na=False)]
    if data.empty:
        return "Tidak ada tempat wisata dalam kategori yang dicari di kota ini."
    
    # Weight categories by preferences
    data['Weight'] = data['Category'].apply(lambda x: sum(score for category, score in category_preferences if category in x))
    
    # Sort data by weight
    data = data.sort_values(by='Weight', ascending=False)
    data.reset_index(drop=True, inplace=True)
    
    # Convert each place name into vectors using TF-IDF and bigram
    tf = TfidfVectorizer(analyzer='word', ngram_range=(2, 2), min_df=1, stop_words='english')
    tfidf_matrix = tf.fit_transform(data['Place_Name'])

    # Calculate the similarity between place names using cosine similarity
    sg = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get the index corresponding to place names
    sig = list(enumerate(sg[-1]))
    sig = sorted(sig, key=lambda x: x[1], reverse=True)

    # Top recommendations
    indices = [i[0] for i in sig[1:int(days)*2+1]]
    recommendations = data.iloc[indices][['Place_Name', 'City', "Price", "Category", "Coordinate"]]

    return recommendations
