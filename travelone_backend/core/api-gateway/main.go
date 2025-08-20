package main

import (
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
)

// Define the URLs for your backend services.
// The service names 'go-auth-service' are automatically resolved by Docker's internal DNS.
var (
	authServiceURL *url.URL
)

// init runs before main() and sets up our target URLs.
func init() {
	var err error
	// The URL for the go-auth-service running in its own container.
	authServiceURL, err = url.Parse("http://go-auth-service:8080")
	if err != nil {
		log.Fatal(err)
	}
}

// newReverseProxy creates a reverse proxy for a given URL.
func newReverseProxy(target *url.URL) *httputil.ReverseProxy {
	proxy := httputil.NewSingleHostReverseProxy(target)
	return proxy
}

// main is the entry point of our custom API gateway.
func main() {
	// Create a reverse proxy for the authentication service.
	authProxy := newReverseProxy(authServiceURL)

	// Create a new handler that strips the "/auth" prefix and forwards the request.
	// This is the key change that resolves the 404 error.
	authHandler := http.StripPrefix("/auth", authProxy)

	// The gateway listens on port 8080.
	http.Handle("/auth/", authHandler)

	log.Println("Custom Go API Gateway is starting on port 8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
