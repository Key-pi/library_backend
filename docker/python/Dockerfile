FROM python:3.9

WORKDIR /backend

COPY backend/requirements.txt backend/requirements.txt

RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin gettext --fix-missing
RUN pip install -r backend/requirements.txt

#COPY backend /backend

CMD ["python", "api/main.py"]