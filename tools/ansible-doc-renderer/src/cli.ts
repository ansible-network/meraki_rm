import { Command } from 'commander';
import * as fs from 'fs';
import * as path from 'path';
import { AnsibleDocOutput } from './types';
import { renderPluginPage, renderIndexPage, inferGroup } from './renderer';
import { getStyles } from './styles';

const program = new Command();

program
  .name('ansible-doc-render')
  .description('Render ansible-doc JSON into a static HTML documentation site')
  .requiredOption('-i, --input <path>', 'Path to ansible-doc JSON file (from --metadata-dump or --json)')
  .requiredOption('-o, --output <dir>', 'Output directory for the generated site')
  .option('-t, --title <title>', 'Site title', 'Ansible Collection Documentation')
  .option('-d, --description <desc>', 'Collection description')
  .option('-v, --version <ver>', 'Collection version')
  .option('--inline-styles', 'Inline CSS in each page instead of a shared styles.css', false)
  .action((opts) => {
    const inputPath = path.resolve(opts.input);
    const outputDir = path.resolve(opts.output);
    const inlineStyles: boolean = opts.inlineStyles;

    if (!fs.existsSync(inputPath)) {
      console.error(`Input file not found: ${inputPath}`);
      process.exit(1);
    }

    console.log(`Reading ${inputPath}...`);
    const raw = fs.readFileSync(inputPath, 'utf-8');
    let docData: AnsibleDocOutput;

    try {
      docData = JSON.parse(raw);
    } catch {
      console.error('Failed to parse JSON input');
      process.exit(1);
    }

    // ansible-doc --metadata-dump wraps everything under "all" > plugin_type
    // Detect and unwrap if necessary
    if ('all' in docData) {
      const all = (docData as Record<string, Record<string, unknown>>)['all'];
      if (all && typeof all === 'object' && 'module' in all) {
        docData = all['module'] as AnsibleDocOutput;
      }
    }

    const pluginNames = Object.keys(docData).filter(name => {
      const d = docData[name];
      return d && d.doc;
    });

    if (pluginNames.length === 0) {
      console.error('No documented plugins found in input');
      process.exit(1);
    }

    console.log(`Found ${pluginNames.length} plugins`);

    // Create output directories
    const modulesDir = path.join(outputDir, 'modules');
    fs.mkdirSync(modulesDir, { recursive: true });

    // Write shared stylesheet
    if (!inlineStyles) {
      const cssPath = path.join(outputDir, 'styles.css');
      fs.writeFileSync(cssPath, getStyles(), 'utf-8');
      console.log(`  styles.css`);
    }

    // Render each plugin page
    for (const fullName of pluginNames) {
      const data = docData[fullName];
      const html = renderPluginPage({
        pluginFullName: fullName,
        data,
        rootPath: '../',
        inlineStyles,
      });
      const outFile = path.join(modulesDir, `${fullName}.html`);
      fs.writeFileSync(outFile, html, 'utf-8');
      console.log(`  modules/${fullName}.html`);
    }

    // Build index page
    const modules = pluginNames.map(fullName => {
      const data = docData[fullName];
      return {
        fullName,
        shortDescription: data.doc?.short_description || '',
        group: inferGroup(fullName),
      };
    });

    const indexHtml = renderIndexPage({
      title: opts.title,
      description: opts.description,
      version: opts.version,
      modules,
      inlineStyles,
    });

    fs.writeFileSync(path.join(outputDir, 'index.html'), indexHtml, 'utf-8');
    console.log(`  index.html`);
    console.log(`\nDone! ${pluginNames.length} pages written to ${outputDir}`);
  });

program.parse();
