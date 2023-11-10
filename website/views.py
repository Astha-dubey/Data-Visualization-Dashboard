from django.shortcuts import render,HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import io
import seaborn as sns
from django.http import Http404
import matplotlib
matplotlib.use('Agg')  # Set the Agg backend
import matplotlib.pyplot as plt

def index(req):
    return HttpResponse('this is index')

def renderform(req):
    countries=["Afghanistan","Albania","Algeria","Andorra","Angola","Antigua and Barbuda","Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Brazil","Brunei","Bulgaria","Burkina Faso","Burundi","Cabo Verde","Cambodia","Cameroon","Canada","Central African Republic","Chad","Chile","China","Colombia","Comoros","Congo, Democratic Republic of the","Congo, Republic of the","Costa Rica","Côte d’Ivoire","Croatia","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","East Timor (Timor-Leste)","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Eswatini","Ethiopia","Fiji","Finland","France","Gabon","The Gambia","Georgia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Honduras","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kiribati","Korea, North","Korea, South","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia, Federated States of","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar (Burma)","Namibia","Nauru","Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","North Macedonia","Norway","Oman","Pakistan","Palau","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Qatar","Romania","Russia","Rwanda","Saint Kitts and Nevis","Saint Lucia","Saint Vincent and the Grenadines","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","Spain","Sri Lanka","Sudan","Sudan, South","Suriname","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Togo","Tonga","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"]
    return render(req,'common.html',{'mode':req.GET.get('mode'),'countries':countries,'id':req.GET.get('id')})


def graph_view(request):
    # Choose the country for which you want to create the graph
    selected_country = request.GET.get("country")

    # Load data from the CSV file (replace 'your_data.csv' with the actual CSV file path)
    data = pd.read_csv('Datasets\corruption.csv')

    # Filter data for the selected country
    country_data = data[data['country'] == selected_country]
    print(type(country_data))
    # Extract the years and data for the selected country
    years = [str(year) for year in range(1998, 2016)]
    country_values = [float(country_data[str(year)].values[0]) if str(year) in country_data.columns and country_data[str(year)].values[0] != "-" else None for year in years]

    # Create a line graph
    plt.figure(figsize=(10, 6))
    plt.plot(years, country_values, marker='o', linestyle='-')
    plt.title(f'Data for {selected_country}')
    plt.xlabel('Year')
    plt.ylabel('Data Value')
    plt.grid(True)

    # Convert the graph to a base64-encoded image
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode()

    table_data = list(zip(range(1, len(years) + 1), years, country_values))
    table_headings = ["S.No","Year", "Value"]
    return render(request, 'render.html', {
        'plot_data': plot_data,
        'label': f'Corruption Index {selected_country}',
        'table_data': table_data,
        'header': table_headings,
    })


def crime_rate_chart(request):
    # Read data from the CSV file using Pandas
    df = pd.read_csv('Datasets\crimerate.csv')
    country_name=request.GET.get("country")
    if country_name is not None:
        # Filter the data for the specified country
        df = df[df['country'] == country_name]

    # Extract the necessary columns
    years = df['year'].tolist()
    crime_rates = df['crime_rate'].tolist()

    # Create a line chart
    plt.figure(figsize=(10, 6))
    plt.plot(years, crime_rates, marker='o')
    plt.title(f'Crime Rate Over Time for {country_name}')
    plt.xlabel('Year')
    plt.ylabel('Crime Rate')
    plt.grid()

    # Save the chart as a base64-encoded image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    table_data = list(zip(range(1, len(years) + 1), years, crime_rates))
    table_headings = ["S.No","Year", "Value"]
    return render(request, 'render.html', {
        'plot_data': chart_image,
        'label': f'Crime Rate Index {country_name}',
        'table_data': table_data,
        'header': table_headings,
    })

def development_index(request):
    # Read data from the CSV file using Pandas
    df = pd.read_csv('Datasets\development index.csv')
    country_name=request.GET.get("country")
    # Check if the specified country name exists in the dataset
    if country_name is not None:
        if country_name not in df['Country Name'].values:
            raise Http404("Country not found")

        # Filter the data for the specified country
        df = df[df['Country Name'] == country_name]

    # Extract the necessary columns (years and population data)
    years = df.columns[4:].tolist()
    population = df.iloc[0, 4:].tolist()

    # Create a line chart
    plt.figure(figsize=(10, 6))
    plt.plot(years, population, marker='o')
    plt.title(f'Population Over Time for {country_name}')
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.grid()

    # Set x-axis tick frequency to display every 5 years (adjust as needed)
    tick_frequency = 5
    plt.xticks(range(0, len(years), tick_frequency), [years[i] for i in range(0, len(years), tick_frequency)], rotation=45)

    # Save the chart as a base64-encoded image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    table_data = list(zip(range(1, len(years) + 1), years, population))
    table_headings = ["S.No","Year", "Value"]
    return render(request, 'render.html', {
        'plot_data': chart_image,
        'label': f'Development Rate Index {country_name}',
        'table_data': table_data,
        'header': table_headings,
    })    

def gdp_chart(request):
    # Read data from the CSV file using Pandas
    df = pd.read_csv('Datasets\gdp.csv')
    country_name=request.GET.get("country")
    # Check if the specified country name exists in the dataset
    if country_name is not None:
        if country_name not in df['Country Name'].values:
            raise Http404("Country not found")

        # Filter the data for the specified country
        df = df[df['Country Name'] == country_name]

    # Extract the necessary columns (years and GDP data)
    years = df.columns[4:].tolist()
    gdp = df.iloc[0, 4:].tolist()

    # Create a line chart
    plt.figure(figsize=(10, 6))
    plt.plot(years, gdp, marker='o')
    plt.title(f'GDP Over Time for {country_name}')
    plt.xlabel('Year')
    plt.ylabel('GDP (current US$)')
    plt.grid()

    # Set x-axis tick frequency to display every 5 years (adjust as needed)
    tick_frequency = 5
    plt.xticks(range(0, len(years), tick_frequency), [years[i] for i in range(0, len(years), tick_frequency)], rotation=45)

    # Save the chart as a base64-encoded image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    table_headings = ["S.No","Year", "Value"]
    table_data = list(zip(range(1, len(years) + 1), years, gdp))
    return render(request, 'render.html', {
        'plot_data': chart_image,
        'label': f'GDP Growth Rate of {country_name}',
        'table_data': table_data,
        'header': table_headings,
    })  
def internet_users(request):
    # Load data from the CSV file
    data = pd.read_csv('Datasets\\net users.csv')
    country_name=request.GET.get("country")
    # Filter the data for the selected country
    selected_country_data = data[data['Country Name'] == country_name]

    if selected_country_data.empty:
        return render(request, 'error.html', {'message': 'Country not found'})

    # Define the range of years to be displayed
    start_year = 1990
    end_year = 2022

    # Extract year-wise data within the defined range
    years = [str(year) for year in range(start_year, end_year + 1)]
    internet_users = [selected_country_data[year].values[0] for year in years]
    print('------------------------------------------------------')
    print(internet_users)
    print('------------------------------------------------------')
    # Create the bar chart year-wise using Seaborn
    plt.figure(figsize=(12, 6))
    sns.barplot(x=years, y=internet_users, palette='viridis')
    plt.xlabel('Year')
    plt.ylabel('Internet Users (% of Population)')
    plt.title(f'Internet Users (% of Population) in {country_name} ({start_year}-{end_year})')

    # Rotate the year labels for better spacing
    plt.xticks(rotation=45, ha='right')

    # Save the plot as a bytes object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.read()).decode()
    buffer.close()
    table_headings = ["S.No","Year", "Value"]
    table_data = list(zip(range(1, len(years) + 1), years, internet_users))
    return render(request, 'render.html', {
        'plot_data': chart_data,
        'label': f'Statictis Internet Users in {country_name}',
        'table_data': table_data,
        'header': table_headings,
    })  

def literacy(request):
    # Load data from the CSV file
    data = pd.read_csv('Datasets\literacy.csv')
    country_name=request.GET.get("country")
    # Filter the data for the selected country
    selected_country_data = data[data['Country Name'] == country_name]

    if selected_country_data.empty:
        return render(request, 'error.html', {'message': 'Country not found'})

    # Extract year-wise data for the selected country
    years = range(1960, 2023)
    internet_users = [selected_country_data[str(year)].values[0] for year in years]

    # Create the line graph using Seaborn
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=years, y=internet_users, marker='o')
    plt.xlabel('Year')
    plt.ylabel('Internet Users (% of Population)')
    plt.title(f'Internet Users (% of Population) in {country_name} (1960-2022)')

    # Save the plot as a bytes object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.read()).decode()
    buffer.close()
    table_headings = ["S.No","Year", "Value"]
    table_data = list(zip(range(1, len(years) + 1), years, internet_users))
    return render(request, 'render.html', {
        'plot_data': chart_data,
        'label': f'Statictis Literacy Rate of {country_name}',
        'table_data': table_data,
        'header': table_headings,
    }) 

def pollution(request):
    df = pd.read_csv('Datasets\pollution.csv')
    country=request.GET.get("country")

    # Filter the DataFrame based on the selected country
    country_data = df[df['Country'] == country]
    print(country_data)
    if country_data.empty:
        return render(request, 'error.html', {'message': 'Country not found'})
    # Create the plot
    plt.plot(country_data['Year'], country_data['Value'])
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.title(f'{country} Data')

    # Convert the plot to a PNG image and store it in a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the image to base64 for displaying in your template
    image_base64 = base64.b64encode(image_png).decode()
    table_data = list(zip(country_data['Year'], country_data['Value']))
    table_headings = ["S.No","Year", ""]
    return render(request, 'render.html', {
        'plot_data': image_base64,
        'label': f'Pollution contribution by {country}',
        'table_data': table_data,
        'header': table_headings,
    }) 
    

def population(request):
    # Load data from the CSV file
    data = pd.read_csv('Datasets\populations.csv')

    country_name=request.GET.get("country")
    # Filter the data for the selected country
    selected_country_data = data[data['Country Name'] == country_name]
    print(selected_country_data)
    if selected_country_data.empty:
        return render(request, 'error.html', {'message': 'Country not found'})

    # Define the range of years to be displayed
    start_year = 1990
    end_year = 2020

    # Extract year-wise data within the defined range
    years = [str(year) for year in range(start_year, end_year + 1)]
    population = [selected_country_data[str(year)].values[0] for year in years]

    # Create the bar graph using Seaborn
    plt.figure(figsize=(12, 6))
    sns.barplot(x=years, y=population, palette='viridis')
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.title(f'Population in {country_name} ({start_year}-{end_year})')

    # Rotate the year labels for better spacing
    plt.xticks(rotation=45, ha='right')

    # Save the plot as a bytes object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.read()).decode()
    buffer.close()
    table_data = list(zip(range(1, len(years) + 1), years, population))
    table_headings = ["S.No","Year", "Value"]
    return render(request, 'render.html', {
        'plot_data': chart_data,
        'label': f'Population graph of {country_name}',
        'table_data': table_data,
        'header': table_headings,
    }) 

#TODO
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def poverty(request):
    # Load data from the CSV file
    data = pd.read_csv('Datasets/poverty.csv')  # Fix the file path here
    matplotlib.use('Agg') 
    # Get the user's selected country from the request
    user_country = request.GET.get("country")

    # Print user_country for debugging
    print(user_country)

    desired_indicator = "total poverty"
    
    # Filter the dataset to get data for the desired indicator
    filtered_df = data[data['Country Name'] == user_country]
    
    print(filtered_df)
    filtered_df=filtered_df[filtered_df['Indicator Name']==desired_indicator]
    # Check if the user's country exists in the dataset
    print(filtered_df)
    years = [str(year) for year in range(1960, 2023)]

    # Filter data for the user's selected country
    country_data = filtered_df[filtered_df['Country Name'] == user_country].iloc[:, 4:-1].values.flatten()

    # Create a line plot for the selected country
    plt.figure(figsize=(12, 6))
    plt.plot(years, country_data, marker='o', linestyle='-', color='b')
    plt.title(f'{desired_indicator} in {user_country}')
    plt.xlabel('Year')
    plt.ylabel('% of Population')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as a bytes object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.read()).decode()
    buffer.close()
    table_data = list(zip(range(1, len(years) + 1), years, country_data))
    table_headings = ["S.No","Year", "Value"]
    return render(request, 'render.html', {
        'plot_data': chart_data,
        'label': f'Poverty rate of {user_country}',
        'table_data': table_data,
        'header': table_headings
    }) 

def unemployment(request):
    # Load data from the CSV file
    data = pd.read_csv('Datasets/unemployment.csv')  # Fix the file path here
    matplotlib.use('Agg') 
    # Get the user's selected country from the request
    user_country = request.GET.get("country")

    # Print user_country for debugging
    print(user_country)

    desired_indicator = "total unemployement"
    
    # Filter the dataset to get data for the desired indicator
    filtered_df = data[data['Country Name'] == user_country]
    
    print(filtered_df)
    filtered_df=filtered_df[filtered_df['Indicator Name']==desired_indicator]
    # Check if the user's country exists in the dataset
    print(filtered_df)
    years = [str(year) for year in range(1960, 2023)]

    # Filter data for the user's selected country
    country_data = filtered_df[filtered_df['Country Name'] == user_country].iloc[:, 4:-1].values.flatten()

    # Create a line plot for the selected country
    plt.figure(figsize=(12, 6))
    plt.plot(years, country_data, marker='o', linestyle='-', color='b')
    plt.title(f'{desired_indicator} in {user_country}')
    plt.xlabel('Year')
    plt.ylabel('% of Unemployemnt')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as a bytes object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.read()).decode()
    buffer.close()
    table_data = list(zip(range(1, len(years) + 1), years, country_data))
    table_headings = ["S.No","Year", "Value"]

    return render(request, 'render.html', {
        'plot_data': chart_data,
        'label': f'Unemployment rate of {user_country}',
        'table_data': table_data,
        'header': table_headings,
    }) 



