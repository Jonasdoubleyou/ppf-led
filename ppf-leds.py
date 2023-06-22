
# Parkplatfest LEDs
# Author: Jonas Wilms, 2.OG D7, 2023
#

import signal
import time
import sys

from rpi_ws281x import *


# LED strip configuration:
LED_COUNT      = 150 + 50      # Number of LED pixels.
LED_PIN        = 12       # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# Letter configuration:
LETTER_D = range(105, 140)
LETTER_R = range(70, 105)
LETTER_I = range(40, 70)
LETTER_N = range(0, 39)
LETTER_K = range(150, 190)

LETTERS = [ LETTER_D, LETTER_R, LETTER_I, LETTER_N, LETTER_K ]

def fromOffset(offset, ranges):
    return [ [ it + offset for it in range ] for range in ranges ]

# vertical letter slices:
D_COLS = fromOffset(104, [
    range(19, 31),
    (32, 18),
    (33, 17), 
    (34, 16),
    (35, 12),
    (36, 11),
    (37, 10),
    (1, 9),
    (2, 8),
    (3, 7),
    (4, 5, 6)
])

R_COLS = fromOffset(69, [
    range(24, 36),
    (9, 10, 23),
    (8, 11, 22),
    (7, 6, 12, 21),
    (5, 13, 20),
    (4, 14, 19),
    (3, 15, 18),
    (2, 1, 16, 17)
])

I_COLS = [ LETTER_I ]

N_COLS = fromOffset(-1, [
    range(27, 39),
    (26,), (25,), (24,), (23,), (22,), (21,), (20,), (19,), (18,), (17,), (16,), (15,), (14,), (13,),
    range(1, 13)
])

K_COLS = fromOffset(149, [
    range(1,14),
    (29, 30),
    (28, 31),
    (27, 32),
    (26, 33),
    (25, 34),
    (24, 35),
    (23, 36),
    (22, 37),
    (21, 38)
])

LETTER_COLS = D_COLS + R_COLS + I_COLS + N_COLS + K_COLS;

# common colors:
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)

COLORS = [ RED, GREEN, BLUE ]

print("-------- Parkplatzfest LEDs start --------")
print(" Anzahl LEDs: " + str(LED_COUNT))
print(" PIN (GIN): " + str(LED_PIN))
print(" Frequenz: " + str(LED_FREQ_HZ) + " Hz")
print(" DMA Channel: " + str(LED_DMA))
print(" Helligkeit: " + str(float(LED_BRIGHTNESS) / 255.0 * 100.0) + "%")

class LEDService:
    # --------- SETUP & SHUTDOWN ---------------

    def __init__(self):
        print(" ----- BEGIN SETUP ----- ")
        
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.strip.begin()
        print(" - NeoPixel library initialized")

        
        signal.signal(signal.SIGTERM, self.shutdown)
        print(" - Shutdown handler attached to SIGTERM")

        print(" ----- END   SETUP  ----- ")
        
        # self.set(LETTER_N, WHITE)
        # self.set(LETTER_R, RED)
        # self.set(LETTER_K, BLUE)
        # self.flush()
        
        self.run_loop()

    def shutdown(self, a, b):
        print(" ----- BEGIN SHUTDOWN ----- ")
        self.clear()
        print(" ----- END   SHUTDOWN ----- ")
        sys.exit(0)


    # --------- MAIN LOOP ----------------------

    def run_loop(self):
        try:
            while True:
                print(" ----- BEGIN LOOP ----- ")
                
                # self.scene_1()
                # self.scene_2()
                # self.scene_3()
                # self.scene_4()
                # self.scene_5()
                
                self.scene_6()

                print(" ----- END   LOOP ----- ")

        except KeyboardInterrupt:
            self.shutdown(None, None)
   
    # --------- COLOR UTILITIES ----------------

    # Turns 0 - 255 into rainbow colors
    def color_wheel(self, pos):
        pos = int(pos) & 255

        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    # --------- TIME UTILITIES -----------------
    # When we sleep we usually want to also flush the light for the viewer to see

    def sleep_second(self):
        print("  + sleep 1s ")
        self.flush()
        time.sleep(1)

    def sleep_short(self):
        print("  + sleep 0.1s")
        self.flush()
        time.sleep(0.1)

    def sleep_blink(self):
        self.flush()
        time.sleep(0.0001)

    # --------- SCENES -------------------------

    def scene_1(self):
        print(" + SCENE 1")
        self.set_all(RED)
        self.sleep_second()

        self.set_all(GREEN)
        self.sleep_second()
        
        self.set_all(BLUE)
        self.sleep_second()

        self.clear()

    # Letters 
    def scene_2(self):
        print(" + SCENE 2 ")
        
        for iteration in range(0, 10):
            for i, letter in enumerate(LETTERS):
               color = COLORS[ (iteration + i) % len(COLORS) ]
               self.set(letter, color)
         
            self.sleep_second()

   
    # Rainbow
    def scene_3(self):
        print(" + SCENE 3")
        for offset in range(0, 255):
            for i in self.led_range():
                self.set(i, self.color_wheel(i+offset))
            self.sleep_blink()

    # Snake
    def scene_4(self):
        print(" + SCENE 4")
        self.clear()


        for i in self.led_range():
            self.set(i, self.color_wheel(i))
            self.sleep_short()

        for i in self.led_range():
            self.set(i, BLACK)
            self.sleep_short()

    # Strobo
    def scene_5(self):
       print (" + SCENE 5")

       for letter in LETTERS:
            self.set(letter, WHITE)
            self.sleep_second()
            self.set(letter, BLACK)
            self.sleep_second()

       for iteration in range(0, 10):
            self.set_all(WHITE)
            self.sleep_short()
            self.set_all(BLACK)
            self.sleep_short()

    # Rainbow moving
    def scene_6(self):
        print (" + SCENE 6")
        for offset in range(0, 255):
            for pos in range(0, len(LETTER_COLS)):
                self.set(LETTER_COLS[pos], self.color_wheel(pos+offset))
            self.sleep_short()

    
    # --------- LED CONTROL --------------------

    def led_range(self):
        return range(0, self.strip.numPixels())

    # Transmit local state to the LEDs:
    def flush(self):
        self.strip.show()
   
    def set(self, led_or_range, color):
        if type(led_or_range) is range or type(led_or_range) is list:
            self.set_range(led_or_range, color)
        else:
            self.set_led(led_or_range, color)

    def set_led(self, led, color):
        self.strip.setPixelColor(led, color)

    def set_range(self, led_range, color):
        if type(led_range) is range:
            print("  + set range (" + str(led_range[0]) + ", " + str(led_range[1]) + ") to color " + str(color))
        else:
            print("  + set list (" + " ".join(map(str, led_range)) + ") to color " + str(color))

        for led in led_range:
            self.strip.setPixelColor(led, color)

    def set_all(self, color):
        print("  + set all to " + str(color))
        self.set(self.led_range(), color)

    def clear(self):
        self.set_all(Color(0, 0, 0))
        self.flush()
       
service = LEDService()
