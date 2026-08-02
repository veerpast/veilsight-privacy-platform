const Icon = ({ children, size = 20, ...props }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" {...props}>
    {children}
  </svg>
);

export const StudioIcon = (props) => <Icon {...props}><rect x="3" y="4" width="18" height="13" rx="1.5"/><path d="M8 21h8M12 17v4"/></Icon>;
export const ChartIcon = (props) => <Icon {...props}><path d="M4 20V10M10 20V4M16 20v-7M22 20V7"/></Icon>;
export const ReportIcon = (props) => <Icon {...props}><path d="M6 2h9l5 5v15H6z"/><path d="M14 2v6h6M9 13h8M9 17h8"/></Icon>;
export const InfoIcon = (props) => <Icon {...props}><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7h.01"/></Icon>;
export const AboutIcon = InfoIcon;
export const UploadIcon = (props) => <Icon {...props}><path d="M12 16V4M7 9l5-5 5 5"/><path d="M5 14H3v7h18v-7h-2"/></Icon>;
export const PlayIcon = (props) => <Icon {...props}><path fill="currentColor" stroke="none" d="M8 5.5v13l10-6.5z"/></Icon>;
export const ShieldIcon = (props) => <Icon {...props}><path d="M12 2 20 5v6c0 5.2-3.4 9.2-8 11-4.6-1.8-8-5.8-8-11V5z"/><path d="m8.5 12 2.2 2.2 4.8-5"/></Icon>;
export const DownloadIcon = (props) => <Icon {...props}><path d="M12 3v12M7 10l5 5 5-5M4 21h16"/></Icon>;
export const CheckIcon = (props) => <Icon {...props}><path d="m5 12 4 4L19 6"/></Icon>;
export const AlertIcon = (props) => <Icon {...props}><path d="M12 3 2.5 20h19z"/><path d="M12 9v4M12 17h.01"/></Icon>;
export const MenuIcon = (props) => <Icon {...props}><path d="M4 7h16M4 12h16M4 17h16"/></Icon>;
export const CloseIcon = (props) => <Icon {...props}><path d="m6 6 12 12M18 6 6 18"/></Icon>;
