FROM node:22.19.0-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
RUN npm run build

FROM node:22.19.0-slim AS final
WORKDIR /app
COPY --from=builder /app/build ./build
EXPOSE 3000
CMD ["npx", "-y", "http-server", "-p", "3000", "./build"]