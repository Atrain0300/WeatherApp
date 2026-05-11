from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def get_weather():
    weather_data = None
    
    if request.method == "POST" and request.form.get("location"):
        location_byuser = request.form.get("location")
        location = location_byuser.strip()
        location = ",".join(location.split())

        geoapify_apikey = "6c7c42cfacb2409e96d3a8bc9d83f237"
        geoapify_url = f"https://api.geoapify.com/v1/geocode/search?text={location}&apiKey={geoapify_apikey}"
        loc_response = requests.get(geoapify_url)
        loc_data = loc_response.json()

        lat, long = loc_data["features"][0]["properties"]["lat"], loc_data["features"][0]["properties"]["lon"]
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m,wind_speed_10m"
        weather_response = requests.get(api_url)
        weather_data = weather_response.json()
        return render_template("index.html", weather_data=weather_data, location=location_byuser)
    
    return render_template("index.html", weather_data=weather_data)


if __name__ == "__main__":
    app.run()
