FROM python:3.8
WORKDIR /usr/src/app
COPY . .
RUN pip install Pillow
ENTRYPOINT [ "python", "./server.py" ]

