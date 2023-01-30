

import os
import subprocess
import platform
from sys import exit
from time import sleep

pkg = ''

# Detect if platform is using apt or dnf or pacman package manager.
try:
    subprocess.run(['apt', '-v'], capture_output=True).stdout
    pkg = 'apt'
except Exception as e:
    try:
        subprocess.run(['dnf', '--version'], capture_output=True).stdout
        pkg = 'dnf'
    except Exception as e:
        try:
            subprocess.run(['pacman', '--version'], capture_output=True).stdout
            pkg = 'pacman'
        except Exception as e:
            try:
                subprocess.run(['xbps-query', '-V'],
                               capture_output=True).stdout
                pkg = 'xbps'
            except:
                print('Platform not supported!')
                sleep(5)
                exit(1)

if platform.system().lower() == 'windows':
    print('Platform not supported!')
    sleep(5)
    exit(1)

tesseract = 'tesseract'

if pkg == 'xbps':
    tesseract = 'tesseract-ocr'

try:
    x = subprocess.run([tesseract, '-v'], capture_output=True)
except Exception as e:
    print('Tesseract Not Found!\n Trying to Install it...')
    if pkg == 'apt':
        subprocess.run(['sudo', 'apt', 'update']).stdout
        subprocess.run(['sudo', 'apt', 'install', 'tesseract-ocr']).stdout
    elif pkg == 'dnf':
        subprocess.run(['sudo', 'dnf', 'install', 'tesseract']).stdout
    elif pkg == 'pacman':
        subprocess.run(['sudo', 'pacman', '-S', 'tesseract']).stdout
    elif pkg == 'xbps':
        subprocess.run(['sudo', 'xbps-install', tesseract]).stdout


try:
    x = subprocess.run(['pdftocairo', '-v'], capture_output=True)
except Exception as e:
    print('pdftocairo Not Found!\n Trying to Install it...')
    if pkg == 'apt':
        subprocess.run(['sudo', 'apt', 'update']).stdout
        subprocess.run(['sudo', 'apt', 'install', 'poppler-utils']).stdout
    elif pkg == 'dnf':
        subprocess.run(['sudo', 'dnf', 'install', 'poppler-utils']).stdout
    elif pkg == 'pacman':
        subprocess.run(['sudo', 'pacman', '-S', 'poppler']).stdout
    elif pkg == 'xbps':
        subprocess.run(['sudo', 'xbps-install', 'poppler-utils']).stdout


# Loop to get names of all PDF files in current working Directory.
for i in os.listdir():
    if i[-3:].lower() == 'pdf':

        print('\nProcessing', i)
        # create an output folder.
        os.mkdir(i+'_output')

        # Move PDF file to output folder.
        x = subprocess.run(['mv', i, i+'_output'])

        # Change directory to output folder.
        os.chdir(i+'_output')

        # Convert PDF file to PNG images using pdftocairo tool in poppler-utils.
        print('\nConverting PDF file into PNGs...')
        x = subprocess.run(['pdftocairo', i, '-png'])

        # Loop to get names of all PNG image files in current working directory.
        for i in os.listdir():
            if i[-3:].lower() == 'png':
                print('Extracting Text from ', i)
                # Pass the image to Tesseract ocr to recover text from images.
                x = subprocess.run([tesseract, i, i[:-3]], capture_output=True)

                # Delete the image generated during Conversion of PDF to Text files.
                os.remove(i)

        # Return to current working Directory.
        os.chdir('..')
        print('Cleaning up PNGs...')
print('\nDone!')
