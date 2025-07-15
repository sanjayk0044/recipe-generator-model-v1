from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Create the Flask application
app = create_app()

# This is for Vercel serverless deployment
# The variable name 'app' is what Vercel looks for by default
