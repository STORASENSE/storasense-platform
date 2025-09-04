FROM node:current-alpine3.22 AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /frontend
COPY ./frontend/package.json ./frontend/package-lock.json* ./
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /frontend
COPY --from=deps ./frontend/node_modules ./node_modules
COPY ./frontend ./
RUN npm run build

FROM base AS runner
WORKDIR /frontend

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

ENV NODE_ENV=production
COPY --from=builder ./frontend/public ./public
COPY --from=builder ./frontend/.next/standalone ./
COPY --from=builder ./frontend/.next/static ./.next/static


EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"
CMD ["node", "server.js"]
