from waitress import serve
import wsgiref
import gunicorn
import waitress
import main

# serve(main.create_app(), host='0.0.0.0', port=8080)
serve(main.app, host='0.0.0.0', port=8080)

# to run the srever python waitress_server.py