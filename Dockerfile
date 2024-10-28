# Stage 1: Backend (Flask-based RAG pipeline)
FROM python:3.9 AS backend
WORKDIR /app/backend

# Install Python dependencies for Flask
COPY requirements.txt /app/backend/requirements.txt
RUN pip install -r /app/backend/requirements.txt

# Copy backend code and data
COPY backend/ .
COPY backend/data/daikin.pdf /app/backend/data/

# Stage 2: Frontend (React app) and Server (Express)
FROM node:14 AS build
WORKDIR /app

# Copy frontend (React) and server (Express) code
COPY client/ client
COPY server/ server

# Install dependencies and build React
WORKDIR /app/client
RUN npm install
RUN npm run build

# Install dependencies for Express server
WORKDIR /app/server
RUN npm install

# Final Stage: Set Up for Production with PM2
FROM python:3.9
WORKDIR /app

# Install Node.js and npm for pm2
RUN apt-get update && apt-get install -y nodejs npm

# Copy backend, server, and frontend build files from previous stages
COPY --from=backend /app/backend /app/backend
COPY --from=build /app/client/build /app/client/build
COPY --from=build /app/server /app/server

# Reinstall Python dependencies for Flask
RUN pip install -r /app/backend/requirements.txt

# Install pm2 globally to manage multiple processes
RUN npm install -g pm2

# Copy the PM2 configuration file for process management
COPY ecosystem.config.js /app/ecosystem.config.js

# Expose necessary ports
EXPOSE 3000 5000 80

# Start both Flask and Express using pm2
CMD ["pm2-runtime", "start", "ecosystem.config.js"]

