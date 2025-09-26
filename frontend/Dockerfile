# build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci
COPY . .
RUN npm run build

# production stage
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
# Optional: copy a custom nginx.conf if you need SPA routing
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]