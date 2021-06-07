FROM python:3.8.5
EXPOSE 5000/tcp
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY main.py .
CMD [ "python", "./main.py" ]