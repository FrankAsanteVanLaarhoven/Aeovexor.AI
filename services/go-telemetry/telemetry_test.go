package main

import (
	"testing"
	"time"
)

func TestTelemetryEngine(t *testing.T) {
	engine := NewTelemetryEngine("Test-LiDAR")

	stats := engine.GetStats()
	if stats.SensorSource != "Test-LiDAR" {
		t.Fatalf("Expected source Test-LiDAR, got %s", stats.SensorSource)
	}
	if stats.Status != "ONLINE" {
		t.Fatalf("Expected status ONLINE, got %s", stats.Status)
	}

	// Simulate frame arrivals
	engine.RecordFrame(15000, 15000*16)
	time.Sleep(5 * time.Millisecond)
	engine.RecordFrame(15000, 15000*16)

	updated := engine.GetStats()
	if updated.TotalFramesReceived != 2 {
		t.Fatalf("Expected 2 frames, got %d", updated.TotalFramesReceived)
	}
	if updated.TotalPointsStreamed != 30000 {
		t.Fatalf("Expected 30000 points, got %d", updated.TotalPointsStreamed)
	}
}

func TestStreamBroadcaster(t *testing.T) {
	broadcaster := NewStreamBroadcaster()

	if broadcaster.ClientCount() != 0 {
		t.Fatalf("Expected 0 clients initially, got %d", broadcaster.ClientCount())
	}

	c1 := broadcaster.RegisterClient("test-1")
	if broadcaster.ClientCount() != 1 {
		t.Fatalf("Expected 1 client, got %d", broadcaster.ClientCount())
	}

	// Broadcast test
	broadcaster.Broadcast("ping", map[string]string{"msg": "pong"})

	select {
	case msg := <-c1.channel:
		if len(msg) == 0 {
			t.Fatal("Expected non-empty broadcast message")
		}
	case <-time.After(50 * time.Millisecond):
		t.Fatal("Broadcast message timed out")
	}

	broadcaster.UnregisterClient("test-1")
	if broadcaster.ClientCount() != 0 {
		t.Fatalf("Expected 0 clients after unregister, got %d", broadcaster.ClientCount())
	}
}
