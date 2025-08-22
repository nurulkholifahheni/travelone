# Stage 1: The Builder Stage
# We use a base image with the Go compiler to build our executable.
# The version should match the Go version you are using, or be a recent stable version.
FROM golang:1.25 AS builder

# Set the working directory inside the container for our source code.
WORKDIR /app

# Copy the Go module file. Since there are no external dependencies,
# go.sum does not exist.
COPY go.mod ./
# No need to run go mod download as there are no dependencies.

# Copy all the application source code into the container.
COPY . .

# Build the Go application.
# CGO_ENABLED=0 disables cgo, which makes the binary statically compiled.
# This means it has no external dependencies and can run on the Alpine base image.
# The -o flag names the output executable as "go-server".
RUN CGO_ENABLED=0 go build -o go-server .

# Stage 2: The Final (Minimal) Image
# We use a minimal base image, `alpine`, to reduce the final container size.
# This image is just a few megabytes, resulting in a very lightweight container.
FROM alpine:latest

# Set the working directory for the final image.
WORKDIR /root/

# Copy the compiled executable from the builder stage.
COPY --from=builder /app/go-server .

# Expose the port on which the Go service will listen.
# This assumes your `main.go` file listens on port 8080.
EXPOSE 8080

# The command to run our executable when the container starts.
CMD ["./go-server"]
