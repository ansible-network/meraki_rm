import { PluginOption, toArray } from './types';
import { escapeHtml, formatText } from './format';

let _subIdCounter = 0;

function nextSubId(name: string, depth: number): string {
  return `sub-${name}-${depth}-${_subIdCounter++}`;
}

/** Reset the ID counter -- useful for tests or multi-pass rendering. */
export function resetSubIdCounter(): void {
  _subIdCounter = 0;
}

export function renderParameters(
  options: Record<string, PluginOption>,
  depth: number = 0,
): string {
  if (Object.keys(options).length === 0) {
    return '<p style="color: var(--text-dim);">No parameters</p>';
  }

  const sortedOptions = Object.entries(options).sort((a, b) =>
    a[0].localeCompare(b[0]),
  );
  const items = sortedOptions
    .map(([name, opt]) => renderParamItem(name, opt, depth))
    .join('');

  if (depth === 0) {
    return `<div class="param-tree">${items}</div>`;
  }
  const subId = nextSubId('group', depth);
  return `<div class="suboptions" id="${subId}">${items}</div>`;
}

export function renderParamItem(
  name: string,
  opt: PluginOption,
  depth: number,
): string {
  const typeStr = opt.type || 'str';
  const elementsStr = opt.elements ? `/${opt.elements}` : '';
  const hasSuboptions =
    opt.suboptions && Object.keys(opt.suboptions).length > 0;
  const subId = nextSubId(name, depth);

  return `
        <div class="param-item">
            <div class="param-header" ${hasSuboptions ? `onclick="toggleSub('${subId}')"` : ''}>
                <span class="param-toggle">${hasSuboptions ? '▶' : ''}</span>
                <span class="param-name">${name}</span>
                <span class="param-type">(${typeStr}${elementsStr})</span>
                ${opt.required ? '<span class="param-required">required</span>' : ''}
            </div>
            ${renderChoicesDefaults(opt, depth)}
            <div class="param-desc">
                ${toArray(opt.description).map(d => `<p>${formatText(d)}</p>`).join('')}
            </div>
            ${hasSuboptions ? `<div class="suboptions" id="${subId}">${Object.entries(opt.suboptions!).sort((a, b) => a[0].localeCompare(b[0])).map(([n, o]) => renderParamItem(n, o, depth + 1)).join('')}</div>` : ''}
        </div>`;
}

export function renderChoicesDefaults(
  opt: PluginOption,
  depth: number = 0,
): string {
  let html = '';
  const marginLeft = depth > 0 ? '' : 'margin-left: 22px;';

  if (opt.choices && opt.choices.length > 0) {
    html += `<div class="param-choices" style="${marginLeft}">`;
    html += opt.choices
      .map(c => {
        const isDefault = opt.default === c;
        return `<span class="param-choice${isDefault ? ' default' : ''}">${escapeHtml(String(c))}</span>`;
      })
      .join('');
    html += '</div>';
  } else if (opt.default !== undefined && opt.default !== null) {
    html += `<div class="param-default" style="${marginLeft}">default: <code>${escapeHtml(JSON.stringify(opt.default))}</code></div>`;
  }

  return html;
}
