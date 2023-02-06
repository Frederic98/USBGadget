import os
import logging
import subprocess

logger = logging.getLogger('usb_gadget')


class ConfigFS:
    path = None

    def __init__(self, path):
        if isinstance(path, ConfigFS):
            path = path.path
        self.path = path

    def mkdir(self, name):
        path = os.path.join(self.path, name)
        os.mkdir(path)
        return ConfigFS(path)

    def exists(self, item):
        return os.path.exists(os.path.join(self.path, item))

    def __getitem__(self, item):
        """Get subdirectory"""
        path = os.path.join(self.path, item)
        if os.path.isdir(path):
            return ConfigFS(path)
        else:
            return self.mkdir(path)

    def __getattr__(self, file, mode='rt'):
        """Read from file"""
        with open(os.path.join(self.path, file), mode) as f:
            return f.read().strip()

    def __setattr__(self, file, value, mode=None):
        """Write to file"""
        if self.path is None:
            return object.__setattr__(self, file, value)
        logger.debug(f'{os.path.join(self.path, file)} = {repr(value)}')
        if mode is None:
            if isinstance(value, str):
                mode = 'wt'
            elif isinstance(value, bytes):
                mode = 'wb'
            else:
                raise RuntimeError('Could not determine file mode')
        with open(os.path.join(self.path, file), mode) as f:
            f.write(value)


class USBGadget(ConfigFS):
    def __init__(self, name, path='/sys/kernel/config/usb_gadget'):
        root = ConfigFS(path)
        ConfigFS.__init__(self, root[name].path)

    def link(self, function: ConfigFS, config: ConfigFS):
        """Link a function to a configuration"""
        link_path = os.path.join(config.path, os.path.basename(function.path))
        os.symlink(function.path, link_path)

    def unlink(self, function: ConfigFS, config: ConfigFS):
        """Unlink a function from a configuration"""
        link_path = os.path.join(config.path, os.path.basename(function.path))
        os.unlink(link_path)

    def activate(self, device=None):
        if device is None:
            ports = os.listdir('/sys/class/udc')
            if ports:
                device = ports[0]
            else:
                raise RuntimeError('No UDC ports present!')
        self.UDC = device

    def deactivate(self):
        # Deactivate if currently assigned to a UDC
        if self.UDC.strip():
            with open(os.path.join(self.path, 'UDC'), 'wb', buffering=0) as f:
                f.write(b'\n')

    def destroy(self):
        for config in os.scandir(self['configs'].path):
            config = ConfigFS(config.path)
            for function in os.scandir(config.path):
                if function.is_symlink():
                    os.remove(function.path)
            for language in os.scandir(config['strings'].path):
                os.rmdir(language.path)
            os.rmdir(config.path)
        for function in os.scandir(self['functions'].path):
            os.rmdir(function.path)
        for language in os.scandir(self['strings'].path):
            os.rmdir(language.path)
        os.rmdir(self.path)


class HIDFunction(ConfigFS):
    def __init__(self, gadget: USBGadget, name: str):
        ConfigFS.__init__(self, gadget['functions']['hid.' + name])

    @property
    def device(self):
        return subprocess.check_output(['udevadm', 'info', '-r', '-q', 'name', f'/sys/dev/char/{self.dev.strip()}']).decode('ascii').strip()
