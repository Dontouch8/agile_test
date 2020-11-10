# Installation

### Backend (Python 3.6+)

```sh
# Clone repo
git clone https://github.com/Dontouch8/agile_test && cd agile_test

# Create python3.6 virtual environment
python3.6 -m venv venv

# Activate virtualenv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

# Starting

```sh
# Start web server
cd src
uvicorn main:app --reload

# Start scheduler
python scheduler.py
```

# Testing

```sh
# Send fake request
curl "127.0.0.1:8000/search/?image_id=4124421"
```