import { AboutIcon, ChartIcon, ReportIcon, ShieldIcon, StudioIcon } from "./Icons";

const destinations = [
  ["studio", "Studio", StudioIcon],
  ["benchmarks", "Benchmarks", ChartIcon],
  ["reports", "Reports", ReportIcon],
  ["about", "About", AboutIcon],
];

export function Sidebar({ active, onNavigate, open }) {
  return (
    <aside className={`sidebar ${open ? "sidebar--open" : ""}`}>
      <button className="brand" onClick={() => onNavigate("studio")} aria-label="Go to Studio">
        <span className="brand__mark"><ShieldIcon size={23} /></span>
        <span>VeilSight</span>
      </button>
      <nav aria-label="Primary navigation">
        {destinations.map(([key, label, NavIcon]) => (
          <button
            key={key}
            className={`nav-item ${active === key ? "nav-item--active" : ""}`}
            onClick={() => onNavigate(key)}
            aria-current={active === key ? "page" : undefined}
          >
            <NavIcon size={21} />
            <span>{label}</span>
          </button>
        ))}
      </nav>
      <div className="sidebar__promise">
        <ShieldIcon size={23} />
        <div><strong>Privacy by design</strong><span>No media is retained</span></div>
      </div>
    </aside>
  );
}
