# bpp-selaawi-webservice

## How to run in local:

#### 1. Make virtual environment
```
python -m venv venv
```
#### 2. Set access to Unrestricted
```
Set-ExecutionPolicy Unrestricted -Scope Process
```
#### 3. Activate virtual environment
```
venv/Scripts/activate
```
#### 4. Install all dependencie
```
pip install -r requirements.txt
```
#### 5. Run the server
```
uvicorn main:app
```
