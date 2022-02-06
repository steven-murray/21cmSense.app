# To start docker container:
`docker run -ti -p 127.0.0.1:80:8081/tcp p43:latest`

# Notes
use of the port publish parameter:
[local bind addr:]local_port:container_port[/protocol]

So to bind port 80 of the container (where nginx is listening) to port 8081 on the local machine,
listening on 0.0.0.0 (all interfaces), use `-p 80:8081/tcp`.


## gunicorn
gunicorn --bind=unix:/tmp/gunicorn.sock --workers=2 wsgi:create_app

gunicorn logging:

gunicorn --bind=unix:/tmp/gunicorn.sock --workers=2 --log-file=/var/log/gune --log-level debug --access-logfile=/var/log/guna wsgi:create_app
