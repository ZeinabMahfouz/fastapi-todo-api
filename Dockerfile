# python:3.10-slim
FROM python:3.10-slim

# 2. selecting the working directory inside the container
WORKDIR /app

# 3. copying the requirements file and installing dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. copying the rest of the project code to the container
COPY . .

# 5. exposing port 8000
EXPOSE 8000

# 6. command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]