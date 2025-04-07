# frontend/Dockerfile
FROM node:18

WORKDIR /app

COPY ./frontend/package*.json ./
RUN npm install

COPY ./frontend .

EXPOSE 5173

CMD ["npx", "vite", "--host", "0.0.0.0"]
