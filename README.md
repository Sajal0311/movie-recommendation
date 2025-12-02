Movie Recommendation System with Integrated Chatbot

This project is a Movie Recommendation System designed to provide personalized movie suggestions based on user preferences and movie similarities. It integrates external APIs to fetch real-time movie details, ratings, and posters, while a chatbot enhances user interaction by offering conversational, dynamic recommendations. The system aims to deliver accurate, efficient, and user-friendly movie discovery.

Features

* Personalized movie recommendations

* Similarity-based movie analysis

* Real-time movie data fetched via APIs (e.g., TMDB)

* Chatbot for interactive suggestions

* User detail storage for enhanced personalization

* Clean and intuitive user interface

* Scalable and efficient architecture

Technologies Used

* Python

* TMDB API (or any other movie data API used)

* JSON for user data storage

* Machine Learning / Similarity Algorithms

* Chatbot Logic (rule-based or AI-based)

How It Works

* User provides movie preferences or interacts with the chatbot.

* System fetches real-time movie metadata from APIs.

* Recommendation engine analyzes similarities and user history.

* Chatbot presents personalized movie suggestions.

Installation

1. Clone the repository:

   git clone <your-repo-link>
2. Install dependencies:

   pip install -r requirements.txt

Run the project using:

* python main.py

Project Structure

/project

│── main.py  

│── recommendation_engine.py  

│── chatbot.py  

│── data/  

│── assets/  

│── requirements.txt  

│── README.md  

API Key Setup

* Create an account on TMDB (or the API provider being used).

* Generate your API key.

* Add it to the configuration file or environment variable as per project instructions.

Future Enhancements

* User login and profile dashboard

* Advanced ML-based recommendation models

* Web or mobile app interface

* Watchlist and rating system
