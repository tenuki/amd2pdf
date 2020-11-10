# Another md2pdf

Another markdown to pdf project. This time including indexed toc generation.

[[TOC]]

## Requirements

### wkhtmltopdf

Install from: https://wkhtmltopdf.org/ .

### popper's pdftohtml

Unix-like systems install popper/libpopper utils.
Windows: install from https://blog.alivate.com.au/poppler-windows/

### Nodejs

- remark-toc-stdin: `npm install -g remark-toc-stdin`


## Usage

```sh
amd2pdf [-v] [-d] [-c/--css filename.css] [-p/--page PAGE-TYPE] 
                     [-t/--title title] input_filename.md
 -v: set verbose mode on
 -d: set debug mode on
 -t: set document title
 -p: set page type. Default is: A4
 filename.css: stylesheet to use, default: style.css
```

Output will be `input_filename.pdf`.

### Environment options

#### Headers and footers

You can set environment variables:

`[WHERE]-[POSITION]="something important"`
 
 where: 
  * WHERE is `HEADER` or `FOOTER`
  * POSITION is `LEFT`, `CENTER` or `RIGHT`

#### General variables

* `TITLE` document's title
* `HEAD`: head section to include in intermediate html
* `PAGE`: the page size

#### TOC levels

Toc levels to include: 

* `TOC_INCLUDE_LEVEL` : json encoded levels array. Default is `[2, 3]` which
 makes ToC generator to include 2 and 3 headings in toc.
 
 Toc tag used in markdown is `[[TOC]]`.
