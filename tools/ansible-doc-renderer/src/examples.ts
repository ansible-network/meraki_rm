import { escapeHtml } from './format';
import { capitalizeTitle } from './format';
import { highlightYaml } from './yaml-highlighter';

interface ExampleSection {
  title: string;
  beforeState?: string;
  task: string;
  taskOutput?: string;
  afterState?: string;
}

export function renderExamples(examples: string): string {
  const sections = parseExamples(examples);

  if (sections.length === 0) {
    return `<div class="example-section">
                <div class="example-code">
                    <pre>${highlightYaml(examples)}</pre>
                </div>
            </div>`;
  }

  return sections
    .map((section, index) => {
      const taskId = `example-${index}`;
      const escapedRaw = escapeHtml(section.task)
        .replace(/'/g, '&#39;')
        .replace(/"/g, '&quot;');

      let html = `<div class="example-section">`;

      html += `<div class="example-header">
                <span class="example-title">${escapeHtml(section.title)}</span>
                <button class="example-copy-btn" id="copy-btn-${taskId}" onclick="copyExample('${taskId}')">
                    Copy
                </button>
            </div>`;

      if (section.beforeState) {
        html += `<div class="example-context">
                    <div class="example-context-label">Before state:</div>
${escapeHtml(section.beforeState)}</div>`;
      }

      html += `<div class="example-code" id="task-${taskId}" data-raw="${escapedRaw}">
                <pre>${highlightYaml(section.task)}</pre>
            </div>`;

      if (section.taskOutput) {
        html += `<div class="example-context">
                    <div class="example-context-label">Task Output:</div>
${escapeHtml(section.taskOutput)}</div>`;
      }

      if (section.afterState) {
        html += `<div class="example-context">
                    <div class="example-context-label">After state:</div>
${escapeHtml(section.afterState)}</div>`;
      }

      html += `</div>`;
      return html;
    })
    .join('');
}

export function parseExamples(examples: string): ExampleSection[] {
  const sections: ExampleSection[] = [];
  const lines = examples.split('\n');

  let currentSection: ExampleSection | null = null;
  let currentPart: 'start' | 'before' | 'task' | 'output' | 'after' = 'start';
  let buffer: string[] = [];
  let sectionHeader: string | null = null;

  const flushBuffer = () => {
    if (!currentSection) { return; }
    const content = buffer.join('\n').trim();
    if (!content) {
      buffer = [];
      return;
    }

    switch (currentPart) {
      case 'before':
        currentSection.beforeState = content;
        break;
      case 'task':
        currentSection.task = (currentSection.task ? currentSection.task + '\n\n' : '') + content;
        break;
      case 'output':
        currentSection.taskOutput = content;
        break;
      case 'after':
        currentSection.afterState = content;
        break;
    }
    buffer = [];
  };

  const saveCurrentSection = () => {
    if (currentSection) {
      flushBuffer();
      if (currentSection.task) {
        sections.push(currentSection);
      }
    }
    currentSection = null;
    currentPart = 'start';
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmedLine = line.trim();

    if (/^#\s*Using\s+\w+/.test(trimmedLine)) {
      saveCurrentSection();
      sectionHeader = trimmedLine.replace(/^#\s*/, '');
      continue;
    }

    if (/^#\s*Before\s+state:?\s*$/i.test(trimmedLine)) {
      flushBuffer();
      currentPart = 'before';
      continue;
    }

    if (/^#\s*Task\s+[Oo]utput:?\s*$/i.test(trimmedLine)) {
      flushBuffer();
      currentPart = 'output';
      continue;
    }

    if (/^#\s*After\s+state:?\s*$/i.test(trimmedLine)) {
      flushBuffer();
      currentPart = 'after';
      continue;
    }

    if (trimmedLine.startsWith('- name:')) {
      saveCurrentSection();

      const rawTaskName = trimmedLine
        .replace(/^-\s*name:\s*/, '')
        .replace(/^["']|["']$/g, '');
      const taskName = capitalizeTitle(rawTaskName);

      currentSection = {
        title: sectionHeader ? `${sectionHeader}: ${taskName}` : taskName,
        task: '',
      };
      sectionHeader = null;
      currentPart = 'task';
      buffer = [line];
      continue;
    }

    if (currentPart === 'task' && trimmedLine.startsWith('#') && buffer.length > 0) {
      const hasYaml = buffer.some(l => !l.trim().startsWith('#') && l.trim().length > 0);
      if (hasYaml) {
        if (/^#\s*-+\s*$/.test(trimmedLine)) {
          continue;
        }
        flushBuffer();
        currentPart = 'output';
        buffer = [line];
        continue;
      }
    }

    if (currentSection) {
      buffer.push(line);
    }
  }

  saveCurrentSection();
  return sections;
}
