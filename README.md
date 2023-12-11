# Vision UnLocked

# Download

Download and extract the following files to the `data` directory/folder. Note: you may need to make this folder yourself as GitHub won't let me keep an empty folder in the repo.
Just keep it in the source directory (on the same level as `sample`)

- [dlib facial landmark detector](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
  - `data/face_landmarks.dat`

# Setup & Installation

## Environment

1. Install `virtualenv`

```bash
pip install virtualenv
```

2. Inside the project folder, run the following command:

```bash
python<version> -m venv env

e.g. python3 -m venv env
```

3. Activate the virtual environment\

- **Mac**:

```bash
  source env/bin/activate
```

- Windows

```bash
env/Scripts/activate.bat # if you're using CMD
env/Scripts/Activate.ps1 # if you're using Powershell
```

Check if you're virtual environment is working by running `pip list`. There should only be two packages:

1. `pip`
2. `setuptools`

## OS Specific
In `display.py` on line 49, please update the command to run the text-to-speech file to one that works with your respective operating system.
- MacOS: `afplay`
- Windows: `start`

## Installation

```bash
pip install -r requirements.txt
```

To check if all the libraries were installed correctly:

```bash
pip freeze > requirements.txt
```
