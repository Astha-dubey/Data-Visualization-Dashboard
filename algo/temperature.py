import requests
import matplotlib.pyplot as plt

def createTemperatureChart():
    api_url = f'https://api.tomorrow.io/v4/weather/forecast?location=sagar&apikey=2BIqri7cEZFymyAp1sNf57tgukOgQzW7'
    
    # Make the API request
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract temperature data from the response's "minutely" timeline
        temperature_values = [entry['values']['temperature'] for entry in data['timelines']['minutely']]
        
        # Create a time series for the x-axis (in this case, use the index)
        time_series = list(range(len(temperature_values)))

        # Create a line graph for temperature
        plt.plot(time_series, temperature_values, marker='o', linestyle='-')
        
        # Add temperature labels directly above the data points
        for x, y in zip(time_series, temperature_values):
            plt.annotate(f'', (x, y), textcoords='offset points', xytext=(0,10), ha='center')
        
        plt.xlabel('Time (minutes)')
        plt.ylabel('Temperature (°C)')
        plt.title('Minute-by-Minute Temperature Forecast')
        plt.grid(True)
        plt.show()
    else:
        print(f'Failed to fetch data from the API. Status Code: {response.status_code}')

createTemperatureChart()
