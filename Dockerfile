FROM python
WORKDIR ~/
COPY CMG.py CMG_data.txt .
CMD ["python3", "CMG.py"]