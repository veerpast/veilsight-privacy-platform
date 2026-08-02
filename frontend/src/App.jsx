import { useEffect, useState } from "react";
import { getDetectorStatus, analyzeImage, analyzeVideo, benchmarkImage } from "./lib/api";
import { About } from "./components/About";
import { BenchmarkTable, initialRows } from "./components/BenchmarkTable";
import { Comparison } from "./components/Comparison";
import { Controls } from "./components/Controls";
import { CheckIcon, CloseIcon, MenuIcon, ShieldIcon } from "./components/Icons";
import { Reports } from "./components/Reports";
import { Sidebar } from "./components/Sidebar";

const sampleOriginal = "/sample-lab.png";
const sampleProtected = "/sample-protected.jpg";

export default function App() {
  const [active, setActive] = useState("studio");
  const [menuOpen, setMenuOpen] = useState(false);
  const [file, setFile] = useState(null);
  const [mediaType, setMediaType] = useState("image");
  const [detectors, setDetectors] = useState([]);
  const [settings, setSettings] = useState({ detector: "haar", anonymization: "blur", confidence: 0.55, intensity: 0.72 });
  const [images, setImages] = useState({ original: sampleOriginal, protected: sampleProtected });
  const [run, setRun] = useState({ face_count: 3, latency_ms: 38, detector: "OpenCV Haar" });
  const [insights, setInsights] = useState({ occupancy_band: "moderate", queue_signal: "clear", privacy_coverage: 1, interpretation: "Face-visible occupancy proxy; no identity, tracking, or biometric matching." });
  const [benchmarkRows, setBenchmarkRows] = useState(initialRows);
  const [history, setHistory] = useState([]);
  const [busy, setBusy] = useState(false);
  const [benchmarkBusy, setBenchmarkBusy] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    getDetectorStatus().then(({ detectors: status }) => {
      setDetectors(status);
      const chosen = status.find((item) => item.key === settings.detector && item.available) || status.find((item) => item.available);
      if (chosen) setSettings((current) => ({ ...current, detector: chosen.key }));
    }).catch(() => setMessage("Demo preview is ready. Start the local API to analyse your own image."));
  }, []);

  const availableCount = detectors.filter((detector) => detector.available).length || 1;

  const navigate = (destination) => { setActive(destination); setMenuOpen(false); };
  const chooseFile = (nextFile) => {
    setFile(nextFile);
    setMessage("");
    if (nextFile) {
      const preview = URL.createObjectURL(nextFile);
      setImages({ original: preview, protected: preview });
      setMediaType(nextFile.type.startsWith("video/") ? "video" : "image");
    }
  };

  const analyse = async () => {
    if (!file) return;
    setBusy(true); setMessage("");
    try {
      if (file.type.startsWith("video/")) {
        const result = await analyzeVideo(file, settings);
        setImages((current) => ({ original: current.original, protected: result.url }));
        const videoRun = { face_count: result.metrics.face_detections || 0, latency_ms: result.metrics.average_detection_ms || 0, detector: settings.detector };
        setRun(videoRun);
        setHistory((items) => [{ detector: settings.detector, faces: `${result.metrics.average_faces_per_frame || 0}/frame`, method: settings.anonymization, latency: result.metrics.average_detection_ms || 0, time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) }, ...items].slice(0, 8));
        setMessage("Protected video ready. Audio was removed because a voice can also reveal identity.");
        return;
      }
      const result = await analyzeImage(file, settings);
      setImages({ original: result.original, protected: result.protected });
      setRun(result.run);
      setInsights(result.insights || insights);
      setHistory((items) => [{ detector: result.run.detector, faces: result.run.face_count, method: settings.anonymization, latency: result.run.latency_ms, time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) }, ...items].slice(0, 8));
    } catch (error) { setMessage(error.message); }
    finally { setBusy(false); }
  };

  const benchmark = async () => {
    if (!file) return;
    setBenchmarkBusy(true); setMessage("");
    try { const result = await benchmarkImage(file, settings.confidence); setBenchmarkRows(result.rows); }
    catch (error) { setMessage(error.message); }
    finally { setBenchmarkBusy(false); }
  };

  const download = () => {
    const anchor = document.createElement("a");
    anchor.href = images.protected;
    anchor.download = "veilsight-protected.jpg";
    anchor.click();
  };

  return (
    <div className="app-shell">
      <Sidebar active={active} onNavigate={navigate} open={menuOpen} />
      {menuOpen && <button className="nav-scrim" aria-label="Close navigation" onClick={() => setMenuOpen(false)} />}
      <main className="main-area">
        <button className="menu-button" onClick={() => setMenuOpen(!menuOpen)} aria-label="Toggle navigation">{menuOpen ? <CloseIcon/> : <MenuIcon/>}</button>
        {message && <div className="toast" role="status"><span>{message}</span><button onClick={() => setMessage("")} aria-label="Dismiss"><CloseIcon size={16}/></button></div>}
        {active === "studio" && <>
          <header className="studio-header">
            <div><h1>Privacy Studio</h1><p>Detect responsibly. Protect identity by default.</p></div>
            <div className="privacy-status"><span className="shield-disc"><ShieldIcon size={25}/></span><div><strong>Privacy status: protected</strong><span>Local API · no media stored</span></div></div>
          </header>
          <div className="workspace-grid">
            <Controls file={file} onFile={chooseFile} settings={settings} onSettings={setSettings} onRun={analyse} busy={busy} detectors={detectors} />
            <Comparison original={images.original} protectedImage={images.protected} busy={busy} onDownload={download} mediaType={mediaType} />
          </div>
          <BenchmarkTable rows={benchmarkRows} onRun={benchmark} canRun={Boolean(file && mediaType === "image")} busy={benchmarkBusy} />
          <section className="insight-panel" aria-label="Operational insight"><div><span className="eyebrow">Operational insight</span><h2>Privacy-preserving space signal</h2><p>{insights.interpretation}</p></div><div className="insight-metrics"><span><b>{insights.occupancy_band || "—"}</b><small>occupancy proxy</small></span><span><b>{insights.queue_signal || "—"}</b><small>queue signal</small></span><span><b>{Math.round((insights.privacy_coverage || 0) * 100)}%</b><small>privacy coverage</small></span></div></section>
          <footer className="status-line"><div><span className="check-disc"><CheckIcon size={16}/></span><strong>{run.face_count} faces detected</strong><i/> <span>{run.face_count} anonymized</span><i/> <span>source media forgotten after response</span></div><span>{availableCount} detector{availableCount === 1 ? "" : "s"} available on this device</span></footer>
        </>}
        {active === "benchmarks" && <div className="page-view"><header className="view-header"><div><h1>Benchmarks</h1><p>Measure what the machine actually did—not what a polished demo claims.</p></div></header><BenchmarkTable rows={benchmarkRows} onRun={benchmark} canRun={Boolean(file)} busy={benchmarkBusy}/><div className="method-note"><h2>Reading the results</h2><p>Latency and FPS measure one local run and will vary by hardware. Agreement compares face counts across detectors; it is a useful diagnostic, not an accuracy score. Add labelled annotations to calculate precision and recall with the included evaluation module.</p></div></div>}
        {active === "reports" && <Reports history={history}/>} 
        {active === "about" && <About/>}
      </main>
    </div>
  );
}
