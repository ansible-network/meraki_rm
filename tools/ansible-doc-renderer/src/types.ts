export interface PluginOption {
  description?: string | string[];
  type?: string;
  default?: unknown;
  choices?: string[];
  required?: boolean;
  elements?: string;
  aliases?: string[];
  suboptions?: Record<string, PluginOption>;
  version_added?: string;
}

export interface SeeAlso {
  module?: string;
  description?: string;
  link?: string;
  name?: string;
}

export interface PluginDoc {
  module?: string;
  plugin_name?: string;
  short_description?: string;
  description?: string | string[];
  version_added?: string;
  author?: string | string[];
  notes?: string | string[];
  options?: Record<string, PluginOption>;
  seealso?: SeeAlso[];
  requirements?: string | string[];
  collection?: string;
  attributes?: Record<string, unknown>;
}

export interface ReturnValue {
  description?: string | string[];
  returned?: string;
  type?: string;
  sample?: unknown;
  contains?: Record<string, unknown>;
}

export interface PluginReturn {
  [key: string]: ReturnValue;
}

export interface PluginData {
  doc?: PluginDoc;
  examples?: string;
  return?: PluginReturn;
  metadata?: unknown;
}

/**
 * The top-level shape of `ansible-doc --json` output:
 * a mapping from fully-qualified plugin name to its documentation data.
 */
export interface AnsibleDocOutput {
  [pluginFullName: string]: PluginData;
}

/** Normalize a value that may be a string or string[] into a string[]. */
export function toArray(value: string | string[] | undefined): string[] {
  if (!value) { return []; }
  if (Array.isArray(value)) { return value; }
  return [value];
}
