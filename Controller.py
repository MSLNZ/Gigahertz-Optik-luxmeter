import os

from msl.loadlib import Client64


class Optik64(Client64):

    def __init__(self, dll_folder, serial):
        root = os.path.dirname(__file__)
        Client64.__init__(self,
                          module32='Server',
                          append_sys_path=[root, dll_folder],
                          append_environ_path=[root, dll_folder],
                          serial = serial)

    def __getattr__(self, method32):
        def send(*args, **kwargs):
            return self.request32(method32, *args, **kwargs)
        return send

