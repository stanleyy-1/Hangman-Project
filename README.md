# Hangman Project

## Setup

**1. Clone the repository**

```bash
git clone https://github.com/stanleyy-1/Hangman-Project.git
cd "Hangman Project"
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Apply database migrations**

```bash
python manage.py migrate
```

**5. Run the development server**

```bash
python manage.py runserver
```

The app will be available at **http://127.0.0.1:8000**

