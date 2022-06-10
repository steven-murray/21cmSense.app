from app import create_app

if not __name__ == "__main__":
    gunicorn_app = create_app()
else:
    raise Exception("Main application should be started with app.py")
