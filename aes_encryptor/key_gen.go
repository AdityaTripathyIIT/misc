package main

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"os"
)

func generateRandomKey() ([]byte, error) {
	key := make([]byte, 16)
	_, err := rand.Read(key)
	if err != nil {
		return nil, err
	}
	return key, nil
}
func main() {
	key, err := generateRandomKey()
	if err != nil {
		fmt.Println("Error generating key:", err)
		return
	}
	hexKey := hex.EncodeToString(key)
	file, err := os.Create("aes_key_hex.txt")
	if err != nil {
		fmt.Println("Error creating file:", err)
		return
	}
	defer file.Close()
	_, err = file.WriteString(hexKey)
	if err != nil {
		fmt.Println("Error writing to file:", err)
		return
	}
}

