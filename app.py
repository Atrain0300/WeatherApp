from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def get_weather():

    weather_data = None
    location_byuser = None
    error = None

    if request.method == "POST":

        location_byuser = request.form.get("location")

        if location_byuser:

            try:
                location = location_byuser.strip()
                location = ",".join(location.split())

                geoapify_apikey = os.getenv("APIKEY")

                geoapify_url = (
                    f"https://api.geoapify.com/v1/geocode/search"
                    f"?text={location}"
                    f"&apiKey={geoapify_apikey}"
                )

                loc_response = requests.get(geoapify_url)
                loc_data = loc_response.json()

                lat = loc_data["features"][0]["properties"]["lat"]
                lon = loc_data["features"][0]["properties"]["lon"]

                api_url = (
                    f"https://api.open-meteo.com/v1/forecast"
                    f"?latitude={lat}"
                    f"&longitude={lon}"
                    f"&current=temperature_2m,wind_speed_10m"
                )
                weather_response = requests.get(api_url)
                weather_data = weather_response.json()

            except Exception as e:
                error = f"Something went wrong: {e}"

    return render_template(
        "index.html",
        weather_data=weather_data,
        location=location_byuser,
        error=error
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
