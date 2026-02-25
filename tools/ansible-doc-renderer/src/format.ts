export function escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

export function escapeAttr(text: string): string {
  return text
    .replace(/'/g, '&#39;')
    .replace(/"/g, '&quot;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

/**
 * Convert Ansible doc markup (I(), C(), B(), U(), :ref:, backticks) to HTML.
 */
export function formatText(text: string): string {
  let html = escapeHtml(text);
  html = html.replace(/I\(([^)]+)\)/g, '<em>$1</em>');
  html = html.replace(/C\(([^)]+)\)/g, '<code>$1</code>');
  html = html.replace(/B\(([^)]+)\)/g, '<strong>$1</strong>');
  html = html.replace(/U\(([^)]+)\)/g, '<a href="$1" target="_blank">$1</a>');
  html = html.replace(/:ref:`([^<]+)\s*<[^>]+>`/g, '$1');
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
  return html;
}

export function capitalizeTitle(text: string): string {
  if (!text) { return text; }
  return text
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}
