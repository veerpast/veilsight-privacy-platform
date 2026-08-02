export const initialRows = [
  { detector: "YOLO Face", available: false, face_count: "—", latency_ms: "—", fps: "—", agreement: 0, note: "Model setup needed" },
  { detector: "MediaPipe", available: false, face_count: "—", latency_ms: "—", fps: "—", agreement: 0, note: "Package setup needed" },
  { detector: "OpenCV Haar", available: true, face_count: 3, latency_ms: 38, fps: 26.3, agreement: 1, note: "Demo preview" },
];

export function BenchmarkTable({ rows = initialRows, onRun, canRun, busy }) {
  return (
    <section className="benchmark-block">
      <div className="section-heading">
        <div><h2>Benchmark comparison</h2><p>Speed and detector agreement on the current image. Accuracy appears only with labelled ground truth.</p></div>
        {onRun && <button className="secondary-button" disabled={!canRun || busy} onClick={onRun}>{busy ? "Benchmarking…" : "Run all available"}</button>}
      </div>
      <div className="table-scroll">
        <table>
          <thead><tr><th>Detector</th><th>Faces</th><th>Latency</th><th>FPS</th><th>Agreement</th><th>Precision / Recall</th></tr></thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.detector} className={!row.available ? "row-muted" : ""}>
                <td><strong>{row.detector}</strong><span className="cell-note">{row.note}</span></td>
                <td>{row.face_count}</td>
                <td>{formatMetric(row.latency_ms, " ms")}</td>
                <td>{formatMetric(row.fps, "")}</td>
                <td><div className="meter"><span style={{ width: `${Number(row.agreement || 0) * 100}%` }} /></div><small>{row.available ? `${Math.round(Number(row.agreement || 0) * 100)}%` : "—"}</small></td>
                <td><span className="needs-labels">Needs labels</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

const formatMetric = (value, suffix) => typeof value === "number" ? `${value.toFixed(value < 10 ? 1 : 0)}${suffix}` : value;
