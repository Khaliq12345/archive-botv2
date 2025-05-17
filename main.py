import sys
import os

sys.path.append(".")

from core.config import FASTAPI_BIN


if __name__ == "__main__":
    os.system(f"{FASTAPI_BIN} run ./api/app.py --port=9500 --host=0.0.0.0")
