"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import json
import requests
import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests

N: int = 10
sample_ms = 10.0
on_ms = 500

def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    # %% let user know game started / is over

    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file.

    Parameters
    ----------

    json_filename: str
        The name of the file to write to. This will overwrite any existing file.

    data: dict
        Dictionary data to write to the file.
    """

    with open(json_filename, "w") as f:
        json.dump(data, f)


def scorer(t: list[int | None]) -> None:
    # %% collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    print(t_good)

    # add key, value to this dict to store the minimum, maximum, average response time
    # and score (non-misses / total flashes) i.e. the score a floating point number
    # is in range [0..1]

    data = {
        "minimum": min(t_good),
        "maximum": max(t_good),
        "average": sum(t_good) / len(t_good),
        "score": 1 - misses / len(t),
    }

    print(data)

    # %% make dynamic filename and write JSON

    now: tuple[int] = time.localtime()

    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"

    print("write", filename)

    # write_json(filename, data)

    # Connection code from: https://core-electronics.com.au/guides/raspberry-pi-pico-w-connect-to-the-internet/
    # Connect to network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Fill in your network name (ssid) and password here:
    ssid = 'Suhani'
    print(ssid)
    password = '****' #omitted for security purposes
    wlan.connect(ssid, password)

    url = f"https://ec463miniprojectv2-default-rtdb.firebaseio.com/{filename}"
    response = requests.post(url, json=data)

    print(response.status_code)  # Status code of the response
    print(response.text)  # The response content (if any)


if __name__ == "__main__":
    # using "if __name__" allows us to reuse functions in other script files

    led = Pin("LED", Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []

    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5, led)

    scorer(t)
