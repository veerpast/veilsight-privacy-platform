import { ShieldIcon } from "./Icons";

export function About() {
  return (
    <div className="page-view about-view">
      <header className="view-header"><div><h1>Why VeilSight exists</h1><p>Face detection is useful. Quietly keeping someone’s identity is not.</p></div></header>
      <div className="essay-layout">
        <article>
          <h2>A small engineering principle</h2>
          <p>I built VeilSight around a simple default: media should be processed for the job at hand, then forgotten. The API keeps no database and the report stores metrics—not faces.</p>
          <p>This is a learning project, not a promise of perfect anonymity. Blur and pixelation can sometimes be reversed or defeated. For genuinely sensitive material, the solid mask is the safer choice.</p>
          <h2>What the benchmark means</h2>
          <p>Latency, FPS and cross-detector agreement can be measured on any input. Precision and recall cannot be honestly claimed without labelled ground truth, so VeilSight refuses to invent them.</p>
        </article>
        <aside className="principles">
          <ShieldIcon size={34}/>
          <h3>Design decisions</h3>
          <ul><li>No face recognition or identity matching</li><li>No analytics database</li><li>No automatic cloud upload</li><li>Clear model availability and limitations</li><li>Reproducible evaluation utilities</li></ul>
        </aside>
      </div>
    </div>
  );
}
