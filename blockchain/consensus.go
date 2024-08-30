package main

import (
	"fmt"
	"sync"
)

// Consensus represents the EcoPulse consensus algorithm
type Consensus struct {
	Blockchain *Blockchain
	Mutex      sync.RWMutex
}

// NewConsensus creates a new EcoPulse consensus algorithm
func NewConsensus(blockchain *Blockchain) *Consensus {
	return &Consensus{
		Blockchain: blockchain,
	}
}

// VerifyBlock verifies a block and adds it to the blockchain if valid
func (c *Consensus) VerifyBlock(block *Block) error {
	c.Mutex.Lock()
	defer c.Mutex.Unlock()

	// Verify block hash
	hash := block.Hash()
	if hash != block.Header.Hash {
		return fmt.Errorf("invalid block hash")
	}

	// Verify block transactions
	for _, tx := range block.Transactions {
		if !tx.Verify() {
			return fmt.Errorf("invalid transaction signature")
		}
	}

	// Add block to blockchain
	c.Blockchain.AddBlock(block)

	return nil
}

// Mine mines a new block and adds it to the blockchain
func (c *Consensus) Mine(transactions []*Transaction) (*Block, error) {
	c.Mutex.Lock()
	defer c.Mutex.Unlock()

	// Create new block header
	header := NewBlockHeader(c.Blockchain.CurrentBlock.Header.Hash, 0)

	// Create new block
	block := NewBlock(header, transactions)

	// Mine block
	for {
		header.Nonce++
		block.Header = header
		hash := block.Hash()
		if hash < "0000000000000000000000000000000000000000000000000000000000000000" {
			break
		}
	}

	// Add block to blockchain
	c.Blockchain.AddBlock(block)

	return block, nil
}
