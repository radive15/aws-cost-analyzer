import os
from dotenv import load_dotenv

load_dotenv()

# Cost Explorer selalu pakai us-east-1, bukan region sendiri
# Ini bukan bug — memang desain AWS-nya begitu
AWS_REGION = "us-east-1"

AWS_PROFILE = os.getenv("AWS_PROFILE", "default")
COST_THRESHOLD_USD = float(os.getenv("COST_THRESHOLD_USD", "100.0"))
