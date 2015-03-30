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
    version = "5.0.4-alpha",
    description = "NUPT_Dr.comLoginer",
    name = "南京邮电大学Dr.(最终版)",
    #data_files=[('', ['logo.dll', 'T.dll'])],
    windows=[{"script": "main.py","uac_info":"highestAvailable", "icon_resources": [(1,"t.ico")] }],
    options=options,
    zipfile=None
)