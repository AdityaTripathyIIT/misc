package main

import (
	"crypto/aes"
  "crypto/cipher"
  "crypto/rand"
	"encoding/hex"
	"fmt"
	"os"
)

func readKeyFromHexFile(filename string) ([]byte, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var hexKey string
	_, err = fmt.Fscanf(file, "%s", &hexKey)
	if err != nil {
		return nil, err
	}
	key, err := hex.DecodeString(hexKey)
	if err != nil {
		return nil, err
	}

	return key, nil
}

func encryptAESGCM(plainText []byte, key []byte) ([]byte, error) {
	aes, err := aes.NewCipher(key)
  gcm, err := cipher.NewGCM(aes)
	if err != nil {
		return nil, err
	}
	if err != nil {
		return nil, err
	}
	nonce := make([]byte, gcm.NonceSize())
	_, err = rand.Read(nonce)
	if err != nil {
		return nil, err
	}
	ciphertext := gcm.Seal(nonce, nonce, plainText, nil)
	return ciphertext, nil
}
func main() {
	key, err := readKeyFromHexFile("aes_key_hex.txt")
	if err != nil {
		fmt.Println("Error reading key from file:", err)
		return
	}
	plainText := []byte("hackerone.aditya.tripathy")

	ciphertext, err := encryptAESGCM(plainText, key)
	if err != nil {
		fmt.Println("Error encrypting:", err)
		return
	}
	fmt.Println("Ciphertext (hex):", hex.EncodeToString(ciphertext))
}

