from distutils.core import setup
import py2exe

includes = ["encodings", "encodings.*","paramiko"]
from glob import glob
data_files = [("upload", glob(r'd:\software_dev\py\upload\*.*')),("", ["d:\software_dev\py\config.ini"])]

options = {"py2exe":{
                     "compressed":1, 
                     "bundle_files":1,
                     "optimize":2,
                     "ascii":1,
                     "includes":includes
                     }}  

setup(
        options=options,
        console=[{"script":"d:\software_dev\py\distribute.py"}],
        data_files=data_files,
        zipfile=None)
