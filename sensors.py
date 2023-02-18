from machine import ADC, Pin
import time

adc = ADC(Pin(26))
adc2 = ADC(Pin(27))


while True:
    print(adc.read_u16())
    print(adc2.read_u16())
    time.sleep(1)