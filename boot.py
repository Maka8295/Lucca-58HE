"""
import board
import digitalio
import storage
import usb_cdc
import usb_hid

# If the encoder push-button is held during boot, don't run the code which hides the storage and disables serial and midi
button = digitalio.DigitalInOut(board.GP7)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

if button.value:
    storage.disable_usb_drive() # Hides device storage
    usb_cdc.disable() # Disables serial comunication
    usb_hid.enable(boot_device=1) # Enables keyboard before OS boot
    
button.deinit()
"""
