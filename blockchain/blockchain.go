package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"log"
	"sync"

	"github.com/ethereum/go-ethereum/core/types"
)

// Blockchain represents the EcoPulse blockchain
type Blockchain struct {
	Blocks  []*Block
	Chain  []*types.Block
	CurrentBlock *Block
	Transactions []*Transaction
	Mutex  sync.RWMutex
}

// NewBlockchain creates a new EcoPulse blockchain
func NewBlockchain() *Blockchain {
	return &Blockchain{
		Blocks:  make([]*Block, 0),
		Chain:  make([]*types.Block, 0),
	}
}

// AddBlock adds a new block to the blockchain
func (b *Blockchain) AddBlock(block *Block) error {
	b.Mutex.Lock()
	defer b.Mutex.Unlock()

	// Verify block hash
	hash := block.Hash()
	if hash != block.Header.Hash {
		return fmt.Errorf("invalid block hash")
	}

	// Add block to chain
	b.Chain = append(b.Chain, block)

	// Update current block
	b.CurrentBlock = block

	return nil
}

// AddTransaction adds a new transaction to the blockchain
func (b *Blockchain) AddTransaction(tx *Transaction) error {
	b.Mutex.Lock()
	defer b.Mutex.Unlock()

	// Verify transaction hash
	hash := tx.Hash()
	if hash != tx.ID {
		return fmt.Errorf("invalid transaction hash")
	}

	// Add transaction to transactions pool
	b.Transactions = append(b.Transactions, tx)

	return nil
}

// GetBlock returns a block by its hash
func (b *Blockchain) GetBlock(hash string) (*Block, error) {
	b.Mutex.RLock()
	defer b.Mutex.RUnlock()

	for _, block := range b.Chain {
		if block.Hash() == hash {
			return block, nil
		}
	}

	return nil, fmt.Errorf("block not found")
}

// GetTransaction returns a transaction by its hash
func (b *Blockchain) GetTransaction(hash string) (*Transaction, error) {
	b.Mutex.RLock()
	defer b.Mutex.RUnlock()

	for _, tx := range b.Transactions {
		if tx.Hash() == hash {
			return tx, nil
		}
	}

	return nil, fmt.Errorf("transaction not found")
}
