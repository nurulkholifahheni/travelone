package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
)

// / di sini [w] ini adalah writernya dan [r] adalah requestnya
func registerHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error Reading Request Body", http.StatusBadRequest)
		log.Printf("Error Reading Request %v", err)
		return
	}

	defer r.Body.Close()

	fmt.Printf("received body = \n%s\n", string(body))
}

func main() {

	http.HandleFunc("/register", registerHandler)

	log.Fatal(http.ListenAndServe(":8080", nil))

}
