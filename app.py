from fastapi import FastAPI
import psutil
import platform
import requests

app = FastAPI()

# API to fetch system resource details
@app.get("/system-info")
def get_system_info():
    # CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # RAM usage
    memory = psutil.virtual_memory()
    ram_total = memory.total / (1024 * 1024)  # Convert to MB
    ram_used = memory.used / (1024 * 1024)  # Convert to MB
    ram_percent = memory.percent

    # Battery status
    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else "No battery"
    battery_plugged = battery.power_plugged if battery else False

    # Python version
    python_version = platform.python_version()

    # Approximate location based on IP
    try:
        ip_info = requests.get("https://ipapi.co/json/").json()
        location = {
            "city": ip_info.get("city"),
            "region": ip_info.get("region"),
            "country": ip_info.get("country_name"),
            "ip": ip_info.get("ip"),
        }
    except Exception as e:
        location = {"error": "Unable to fetch location"}

    return {
        "cpu_usage": f"{cpu_usage}%",
        "ram": {
            "total": f"{ram_total:.2f} MB",
            "used": f"{ram_used:.2f} MB",
            "percent": f"{ram_percent}%",
        },
        "battery": {
            "percent": battery_percent,
            "plugged_in": battery_plugged,
        },
        "python_version": python_version,
        "location": location,
    }


# API to fetch current time
@app.get("/current-time")
def get_current_time():
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"current_time": current_time}
