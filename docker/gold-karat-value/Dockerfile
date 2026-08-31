FROM python:3.12-alpine

LABEL org.opencontainers.image.title="gold-karat-value"
LABEL org.opencontainers.image.description="Estimate gold melt and scrap value from karat, weight, and a 24K price per gram."
LABEL org.opencontainers.image.url="https://mygoldcalc.com/scrap-gold-calculator"
LABEL org.opencontainers.image.source="https://github.com/ilovejackylee/gold-karat-value"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app
COPY gold_karat_value.py /app/gold_karat_value.py

ENTRYPOINT ["python", "/app/gold_karat_value.py"]
CMD ["--help"]
