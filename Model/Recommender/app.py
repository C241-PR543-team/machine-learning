from flask import Flask, request, jsonify
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

app = Flask(__name__)

# Load your DataFrame df2
df2 = pd.read_csv("./Model/Recommender/data.csv")
df2["Category"] = df2["Category"].str.replace("'", "")
df2['Category'] = df2['Category'].str.strip('[]')
df2.drop("Unnamed: 0", axis=1, inplace=True)

def recommendation(city, categories):
    data = df2[(df2['City'] == city) & (df2['Category'].str.contains('|'.join(categories), case=False, na=False))]
    if data.empty:
        return "Tidak ada tempat wisata dalam kategori yang dicari di kota ini."
    data.reset_index(drop=True, inplace=True)

    # Convert each place name into vectors using TF-IDF and bigram
    tf = TfidfVectorizer(analyzer='word', ngram_range=(2, 2), min_df=1, stop_words='english')
    tfidf_matrix = tf.fit_transform(data['Place_Name'])

    # Calculate the similarity between place names using cosine similarity
    sg = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get the index corresponding to place names
    sig = list(enumerate(sg[-1]))
    sig = sorted(sig, key=lambda x: x[1], reverse=True)

    # Top 10 recommendations
    top_10_indices = [i[0] for i in sig[1:11]]
    recommendations = data.iloc[top_10_indices][['Place_Name', 'City', "Price", "Category"]]

    return recommendations.to_dict(orient='records')

@app.route('/recommend', methods=['GET'])
def get_recommendation():
    city = request.args.get('city')
    categories = request.args.get('categories').split(',')
    result = recommendation(city, categories)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
