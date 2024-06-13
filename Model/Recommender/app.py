from flask import Flask, request, jsonify
from itinerary import plan_tour
from recsys import recommendation

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/recommend', methods=['GET'])
def get_recommendation():
    city = request.args.get('city')
    categories = request.args.get('categories')
    days= request.args.get('days')
    
    # Parse category preferences
    category_preferences = [(cat.split(':')[0], int(cat.split(':')[1])) for cat in categories.split(',')]
    result = recommendation(city, category_preferences, days).to_dict(orient='records')       
    return jsonify(result)

@app.route('/plan', methods=['GET'])
def itinerary_plan():
    city = request.args.get('city')
    categories = request.args.get('categories')
    days= int(request.args.get('days'))
    category_preferences = [(cat.split(':')[0], int(cat.split(':')[1])) for cat in categories.split(',')]
    recommendations = recommendation(city, category_preferences, days)

    places = {}

    for idx, row in recommendations.iterrows():
        # Handle Coordinate string which is in JSON format
        coordinate_dict = eval(row['Coordinate'])  # Convert JSON string to dictionary
        lat = float(coordinate_dict['lat'])  
        lng = float(coordinate_dict['lng']) 
        places[idx] = {
            'name': row['Place_Name'],
            'lat': lat,
            'lng': lng
        }

    result = plan_tour(places, days)
    day_plans = result['day_plans']
    return jsonify(day_plans=day_plans)

if __name__ == '__main__':
    app.run(debug=True)