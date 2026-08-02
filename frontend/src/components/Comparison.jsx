import { DownloadIcon } from "./Icons";

export function Comparison({ original, protectedImage, busy, onDownload, mediaType = "image" }) {
  return (
    <section className={`comparison ${busy ? "comparison--busy" : ""}`} aria-label="Original and protected comparison">
      <div className="media-half">
        <span className="media-label">Original</span>
        {mediaType === "video" ? <video src={original} controls muted aria-label="Original uploaded video" /> : <img src={original} alt="Original uploaded sample" />}
      </div>
      <div className="media-half">
        <span className="media-label">Protected</span>
        {mediaType === "video" ? <video src={protectedImage} controls muted aria-label="Face-anonymized video" /> : <img src={protectedImage} alt="Face-anonymized result" />}
      </div>
      <div className="split-handle" aria-hidden="true"><span>‹</span><span>›</span></div>
      {busy && <div className="analysis-scrim"><span className="spinner" /><strong>Analysing locally</strong><span>Finding faces, then applying your privacy settings</span></div>}
      <button className="download-button" onClick={onDownload} title="Download protected image" aria-label="Download protected image">
        <DownloadIcon size={18} />
      </button>
    </section>
  );
}
