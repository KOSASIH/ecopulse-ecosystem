package main

import (
	"crypto/ecdsa"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
)

// Transaction represents an EcoPulse transaction
type Transaction struct {
	ID        string
	Sender    *ecdsa.PublicKey
	Recipient *ecdsa.PublicKey
	Amount     uint64
	Fee       uint64
	Data      []byte
	Signature []byte
}

// NewTransaction creates a new EcoPulse transaction
func NewTransaction(sender, recipient *ecdsa.PublicKey, amount, fee uint64, data []byte) (*Transaction, error) {
	tx := &Transaction{
		Sender:    sender,
		Recipient: recipient,
		Amount:     amount,
		Fee:       fee,
		Data:      data,
	}

	// Generate transaction ID
	hash := sha256.Sum256([]byte(fmt.Sprintf("%x%x%x%x", sender, recipient, amount, fee)))
	tx.ID = hex.EncodeToString(hash[:])

	return tx, nil
}

// Hash returns the transaction hash
func (t *Transaction) Hash() string {
	hash := sha256.Sum256([]byte(fmt.Sprintf("%x%x%x%x", t.Sender, t.Recipient, t.Amount, t.Fee)))
	return hex.EncodeToString(hash[:])
}

// Sign signs the transaction with the sender's private key
func (t *Transaction) Sign(privateKey *ecdsa.PrivateKey) error {
	hash := sha256.Sum256([]byte(t.ID))
	signature, err := ecdsa.SignASN1(rand.Reader, privateKey, hash[:])
	if err != nil {
		return err
	}

	t.Signature = signature

	return nil
}

// Verify verifies the transaction signature
func (t *Transaction) Verify() bool {
	hash := sha256.Sum256([]byte(t.ID))
	return ecdsa.VerifyASN1(t.Sender, hash[:], t.Signature)
}
