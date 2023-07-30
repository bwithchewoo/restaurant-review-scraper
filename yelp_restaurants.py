import requests
import csv

url = "https://api.yelp.com/v3/businesses/search?location=11377&categories=restaurant"

headers = {"accept": "application/json",
           "Authorization": "Bearer POBPpq7oVwYqtqbTtyEr0i7WiaXgK72KUHo3fpq0SK_rEW5MYQ7IXoVm-nVoNUdxYDO-gEP-FwEIvOLsD32B810F0uTpptAZ65mVQD5HstPNYZqaRlIfoIDqcXLEZHYx"}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    # Parse the JSON data from the response
    data = response.json()
    businesses = data.get('businesses', [])

    # File name for the CSV file
    csv_file_name = 'yelp_data.csv'

    # Define the field names for the CSV header
    field_names = ['Name', 'Rating', 'Review Count', 'Latitude', 'Longitude', 'Address', 'City', 'Zip Code', 'Url']

    # Write JSON data to CSV file
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the header row to the CSV file
        csv_writer.writerow(field_names)

        # Write each business as a row in the CSV file
        for business in businesses:
            name = business.get('name', '')
            rating = business.get('rating', '')
            review_count = business.get('review_count', '')
            latitude = business.get('coordinates', {}).get('latitude', '')
            longitude = business.get('coordinates', {}).get('longitude', '')
            address = business.get('location', {}).get('address1', '')
            city = business.get('location', {}).get('city', '')
            zip_code = business.get('location', {}).get('zip_code', '')
            url = business.get('url', '')

            # Write the business data as a row in the CSV file
            csv_writer.writerow([name, rating, review_count, latitude, longitude, address, city, zip_code, url])

    print(f"CSV file '{csv_file_name}' created successfully.")
else:
    # Print an error message if the request was not successful
    print(f"Error: Request failed with status code {response.status_code}")