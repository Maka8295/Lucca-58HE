# SPDX-FileCopyrightText: 2022 Phil Underwood
#
# SPDX-License-Identifier: Unlicense
"""
example that reads from the cdc data serial port in groups of four and prints
to the console. The USB CDC data serial port will need enabling. This can be done
by copying examples/usb_cdc_boot.py to boot.py in the CIRCUITPY directory

Meanwhile a simple counter counts up every second and also prints
to the console.
"""


import asyncio

USE_USB = True
USE_UART = True
USE_BLE = True


if USE_USB:
    import usb_cdc

    async def usb_client():
        usb_cdc.data.timeout = 0
        s = asyncio.StreamReader(usb_cdc.data)
        while True:
            text = await s.readline()
            print("USB: ", text)


if USE_UART:
    import board

    async def uart_client():
        uart = board.UART()
        uart.timeout = 0
        s = asyncio.StreamReader(board.UART())
        while True:
            text = await s.readexactly(4)
            print("UART: ", text)


if USE_BLE:
    from adafruit_ble import BLERadio
    from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
    from adafruit_ble.services.nordic import UARTService

    async def ble_client():
        ble = BLERadio()
        uart = UARTService()
        advertisement = ProvideServicesAdvertisement(uart)
        ble.start_advertising(advertisement)
        s = asyncio.StreamReader(uart._rx)  # pylint: disable=protected-access
        while True:
            text = await s.read(6)
            print("BLE: ", text)


async def counter():
    i = 0
    while True:
        print(i)
        i += 1
        await asyncio.sleep(1)


async def main():
    clients = [asyncio.create_task(counter())]
    if USE_USB:
        clients.append(asyncio.create_task(usb_client()))
    if USE_UART:
        clients.append(asyncio.create_task(uart_client()))
    if USE_BLE:
        clients.append(asyncio.create_task(ble_client()))
    await asyncio.gather(*clients)


asyncio.run(main())
