# Synthonnel

One Prompt, Many LLMs.

## User Guide

See the Tutorial at [Synthonnel.com](https://www.synthonnel.com/) for more information.

## Super Quick Start - From Source

#### Create and Activate Virtual Environment

```
python -m venv venv
```

- **Windows**:

```
.\venv\Scripts\activate
```

- **macOS/Linux**:

```
source venv/bin/activate
```


#### Install Required Packages:

```
pip install -r requirements.txt
```


#### Start Backend:

```
uvicorn main:app --reload
```


#### Use Browser for UI:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)


#### To Make the PyInstaller:

This creates `synthonnel.exe` and a directory `_internal` at `/dist/synthonnel/`. You need both of these, especially all the contents of `_internal`. Put the exe and the `_internal` directory into the same folder, then just double click the exe file.

```
pyinstaller --clean --noconfirm synthonnel.spec
```
