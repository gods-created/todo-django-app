FROM python:3.13-alpine
COPY . /app 
WORKDIR /app 
EXPOSE 8001 
RUN chmod 777 -R /app/*
RUN pip install --no-cache-dir --upgrade -r requirements.txt
ENTRYPOINT [ "/app/entrypoint.sh" ]