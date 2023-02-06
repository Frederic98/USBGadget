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
