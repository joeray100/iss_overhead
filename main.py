# To execute file use Python Anywhere Account
# https://www.pythonanywhere.com/user/Rayj/
# OR
# In MAC OS background use crontab commands in terminal. The video linked below shows how.
# https://www.youtube.com/watch?v=EgrpfvBc7ks

# ----------------------------------- WHAT APP DOES ----------------------------------- #

# If the ISS is close to my current position and it is currently dark
# then send me an email to tell me to look up.
# Run the code every 60 seconds.

# ----------------------------------- IMPORTS ----------------------------------- #

import requests
from datetime import datetime
import smtplib
import time

# ----------------------------------- GLOBAL CONSTANTS ----------------------------------- #

MY_EMAIL = "jray100.jr@gmail.com"
MY_PASSWORD = "fcmofnobyjjgryht"

MY_LAT = 39.654251
MY_LONG = -106.823601

# ----------------------------------- FUNCTIONS ----------------------------------- #


# Pull current ISS location from API and confirm if it's close to you
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


# Using your geolocation get current sunset and sunrise times and confirm your current time is during the night.
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


# If both functions above are true, then send an email to your self.
while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject: The ISS Is Currently Visible Over Eagle\n\nJoe,\n\n\nUsing your Python App you automated sending the below message.\nThe International Space Station is currently above you in the sky."
        )

