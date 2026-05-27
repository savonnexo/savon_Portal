/**
 * Node.js Builder for Savon Nexo Employee Portal — Version 0.1
 * Updates build_portal.py and compiles the final SavonNexo_Portal_v0.1.html
 */
const fs = require('fs');
const path = require('path');

const CWD = process.cwd();

console.log('--- SAVON NEXO PORTAL COMPILER ---');

// 1. Resolve file paths
const themeCssPath = path.join(CWD, 'savon_nexo_theme.css');
const patchAPath = path.join(CWD, 'patch_a_views.js');
const patchBPath = path.join(CWD, 'patch_b_views.js');
const logoB64Path = path.join(CWD, 'logo_b64.txt');
const tastingDataPath = path.join(CWD, 'tastings_data_compact.json');
const buildPyPath = path.join(CWD, 'build_portal.py');
const outputHtmlPath = path.join(CWD, 'SavonNexo_Portal_v0.1.html');

// 2. Read resource files
if (!fs.existsSync(themeCssPath)) throw new Error('Missing savon_nexo_theme.css');
if (!fs.existsSync(patchAPath)) throw new Error('Missing patch_a_views.js');
if (!fs.existsSync(patchBPath)) throw new Error('Missing patch_b_views.js');
if (!fs.existsSync(logoB64Path)) throw new Error('Missing logo_b64.txt');
if (!fs.existsSync(tastingDataPath)) throw new Error('Missing tastings_data_compact.json');
if (!fs.existsSync(buildPyPath)) throw new Error('Missing build_portal.py');

console.log('Reading assets and patches...');
const newCss = fs.readFileSync(themeCssPath, 'utf8').trim();
const patchA = fs.readFileSync(patchAPath, 'utf8').trim();
const patchB = fs.readFileSync(patchBPath, 'utf8').trim();
const logoB64 = fs.readFileSync(logoB64Path, 'utf8').trim();
const tastingData = fs.readFileSync(tastingDataPath, 'utf8').trim();
let pyContent = fs.readFileSync(buildPyPath, 'utf8');

const logoDataUrl = `data:image/png;base64,${logoB64}`;

// 3. Update build_portal.py CSS variable
console.log('Integrating brand CSS into build_portal.py...');
const cssStartMarker = 'CSS = r"""';
const cssEndMarker = '"""';

const cssStartIndex = pyContent.indexOf(cssStartMarker);
if (cssStartIndex === -1) throw new Error('Could not find CSS start block in build_portal.py');

const cssBlockEndIndex = pyContent.indexOf(cssEndMarker, cssStartIndex + cssStartMarker.length);
if (cssBlockEndIndex === -1) throw new Error('Could not find CSS end block in build_portal.py');

// Replace CSS block
pyContent = 
  pyContent.slice(0, cssStartIndex + cssStartMarker.length) + 
  '\n' + newCss + '\n' + 
  pyContent.slice(cssBlockEndIndex);


// 4. Update build_portal.py JS variable (inject patches)
console.log('Integrating Weekly Timesheet & Org Chart JS into build_portal.py...');
const bootMarker = '// ============ BOOT ============';

// Check if patches are already in build_portal.py to avoid double injection
if (pyContent.includes('// ============ INTEGRATED VIEWS (FROM PATCH A) ============')) {
  console.log('Patches already detected in build_portal.py. Cleaning up previous patch injections...');
  // We will restore build_portal.py JS first to avoid doubling it up
  const patchStartMarker = '// ============ INTEGRATED VIEWS (FROM PATCH A) ============';
  const pStartIndex = pyContent.indexOf(patchStartMarker);
  const bootIndex = pyContent.indexOf(bootMarker);
  if (pStartIndex !== -1 && bootIndex !== -1) {
    pyContent = pyContent.slice(0, pStartIndex) + pyContent.slice(bootIndex);
  }
}

const bootIndex = pyContent.indexOf(bootMarker);
if (bootIndex === -1) throw new Error('Could not find BOOT marker in build_portal.py JS');

const integratedJS = `// ============ INTEGRATED VIEWS (FROM PATCH A) ============
${patchA}

// ============ INTEGRATED VIEWS (FROM PATCH B) ============
${patchB}

`;

pyContent = 
  pyContent.slice(0, bootIndex) + 
  integratedJS + 
  pyContent.slice(bootIndex);

// Write the updated build_portal.py back to disk
fs.writeFileSync(buildPyPath, pyContent, 'utf8');
console.log('Success: build_portal.py has been updated and fully integrated!');


// 5. Compile the final HTML Portal from the updated python script components
console.log('Compiling SavonNexo_Portal_v0.1.html...');

// Re-read python file to extract variables cleanly
const updatedPyContent = fs.readFileSync(buildPyPath, 'utf8');

// Helper to extract triple-quoted raw strings from python
function extractPyString(source, varName, isRaw) {
  const marker = varName + (isRaw ? ' = r"""' : ' = """');
  const startIndex = source.indexOf(marker);
  if (startIndex === -1) throw new Error(`Could not find variable ${varName} in python script`);
  
  const endIndex = source.indexOf('"""', startIndex + marker.length);
  if (endIndex === -1) throw new Error(`Could not find closing quotes for ${varName}`);
  
  return source.slice(startIndex + marker.length, endIndex);
}

const finalCss = extractPyString(updatedPyContent, 'CSS', true);
const finalJs = extractPyString(updatedPyContent, 'JS', true);
const finalHtml = extractPyString(updatedPyContent, 'HTML', false);

// Build final output
let outputHtml = finalHtml
  .replace('__CSS__', finalCss)
  .replace('__DATA__', tastingData)
  .replace('__JS__', finalJs)
  .replace('__LOGO_DATA_URL__', logoDataUrl);

// Write compiled portal to disk
fs.writeFileSync(outputHtmlPath, outputHtml, 'utf8');

console.log('Success: standalone HTML portal compiled successfully!');
const stats = fs.statSync(outputHtmlPath);
console.log(`File Name: SavonNexo_Portal_v0.1.html`);
console.log(`File Path: ${outputHtmlPath}`);
console.log(`File Size: ${stats.size.toLocaleString()} bytes`);
console.log('-----------------------------------');
