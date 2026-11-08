# SCANNAI Frontend Dockerfile
# Stage 1: Build the React + TypeScript + Vite application
FROM node:22-alpine AS build

WORKDIR /app

# Install dependencies with lockfile consistency
COPY package.json package-lock.json ./
RUN npm ci

# Copy frontend source and build production bundle
COPY . .
RUN npm run build

# Stage 2: Serve production bundle with hardened Nginx
FROM nginx:alpine

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy compiled assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
