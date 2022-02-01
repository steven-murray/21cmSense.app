from app import create_app

if not __name__ == "__main__":
	gunicorn_app = create_app('default')
else:
	print("ERROR: Main application should be started with app.py");
