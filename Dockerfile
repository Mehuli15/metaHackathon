FROM python:3.10

WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn pandas openai pydantic openenv-core

# Expose HuggingFace port
EXPOSE 7860

# Run correct FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]