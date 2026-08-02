import { AlertIcon, PlayIcon, UploadIcon } from "./Icons";

const detectorLabels = { yolo: "YOLO Face", mediapipe: "MediaPipe", haar: "OpenCV Haar" };

export function Controls({ file, onFile, settings, onSettings, onRun, busy, detectors }) {
  const set = (key) => (event) => onSettings({ ...settings, [key]: event.target.value });
  const availableDetectors = detectors.length ? detectors : [
    { key: "haar", label: "OpenCV Haar", available: true },
    { key: "mediapipe", label: "MediaPipe", available: false, reason: "Optional setup" },
    { key: "yolo", label: "YOLO Face", available: false, reason: "Optional setup" },
  ];

  return (
    <section className="controls-panel" aria-label="Privacy analysis controls">
      <label className="upload-zone">
        <input type="file" accept="image/png,image/jpeg,image/webp,video/mp4,video/quicktime,video/x-msvideo" onChange={(event) => onFile(event.target.files?.[0] || null)} />
        <UploadIcon size={36} />
        <strong>{file ? file.name : "Drop an image here"}</strong>
        <span>{file ? `${(file.size / 1024 / 1024).toFixed(1)} MB · ready to analyse` : "PNG, JPG, WebP up to 15 MB · video up to 200 MB"}</span>
      </label>

      <button className="primary-button" onClick={onRun} disabled={!file || busy}>
        <PlayIcon size={18} />
        {busy ? "Protecting faces…" : "Run privacy analysis"}
      </button>

      <div className="control-rule" />
      <label className="field">
        <span>Detector</span>
        <select value={settings.detector} onChange={set("detector")}>
          {availableDetectors.map((detector) => (
            <option key={detector.key} value={detector.key} disabled={!detector.available}>
              {detector.label || detectorLabels[detector.key]}{detector.available ? "" : " · setup needed"}
            </option>
          ))}
        </select>
      </label>

      <label className="field">
        <span>Anonymization</span>
        <select value={settings.anonymization} onChange={set("anonymization")}>
          <option value="blur">Gaussian blur</option>
          <option value="pixelate">Pixelation</option>
          <option value="solid">Solid privacy mask</option>
        </select>
      </label>

      <RangeField label={settings.detector === "haar" ? "Sensitivity" : "Confidence"} value={settings.confidence} onChange={set("confidence")} />
      <RangeField label="Protection intensity" value={settings.intensity} onChange={set("intensity")} />

      <div className="human-note">
        <AlertIcon size={18} />
        <p><strong>A practical caution</strong>Blur lowers identification risk, but it cannot guarantee anonymity. Use a solid mask for sensitive material.</p>
      </div>
    </section>
  );
}

function RangeField({ label, value, onChange }) {
  return (
    <label className="range-field">
      <span><span>{label}</span><output>{Number(value).toFixed(2)}</output></span>
      <input type="range" min="0.1" max="1" step="0.05" value={value} onChange={onChange} />
      <small><span>Lower</span><span>Higher</span></small>
    </label>
  );
}
