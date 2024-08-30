package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"time"
)

// Block represents an EcoPulse block
type Block struct {
	Header  *BlockHeader
	Transactions []*Transaction
}

// NewBlock creates a new EcoPulse block
func NewBlock(header *BlockHeader, transactions []*Transaction) *Block {
	return &Block{
		Header:  header,
		Transactions: transactions,
	}
}

// Hash returns the block hash
func (b *Block) Hash() string {
	hash := sha256.Sum256([]byte(fmt.Sprintf("%x%x%x", b.Header.Hash, b.Header.Timestamp, b.Header.Nonce)))
	return hex.EncodeToString(hash[:])
}

// BlockHeader represents the header of an EcoPulse block
type BlockHeader struct {
	Hash      string
	Timestamp int64
	Nonce     uint64
	PrevHash  string
}

// NewBlockHeader creates a new EcoPulse block header
func NewBlockHeader(prevHash string, nonce uint64) *BlockHeader {
	return &BlockHeader{
		Timestamp: time.Now().UnixNano(),
		Nonce:     nonce,
		PrevHash:  prevHash,
	}
}

// Hash returns the block header hash
func (h *BlockHeader) Hash() string {
	hash := sha256.Sum256([]byte(fmt.Sprintf("%x%x%x", h.Timestamp, h.Nonce, h.PrevHash)))
	return hex.EncodeToString(hash[:])
}
