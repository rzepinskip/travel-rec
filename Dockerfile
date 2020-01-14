FROM python

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get install -y nodejs

WORKDIR /app
COPY . .

RUN cd travelrec-web && \
    npm install && \
    npm install -g @angular/cli && \
    ng build --base-href /app/ --prod && \
    cd .. 

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "server.py"]
