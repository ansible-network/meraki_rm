import { escapeHtml } from './format';

/**
 * Apply syntax highlighting to a YAML string, returning HTML with
 * span-wrapped tokens for keys, strings, numbers, booleans, comments, etc.
 */
export function highlightYaml(yaml: string): string {
  const lines = yaml.split('\n');
  return lines.map(line => {
    if (line.trim().startsWith('#')) {
      return `<span class="yaml-comment">${escapeHtml(line)}</span>`;
    }

    if (line.trim() === '') {
      return '';
    }

    const commentMatch = line.match(/^(.+?)(  # .*)$/);
    let codePart = line;
    let commentPart = '';

    if (commentMatch) {
      codePart = commentMatch[1];
      commentPart = commentMatch[2];
    }

    let result = escapeHtml(codePart);

    // List markers with inline key (e.g., "- neighbor_address: value")
    result = result.replace(
      /^(\s*)(-\s)([a-zA-Z_][a-zA-Z0-9_]*)(:)/,
      '$1<span class="yaml-list-marker">$2</span><span class="yaml-key">$3</span>$4',
    );

    // List markers with string value
    result = result.replace(
      /^(\s*)(-\s)(&quot;[^&]*&quot;|&#039;[^&]*&#039;)(\s*)$/,
      '$1<span class="yaml-list-marker">$2</span><span class="yaml-string">$3</span>$4',
    );

    // List markers with simple value
    result = result.replace(
      /^(\s*)(-\s)([^\s].*)$/,
      (match, spaces, marker, value) => {
        if (value.includes('<span')) {
          return match;
        }
        const trimmedValue = value.trim();
        let valueClass = 'yaml-string';
        if (/^(true|false|yes|no|on|off)$/i.test(trimmedValue)) {
          valueClass = 'yaml-bool';
        } else if (/^(null|~)$/i.test(trimmedValue)) {
          valueClass = 'yaml-null';
        } else if (/^-?\d+(\.\d+)?$/.test(trimmedValue)) {
          valueClass = 'yaml-number';
        }
        return `${spaces}<span class="yaml-list-marker">${marker}</span><span class="${valueClass}">${value}</span>`;
      },
    );

    // Regular list markers (bare)
    result = result.replace(/^(\s*)(-\s)$/, '$1<span class="yaml-list-marker">$2</span>');

    // Key-value pairs
    result = result.replace(
      /^(\s*)([a-zA-Z_][a-zA-Z0-9_]*)(:)(\s|$)/,
      '$1<span class="yaml-key">$2</span>$3$4',
    );

    // Quoted string values after colon
    result = result.replace(
      /:(\s+)(".*?"|'.*?')(\s*)$/,
      ':$1<span class="yaml-string">$2</span>$3',
    );

    // Unquoted values after colon
    result = result.replace(/:(\s+)(\S.*)$/, (_match, space, value) => {
      const trimmedValue = value.trim();
      if (/^(true|false|yes|no|on|off)$/i.test(trimmedValue)) {
        return `:${space}<span class="yaml-bool">${value}</span>`;
      }
      if (/^(null|~)$/i.test(trimmedValue)) {
        return `:${space}<span class="yaml-null">${value}</span>`;
      }
      if (/^-?\d+(\.\d+)?$/.test(trimmedValue)) {
        return `:${space}<span class="yaml-number">${value}</span>`;
      }
      return `:${space}<span class="yaml-string">${value}</span>`;
    });

    if (commentPart) {
      result += highlightComment(commentPart);
    }

    return result;
  }).join('\n');
}

/**
 * Highlight a trailing inline comment, with special handling for
 * structured comments like `# (type, required) description`.
 */
export function highlightComment(comment: string): string {
  const structuredMatch = comment.match(
    /^(  # \()([^,]+)(, )(required|optional)(\) )(.*)$/,
  );
  if (structuredMatch) {
    const [, prefix, type, comma, reqOpt, closeParen, desc] = structuredMatch;
    const reqClass = reqOpt === 'required' ? 'yaml-comment-required' : 'yaml-comment-optional';
    return (
      `<span class="yaml-comment-dim">${escapeHtml(prefix)}</span>` +
      `<span class="yaml-comment-type">${escapeHtml(type)}</span>` +
      `<span class="yaml-comment-dim">${escapeHtml(comma)}</span>` +
      `<span class="${reqClass}">${escapeHtml(reqOpt)}</span>` +
      `<span class="yaml-comment-dim">${escapeHtml(closeParen)}${escapeHtml(desc)}</span>`
    );
  }

  return `<span class="yaml-comment-dim">${escapeHtml(comment)}</span>`;
}
