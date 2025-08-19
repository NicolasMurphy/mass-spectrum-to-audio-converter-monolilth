FROM node:22-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./

# Production API URL - will be set by Render or build args
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM python:3.13
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./api/
COPY audio/ ./audio/
COPY db/ ./db/
COPY utils/ ./utils/
COPY app.py ./
COPY --from=frontend-builder /app/frontend/dist ./static/

EXPOSE 5000
CMD ["python", "app.py"]
