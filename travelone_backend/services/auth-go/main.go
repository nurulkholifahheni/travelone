package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
)

// / di sini [w] ini adalah writernya dan [r] adalah requestnya
// / [http.ResponseWriter] itu adalah objek yang didefinisikan di [http]
// / [Request] juga adalah objek yang didefinisikan di [http]
// / Syntaxnya mirip seperti fungsi biasa, bedanya di sini nama variablenya disebutin duluan
// / kemudian baru class of objectnya, jadi klo di Java biasanya send(Request req), klo di sini jadi
// / send(req Request)
func registerHandler(w http.ResponseWriter, r *http.Request) {

	// / [r.Method] adalah atribut yang dimiliki oleh [r]
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
