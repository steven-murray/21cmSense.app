from app import create_app

# from mod_main import mod_main as main_blueprint
# app.register_blueprint(main_blueprint)

# from . import views, errors

app=create_app('default')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
