import { DownloadIcon, ReportIcon } from "./Icons";

export function Reports({ history }) {
  const exportReport = () => {
    const report = { exported_at: new Date().toISOString(), privacy_notice: "No source media is included.", runs: history };
    const url = URL.createObjectURL(new Blob([JSON.stringify(report, null, 2)], { type: "application/json" }));
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "veilsight-session-report.json";
    anchor.click();
    URL.revokeObjectURL(url);
  };
  return (
    <div className="page-view">
      <header className="view-header"><div><h1>Session reports</h1><p>Only lightweight metrics live here, in this browser tab. Source media is never included.</p></div><button className="secondary-button" onClick={exportReport} disabled={!history.length}><DownloadIcon size={17}/>Export JSON</button></header>
      {history.length ? <div className="report-list">{history.map((run, index) => <article key={`${run.time}-${index}`}><span className="report-index">{String(index + 1).padStart(2, "0")}</span><div><strong>{run.detector}</strong><p>{run.faces} faces · {run.method} · {run.latency} ms</p></div><time>{run.time}</time></article>)}</div> : <div className="empty-state"><ReportIcon size={38}/><h2>No analyses yet</h2><p>Run an image through Privacy Studio. A small, media-free summary will appear here for your report.</p></div>}
    </div>
  );
}
