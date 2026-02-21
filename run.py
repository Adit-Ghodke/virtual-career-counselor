import os

from flask import Flask
from app import create_app

app: Flask = create_app()

if __name__ == "__main__":
    port: int = int(os.environ.get("PORT", "10000"))
    app.run(debug=True, host="0.0.0.0", port=port)
