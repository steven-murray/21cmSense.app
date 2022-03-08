# use python 3.9.8
FROM python:3.9.8-bullseye

# os-level dependency for hd5 library
RUN apt-get update -y && \
    apt-get install -y libhdf5-dev && \
    apt-get install -y nginx && \
    apt install -y vim && \
    apt install -y netcat && \
    apt install -y redis


COPY nginx.conf /etc/nginx/sites-available/p43_nginx
RUN rm -f /etc/nginx/sites-enabled/default && \
    ln -s ../sites-available/p43_nginx /etc/nginx/sites-enabled/p43_nginx

# install python dependencies
RUN python3 -m pip install --upgrade pip

WORKDIR /home/app
RUN git clone git@github.com:bpape1usa/SER401-Project43.git
COPY docker-run-app.sh /home/app/SER401-Project43

RUN cd SER401-Project43 && \
    git checkout bpape1-s7 && \
    pip install -r requirements.txt && \
    cd ..

# download and configure py21cmSense dependency
WORKDIR /home/app/SER401-Project43
RUN git clone https://github.com/steven-murray/21cmSense && \
    cd 21cmSense && \
    python ./setup.py install && \
    cd ..


# nginx runs on port 80 inside container.
# start container like this: docker run -p8081:80 p43
ENTRYPOINT [ "./docker-run-app.sh" ]

# Flask app can use parameters --port=8080 --bind-address=1.2.3.4
# but this container uses nginx and WSGI
#CMD [ "" ]

