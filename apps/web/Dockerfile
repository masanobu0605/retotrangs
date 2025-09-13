# Dev-oriented Dockerfile
FROM node:22-alpine
WORKDIR /app

# Enable pnpm via corepack
RUN corepack enable && corepack prepare pnpm@latest --activate

COPY package.json ./
COPY tsconfig.json ./
COPY next.config.mjs ./
COPY next-env.d.ts ./
COPY .eslintrc.json ./
COPY tailwind.config.cjs ./
COPY postcss.config.cjs ./
COPY app ./app
COPY lib ./lib

RUN pnpm install --ignore-scripts || true

ENV HOST=0.0.0.0 PORT=3000
EXPOSE 3000
CMD ["pnpm", "dev"]
