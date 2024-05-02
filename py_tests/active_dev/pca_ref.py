# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Outputs a 50% duty cycle PWM single on the 0th channel.
# Connect an LED and resistor in series to the pin
# to visualize duty cycle changes and its impact on brightness.


import board
import busio
import time

import adafruit_pca9685 as PCA9685

# Create the I2C bus interface.
i2c = busio.I2C(board.SCL, board.SDA)  # uses board.SCL and board.SDA
# i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040

# Create a simple PCA9685 class instance.
pca = PCA9685.PCA9685(i2c, address=0x40)

# Set the PWM frequency to 60hz.
pca.frequency = 60

# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.
motor1 = pca.channels[0]
pca.channels[0].duty_cycle = 0x7FFF
