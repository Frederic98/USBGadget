import time
import logging

import usb_gadget

logging.basicConfig(level=logging.DEBUG)

###
# Step 1: Create USB gadget (probably needs root permissions)
gadget = usb_gadget.USBGadget('test_gadget')
gadget.idVendor = '0x1d6b'
gadget.idProduct = '0x0104'
gadget.bcdDevice = '0x0100'
gadget.bcdUSB = '0x0200'

strings = gadget['strings']['0x409']
strings.serialnumber = '0123456789'
strings.manufacturer = 'Test'
strings.product = 'Test USB Gadget'

config = gadget['configs']['c.1']
config.bmAttributes = '0x80'
config.MaxPower = '250'
config['strings']['0x409'].configuration = 'Test Configuration'

function = usb_gadget.HIDFunction(gadget, 'keyboard0')
descriptor = [
0x05, 0x01,        # Usage Page (Generic Desktop Ctrls)
0x09, 0x06,        # Usage (Keyboard)
0xA1, 0x01,        # Collection (Application)
0x05, 0x07,        #   Usage Page (Kbrd/Keypad)
0x19, 0xE0,        #   Usage Minimum (0xE0)
0x29, 0xE7,        #   Usage Maximum (0xE7)
0x15, 0x00,        #   Logical Minimum (0)
0x25, 0x01,        #   Logical Maximum (1)
0x75, 0x01,        #   Report Size (1)
0x95, 0x08,        #   Report Count (8)
0x81, 0x02,        #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0x95, 0x01,        #   Report Count (1)
0x75, 0x08,        #   Report Size (8)
0x81, 0x03,        #   Input (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0x95, 0x06,        #   Report Count (6)
0x75, 0x08,        #   Report Size (8)
0x15, 0x00,        #   Logical Minimum (0)
0x25, 0x65,        #   Logical Maximum (101)
0x05, 0x07,        #   Usage Page (Kbrd/Keypad)
0x19, 0x00,        #   Usage Minimum (0x00)
0x29, 0x65,        #   Usage Maximum (0x65)
0x81, 0x00,        #   Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
0xC0,              # End Collection
]
function.protocol = '0'
function.subclass = '0'
function.report_length = '8'
function.report_desc = bytes(descriptor)
gadget.link(function, config)

gadget.activate()


###
# Step 2: Use USB Gadget

# gadget = usb_gadget.USBGadget('test_gadget')
# function = usb_gadget.HIDFunction(gadget, 'keyboard0')
keyboard = usb_gadget.KeyboardGadget(function.device, 6)    # Above, we defined a report count of 6

print('Typing in 5 seconds...')
time.sleep(5)
for letter in 'Hello, world':
    keyboard.press_and_release(letter)


###
# Step 3: Destroy the gadget
#   When you want to remove the USB gadget, call gadget.destroy()

# gadget = usb_gadget.USBGadget('test_gadget')
gadget.destroy()
