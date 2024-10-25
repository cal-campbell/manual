# Stage 1: Backend (Flask-based RAG pipeline)
FROM python:3.9 AS backend
WORKDIR /app/backend

# Copy requirements.txt from the root to /app/backend and install dependencies
COPY requirements.txt /app/backend/requirements.txt
RUN pip install -r /app/backend/requirements.txt

# Copy the backend code from backend/ to /app/backend in the container
COPY backend/ .

# Copy daikin.pdf specifically to the data directory in the backend stage
COPY backend/data/daikin.pdf /app/backend/data/

# Stage 2: Frontend (React app) and Server (Express)
FROM node:14 AS build
WORKDIR /app

# Copy the frontend (React) and server (Express) code from local folders to the container
COPY client/ client
COPY server/ server

# Install dependencies and build the React frontend
WORKDIR /app/client
RUN npm install
RUN npm run build

# Install dependencies for the Express server
WORKDIR /app/server
RUN npm install

# Final Stage: Combine and Set Up for Production
FROM python:3.9
WORKDIR /app

# Install Node.js and npm to make pm2 available
RUN apt-get update && apt-get install -y nodejs npm

# Copy backend, server, and frontend build files from previous stages
COPY --from=backend /app/backend /app/backend
COPY --from=build /app/client/build /app/client/build
COPY --from=build /app/server /app/server

# Reinstall Python dependencies in the final stage to ensure Flask and others are available
COPY requirements.txt /app/backend/requirements.txt
RUN pip install -r /app/backend/requirements.txt

# Install pm2 globally for managing multiple processes (Flask and Express)
RUN npm install -g pm2

# Copy the ecosystem.config.js to configure PM2
COPY ecosystem.config.js /app/ecosystem.config.js

# Expose ports for Flask (5000), Express (3000), and the React app (80)
EXPOSE 3000 5000 80

# Start both Flask and Express apps with pm2 using ecosystem.config.js
CMD ["pm2-runtime", "start", "ecosystem.config.js"]

