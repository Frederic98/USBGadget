# USBGadget
A python library for creating and interfacing with USB Gadgets on Linux through libcomposite.

This library assumes the ConfigFS gadget directory to be
`/sys/kernel/config/usb_gadget`.
If this is not the case, specify the correct directory in the call to USBGadget(name, path).

## Creating a gadget
Any gadget type that libcomposite supports can be created.
```python
import usb_gadget
gadget = usb_gadget.USBGadget('my_test_gadget')
# ... set up gadget parameters, functions and configurations
gadget.activate()
```

## Interfacing with a gadget
This library has an interface for HID gadgets. Specifically, keyboard, mouse and game controller.
```python
import usb_gadget
gadget = usb_gadget.USBGadget('my_test_gadget')
function = usb_gadget.HIDFunction(gadget, 'keyboard0')
keyboard = usb_gadget.KeyboardGadget(function.device)
keyboard.press_and_release('a')
```

See also `example.py` for a full keyboard setup

## Example HID Report Descriptors
<details>
  <summary>Keyboard</summary>

- 1 byte modifier keys
- 1 byte empty
- 6 bytes scancodes currently pressed keys

Report length: 8
```
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
```
</details>
<details>
  <summary>Mouse</summary>

- 1 byte currently pressed buttons
- 2 bytes X movement
- 2 bytes Y movement
- 1 byte vertical scroll wheel
- 1 byte horizontal scroll wheel

Report length: 7
```
0x05, 0x01,        # Usage Page (Generic Desktop Ctrls)
0x09, 0x02,        # Usage (Mouse)
0xA1, 0x01,        # Collection (Application)
0x05, 0x09,        #   Usage Page (Button)
0x19, 0x01,        #   Usage Minimum (0x01)
0x29, 0x08,        #   Usage Maximum (0x08)
0x15, 0x00,        #   Logical Minimum (0)
0x25, 0x01,        #   Logical Maximum (1)
0x95, 0x08,        #   Report Count (8)
0x75, 0x01,        #   Report Size (1)
0x81, 0x02,        #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0x05, 0x01,        #   Usage Page (Generic Desktop Ctrls)
0x09, 0x30,        #   Usage (X)
0x09, 0x31,        #   Usage (Y)
0x16, 0x00, 0x80,  #   Logical Minimum (-32768)
0x26, 0xFF, 0x7F,  #   Logical Maximum (32767)
0x75, 0x10,        #   Report Size (16)
0x95, 0x02,        #   Report Count (2)
0x81, 0x06,        #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0x09, 0x38,        #   Usage (Wheel)
0x15, 0x81,        #   Logical Minimum (-127)
0x25, 0x7F,        #   Logical Maximum (127)
0x75, 0x08,        #   Report Size (8)
0x95, 0x01,        #   Report Count (1)
0x81, 0x06,        #   Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
0x05, 0x0C,        #   Usage Page (Consumer)
0x0A, 0x38, 0x02,  #   Usage (AC Pan)
0x15, 0x81,        #   Logical Minimum (-127)
0x25, 0x7F,        #   Logical Maximum (127)
0x75, 0x08,        #   Report Size (8)
0x95, 0x01,        #   Report Count (1)
0x81, 0x06,        #   Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
0xC0,              # End Collection
```
</details>
<details>
  <summary>Joystick</summary>

- 4 bytes joystick positions (2x XY)
- 2 bytes trigger positions (2x Z)
- 3 bytes currently pressed buttons (24 buttons total)

Report length: 9
```
0x05, 0x01,        # Usage Page (Generic Desktop Ctrls)
0x09, 0x04,        # Usage (Joystick)
0xA1, 0x01,        # Collection (Application)
0x15, 0x81,        #   Logical Minimum (-127)
0x25, 0x7F,        #   Logical Maximum (127)
0x09, 0x01,        #   Usage (Pointer)
0xA1, 0x00,        #   Collection (Physical)
0x09, 0x30,        #     Usage (X)
0x09, 0x31,        #     Usage (Y)
0x09, 0x33,        #     Usage (Rx)
0x09, 0x34,        #     Usage (Ry)
0x75, 0x08,        #     Report Size (8)
0x95, 0x04,        #     Report Count (4)
0x81, 0x02,        #     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0xC0,              #   End Collection
0x15, 0x00,        #   Logical Minimum (0)
0x25, 0x7F,        #   Logical Maximum (127)
0x09, 0x01,        #   Usage (Pointer)
0xA1, 0x00,        #   Collection (Physical)
0x09, 0x32,        #     Usage (Z)
0x09, 0x35,        #     Usage (Rz)
0x75, 0x08,        #     Report Size (8)
0x95, 0x02,        #     Report Count (2)
0x81, 0x02,        #     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0xC0,              #   End Collection
0xA1, 0x00,        #   Collection (Physical)
0x05, 0x09,        #     Usage Page (Button)
0x19, 0x01,        #     Usage Minimum (0x01)
0x29, 0x18,        #     Usage Maximum (0x18)
0x15, 0x00,        #     Logical Minimum (0)
0x25, 0x01,        #     Logical Maximum (1)
0x75, 0x01,        #     Report Size (1)
0x95, 0x18,        #     Report Count (24)
0x81, 0x02,        #     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0xC0,              #   End Collection
0xC0,              # End Collection
```
</details>
