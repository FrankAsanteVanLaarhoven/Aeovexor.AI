package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
)

// BroadcastMessage encapsulates data fanned out to clients
type BroadcastMessage struct {
	Timestamp int64       `json:"timestamp"`
	Type      string      `json:"type"`
	Payload   interface{} `json:"payload"`
}

// Client represents a connected HTTP stream consumer
type Client struct {
	id      string
	channel chan []byte
}

// StreamBroadcaster manages client subscriptions and non-blocking broadcasting
type StreamBroadcaster struct {
	mu      sync.RWMutex
	clients map[string]*Client
}

// NewStreamBroadcaster initializes the broadcaster
func NewStreamBroadcaster() *StreamBroadcaster {
	return &StreamBroadcaster{
		clients: make(map[string]*Client),
	}
}

// RegisterClient adds a new subscriber
func (b *StreamBroadcaster) RegisterClient(id string) *Client {
	b.mu.Lock()
	defer b.mu.Unlock()

	c := &Client{
		id:      id,
		channel: make(chan []byte, 64),
	}
	b.clients[id] = c
	return c
}

// UnregisterClient removes a subscriber
func (b *StreamBroadcaster) UnregisterClient(id string) {
	b.mu.Lock()
	defer b.mu.Unlock()

	if c, ok := b.clients[id]; ok {
		close(c.channel)
		delete(b.clients, id)
	}
}

// Broadcast sends JSON data to all active clients without blocking
func (b *StreamBroadcaster) Broadcast(msgType string, payload interface{}) {
	b.mu.RLock()
	defer b.mu.RUnlock()

	msg := BroadcastMessage{
		Timestamp: 1729881600,
		Type:      msgType,
		Payload:   payload,
	}

	data, err := json.Marshal(msg)
	if err != nil {
		return
	}

	for _, client := range b.clients {
		select {
		case client.channel <- data:
		default:
			// Drop frame if client buffer is full to prevent pipeline stalls
		}
	}
}

// ClientCount returns number of connected clients
func (b *StreamBroadcaster) ClientCount() int {
	b.mu.RLock()
	defer b.mu.RUnlock()
	return len(b.clients)
}

// ServeSSE handles Server-Sent Events HTTP connections
func (b *StreamBroadcaster) ServeSSE(w http.ResponseWriter, r *http.Request, engine *TelemetryEngine) {
	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")
	w.Header().Set("Access-Control-Allow-Origin", "*")

	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming unsupported", http.StatusInternalServerError)
		return
	}

	clientID := fmt.Sprintf("client-%d", r.Context().Value("id"))
	if clientID == "client-%!d(<nil>)" {
		clientID = fmt.Sprintf("client-%s", r.RemoteAddr)
	}

	client := b.RegisterClient(clientID)
	engine.SetClientCount(b.ClientCount())
	defer func() {
		b.UnregisterClient(clientID)
		engine.SetClientCount(b.ClientCount())
	}()

	notify := r.Context().Done()
	for {
		select {
		case <-notify:
			return
		case msg, ok := <-client.channel:
			if !ok {
				return
			}
			fmt.Fprintf(w, "data: %s\n\n", msg)
			flusher.Flush()
		}
	}
}
