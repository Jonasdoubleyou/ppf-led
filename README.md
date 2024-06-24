# Parkplatzfest LEDs

Some LED animations controlled by a Raspberry Pi (Raspi). Required Hardware:
 - [Power Supply](https://www.amazon.de/Zolt-Schaltnetzteil-Multi-Voltage-Lautsprecher-Haushaltselektronik/dp/B0932Y7CXJ/)
 - [LED stripes](https://www.amazon.de/BTF-LIGHTING-WS2812B-adressierbare-Streifen-Wasserdicht/dp/B01CDTEEZ2/?th=1)
 - A Raspi 3A+ (or any other, though the GPIOs might be different)

This repo is slightly inspired by [this tutorial](https://tutorials-raspberrypi.de/raspberry-pi-ws2812-ws2811b-rgb-led-streifen-steuern/).

## Installation

**Hardware**

Attach a power supply to the Raspi (i.e. via Micro USB). Attach the 5V+ and GND (ground) of the LED stripes to +/- of the power supply
 (this ensures that the LEDs have a stable power supply, as the Raspis output pins might not have enough ampere).
If the power supply is blinking, there is a short circuit between 5V+ and GND, fix your wiring ...

Attach GND of the LED stripes to a GND pin of the Raspi, also attach the DIN (Data In) of the LED stripes to a GPIO port of the Raspi that supports PWM
 (i.e. for the Pi 3A+ the fifth pin from the upper left - so port 32).
Note that we use the GPIO numbering, NOT the WiringPi numbering (which is also called "GPIO" in many places).
See [pinout.xyz](https://pinout.xyz/). 

Clone this Repo into the home directory of the "pi" user. Install Python 3 and Pip. Then run 

```
sudo apt install python3-dev
pip install rpi_ws281x
```

To install as a SystemD Service, copy `ppf-led.service` to `/lib/systemd/system/`, then run `sudo systemctl daemon-reload`.
Open `ppf-leds.py` and adapt the section "LED stripe configuration" accordingly.

# Run

To run the script locally (`-E` ensures the PYTHONPATH is set correctly, needs to run as root to write GPIO pins):

```
sudo -E python3 ./ppf-leds.py
```

To run the script in the background one can use the SystemD service that can be started and stopped (and also enabled, so it will be started when the Raspi is rebootet):

```
sudo systemctl (start|stop|enable) ppf-led
```

To check what the background job is doing run:

```
sudo journalctl -u ppf-led
```