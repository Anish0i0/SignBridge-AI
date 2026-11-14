function Navbar() {
  return (
    <header className="navbar">
      <div className="container navbar-inner">
        <div className="brand">
          <span className="brand-logo" aria-hidden="true">
            <svg
              viewBox="0 0 24 24"
              width="20"
              height="20"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M3 18h18" />
              <path d="M5 18c0-5 3-8 7-8s7 3 7 8" />
              <path d="M12 10V6" />
            </svg>
          </span>
          <span className="brand-name">SignBridge AI</span>
        </div>
        <span className="navbar-badge">BCA Minor Project</span>
      </div>
    </header>
  );
}

export default Navbar;
