FROM continuumio/miniconda3
RUN apt-get update && apt-get install libgl1 -y && apt-get install curl -y && apt-get install gcc python3-dev -y
RUN python -m pip install mlflow==2.8