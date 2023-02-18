import network
import urequests as requests
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
from machine import ADC, Pin
import config

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config.ssid, config.password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        pico_led.blink(0.25, 0.25, 2)
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


def serve():
    #Start a web server
    state = 'OFF'
    pico_led.on()
    temperature = 0
    relay = Pin(16, Pin.OUT)
    adc = ADC(Pin(26))

    while True:
        print('requesting')
        request = requests.get('https://webhook.site/80fddaad-e984-4f99-904a-01ab0aa83820')
        print(request.json())
        sensorVal = adc.read_u16()
        print('sensor:')
        print(sensorVal)
        instructions = request.json()
        request.close()

        if 'light' in instructions:
            if instructions['light'] == 'on':
                state = 'ON'
                if 'set' in instructions:
                    setpoint = int(instructions['set'])
                    print('setpoint:')
                    print(setpoint)
                    if setpoint < sensorVal:
                        state = 'OFF'
            elif instructions['light'] =='off':
                state = 'OFF'

        print(state)

        if (state == 'ON'):
            relay.on()
        else:
            relay.off()
        sleep(2)

try:
    ip = connect()
    serve()
except KeyboardInterrupt:
    machine.reset()