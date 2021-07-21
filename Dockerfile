FROM python:3.8

RUN mkdir -p /home/app


WORkDIR /home/app
EXPOSE 5000
COPY requirements.txt .
RUN pip install --upgrade -r requirements.txt 

COPY . /home/app


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD ["python", "app.py"]
