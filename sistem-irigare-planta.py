# Proiect SM

import machine
import time
import _thread

# CONSTANTE
valoare_maxima_citita = 65535

# PINI
relay_pin = 16
sensor_pin = 26
sensor_ploaie_pin = 27

motor = 0
running = True

senzor_umiditate = machine.ADC(machine.Pin(26, machine.Pin.IN))
relay = machine.Pin(relay_pin, machine.Pin.OUT);
senzor_ploaie = machine.ADC(machine.Pin(27, machine.Pin.IN))
bluetooth = machine.UART(1, 9600)

def relay_on(timp: int):
    relay.value(0)
    print("Pompa a pornit.")
    time.sleep(timp)
    
def relay_off(timp: int):
    relay.value(1)
    time.sleep(timp)
    print("Pompa este oprita.")

def calcul_senzor_umiditate(input: int):
    return 130 - (input * 100 / valoare_maxima_citita)

def calcul_senzor_ploaie(input: int):
    return 100 - (input * 100 / valoare_maxima_citita)

def citire():
    global motor, running
    while True:
        if motor == 1:
            bluetooth.write("A pornit pompa de apa!\r\n")
            time.sleep(0.2)
        if motor == 2:
            bluetooth.write("A inceput ploaia!\r\n")
            time.sleep(0.2)

        mesaj = bluetooth.read()
        if(mesaj != None):
            print(mesaj)
            
            if mesaj.decode("utf-8") == "on":
                print("on")
                running = True
                time.sleep(0.1)
            if mesaj.decode("utf-8") == "off":
                print("off")
                running = False
                time.sleep(0.1)
            
        time.sleep(0.2)

th = _thread.start_new_thread(citire, ())

relay_off(3)

while True:
    while running:
        time.sleep(0.5)
        umiditate = calcul_senzor_umiditate(senzor_umiditate.read_u16())
        print("UMIDITATE: " + str(umiditate))
        
        ploaie = calcul_senzor_ploaie(senzor_ploaie.read_u16())
        print("PLOAIE: " + str(ploaie))
        
        if ploaie > 50:
            print("Senzorul de ploaie a detectat apa.")
            time.sleep(0.5)
            motor = 2
            time.sleep(0.2)
            motor = 0
            relay_off(5)
        
        if umiditate < 70:
            relay_on(5)
            # mesaj prin bluetooth
            print("Motorul a pornit!")
            motor = 1
            time.sleep(0.2)
            motor = 0

        relay_off(5)
        

