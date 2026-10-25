package main

import (
	"sync"
	"time"
)

// Point3D represents a single LiDAR point
type Point3D struct {
	X         float32 `json:"x"`
	Y         float32 `json:"y"`
	Z         float32 `json:"z"`
	Intensity float32 `json:"intensity"`
}

// TelemetryStats tracks live sensor streaming health and metrics
type TelemetryStats struct {
	TotalFramesReceived uint64    `json:"total_frames_received"`
	TotalPointsStreamed uint64    `json:"total_points_streamed"`
	CurrentFPS          float64   `json:"current_fps"`
	BandwidthMbps       float64   `json:"bandwidth_mbps"`
	AverageJitterMs     float64   `json:"average_jitter_ms"`
	ActiveClients       int       `json:"active_clients"`
	SensorSource        string    `json:"sensor_source"`
	Status              string    `json:"status"`
	LastHeartbeat       time.Time `json:"last_heartbeat"`
}

// TelemetryEngine safely aggregates concurrent metrics
type TelemetryEngine struct {
	mu            sync.RWMutex
	stats         TelemetryStats
	lastFrameTime time.Time
	frameInterval time.Duration
}

// NewTelemetryEngine initializes the engine
func NewTelemetryEngine(source string) *TelemetryEngine {
	return &TelemetryEngine{
		stats: TelemetryStats{
			SensorSource:  source,
			Status:        "ONLINE",
			LastHeartbeat: time.Now(),
		},
		lastFrameTime: time.Now(),
	}
}

// RecordFrame updates metrics with a new frame arrival
func (te *TelemetryEngine) RecordFrame(pointCount int, byteSize int) {
	te.mu.Lock()
	defer te.mu.Unlock()

	now := time.Now()
	elapsed := now.Sub(te.lastFrameTime)
	te.lastFrameTime = now

	te.stats.TotalFramesReceived++
	te.stats.TotalPointsStreamed += uint64(pointCount)
	te.stats.LastHeartbeat = now

	if elapsed > 0 {
		fps := 1.0 / elapsed.Seconds()
		// Exponential moving average for FPS
		te.stats.CurrentFPS = 0.9*te.stats.CurrentFPS + 0.1*fps
		// Bandwidth in Mbps
		mbps := (float64(byteSize) * 8.0) / (elapsed.Seconds() * 1_000_000.0)
		te.stats.BandwidthMbps = 0.9*te.stats.BandwidthMbps + 0.1*mbps

		jitter := (elapsed - te.frameInterval).Abs().Seconds() * 1000.0
		te.stats.AverageJitterMs = 0.9*te.stats.AverageJitterMs + 0.1*jitter
		te.frameInterval = elapsed
	}
}

// SetClientCount updates current subscriber count
func (te *TelemetryEngine) SetClientCount(count int) {
	te.mu.Lock()
	defer te.mu.Unlock()
	te.stats.ActiveClients = count
}

// GetStats returns a copy of current metrics
func (te *TelemetryEngine) GetStats() TelemetryStats {
	te.mu.RLock()
	defer te.mu.RUnlock()
	return te.stats
}
