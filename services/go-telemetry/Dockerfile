# Multi-stage Dockerfile for Go Telemetry Service
FROM golang:1.23-alpine AS builder

WORKDIR /app
COPY go.mod ./
COPY *.go ./

RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o aeovexor-telemetry-service .

FROM alpine:3.20
RUN apk --no-cache add ca-certificates tzdata

WORKDIR /app
COPY --from=builder /app/aeovexor-telemetry-service .

EXPOSE 8766
ENTRYPOINT ["./aeovexor-telemetry-service"]
