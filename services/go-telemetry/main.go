package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	port := flag.Int("port", 8766, "Port to listen on for Go telemetry service")
	flag.Parse()

	log.Printf("[AEOVEXOR GO TELEMETRY] Initializing service on port %d...", *port)

	engine := NewTelemetryEngine("Ouster-OS1-64 / KITTI-Velodyne")
	broadcaster := NewStreamBroadcaster()

	// Simulate high-frequency 60Hz telemetry generation
	go func() {
		ticker := time.NewTicker(16 * time.Millisecond) // ~60 FPS
		defer ticker.Stop()

		var frameID uint64
		for range ticker.C {
			frameID++
			pointCount := 17238
			byteSize := pointCount * 16 // 16 bytes per point

			engine.RecordFrame(pointCount, byteSize)

			if frameID%10 == 0 { // Broadcast spatial frame header at 6 Hz
				broadcaster.Broadcast("frame_telemetry", map[string]interface{}{
					"frame_id":    frameID,
					"point_count": pointCount,
					"timestamp":   time.Now().UnixNano(),
					"metrics":     engine.GetStats(),
				})
			}
		}
	}()

	mux := http.NewServeMux()

	// 1. Health check
	mux.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"status":    "healthy",
			"service":   "aeovexor-telemetry-go",
			"version":   "2.4.0",
			"timestamp": time.Now().UTC().Format(time.RFC3339),
		})
	})

	// 2. Telemetry metrics endpoint
	mux.HandleFunc("/metrics", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		stats := engine.GetStats()
		json.NewEncoder(w).Encode(stats)
	})

	// 3. API telemetry endpoint
	mux.HandleFunc("/api/telemetry", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		stats := engine.GetStats()
		json.NewEncoder(w).Encode(map[string]interface{}{
			"status": "success",
			"data":   stats,
		})
	})

	// 4. Live SSE telemetry stream
	mux.HandleFunc("/events", func(w http.ResponseWriter, r *http.Request) {
		broadcaster.ServeSSE(w, r, engine)
	})

	server := &http.Server{
		Addr:    fmt.Sprintf(":%d", *port),
		Handler: mux,
	}

	go func() {
		log.Printf("[AEOVEXOR GO TELEMETRY] Listening on http://127.0.0.1:%d", *port)
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Server error: %v", err)
		}
	}()

	// Wait for termination signal
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt, syscall.SIGTERM)
	<-stop

	log.Println("[AEOVEXOR GO TELEMETRY] Shutting down gracefully...")
}
