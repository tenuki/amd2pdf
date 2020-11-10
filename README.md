# Another markdown to pdf tool: md2pdf

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
 -t: set document title
 -o: output filename (default is input_filename.pdf)
 -p: set page type. Default is: A4
 -d: set debug mode on
 filename.css: stylesheet to use, default: style.css
```

Output will be `input_filename.pdf`.

### Environment options

#### Headers and footers

You can set environment variables:

`[WHERE]_[POSITION]="something important"`
 
 where: 
  * WHERE is `HEADER` or `FOOTER`
  * POSITION is `LEFT`, `CENTER` or `RIGHT`

Examples:

 * `set HEADER_LEFT="This is my document"`
 * `set FOOTER_CENTER="[page] of [topage]"`

##### Special variables

You can use some special variables in the headers and footers:

* `[page]`       Replaced by the number of the pages currently being printed
* `[frompage]`   Replaced by the number of the first page to be printed
* `[topage]`     Replaced by the number of the last page to be printed
* `[webpage]`    Replaced by the URL of the page being printed
* `[section]`    Replaced by the name of the current section
* `[subsection]` Replaced by the name of the current subsection
* `[date]`       Replaced by the current date in system local format
* `[isodate]`    Replaced by the current date in ISO 8601 extended format
* `[time]`       Replaced by the current time in system local format
* `[title]`      Replaced by the title of the of the current page object
* `[doctitle]`   Replaced by the title of the output document
* `[sitepage]`   Replaced by the number of the page in the current site being converted
* `[sitepages]`  Replaced by the number of pages in the current site being converted

More detail about this in [wkhtmltopdf documentation](https://wkhtmltopdf.org/usage/wkhtmltopdf.txt).

#### Other Parameters

* `TITLE` document's title
* `HEAD`: head section to include in intermediate html
* `PAGE`: the page size

#### TOC levels

Toc levels to include: 

* `TOC_INCLUDE_LEVEL` : json encoded levels array. Default is `[2, 3]` which
 makes ToC generator to include 2 and 3 headings in toc.
 
 Toc tag used in markdown is `[[TOC]]`.

## Examples

This same readme converted to pdf:

 * [README.sample1.pdf](https://github.com/tenuki/amd2pdf/blob/main/README.sample1.pdf)
 * [README.sample2.pdf](https://github.com/tenuki/amd2pdf/blob/main/README.sample2.pdf)
 
