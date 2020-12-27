let hljs;
try {
    hljs = require('highlight.js'); // https://highlightjs.org
} catch (err) {
    console.error("No highlight.js module!");
    hljs = null;
}
let pikchr;
try {
    pikchr = require('pikchr');
} catch (err) {
    console.error("No pikchr module!");
    pikchr = null;
}

const markdown_it = require('markdown-it')({
    html: true,        // Enable HTML tags in source
    xhtmlOut: false,        // Use '/' to close single tags (<br />).
                            // This is only for full CommonMark compatibility.
    breaks: false,        // Convert '\n' in paragraphs into <br>
    //langPrefix:   'language-',  // CSS language prefix for fenced blocks. Can be
    // useful for external highlighters.
    linkify: true,        // Autoconvert URL-like text to links

    // Enable some language-neutral replacement + quotes beautification
    typographer: true,
    // Double + single quotes replacement pairs, when typographer enabled,
    // and smartquotes on. Could be either a String or an Array.
    //
    // For example, you can use '«»„“' for Russian, '„“‚‘' for German,
    // and ['«\xA0', '\xA0»', '‹\xA0', '\xA0›'] for French (including nbsp).
    quotes: '“”‘’',

    // Highlighter function. Should return escaped HTML,
    // or '' if the source string is not changed and should be escaped externally.
    // If result starts with <pre... internal wrapper is skipped.
    highlight: function (str, lang) {
        if (pikchr && lang && lang.trim()==="pikchr") {
            const result = pikchr.pikchrex(str);
            const output = result.output.replace('svg',
                                `svg width="${result.width}" height="${result.height}"`);
            return `<pre style="visibility: hidden"></pre><div style="width: 100px;">${output}</div>`;
        }
        if (hljs && lang && hljs.getLanguage(lang)) {
          try {
            return '<pre class="hljs"><code>' +
                   hljs.highlight(lang, str, true).value +
                   '</code></pre>';
          } catch (err) {
              console.error("Highlight error for: "+lang);
              return '';
          }
        }

        return '<pre class="hljs"><code>' + markdown_it.utils.escapeHtml(str) + '</code></pre>';
    }
});
const md_it_anchor = require('markdown-it-anchor');
const toc = require("markdown-it-table-of-contents");
const stripBom = require('strip-bom');
const fs = require('fs');

//import markdownIt from 'markdown-it'
const markdownItMermaid = require('markdown-it-mermaid').default;


function markdown_it_version(source, get_pagenr) {
    markdown_it.use(md_it_anchor);
    markdown_it.use(markdownItMermaid);
    markdown_it.use(toc, {
        format: function(heading, md, link) {
                    const pagenr = get_pagenr(heading, link, md);
                    return `${heading}</a> <a style="float:right; text-align: right" href="${link}">${pagenr}`;
        },
        includeLevel: (process.env.TOC_INCLUDE_LEVEL ? JSON.parse(process.env.TOC_INCLUDE_LEVEL) : [2, 3])
    });
    return markdown_it.render(source);
}

async function read_stdin() {
    return new Promise((resolve, reject) => {
        const chunks = [];
        try {
            process.stdin.on('data', function (chunk) {
                chunks.push(chunk);
            });
            process.stdin.on('end', function () {
                resolve(chunks.join(''));
            })
            process.stdin.setEncoding(process.env['REMARK_ENCODING'] || 'utf8');
            process.stdin.resume();
        } catch (err) {
            reject(err);
        }
    });
}

function stdmain(source, get_pagenr) {
    return markdown_it_version(stripBom(source), get_pagenr);
}

async function a_main_wrapper(get_pagenr, source) {
    let input;
    if ( source==='-') {
        input = await read_stdin();
    } else {
        input = fs.readFileSync(source).toString();
    }
    const output = stdmain(input, get_pagenr);
    console.log(output);
}

exports.stdmain = stdmain;
exports.main = a_main_wrapper;

if (!module.parent) {
    const tag = process.argv[2]
    let source = '-';
    if (process.argv.length>3) {
        source = process.argv[3];
    }
    a_main_wrapper(()=>tag, source).then(()=>{}).catch(console.error);
}
