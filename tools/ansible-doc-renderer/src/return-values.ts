import { PluginReturn } from './types';
import { escapeHtml } from './format';

export function renderReturnValues(returnVals: PluginReturn): string {
  const entries = Object.entries(returnVals);
  if (entries.length === 0) {
    return '<p style="color: var(--text-dim);">No return values documented</p>';
  }

  return `<div class="param-tree">
            ${entries
              .map(
                ([name, val]) => `
            <div class="return-item">
                <div class="return-name">${name}</div>
                <div class="return-meta">${val.type || 'unknown'} — returned: ${val.returned || 'always'}</div>
                <div class="return-desc">${Array.isArray(val.description) ? val.description.join(' ') : val.description || ''}</div>
                ${val.sample !== undefined ? `<div class="return-sample">${escapeHtml(JSON.stringify(val.sample, null, 2))}</div>` : ''}
            </div>
            `,
              )
              .join('')}
        </div>`;
}
