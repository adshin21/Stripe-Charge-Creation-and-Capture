# Stripe-Charge-Creation-and-Capture

## Steps for running the project

#### (Should have python 3.6+ installed, and venv)


### Clone the repo and go to parent dir of the project
```bash
git clone https://github.com/adshin21/Stripe-Charge-Creation-and-Capture.git
cd Stripe-Charge-Creation-and-Capture
```

### create a virtual envirnoment

```bash
python3 -m venv <your_envirnoment_name>
```

### activate the envirnoment

```bash
source <your_envirnoment_name>/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the app

Before running make sure to put the stripe test api key inside `config.py`
```bash
python3 app.py
```