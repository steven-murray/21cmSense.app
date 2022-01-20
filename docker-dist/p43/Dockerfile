FROM python:3.10.2-bullseye

ARG ssh_prv_key
ARG ssh_pub_key

RUN mkdir -p /root/.ssh && chmod 0700 /root/.ssh
RUN echo "$ssh_prv_key" > /root/.ssh/id_ed25519 && \
    echo "$ssh_pub_key" > /root/.ssh/id_ed25519.pub && \
    chmod 600 /root/.ssh/id_ed25519 && \
    chmod 600 /root/.ssh/id_ed25519.pub && \
    ssh-keyscan github.com > /root/.ssh/known_hosts


RUN echo "Host github.com\nIdentityFile=/root/.ssh/id_ed25519"

RUN apt-get update -y && \
    apt-get install -y libhdf5-dev

#StrictHostKeyChecking no\n" > ~/.ssh/config &&

RUN python3 -m pip install --upgrade pip

WORKDIR /home/app
#RUN git clone https://github.com/bpape1usa/SER401-Project43.git
RUN git clone git@github.com:bpape1usa/SER401-Project43.git

RUN rm -rf /root/.ssh/

RUN cd SER401-Project43 && pip install -r requirements.txt && cd ..


WORKDIR /home/app/SER401-Project43
RUN git clone https://github.com/steven-murray/21cmSense
#WORKDIR /home/app

#RUN python3 -m venv venv && source venv/bin/activate

RUN cd 21cmSense && python ./setup.py install && cd ..

ENTRYPOINT [ "/usr/local/bin/python3", "app.py" ]
CMD [ ]

#WORKDIR /usr/src/app

#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt
#
#COPY . .
#
#CMD [ "python", "./your-daemon-or-script.py" ]
