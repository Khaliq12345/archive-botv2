import sys
import os

sys.path.append(".")


if __name__ == "__main__":
    os.system("fastapi run ./api/app.py --port=9500 --host=0.0.0.0")
