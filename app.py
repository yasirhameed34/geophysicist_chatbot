import gradio as gr
import requests

# 🔑 Your API Key (WeatherAPI)
API_KEY = "aa5c858f756d4db3b47151856260904"

# 🌤️ Weather Function
def get_weather(city):
    if not city.strip():
        return "❌ Please enter a city name", "", "", "", "", "", "", None

    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=yes"

    try:
        res = requests.get(url)
        data = res.json()

        # ❌ Handle API error
        if "error" in data:
            return f"❌ {data['error']['message']}", "", "", "", "", "", "", None

        # 🌍 Location
        location = f"{data['location']['name']}, {data['location']['country']}"

        # 🌡️ Weather Details
        temp = f"{data['current']['temp_c']} °C"
        feels = f"{data['current']['feelslike_c']} °C"
        humidity = f"{data['current']['humidity']} %"
        wind = f"{data['current']['wind_kph']} km/h"
        pressure = f"{data['current']['pressure_mb']} mb"
        condition = data['current']['condition']['text']

        # 🌄 Icon
        icon = "https:" + data['current']['condition']['icon']

        # 🌫️ Air Quality
        aqi = data['current'].get('air_quality', {})
        if aqi:
            pm25 = aqi.get('pm2_5')
            aqi_text = f"PM2.5: {pm25:.1f}" if pm25 is not None else "N/A"
        else:
            aqi_text = "N/A"

        return location, temp, feels, humidity, wind, pressure, condition + f" | AQI: {aqi_text}", icon

    except Exception as e:
        return f"⚠️ Error: {str(e)}", "", "", "", "", "", "", None


# 🎨 UI Design
with gr.Blocks(theme=gr.themes.Soft(), title="Weather Dashboard") as demo:

    gr.Markdown("## 🌤️ Advanced Weather Dashboard")
    gr.Markdown("Check real-time weather for any city worldwide 🌍")

    with gr.Row():
        city_input = gr.Textbox(
            label="📍 Enter City",
            placeholder="e.g., Islamabad, Lahore, Karachi, London"
        )
        btn = gr.Button("🔍 Get Weather", variant="primary")

    location_out = gr.Textbox(label="🌍 Location", interactive=False)

    with gr.Row():
        temp_out = gr.Textbox(label="🌡️ Temperature", interactive=False)
        feels_out = gr.Textbox(label="🤗 Feels Like", interactive=False)

    with gr.Row():
        hum_out = gr.Textbox(label="💧 Humidity", interactive=False)
        wind_out = gr.Textbox(label="💨 Wind Speed", interactive=False)

    with gr.Row():
        pressure_out = gr.Textbox(label="📊 Pressure", interactive=False)
        cond_out = gr.Textbox(label="🌥️ Condition + AQI", interactive=False)

    icon_out = gr.Image(label="Weather Icon")

    btn.click(
        fn=get_weather,
        inputs=city_input,
        outputs=[
            location_out,
            temp_out,
            feels_out,
            hum_out,
            wind_out,
            pressure_out,
            cond_out,
            icon_out
        ]
    )

# 🚀 Hugging Face uses default launch
demo.launch()