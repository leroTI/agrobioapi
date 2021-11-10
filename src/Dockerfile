FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt
RUN pip install uwsgi

ENV FLASK_APP=wsgi.py
ENV FLASK_ENV="production"
ENV FLASK_DEBUG=False


EXPOSE 4000

# RUN python confignltk.py
ENV API_VERSION_AGRO=1.0.1


CMD ["uwsgi","app.ini"]
# CMD [ "python3", "src/bioapp.py" ]