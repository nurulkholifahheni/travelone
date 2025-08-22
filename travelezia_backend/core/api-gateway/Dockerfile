# Stage 1: The Builder Stage
FROM golang:1.25 AS builder

# Set the working directory inside the container for our source code.
WORKDIR /app

# Copy go.mod and go.sum separately to avoid issues if go.sum is missing.
COPY go.mod .

# Download the Go modules.
RUN go mod download

# Copy all the application source code into the container.
COPY . .

# Build the Go application.
# CGO_ENABLED=0 disables cgo, which makes the binary statically compiled.
# The -o flag names the output executable as "go-gateway".
RUN CGO_ENABLED=0 go build -o go-gateway .

# Stage 2: The Final (Minimal) Image
# We use a minimal base image, `alpine`, to reduce the final container size.
FROM alpine:latest

# Set the working directory for the final image.
WORKDIR /root/

# Copy the compiled executable from the builder stage.
COPY --from=builder /app/go-gateway .

# Expose the port on which the Go service will listen.
EXPOSE 8080

# The command to run our executable when the container starts.
CMD ["./go-gateway"]
