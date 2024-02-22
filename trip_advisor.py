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
        return f"Name: {self.name}\nSeason: {', '.join(self.season)}\nWeather: {', '.join(self.weather)}\nDemography: {', '.join(self.demography)}\nFoods: {', '.join(self.foods)}\n"

class VacationRecommendationSystem:
    def __init__(self, destinations):
        self.destinations = destinations

    def recommend_destination(self, season, weather, demography, foods):
        matching_destinations = []
        for destination in self.destinations:
            if (season in destination.season and
                weather in destination.weather and
                demography in destination.demography and
                any(food in destination.foods for food in foods)):
                matching_destinations.append(destination)
        return matching_destinations

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
    user_season = st.selectbox("Select your favorite season:", seasons).lower()
    user_weather = st.selectbox("Select preferred weather:", weathers).lower()
    user_demography = st.selectbox("Select your demography:", demographies).lower()
    user_foods = [st.selectbox("Select preferred food {}: ".format(i), foods).lower() for i in range(1, 4)]

    # Get recommendations
    recommendations = recommendation_system.recommend_destination(user_season, user_weather, user_demography, user_foods)

    # Display recommendations
    if recommendations:
        st.header("Here are some vacation destinations matching your preferences:")
        for destination in recommendations:
            st.write(destination)
    else:
        st.write("Sorry, we couldn't find any matching destinations for your preferences. Here's a random suggestion:")
        random_destination = recommendation_system.predict_random_destination()
        st.write(random_destination)

if __name__ == "__main__":
    main()
