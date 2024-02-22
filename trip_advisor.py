import csv
import streamlit as st

class VacationDestination:
    def __init__(self, name, season, weather, demography, foods):
        self.name = name
        self.season = season
        self.weather = weather
        self.demography = demography
        self.foods = foods

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

    # User input
    user_season = st.text_input("Enter your favorite season: ").lower()
    user_weather = st.text_input("Enter preferred weather: ").lower()
    user_demography = st.text_input("Enter your demography: ").lower()
    user_foods = [st.text_input("Enter preferred food: ".format(i)).lower() for i in range(1, 4)]

    # Get recommendations
    recommendations = recommendation_system.recommend_destination(user_season, user_weather, user_demography, user_foods)

    # Display recommendations
    if recommendations:
        st.header("Here are some vacation destinations matching your preferences:")
        for destination in recommendations:
            st.write(destination.name)
    else:
        st.write("Sorry, we couldn't find any matching destinations for your preferences.")

if __name__ == "__main__":
    main()
