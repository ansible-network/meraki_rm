export { renderPluginPage, renderIndexPage, inferGroup } from './renderer';
export type { RenderPluginPageOptions, IndexPageOptions } from './renderer';
export { renderParameters, resetSubIdCounter } from './parameters';
export { renderExamples, parseExamples } from './examples';
export { renderReturnValues } from './return-values';
export { renderSampleTask, generateSampleYaml } from './sample-task';
export { highlightYaml, highlightComment } from './yaml-highlighter';
export { escapeHtml, escapeAttr, formatText, capitalizeTitle } from './format';
export { getStyles } from './styles';
export type {
  PluginData,
  PluginDoc,
  PluginOption,
  PluginReturn,
  ReturnValue,
  SeeAlso,
  AnsibleDocOutput,
} from './types';
export { toArray } from './types';
