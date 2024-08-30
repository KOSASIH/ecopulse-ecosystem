package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
)

// Config represents the EcoPulse node configuration
type Config struct {
	EthRPCURL    string `json:"eth_rpc_url"`
	PrivateKey  string `json:"private_key"`
	NetworkConfig `json:"network_config"`
}

// NetworkConfig represents the EcoPulse network configuration
type NetworkConfig struct {
	NetworkID  string `json:"network_id"`
	NodeID    string `json:"node_id"`
	Peers     []string `json:"peers"`
	ListenAddr string `json:"listen_addr"`
}

// LoadConfig loads the EcoPulse node configuration from a file
func LoadConfig(filename string) (*Config, error) {
	var config Config

	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}

	err = json.Unmarshal(data, &config)
	if err != nil {
		return nil, err
	}

	return &config, nil
}
