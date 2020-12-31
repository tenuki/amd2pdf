let hljs;
try {
    hljs = require('highlight.js'); // https://highlightjs.org
} catch (err) {
    console.error("No highlight.js module!");
    hljs = null;
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
        if (hljs && lang && hljs.getLanguage(lang)) {
            try {
                return '<pre class="hljs"><code>' +
                    hljs.highlight(lang, str, true).value +
                    '</code></pre>';
            } catch (err) {
                console.error("Highlight error for: " + lang);
                return '';
            }
        }
        return '<pre class="hljs"><code>' + markdown_it.utils.escapeHtml(str) + '</code></pre>';
    }
});

const LIBS = [];
for (const name of ['markdown-it-pikchr',]) {
    let obj = {};
    LIBS.push([require(name), obj]);
}

let md_it_plantuml;
try {
    md_it_plantuml = require('markdown-it-plantuml-online');
} catch(err) {
    md_it_plantuml = null;
}

const md_it_anchor = require('markdown-it-anchor');
const toc = require("markdown-it-table-of-contents");
const stripBom = require('strip-bom');
const fs = require('fs');



function gen_id() {
    return Math.random().toString(26).slice(2);
}


let GLOBAL_render_default_loadfunc = false;

function render_default(render_info) {
    if (render_info.output_type!=="txt") {
        return md_it_plantuml.render_default(render_info);
    }
    const the_id = gen_id();
    const load_func = `function loadXMLDoc(url, elem_id) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState===XMLHttpRequest.DONE) {   // XMLHttpRequest.DONE == 4
           if (xmlhttp.status=== 200) {
               document.getElementById(elem_id).innerHTML = xmlhttp.responseText;
           }
           else if (xmlhttp.status>=400) {
               console.error('There was an error 400 fetching:'+url);
           }
           else {
               console.error('something else other than 200 was returned while fetching:'+url);
           }
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}
`;
    let code = (!GLOBAL_render_default_loadfunc)?load_func:"";
    GLOBAL_render_default_loadfunc = true;
    code += `loadXMLDoc("${render_info.final_url}", "${the_id}");`;
    return `<script type="text/javascript">${code}</script><pre id="${the_id}"></pre>`
}


function markdown_it_version(source, get_pagenr) {
    markdown_it.use(md_it_anchor);
    for (const lib of LIBS) {
        markdown_it.use(lib[0].default, lib[1]);
    }
    if (md_it_plantuml!==null) {
        markdown_it.use(md_it_plantuml.default, {render_f: render_default})
    }
    markdown_it.use(toc, {
        format: function (heading, md, link) {
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
    if (source === '-') {
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
    if (process.argv.length > 3) {
        source = process.argv[3];
    }
    a_main_wrapper(() => tag, source).then(() => {
    }).catch(console.error);
}
