FROM python:3.11 
LABEL author="Yufo Fukuda"

WORKDIR minesweeperapp

COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install -y iputils-ping
RUN pip install numpy pandas scikit-learn
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY tests/ tests/
COPY web/ web/

CMD ["python", "web/app.py"]