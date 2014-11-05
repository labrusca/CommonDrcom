# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe

includes = ["encodings", "encodings.*"]
options = {"py2exe":
           
    {"compressed": 1,
     "optimize": 2,
     "ascii": 1,
     "includes": includes,
     "bundle_files": 3
     }
}

setup(
    version = "4.5",
    description = "NUPT Dr.com Loginer",
    name = "Loginer",
    data_files=[('', ['logo.dll', 'T.dll'])],
    windows=[{"script": "main.py", "icon_resources": [(1,"T.dll")] }],
    options=options,
    zipfile=None
)
