import { PluginData, PluginDoc, toArray } from './types';
import { escapeHtml, formatText } from './format';
import { renderParameters, resetSubIdCounter } from './parameters';
import { renderExamples } from './examples';
import { renderReturnValues } from './return-values';
import { renderSampleTask } from './sample-task';
import { highlightYaml } from './yaml-highlighter';
import { getStyles } from './styles';

export interface RenderPluginPageOptions {
  pluginFullName: string;
  pluginType?: string;
  data: PluginData;
  /** Relative path back to the site root (e.g. "../" from modules/) */
  rootPath?: string;
  /** Inline the CSS instead of linking to styles.css */
  inlineStyles?: boolean;
}

/**
 * Render a complete HTML page for a single plugin.
 */
export function renderPluginPage(opts: RenderPluginPageOptions): string {
  const {
    pluginFullName,
    pluginType = 'module',
    data,
    rootPath = '../',
    inlineStyles = false,
  } = opts;

  resetSubIdCounter();

  const doc = data.doc!;
  const parts = pluginFullName.split('.');
  const namespace = parts[0];
  const collection = parts[1];
  const pluginName = parts.slice(2).join('.');

  const styleTag = inlineStyles
    ? `<style>${getStyles()}</style>`
    : `<link rel="stylesheet" href="${rootPath}styles.css">`;

  return `<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${pluginFullName}</title>
    ${styleTag}
</head>
<body>
    <div class="toolbar">
        <button class="toolbar-btn" id="zoom-out-btn" title="Zoom out">\u2212</button>
        <span class="zoom-label" id="zoom-level">100%</span>
        <button class="toolbar-btn" id="zoom-in-btn" title="Zoom in">+</button>
        <div class="toolbar-divider"></div>
        <button class="toolbar-btn" id="theme-btn" title="Toggle theme">auto</button>
    </div>
    
    <div class="container">
        <div class="breadcrumb">
            <a href="${rootPath}index.html">${namespace}.${collection}</a>
            <span class="breadcrumb-separator">\u203A</span>
            <span>${pluginType}</span>
            <span class="breadcrumb-separator">\u203A</span>
            <strong>${pluginName}</strong>
        </div>
        
        <div class="header">
            <div class="header-title">
                <h1>${pluginName}</h1>
                <span class="plugin-type-badge">${pluginType}</span>
            </div>
            <div class="short-desc">${escapeHtml(doc.short_description || '')}</div>
            ${doc.version_added ? `<div class="version-info">Added in version ${doc.version_added}</div>` : ''}
        </div>
        
        <div class="nav-tabs">
            <span class="nav-tab active" data-tab="synopsis">Synopsis</span>
            <span class="nav-tab" data-tab="parameters">Parameters</span>
            <span class="nav-tab" data-tab="sample">Sample Task</span>
            ${doc.notes ? '<span class="nav-tab" data-tab="notes">Notes</span>' : ''}
            ${data.examples ? '<span class="nav-tab" data-tab="examples">Examples</span>' : ''}
            ${data.return ? '<span class="nav-tab" data-tab="return">Return Values</span>' : ''}
        </div>
        
        <div id="synopsis" class="tab-content active">
            <div class="section">
                <h2 class="section-title">Synopsis</h2>
                <div class="synopsis">
                    <ul>
                        ${toArray(doc.description).map(d => `<li>${formatText(d)}</li>`).join('')}
                    </ul>
                </div>
            </div>
            
            ${renderRequirements(doc)}
            ${renderAuthor(doc)}
        </div>
        
        <div id="parameters" class="tab-content">
            <div class="section">
                <h2 class="section-title">Parameters</h2>
                ${renderParameters(doc.options || {})}
            </div>
        </div>
        
        <div id="sample" class="tab-content">
            <div class="section">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <h2 class="section-title" style="margin-bottom: 0;">Sample Task</h2>
                    <button class="example-copy-btn" id="copy-btn-sample" onclick="copySampleTask()">
                        Copy
                    </button>
                </div>
                <p style="color: var(--text-muted); font-size: 12px; margin-bottom: 12px;">
                    A template task showing all available parameters with their defaults or example values.
                </p>
                ${renderSampleTask(pluginFullName, doc.options || {})}
            </div>
        </div>
        
        ${renderNotes(doc, data)}
        ${renderExamplesTab(data)}
        ${renderReturnTab(data)}
    </div>
    
    ${getPageScript()}
</body>
</html>`;
}

function renderRequirements(doc: PluginDoc): string {
  if (!doc.requirements) { return ''; }
  return `
            <div class="section">
                <h2 class="section-title">Requirements</h2>
                <div class="synopsis">
                    <ul>
                        ${toArray(doc.requirements).map(r => `<li>${escapeHtml(r)}</li>`).join('')}
                    </ul>
                </div>
            </div>`;
}

function renderAuthor(doc: PluginDoc): string {
  if (!doc.author) { return ''; }
  return `
            <div class="section">
                <h2 class="section-title">Author</h2>
                <div class="author">
                    ${Array.isArray(doc.author) ? doc.author.join(', ') : doc.author}
                </div>
            </div>`;
}

function renderNotes(doc: PluginDoc, _data: PluginData): string {
  if (!doc.notes) { return ''; }
  return `
        <div id="notes" class="tab-content">
            <div class="section">
                <h2 class="section-title">Notes</h2>
                <div class="notes">
                    <ul>
                        ${toArray(doc.notes).map(n => `<li>${formatText(n)}</li>`).join('')}
                    </ul>
                </div>
            </div>
        </div>`;
}

function renderExamplesTab(data: PluginData): string {
  if (!data.examples) { return ''; }
  return `
        <div id="examples" class="tab-content">
            <div class="section">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <h2 class="section-title" style="margin-bottom: 0;">Examples</h2>
                    <div class="view-toggle">
                        <button class="view-toggle-btn active" id="btn-formatted" onclick="toggleExamplesView('formatted')">Formatted</button>
                        <button class="view-toggle-btn" id="btn-raw" onclick="toggleExamplesView('raw')">Raw</button>
                    </div>
                </div>
                <div class="examples-formatted active" id="examples-formatted">
                    ${renderExamples(data.examples)}
                </div>
                <div class="examples-raw" id="examples-raw">
                    <div class="raw-examples">
                        <pre>${highlightYaml(data.examples)}</pre>
                    </div>
                </div>
            </div>
        </div>`;
}

function renderReturnTab(data: PluginData): string {
  if (!data.return) { return ''; }
  return `
        <div id="return" class="tab-content">
            <div class="section">
                <h2 class="section-title">Return Values</h2>
                ${renderReturnValues(data.return)}
            </div>
        </div>`;
}

function getPageScript(): string {
  return `<script>
// Tab switching
document.querySelectorAll('.nav-tab').forEach(function(tab) {
    tab.addEventListener('click', function() {
        document.querySelectorAll('.nav-tab').forEach(function(t) { t.classList.remove('active'); });
        document.querySelectorAll('.tab-content').forEach(function(c) { c.classList.remove('active'); });
        tab.classList.add('active');
        document.getElementById(tab.dataset.tab).classList.add('active');
    });
});

// Collapsible suboptions
function toggleSub(id) {
    var el = document.getElementById(id);
    if (el) {
        el.classList.toggle('expanded');
        var header = el.previousElementSibling;
        while (header && !header.classList.contains('param-header')) {
            header = header.previousElementSibling;
        }
        if (header) {
            var toggle = header.querySelector('.param-toggle');
            if (toggle) {
                toggle.textContent = el.classList.contains('expanded') ? '\\u25BC' : '\\u25B6';
            }
        }
    }
}

// Copy example to clipboard
function copyExample(id) {
    var el = document.getElementById('task-' + id);
    if (el) {
        var text = el.getAttribute('data-raw');
        navigator.clipboard.writeText(text).then(function() {
            var btn = document.getElementById('copy-btn-' + id);
            if (btn) {
                btn.classList.add('copied');
                btn.innerHTML = '\\u2713 Copied';
                setTimeout(function() {
                    btn.classList.remove('copied');
                    btn.innerHTML = 'Copy';
                }, 2000);
            }
        });
    }
}

// Toggle between formatted and raw examples view
function toggleExamplesView(view) {
    var formatted = document.getElementById('examples-formatted');
    var raw = document.getElementById('examples-raw');
    var btnFormatted = document.getElementById('btn-formatted');
    var btnRaw = document.getElementById('btn-raw');
    if (view === 'formatted') {
        formatted.classList.add('active');
        raw.classList.remove('active');
        btnFormatted.classList.add('active');
        btnRaw.classList.remove('active');
    } else {
        formatted.classList.remove('active');
        raw.classList.add('active');
        btnFormatted.classList.remove('active');
        btnRaw.classList.add('active');
    }
}

// Sample task view switching
var currentSampleView = 'optional';
function switchSampleView(view) {
    currentSampleView = view;
    document.querySelectorAll('.sample-toolbar .view-toggle-btn').forEach(function(btn) {
        btn.classList.remove('active');
    });
    var btnMap = { 'none': 'btn-no-comments', 'optional': 'btn-optional', 'descriptions': 'btn-descriptions' };
    var activeBtn = document.getElementById(btnMap[view]);
    if (activeBtn) activeBtn.classList.add('active');
    document.querySelectorAll('.sample-view').forEach(function(v) { v.classList.remove('active'); });
    var viewMap = { 'none': 'sample-none', 'optional': 'sample-optional', 'descriptions': 'sample-descriptions' };
    var activeView = document.getElementById(viewMap[view]);
    if (activeView) activeView.classList.add('active');
}

function copySampleTask() {
    var viewMap = { 'none': 'sample-none', 'optional': 'sample-optional', 'descriptions': 'sample-descriptions' };
    var el = document.getElementById(viewMap[currentSampleView]);
    if (el) {
        var text = el.getAttribute('data-raw');
        navigator.clipboard.writeText(text).then(function() {
            var btn = document.getElementById('copy-btn-sample');
            if (btn) {
                btn.classList.add('copied');
                btn.innerHTML = '\\u2713 Copied';
                setTimeout(function() {
                    btn.classList.remove('copied');
                    btn.innerHTML = 'Copy';
                }, 2000);
            }
        });
    }
}

switchSampleView('optional');

// Zoom
(function() {
    var currentZoom = 100;
    var container = document.querySelector('.container');
    var zoomLevel = document.getElementById('zoom-level');
    document.getElementById('zoom-in-btn').onclick = function() {
        if (currentZoom < 200) { currentZoom += 10; container.style.zoom = currentZoom / 100; zoomLevel.textContent = currentZoom + '%'; }
    };
    document.getElementById('zoom-out-btn').onclick = function() {
        if (currentZoom > 50) { currentZoom -= 10; container.style.zoom = currentZoom / 100; zoomLevel.textContent = currentZoom + '%'; }
    };
})();

// Theme toggle
(function() {
    var themes = ['auto', 'light', 'dark'];
    var prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    var currentSetting = 'auto';
    var themeBtn = document.getElementById('theme-btn');

    function resolveTheme(setting) {
        if (setting === 'auto') return prefersDark.matches ? 'dark' : 'light';
        return setting;
    }

    function apply() {
        document.documentElement.setAttribute('data-theme', resolveTheme(currentSetting));
        if (themeBtn) themeBtn.textContent = currentSetting;
    }

    if (themeBtn) {
        themeBtn.onclick = function() {
            var idx = themes.indexOf(currentSetting);
            currentSetting = themes[(idx + 1) % themes.length];
            apply();
        };
    }

    prefersDark.addEventListener('change', function() { apply(); });
    apply();
})();
</script>`;
}

// ──────────────────────────────────────────────────────────
//  Index page
// ──────────────────────────────────────────────────────────

export interface IndexPageOptions {
  title: string;
  description?: string;
  version?: string;
  modules: Array<{
    fullName: string;
    shortDescription: string;
    /** Product area grouping key (e.g. "appliance", "switch") */
    group: string;
  }>;
  inlineStyles?: boolean;
}

/**
 * Render the collection index / landing page.
 */
export function renderIndexPage(opts: IndexPageOptions): string {
  const { title, description, version, modules, inlineStyles = false } = opts;

  const styleTag = inlineStyles
    ? `<style>${getStyles()}</style>`
    : `<link rel="stylesheet" href="styles.css">`;

  // Group modules by product area
  const groups = new Map<string, typeof modules>();
  for (const mod of modules) {
    const g = groups.get(mod.group) || [];
    g.push(mod);
    groups.set(mod.group, g);
  }

  const sortedGroupNames = Array.from(groups.keys()).sort();

  const groupsHtml = sortedGroupNames
    .map(groupName => {
      const mods = groups.get(groupName)!;
      mods.sort((a, b) => a.fullName.localeCompare(b.fullName));
      return `
            <div class="module-group" data-group="${escapeHtml(groupName)}">
                <div class="module-group-title">${escapeHtml(groupName)} (${mods.length})</div>
                <ul class="module-list">
                    ${mods
                      .map(
                        m => `
                    <li class="module-entry" data-name="${escapeHtml(m.fullName.toLowerCase())}">
                        <a href="modules/${escapeHtml(m.fullName)}.html">${escapeHtml(m.fullName)}</a>
                        <span class="module-short-desc">${escapeHtml(m.shortDescription)}</span>
                    </li>`,
                      )
                      .join('')}
                </ul>
            </div>`;
    })
    .join('');

  return `<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${escapeHtml(title)}</title>
    ${styleTag}
</head>
<body>
    <div class="toolbar">
        <button class="toolbar-btn" id="theme-btn" title="Toggle theme">auto</button>
    </div>
    
    <nav class="nav-bar" style="padding: 0.75rem 2rem; border-bottom: 1px solid var(--border-color, #444);">
        <a href="index.html" style="color: var(--accent-color, #4a9eff); text-decoration: none; margin-right: 1.5rem; font-weight: 600;">Modules</a>
        <a href="mcp-server.html" style="color: var(--accent-color, #4a9eff); text-decoration: none; margin-right: 1.5rem;">MCP Server</a>
        <a href="cli.html" style="color: var(--accent-color, #4a9eff); text-decoration: none; margin-right: 1.5rem;">CLI</a>
    </nav>

    <div class="container">
        <div class="index-header">
            <h1>${escapeHtml(title)}</h1>
            ${description ? `<div class="index-desc">${escapeHtml(description)}</div>` : ''}
            ${version ? `<div class="index-meta">Version ${escapeHtml(version)} &middot; ${modules.length} modules</div>` : `<div class="index-meta">${modules.length} modules</div>`}
        </div>
        
        <input type="text" class="search-box" id="module-search" placeholder="Search modules..." autocomplete="off">
        
        ${groupsHtml}
    </div>
    
    <script>
    // Search / filter
    (function() {
        var searchBox = document.getElementById('module-search');
        searchBox.addEventListener('input', function() {
            var query = searchBox.value.toLowerCase();
            document.querySelectorAll('.module-entry').forEach(function(entry) {
                var name = entry.getAttribute('data-name') || '';
                var desc = (entry.querySelector('.module-short-desc') || {}).textContent || '';
                var match = name.includes(query) || desc.toLowerCase().includes(query);
                entry.style.display = match ? '' : 'none';
            });
            document.querySelectorAll('.module-group').forEach(function(group) {
                var visible = group.querySelectorAll('.module-entry[style=""],.module-entry:not([style])');
                var anyVisible = false;
                visible.forEach(function(e) { if (e.style.display !== 'none') anyVisible = true; });
                group.style.display = anyVisible ? '' : 'none';
            });
        });
    })();

    // Theme toggle
    (function() {
        var themes = ['auto', 'light', 'dark'];
        var prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
        var currentSetting = 'auto';
        var themeBtn = document.getElementById('theme-btn');
        function resolveTheme(s) { return s === 'auto' ? (prefersDark.matches ? 'dark' : 'light') : s; }
        function apply() {
            document.documentElement.setAttribute('data-theme', resolveTheme(currentSetting));
            if (themeBtn) themeBtn.textContent = currentSetting;
        }
        if (themeBtn) {
            themeBtn.onclick = function() {
                var idx = themes.indexOf(currentSetting);
                currentSetting = themes[(idx + 1) % themes.length];
                apply();
            };
        }
        prefersDark.addEventListener('change', function() { apply(); });
        apply();
    })();
    </script>
</body>
</html>`;
}

/**
 * Infer a product-area group from a module's fully qualified name.
 * E.g. "cisco.meraki_rm.meraki_appliance_prefixes" -> "appliance"
 */
export function inferGroup(pluginFullName: string): string {
  const pluginName = pluginFullName.split('.').pop() || pluginFullName;
  const withoutPrefix = pluginName.replace(/^meraki_/, '');

  const knownGroups = [
    'appliance', 'camera', 'device', 'floor', 'group',
    'mqtt', 'organization', 'sensor', 'switch', 'vlan',
    'webhooks', 'wireless',
  ];

  for (const g of knownGroups) {
    if (withoutPrefix.startsWith(g)) {
      return g;
    }
  }

  const firstWord = withoutPrefix.split('_')[0];
  return firstWord || 'other';
}
