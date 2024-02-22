import csv
import random
import streamlit as st

class VacationDestination:
    def __init__(self, name, season, weather, demography, foods):
        self.name = name
        self.season = season
        self.weather = weather
        self.demography = demography
        self.foods = foods

    def __str__(self):
        return f"Name: {self.name}\n\nSeason: {', '.join(self.season)}\n\nWeather: {', '.join(self.weather)}\n\nDemography: {', '.join(self.demography)}\n\nFoods: {', '.join(self.foods)}\n\n"

class VacationRecommendationSystem:
    def __init__(self, destinations):
        self.destinations = destinations

    def recommend_destination(self, seasons, weathers, demographies, foods):
        matching_destinations = []
        for destination in self.destinations:
            if (any(season in destination.season for season in seasons) or
                any(weather in destination.weather for weather in weathers) or
                any(demography in destination.demography for demography in demographies) or
                any(food in destination.foods for food in foods)):
                matching_destinations.append(destination)
        return matching_destinations[:5]

    def predict_random_destination(self):
        # You can define your criteria for random selection here
        return random.choice(self.destinations)

# Load destinations from CSV
def load_destinations_from_csv(filename):
    destinations = []
    with open(filename, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Place Name']
            season = row['Season'].split(',')
            weather = row['Weather'].split(',')
            demography = row['Demography'].split(',')
            foods = [row['Food1'], row['Food2'], row['Food3']]
            destinations.append(VacationDestination(name, season, weather, demography, foods))
    return destinations

# Streamlit UI
def main():
    st.title("Vacation Destination Recommender")

    # Load destinations from CSV file
    destinations_data = load_destinations_from_csv('destinations.csv')

    # Initialize recommendation system
    recommendation_system = VacationRecommendationSystem(destinations_data)

    # Define options for dropdown menus
    seasons = sorted(set(sum([destination.season for destination in destinations_data], [])))
    weathers = sorted(set(sum([destination.weather for destination in destinations_data], [])))
    demographies = sorted(set(sum([destination.demography for destination in destinations_data], [])))
    foods = sorted(set(sum([destination.foods for destination in destinations_data], [])))

    # User input
    user_seasons = st.multiselect("Select your favorite season:", seasons)
    user_weathers = st.multiselect("Select preferred weather:", weathers)
    user_demographies = st.multiselect("Select your demography:", demographies)
    user_foods = st.multiselect("Select preferred foods: ", foods)

    # Get recommendations
    recommendations = recommendation_system.recommend_destination(user_seasons, user_weathers, user_demographies, user_foods)

    # Display recommendations
    if recommendations:
        st.header("Here are some vacation destinations matching your preferences:")
        for destination in recommendations:
            st.success(destination)
    else:
        st.write("Sorry, we couldn't find any matching destinations for your preferences. Here's a random suggestion:")
        random_destination = recommendation_system.predict_random_destination()
        st.success(random_destination)

if __name__ == "__main__":
    main()
