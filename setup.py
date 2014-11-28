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
    version = "5.0.1",
    description = "NUPT Dr.com Loginer",
    name = "南京邮电大学Dr.com客户端",
    #data_files=[('', ['logo.dll', 'T.dll'])],
    windows=[{"script": "main.py", "icon_resources": [(1,"t.ico")] }],
    options=options,
    zipfile=None
)