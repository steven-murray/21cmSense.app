# use python 3.10.2
FROM python:3.10.2-bullseye

ARG branch

# os-level dependency for hd5 library
RUN apt-get update -y && \
    apt-get install -y libhdf5-dev && \
    apt-get install -y nginx && \
    apt install -y vim && \
    apt install -y netcat && \
    apt install -y redis

# set up self-signed certificate for nginx
COPY openssl.cnf /tmp
COPY nginx-selfsigned-ssl.conf /etc/nginx/snippets
RUN openssl req -x509 -nodes -days 1825 -newkey rsa:2048 -config /tmp/openssl.cnf -keyout /etc/ssl/private/nginx.key -out /etc/ssl/certs/nginx.crt

# this step takes a very long time; only use when you're ready for a production image
#RUN openssl dhparam -out /etc/nginx/dhparam.pem 4096

COPY nginx.conf /etc/nginx/sites-available/p43_nginx
RUN rm -f /etc/nginx/sites-enabled/default && \
    ln -s ../sites-available/p43_nginx /etc/nginx/sites-enabled/p43_nginx

# install python dependencies
RUN python3 -m pip install --upgrade pip

WORKDIR /home/app
RUN git clone git@github.com:steven-murray/21cmSense-app.git
COPY docker-run-app.sh /home/app/SER401-Project43

RUN cd SER401-Project43 && \
    git checkout ${branch} && \
    pip install -r requirements.txt && \
    cd ..

# download and configure py21cmSense dependency
WORKDIR /home/app/SER401-Project43
RUN git clone https://github.com/steven-murray/21cmSense && \
    cd 21cmSense && \
    pip install . && \
    cd ..


# nginx runs on port 80 inside container.
# start container like this: docker run -p8081:80 p43
ENTRYPOINT [ "./docker-run-app.sh" ]

# Flask app can use parameters --port=8080 --bind-address=1.2.3.4
# but this container uses nginx and WSGI
#CMD [ "" ]
