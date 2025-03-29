# ==== imports ====
import os
from dotenv import load_dotenv

# ===== environmental variables =====
load_dotenv()

# Headers
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json; charset=UTF-8",
}

# Settings
ADDRESS = os.getenv("MCSMANAGER_ADDRESS")
API_KEY = os.getenv("MCSMANAGER_API_KEY")
OUTPUT_SIZE = os.getenv("OUT_PUT_SIZE")
PAGE_SIZE = os.getenv("PAGE_SIZE")
PAGE = os.getenv("PAGE")
PAGE_SIZE_PAGE = f"&page_size={PAGE_SIZE}&page={PAGE}"

instanceData = []
daemonData = []
userData = []


# ===== functions ======
def bytes_gigabytes(data):
    return data / 1024 / 1024 / 1024


def true_false_tran(data):
    if data is True:
        return "✅"
    elif data is False:
        return "❌"
    else:
        return None
