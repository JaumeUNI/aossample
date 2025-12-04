from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Supabase configuration from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validate that environment variables are set
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "SUPABASE_URL and SUPABASE_KEY must be set in environment variables or .env file"
    )

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
