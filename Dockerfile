FROM node:10-alpine

# https://github.com/labhackercd/alpine-python3-nodejs/blob/master/Dockerfile
RUN apk add --no-cache python python-dev python3 python3-dev \
    linux-headers build-base bash git ca-certificates && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    rm -r /root/.cache


WORKDIR /app
COPY . .
RUN cd travelrec-web && \
    npm install && \
    npm install -g @angular/cli && \
    ng build --base-href /app/ --prod && \
    cd .. && \
    pip install -r requirements.txt

# EXPOSE 5000
# CMD ["python", "server.py"]
