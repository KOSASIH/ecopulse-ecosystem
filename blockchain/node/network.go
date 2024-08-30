package main

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"log"
	"net"
	"sync"

	"github.com/libp2p/go-libp2p-core/network"
	"github.com/libp2p/go-libp2p-core/peer"
)

// Network represents the EcoPulse network
type Network struct {
	Config *NetworkConfig
	Peers  map[string]*peer.Peer
	ListenAddr string
}

// NewNetwork creates a new EcoPulse network
func NewNetwork(config *NetworkConfig) (*Network, error) {
	network := &Network{
		Config: config,
		Peers:  make(map[string]*peer.Peer),
	}

	// Initialize libp2p network
host, err := network.NewHost(
	config.NetworkID,
	config.NodeID,
	config.Peers,
	config.ListenAddr,
)
if err != nil {
	return nil, err
}

network.Host = host

// Start listening for incoming connections
lis, err := net.Listen("tcp", config.ListenAddr)
if err != nil {
	return nil, err
}
defer lis.Close()

log.Println("Listening on", config.ListenAddr)

// Start libp2p network
err = network.Host.SetListenCloseFunc(func(ln net.Listener) {
	ln.Close()
})
if err != nil {
	return nil, err
}

err = network.Host.SetStreamHandler(protocol.ID("/ecopulse/1.0.0"), network.handleStream)
if err != nil {
	return nil, err
}

return network, nil
}

// handleStream handles incoming streams
func (n *Network) handleStream(s network.Stream) {
	log.Println("Incoming stream from", s.Conn().RemotePeer())

	// Handle stream data
	buf := make([]byte, 1024)
	_, err := s.Read(buf)
	if err != nil {
		log.Println(err)
		return
	}

	log.Println("Received data:", string(buf))

	// Send response back
	_, err = s.Write([]byte("Hello from EcoPulse!"))
	if err != nil {
		log.Println(err)
		return
	}
}

// Connect connects to a peer
func (n *Network) Connect(peerID string) error {
	pi, err := peer.Decode(peerID)
	if err != nil {
		return err
	}

	err = n.Host.Connect(context.Background(), pi)
	if err != nil {
		return err
	}

	log.Println("Connected to", peerID)

	return nil
}

// Disconnect disconnects from a peer
func (n *Network) Disconnect(peerID string) error {
	pi, err := peer.Decode(peerID)
	if err != nil {
		return err
	}

	err = n.Host.CloseConnection(pi)
	if err != nil {
		return err
	}

	log.Println("Disconnected from", peerID)

	return nil
}

// Send sends data to a peer
func (n *Network) Send(peerID string, data []byte) error {
	pi, err := peer.Decode(peerID)
	if err != nil {
		return err
	}

	s, err := n.Host.NewStream(context.Background(), pi, protocol.ID("/ecopulse/1.0.0"))
	if err != nil {
		return err
	}

	_, err = s.Write(data)
	if err != nil {
		return err
	}

	return nil
}

// Start starts the EcoPulse network
func (n *Network) Start() error {
	log.Println("Starting EcoPulse network")

	return nil
}
