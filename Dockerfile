FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./.env.sampl[e] /code/.env.sample

COPY ./.en[v] /code/.env
#add checking of exitsting

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]