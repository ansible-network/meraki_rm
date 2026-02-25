/**
 * All CSS for the rendered documentation pages.
 * Ported from PluginDocPanel.ts inline styles, with VS Code CSS variables
 * replaced by standalone custom properties and a light/dark toggle.
 */
export function getStyles(): string {
  return `
/* Dark theme (default) */
:root, [data-theme="dark"] {
    --bg: #0d0d0d;
    --surface: #161616;
    --surface-light: #1e1e1e;
    --border: #333;
    --text: #e0e0e0;
    --text-muted: #888;
    --text-dim: #666;
    --accent: #fff;
    --code-bg: #0a0a0a;
    --required: #e57373;
    --success: #81c784;
    --yaml-key: #9cdcfe;
    --yaml-string: #ce9178;
    --yaml-number: #b5cea8;
    --yaml-bool: #569cd6;
    --yaml-comment: #6a9955;
    --yaml-anchor: #c586c0;
}

/* Light theme */
[data-theme="light"] {
    --bg: #ffffff;
    --surface: #f5f5f5;
    --surface-light: #e8e8e8;
    --border: #ddd;
    --text: #1a1a1a;
    --text-muted: #555;
    --text-dim: #777;
    --accent: #000;
    --code-bg: #f8f8f8;
    --required: #c62828;
    --success: #2e7d32;
    --yaml-key: #0451a5;
    --yaml-string: #a31515;
    --yaml-number: #098658;
    --yaml-bool: #0000ff;
    --yaml-comment: #008000;
    --yaml-anchor: #800080;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 13px;
    background: var(--bg);
    color: var(--text);
    line-height: 1.5;
}

.container { max-width: 960px; margin: 0 auto; padding: 16px; }

/* Breadcrumb */
.breadcrumb { font-size: 11px; color: var(--text-dim); margin-bottom: 12px; }
.breadcrumb a { color: var(--text-dim); text-decoration: none; }
.breadcrumb a:hover { color: var(--text); text-decoration: underline; }
.breadcrumb-separator { margin: 0 4px; }

/* Header */
.header { border-bottom: 1px solid var(--border); padding-bottom: 12px; margin-bottom: 16px; }
.header-title { display: flex; align-items: center; gap: 10px; }
.header-title h1 {
    font-size: 18px;
    font-weight: 600;
    font-family: 'SFMono-Regular', Consolas, monospace;
}
.plugin-type-badge {
    background: var(--surface-light);
    border: 1px solid var(--border);
    color: var(--text-muted);
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 10px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.short-desc { color: var(--text-muted); font-size: 12px; margin-top: 6px; }
.version-info { font-size: 11px; color: var(--text-dim); margin-top: 4px; }

/* Navigation tabs */
.nav-tabs { display: flex; gap: 0; border-bottom: 1px solid var(--border); margin-bottom: 16px; }
.nav-tab {
    padding: 8px 14px;
    font-size: 12px;
    color: var(--text-muted);
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
    cursor: pointer;
    text-decoration: none;
}
.nav-tab:hover { color: var(--text); }
.nav-tab.active { color: var(--accent); border-bottom-color: var(--accent); }

/* Sections */
.section { margin-bottom: 20px; }
.section-title { font-size: 14px; font-weight: 600; margin-bottom: 10px; color: var(--text); }

/* Synopsis */
.synopsis {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 12px;
    font-size: 12px;
}
.synopsis ul { margin: 0; padding-left: 16px; }
.synopsis li { margin-bottom: 4px; }

/* Parameters - Tree Style */
.param-tree { font-size: 12px; }
.param-item { border-bottom: 1px solid var(--border); padding: 8px 0; }
.param-item:last-child { border-bottom: none; }
.param-header {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    cursor: pointer;
    user-select: none;
}
.param-toggle {
    width: 14px; height: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; color: var(--text-dim);
    flex-shrink: 0; margin-top: 2px;
}
.param-toggle:empty { visibility: hidden; }
.param-name { font-family: 'SFMono-Regular', Consolas, monospace; font-weight: 600; color: var(--text); }
.param-type { font-size: 11px; color: var(--text-dim); font-family: monospace; }
.param-required { color: var(--required); font-size: 10px; font-weight: 600; }
.param-meta { display: flex; gap: 12px; margin-top: 4px; margin-left: 22px; }
.param-desc { color: var(--text-muted); margin-top: 4px; margin-left: 22px; font-size: 12px; }
.param-desc p { margin: 0 0 4px 0; }
.param-choices { margin-top: 4px; margin-left: 22px; }
.param-choice {
    display: inline-block;
    background: var(--code-bg);
    border: 1px solid var(--border);
    padding: 1px 6px;
    border-radius: 3px;
    font-family: monospace;
    font-size: 11px;
    margin-right: 4px;
    margin-bottom: 2px;
}
.param-choice.default { border-color: var(--success); color: var(--success); }
.param-default { font-size: 11px; color: var(--success); }

/* Suboptions */
.suboptions {
    margin-left: 22px; margin-top: 8px;
    padding-left: 12px;
    border-left: 1px solid var(--border);
    display: none;
}
.suboptions.expanded { display: block; }

/* Notes */
.notes {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 12px;
    font-size: 12px;
}
.notes ul { margin: 0; padding-left: 16px; }
.notes li { margin-bottom: 4px; }

/* Examples */
.example-section { margin-bottom: 16px; }
.example-header {
    display: flex; align-items: center; justify-content: space-between;
    background: var(--surface);
    border: 1px solid var(--border);
    border-bottom: none;
    border-radius: 4px 4px 0 0;
    padding: 8px 12px;
}
.example-title { font-weight: 600; font-size: 12px; color: var(--text); }
.example-copy-btn {
    background: var(--surface-light);
    border: 1px solid var(--border);
    color: var(--text-muted);
    padding: 4px 10px;
    border-radius: 3px;
    font-size: 11px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 4px;
}
.example-copy-btn:hover { background: var(--border); color: var(--text); }
.example-copy-btn.copied { color: var(--success); border-color: var(--success); }
.example-code {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 0 0 4px 4px;
    padding: 12px;
    overflow-x: auto;
    margin: 0;
}
.example-code pre {
    font-family: 'SFMono-Regular', Consolas, monospace;
    font-size: 12px; line-height: 1.5;
    white-space: pre; color: var(--text);
    margin: 0;
}
.example-context {
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: none;
    padding: 10px 12px;
    font-size: 11px;
    color: var(--text-dim);
    font-family: 'SFMono-Regular', Consolas, monospace;
    white-space: pre-wrap;
}
.example-context:first-of-type {
    border-radius: 4px 4px 0 0;
    border-top: 1px solid var(--border);
}
.example-context-label {
    font-weight: 600; color: var(--text-muted); margin-bottom: 4px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* YAML Syntax Highlighting */
.yaml-key { color: var(--yaml-key); }
.yaml-string { color: var(--yaml-string); }
.yaml-number { color: var(--yaml-number); }
.yaml-bool { color: var(--yaml-bool); }
.yaml-null { color: var(--yaml-bool); }
.yaml-comment { color: var(--yaml-comment); font-style: italic; }
.yaml-comment-dim { color: var(--text-dim); font-style: italic; }
.yaml-comment-type { color: var(--yaml-bool); font-style: italic; }
.yaml-comment-required { color: var(--required); font-style: italic; }
.yaml-comment-optional { color: var(--text-dim); font-style: italic; }
.yaml-list-marker { color: var(--text-muted); }

/* Examples view toggle */
.examples-toolbar { display: flex; justify-content: flex-end; margin-bottom: 12px; }
.view-toggle {
    display: flex; background: var(--surface);
    border: 1px solid var(--border); border-radius: 4px; overflow: hidden;
}
.view-toggle-btn {
    background: transparent; border: none; color: var(--text-muted);
    padding: 6px 12px; font-size: 11px; cursor: pointer;
}
.view-toggle-btn:hover { background: var(--surface-light); }
.view-toggle-btn.active { background: var(--border); color: var(--text); }
.examples-formatted, .examples-raw { display: none; }
.examples-formatted.active, .examples-raw.active { display: block; }
.sample-view { display: none; }
.sample-view.active { display: block; }
.raw-examples {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 4px; padding: 12px; overflow-x: auto;
}
.raw-examples pre {
    font-family: 'SFMono-Regular', Consolas, monospace;
    font-size: 12px; line-height: 1.5;
    white-space: pre; color: var(--text); margin: 0;
}

/* Return values */
.return-item { border-bottom: 1px solid var(--border); padding: 8px 0; }
.return-item:last-child { border-bottom: none; }
.return-name { font-family: 'SFMono-Regular', Consolas, monospace; font-weight: 600; }
.return-meta { font-size: 11px; color: var(--text-dim); margin-top: 2px; }
.return-desc { color: var(--text-muted); font-size: 12px; margin-top: 4px; }
.return-sample {
    background: var(--code-bg);
    border: 1px solid var(--border);
    padding: 6px 10px; border-radius: 3px;
    font-family: monospace; font-size: 11px;
    margin-top: 6px; overflow-x: auto; white-space: pre;
}

/* Author */
.author { color: var(--text-dim); font-size: 12px; }

/* Tab content */
.tab-content { display: none; }
.tab-content.active { display: block; }

/* Toolbar */
.toolbar {
    position: fixed; top: 12px; right: 20px;
    display: flex; gap: 4px; z-index: 100;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px; padding: 4px;
}
.toolbar-btn {
    background: transparent; border: none;
    color: var(--text-muted);
    width: 28px; height: 28px; border-radius: 4px;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 600;
}
.toolbar-btn:hover { background: var(--surface-light); color: var(--text); }
.toolbar-divider { width: 1px; background: var(--border); margin: 4px 2px; }
.zoom-label {
    font-size: 11px; color: var(--text-dim);
    display: flex; align-items: center; padding: 0 4px;
}

/* Inline code */
code {
    background: var(--code-bg);
    padding: 1px 4px; border-radius: 3px;
    font-family: 'SFMono-Regular', Consolas, monospace;
    font-size: 0.9em;
}

/* Links */
a { color: var(--text-muted); text-decoration: underline; }
a:hover { color: var(--text); }

/* --- Index page --- */
.index-header {
    border-bottom: 1px solid var(--border);
    padding-bottom: 16px;
    margin-bottom: 24px;
}
.index-header h1 { font-size: 22px; font-weight: 600; }
.index-desc { color: var(--text-muted); font-size: 13px; margin-top: 6px; }
.index-meta { font-size: 11px; color: var(--text-dim); margin-top: 4px; }

.search-box {
    width: 100%;
    padding: 8px 12px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text);
    font-size: 13px;
    margin-bottom: 20px;
    outline: none;
}
.search-box:focus { border-color: var(--accent); }
.search-box::placeholder { color: var(--text-dim); }

.module-group { margin-bottom: 24px; }
.module-group-title {
    font-size: 13px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.5px;
    color: var(--text-dim); margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid var(--border);
}
.module-list { list-style: none; padding: 0; }
.module-entry {
    display: flex; align-items: baseline; gap: 12px;
    padding: 6px 0;
    border-bottom: 1px solid var(--surface-light);
}
.module-entry:last-child { border-bottom: none; }
.module-entry a {
    font-family: 'SFMono-Regular', Consolas, monospace;
    font-weight: 500; font-size: 12px;
    color: var(--text); text-decoration: none;
}
.module-entry a:hover { text-decoration: underline; }
.module-short-desc { color: var(--text-muted); font-size: 12px; }
`;
}
