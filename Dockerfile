FROM python:3.11-bullseye

# install lts nodejs
# RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
# RUN apt-get install -y nodejs

WORKDIR /app

COPY . .

# RUN npm install -g @vue/cli
# RUN npm install
RUN pip install -r requirements.txt

CMD [ "bash" ]


# docker build -t hello-world .
# docker run -it --rm hello-world





