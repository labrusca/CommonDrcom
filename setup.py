# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe

includes = ["encodings", "encodings.*"]
options = {"py2exe":
           
    {"compressed": 1,
     "optimize": 2,
     "ascii": 1,
     "includes": includes,
     "bundle_files": 1
     }
}

setup(
    version = "4.3",
    description = "NUPT Dr.com Loginer",
    name = "Loginer",
    windows=[{"script": "main.py", "icon_resources": [(1,"T.dll")] }],
    options=options,
    zipfile=None
)
