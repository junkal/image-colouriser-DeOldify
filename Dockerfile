FROM python:3.8.5

COPY ./server ./server

WORKDIR /server

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt

ENV FLASK_APP server.py

EXPOSE 4000

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port", "4000"]