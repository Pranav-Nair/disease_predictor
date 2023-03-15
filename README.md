# Disease Prediction Web App

This is a web application that can predict is user has any of the below diseases

* Diabetese
* Heart disease
* Thyroid issue
* Lung cancer

## Setup instructions

This is a self hostable web app and can be run on any machine wih python installed

* Step 1 : make sure python3 and pip are installed on your system.
* Step 2 : download and extract the source code to a location in your system.
* Step 3 : open cmd or terminal inside the project folder in local machine.
* Step 4 : setup virtualenv.

```
pip install virtualenv
python3 -m venv venv

# windows specefic
./venv/Scripts/activate.bat

# linux and mac
source venv/bin/activate
```

* Step 5 : install dependencies.

`pip install -r depends.txt`

* Step 6 : start the server.

`python3 main.py`
