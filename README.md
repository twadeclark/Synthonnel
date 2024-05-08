# Synthonnel

One Prompt, Many LLMs.

## User Guide

See the User Guide at [Synthonnel.com](https://www.synthonnel.com/docs/userGuide) for more information.

## Super Quick Start - From Source


#### 1. Git Clone

```
git clone https://github.com/twadeclark/Synthonnel.git
```


#### 2. Create and Activate Virtual Environment

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


#### 3. Install Required Packages:

```
pip install -r requirements.txt
```


#### 4. Start Backend:

```
uvicorn main:app --reload
```


#### 5. Use Browser for UI:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)


### To Make the PyInstaller:
```
pyinstaller --clean --noconfirm synthonnel.spec
```
This creates `synthonnel.exe` and a directory `_internal` at `/dist/synthonnel/`. You need both of these, especially all the contents of `_internal`. Put the exe and the `_internal` directory into the same folder, then just double click the exe file.

