import network
import time
import urandom
from umqtt.simple import MQTTClient

# ThingSpeak and Wi-Fi settings
mqtt_client_id = "JSYFAA4YLQcpBgwSHyYsKgA"
mqtt_user = "JSYFAA4YLQcpBgwSHyYsKgA"
mqtt_password = "S+Ex8lqfojeiIciNNu16mkRD"
mqtt_server = "mqtt3.thingspeak.com"
mqtt_port = 1883
mqtt_topic_temperature = "channels/2488613/publish/fields/field1"
mqtt_topic_humidity = "channels/2488613/publish/fields/field2"
mqtt_topic_co2 = "channels/2488613/publish/fields/field3"
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# Connect to Wi-Fi
def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            time.sleep(1)
    print("Wi-Fi Connected")

# Generate sensor data
def generate_sensor_data():
    return (
        urandom.uniform(-50, 50),  # Temperature
        urandom.uniform(0, 100),   # Humidity
        urandom.uniform(300, 2000) # CO2
    )

# Publish to ThingSpeak
def publish_to_thingspeak(temp, humid, co2):
    client = MQTTClient(mqtt_client_id, mqtt_server, user=mqtt_user, password=mqtt_password, port=mqtt_port)
    client.connect()
    client.publish(mqtt_topic_temperature, str(temp))
    client.publish(mqtt_topic_humidity, str(humid))
    client.publish(mqtt_topic_co2, str(co2))
    client.disconnect()

connect_wifi()

# Main loop
while True:
    temperature, humidity, co2 = generate_sensor_data()
    publish_to_thingspeak(temperature, humidity, co2)
    print(f"Published: Temperature={temperature:.2f}C, Humidity={humidity:.2f}%, CO2={co2:.2f}ppm")
    time.sleep(5)
