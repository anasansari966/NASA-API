import sys
import os

# Add the directory containing your Flask application to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import your Flask application
from main import app as application  # Assuming your Flask app is named 'app' and is in 'main.py'

# Define WSGI application object
application.wsgi_app = app

# Function to run the application
def run():
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, application)

if __name__ == "__main__":
    run()
