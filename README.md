<<<<<<< HEAD
# rihal-machine-learning-challenge
This repository contains solution for CityX Machine Learning challenge
=======
🚔 Crime Report Analysis & Prediction
📌 Overview
This project analyzes crime reports using machine learning and data visualization. The goal is to extract key information, visualize crime hotspots, and predict crime categories based on historical data.

📂 Dataset
The project works with three CSV files containing crime reports with details such as date, location, crime category, and resolution.

🔧 Technologies Used
The project leverages Python and several key libraries:

📊 Data Analysis & Visualization
pandas → Data manipulation

numpy → Numerical computations

matplotlib.pyplot → Data visualization

seaborn → Advanced statistical plots

folium → Interactive crime maps

🤖 Machine Learning
sklearn.model_selection → Train-test splitting

sklearn.feature_extraction.text.TfidfVectorizer → Text vectorization

sklearn.naive_bayes.MultinomialNB → Naïve Bayes classifier

sklearn.pipeline.make_pipeline → Machine learning pipeline

sklearn.metrics → Model evaluation (confusion matrix, classification report)

🗺️ Crime Visualization
Crime data is displayed on an interactive map using folium. Features include:
✅ Heatmaps to highlight crime-dense areas
✅ Markers for crime epicenters
✅ Clusters to group similar incidents

🚀 Crime Prediction
A Naïve Bayes classifier is trained to predict crime categories based on textual descriptions.

🔨 How to Run
1️⃣ Install dependencies:

bash
Copier
Modifier
pip install pandas numpy matplotlib seaborn scikit-learn folium
2️⃣ Load and process the crime dataset.
3️⃣ Train the Naïve Bayes model and visualize the predictions.
4️⃣ Generate interactive crime maps with folium.

📜 Results
Model performance is evaluated using a confusion matrix and classification report.

Crime trends are visualized through heatmaps and statistical plots.

🏗️ Future Enhancements
Improve model accuracy with advanced NLP techniques.

Integrate real-time crime data for live predictions.

Deploy as a web application using Streamlit.
>>>>>>> ef88ba5 (Create README.md)
