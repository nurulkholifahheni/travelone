// utils.go
// This file contains a utility function to establish a database connection.
package database

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/jackc/pgx/v5/pgxpool"
)

// Config represents the database connection configuration.
type Config struct {
	Host     string
	Port     int
	User     string
	Password string
	DBName   string
}

// NewDBPool creates and returns a new database connection pool.
// It uses environment variables for configuration, which is a best practice for security.
func NewDBPool(ctx context.Context) (*pgxpool.Pool, error) {
	// Build the connection string from environment variables.
	connStr := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
		os.Getenv("DB_HOST"),
		os.Getenv("DB_PORT"),
		os.Getenv("DB_USER"),
		os.Getenv("DB_PASSWORD"),
		os.Getenv("DB_NAME"),
	)

	// Use pgxpool.Connect to establish a connection pool.
	// A connection pool is more efficient for high-traffic applications than a single connection.
	pool, err := pgxpool.New(ctx, connStr)
	if err != nil {
		log.Fatalf("Unable to connect to database: %v\n", err)
		return nil, fmt.Errorf("unable to connect to database: %w", err)
	}

	// Ping the database to ensure the connection is successful.
	err = pool.Ping(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to ping database: %w", err)
	}

	fmt.Println("Successfully connected to the database!")
	return pool, nil
}

// You can add other utility functions here, such as:
// - A function to run database migrations
// - A function to seed data for development
