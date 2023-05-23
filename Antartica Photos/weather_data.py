import boto3
import requests
import datetime
import csv

# AccuWeather API details
API_KEY = 'sUjqtd0QYWrIMrxlJxHKuo5H6Ba6NXxS'
LOCATION_KEY = '231011' # location key for McMurdo station
URL = f'http://dataservice.accuweather.com/currentconditions/v1/{LOCATION_KEY}?apikey={API_KEY}'

# DynamoDB details
ARN = 'arn:aws:dynamodb:us-east-1:782863115905:table/weather_data'
TABLE_NAME = 'weather_data'

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Get the DynamoDB table
table = dynamodb.Table(TABLE_NAME)

try:
    # Get the weather data from AccuWeather
    response = requests.get(URL).json()[0]

    # Extract the relevant data
    temperature = response['Temperature']['Metric']['Value']
    wind_speed = response['Wind']['Speed']['Metric']['Value']
    precipitation = response['PrecipitationSummary']['Precipitation']['Metric']['Value']
    cloud_conditions = response['CloudCover']
    date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Put the data in DynamoDB
    table.put_item(
        Item={
            'location': 'McMurdo station, Antarctica',
            'date_time': date_time,
            'temperature': temperature,
            'wind_speed': wind_speed,
            'precipitation': precipitation,
            'cloud_conditions': cloud_conditions
        }
    )

    # Save the data to a CSV file
    csv_data = [[LOCATION_KEY, date_time, temperature, wind_speed, precipitation, cloud_conditions]]
    with open('/var/www/html/weather_data.csv', mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(csv_data)

    print('Data saved to DynamoDB and CSV')
except Exception as e:
    print(f'Error saving data to DynamoDB: {str(e)}')
