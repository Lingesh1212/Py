from flask import Flask, render_template, request
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Updated sample data for demonstration
data = {
    'Trees': [50, 200, 500, 700, 1000],
    'Residents': [50, 200, 500, 700, 1000],
    '2Wheelers': [50, 200, 500, 700, 1000],
    '4Wheelers': [50, 200, 500, 700, 1000],
    'AirQuality': [10, 25, 50, 75, 100]  # Representing air quality as a percentage
}

df = pd.DataFrame(data)

# Assign weights to features
weights = {
    'Trees': 3,        # Higher weight for Trees
    'Residents': 2,
    '2Wheelers': 0.5,
    '4Wheelers': 1
}

# Apply weights to the features
for feature, weight in weights.items():
    df[feature] *= weight

# Training KNN model
X = df[['Trees', '2Wheelers', '4Wheelers', 'Residents']]
y = df['AirQuality']
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    # Get input data from the form
    trees = int(request.form['trees'])
    residents = int(request.form['residents'])
    two_wheelers = int(request.form['two_wheelers'])
    four_wheelers = int(request.form['four_wheelers'])

    # Apply weights to the input features
    trees_weighted = trees * weights['Trees']
    residents_weighted = residents * weights['Residents']
    two_wheelers_weighted = two_wheelers * weights['2Wheelers']
    four_wheelers_weighted = four_wheelers * weights['4Wheelers']

    # Predict air quality using the trained KNN model
    prediction = knn.predict([[trees_weighted, two_wheelers_weighted, four_wheelers_weighted, residents_weighted]])[0]

    # Data for charts
    chart_data = df.sum().to_dict()

    # Plot pie chart
    pie_chart = plt.figure(figsize=(7, 7))
    plt.pie([chart_data['2Wheelers'], chart_data['4Wheelers']], labels=['2 Wheelers', '4 Wheelers'], autopct='%1.1f%%')
    pie_chart_data = get_image_data(pie_chart)

    # Plot bar chart with weighted data
    bar_chart = plt.figure(figsize=(8, 5))
    plt.bar(df.columns[:-1], df.mean()[:-1])  # Use mean() for 'AirQuality'
    bar_chart_data = get_image_data(bar_chart)

    # Plot area chart with weighted data
    area_chart = plt.figure(figsize=(8, 5))
    plt.stackplot(df.index, df['Residents'], df['2Wheelers'], df['4Wheelers'], labels=['Residents', '2 Wheelers', '4 Wheelers'])
    plt.legend(loc='upper left')
    area_chart_data = get_image_data(area_chart)

    return render_template('result.html', prediction=prediction, pie_chart=pie_chart_data,
                           bar_chart=bar_chart_data, area_chart=area_chart_data)


def get_image_data(chart):
    buffer = BytesIO()
    chart.savefig(buffer, format='png')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.read()).decode('utf-8')
    return chart_data


if __name__ == '__main__':
    app.run(debug=True)
