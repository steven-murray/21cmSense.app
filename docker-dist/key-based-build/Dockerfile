# use python 3.10.2
FROM python:3.10.2-bullseye

# pass keys during build in order to clone from repo
ARG ssh_prv_key
ARG ssh_pub_key
ARG branch

# set up ssh configuration
RUN mkdir -p /root/.ssh && chmod 0700 /root/.ssh
RUN echo "$ssh_prv_key" > /root/.ssh/id_ed25519 && \
    echo "$ssh_pub_key" > /root/.ssh/id_ed25519.pub && \
    chmod 600 /root/.ssh/id_ed25519 && \
    chmod 600 /root/.ssh/id_ed25519.pub && \
    ssh-keyscan github.com > /root/.ssh/known_hosts

# utilize correct key when cloning
RUN echo "Host github.com\nIdentityFile=/root/.ssh/id_ed25519"

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

# remove ssh keys
RUN rm -rf /root/.ssh/

RUN cd SER401-Project43 && \
    git checkout ${branch} && \
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

