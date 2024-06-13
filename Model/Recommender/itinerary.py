import numpy as np

def plan_tour(places, days):
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0  # Earth radius in kilometers
        dlat = np.radians(lat2 - lat1)
        dlon = np.radians(lon2 - lon1)
        a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        distance = R * c
        return distance

    def generate_tour(distance_matrix):
        num_places = len(distance_matrix)
        unvisited = set(range(1, num_places))  # Start from index 1 to skip the origin
        current = 0  # Start at the origin
        tour = [current]

        while unvisited:
            nearest = min(unvisited, key=lambda x: distance_matrix[current][x])
            tour.append(nearest)
            unvisited.remove(nearest)
            current = nearest

        return tour

    def calculate_total_distance(tour, distance_matrix):
        total_distance = 0
        for i in range(len(tour) - 1):
            total_distance += distance_matrix[tour[i]][tour[i+1]]
        return total_distance

    def print_tour(tour, places):
        plan_output = 'Route:\n'
        for index in tour:
            plan_output += ' {} ->'.format(places[index]['name'])
        plan_output = plan_output[:-2] + '\n'  # Remove the last arrow
        return plan_output

    def divide_tour_into_days(tour, places, days):
        places_per_day = [[] for _ in range(days)]
        for i, place_index in enumerate(tour):
            day_index = i % days
            places_per_day[day_index].append(place_index)
        
        day_plans = []
        for day, places_in_day in enumerate(places_per_day):
            day_plan = f"Day {day + 1}:\n"
            for place_index in places_in_day:
                day_plan += f" - {places[place_index]['name']}\n"
            day_plans.append(day_plan)
        
        return day_plans

    # Calculate distance matrix
    num_places = len(places)
    distance_matrix = np.zeros((num_places, num_places), dtype=float)

    for i in range(num_places):
        for j in range(num_places):
            if i != j:
                distance_matrix[i][j] = haversine(
                    places[i]['lat'], places[i]['lng'],
                    places[j]['lat'], places[j]['lng']
                )

    # Generate tour
    tour = generate_tour(distance_matrix)
    total_distance = calculate_total_distance(tour, distance_matrix)
    tour_plan = print_tour(tour, places)

    # Divide tour into days
    day_plans = divide_tour_into_days(tour, places, days)

    # Prepare output
    output = {
        'tour_plan': tour_plan,
        'total_distance': total_distance,
        'day_plans': day_plans
    }
    return output