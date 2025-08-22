package main

// / Ini syntax untuk importnya bentuknya seperti ini.
import (
	"fmt"
	"io"
	"log"
	"net/http"
)

// / di sini [w] ini adalah writernya dan [r] adalah requestnya
// / [w] itu barangnya adalah [http.ResponseWriter] yang objek yang didefinisikan di [http]
// / [r] itu barangnya adalah [Request] yang juga didefinisikan di [http]
// / Syntaxnya mirip seperti fungsi biasa, bedanya di sini nama variablenya disebutin duluan
// / kemudian baru class of objectnya, jadi klo di Java biasanya send(Request req), klo di sini jadi
// / send(req Request)
func registerHandler(w http.ResponseWriter, r *http.Request) {

	// / [r.Method] adalah atribut yang dimiliki oleh [r].
	// / [e.Method] menampilkan metode request yang dikirimkan oleh client
	// / contonya adalah GET, POST, PUT, DELETE, dll
	// / [http.Error] adalah fungsi yang tugasnya untuk menampilkan error
	if r.Method != "POST" {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)

		// / Ini misalkan metodenya bukan POST maka eksekusi fungsinya akan berakhir, alias return
		return
	}

	// / Di sini, [body, err] adalah output dari [io.ReadAll(r.Body)]. [body] di sini adalah body request
	// / dan [err] adalah error yang dihasilkan oleh [io.ReadAll].
	body, err := io.ReadAll(r.Body)
	if err != nil {

		// /Jadi klo requestnya gagal dibaca, alias bodynya
		// / tidak bisa dibaca, maka dia akan menghasilkan error
		// / di golang, fungsi [http.Error] punya 3 argumen, yaitu [w], yang merupakan writer
		// / kemudian text errornya, kemudian statusnya.
		http.Error(w, "Error Reading Request Body", http.StatusBadRequest)
		log.Printf("Error Reading Request %v", err)
		return
	}

	// / ini aku kurang ngerti untuk apa, tapi yaudah lah ya... ikutin aja.
	defer r.Body.Close()

	// / ini sama kyk print di python.
	fmt.Printf("received body = \n%s\n", string(body))
}

// / Ini adalah main functionnya yang merupakan fungsi utama yang dipakai untuk menjalankan
// / seluruh fungsional yang ada di aplikasi backend ini.
func main() {

	// / [http.HandleFunc] ini adalah fungsi yang dipakai untuk meneruskan route ke fungsi yang bersesuaian
	// / Jadi kalo requestnya memanggil endpoint /register, maka dia akan memanggil registerHandler
	http.HandleFunc("/register", registerHandler)

	// / Ini adalah fungsi yang paling harus ditulis, yaitu ListenAndServe, karena ini adalah
	// / Fungsi untuk serving aplikasi golang.
	log.Fatal(http.ListenAndServe(":8080", nil))

}
