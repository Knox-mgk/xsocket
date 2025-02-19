import subprocess
import sys

try:
    import setuptools

except ImportError:
    print('installing setuptools...')
    subprocess.check_call([sys.executable, '-m', 'pip' 'install', 'setuptools'])  

from setuptools import setup, find_packages

setup(
    name='xsocket'
    version='1.0.0',
    py_modules=['xsocket']
    install_requires=[],
    author='Odusipe Kayode Oluwaseun',
    author_email='kodusipe@gmail.com',
    description='A customizable socket wrapper with various IO models.',
    url='https://github/Knox-mgk/xsocket',
    classifiers=[
        'Programming Language :: python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent,'
    ],
    python_requires='>=3.6'
)