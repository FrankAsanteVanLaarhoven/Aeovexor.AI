# AEOVEXOR Scientific Pipeline: Kaufman Adaptive Filter (KAMA)
# Dynamic noise suppression via Efficiency Ratio (ER) preserving step edges

# 1. Inspect loaded 3D point cloud coordinates
print(f"Loaded LiDAR Frame: {points.shape[0]:,} coordinates, dtype={points.dtype}")

# 2. Extract radial distances
r = np.linalg.norm(points, axis=1)

# 3. Apply Kaufman Adaptive Filter (period=10)
filtered_r = kaufman_adaptive_filter_1d(r[:2000], period=10)

# 4. Generate Scientific Diagnostic Plot
plt.figure(figsize=(7, 3.5))
plt.plot(r[:200], label='Raw Sensor Distance', color='#94A3B8', alpha=0.5, linewidth=1)
plt.plot(filtered_r[:200], label='KAMA Adaptive Filter', color='#00E5FF', linewidth=1.8)
plt.title('Kaufman Adaptive Moving Average: Step-Edge Conservation', fontsize=10)
plt.xlabel('Sensor Azimuth Index', fontsize=9)
plt.ylabel('Radial Range (m)', fontsize=9)
plt.legend(frameon=False, fontsize=8)
plt.grid(True, linestyle='--', alpha=0.15)
plt.tight_layout()
plt.show()

print(f"KAMA Processing complete. Filtered {len(filtered_r):,} points successfully.")
