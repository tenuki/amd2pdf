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

You must have installed or installa `nodejs` for your platform with the 
following modules (with the following minimal version) :

 * markdown-it: 12.0.2
 * markdown-it-anchor: 6.0.0
 * markdown-it-table-of-contents: 0.5.1
 * strip-bom: 4.0.0


## Usage

```sh
python -m amd2pdf [-v] [-d] [-O] [-c/--css filename.css] [-p/--page PAGE-TYPE] 
[-t/--title title] [-o/--output filename] input_filename.md
 -v: set verbose mode on
 -d: set debug mode on
 -O: open output in browser
 -t title: set document title
 -o filename: set output filename
 -c/--css filename.css: stylesheet to use, default: style.css
 -p/--page PAGE-TYPE: Default A4

Output will be: input_filename.pdf 
```

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

* `TITLE`: document's title
* `HEAD`: head section to include in intermediate html
* `PAGE`: the page size

#### TOC levels

Toc levels to include: 

* `TOC_INCLUDE_LEVEL` : json encoded levels array. Default is `[2, 3]` which
 makes ToC generator to include 2 and 3 headings in toc.
 
 Toc tag used in markdown is `[[TOC]]`.

## Examples

## Some exemplary text

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?

> At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. 
>> Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat

     Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur ac mattis diam, sit amet fermentum ex. Cras elementum at urna ut interdum. Nullam at felis risus. Ut tortor turpis, porttitor et consectetur vel, varius eget purus. Sed dolor ipsum, vulputate nec est eget, dignissim sagittis metus. Nullam ut velit elit. Phasellus sit amet nisi eu sem sagittis vestibulum.


## Pikchr diagrams!

```pikchr
line ; box "Hello," "World!"; arrow ; box "Hello," "World!"; arrow
```

or:

```pikchr
# Impossible trident pikchr script
# https://en.wikipedia.org/wiki/Impossible_trident
# pikchr script by Kees Nuyt, license Creative Commons BY-NC-SA 
# https://creativecommons.org/licenses/by-nc-sa/4.0/

scale = 1.0
eh = 0.5cm
ew = 0.2cm
ed = 2 * eh
er = 0.4cm
lws = 4.0cm
lwm = lws + er
lwl = lwm + er

ellipse height eh width ew
L1: line width lwl from last ellipse.n
line width lwm from last ellipse.s
LV: line height eh down

move right er down ed from last ellipse.n
ellipse height eh width ew
L3: line width lws right from last ellipse.n to LV.end then down eh right ew
line width lwm right from last ellipse.s then to LV.start

move right er down ed from last ellipse.n
ellipse height eh width ew
line width lwl right from last ellipse.n then to L1.end
line width lwl right from last ellipse.s then up eh
```

## Syntax highlighting

```python
def main():
    print("something")
```

## Plantuml
### standard image output
```plantuml Sample
class SimplePlantUMLPlugin {
    + transform(syntaxTree: AST): AST
}
```

### vectorial output
```plantuml svg
class SimplePlantUMLPlugin {
    + transform(syntaxTree: AST): AST
}
```

### text output
```plantuml txt
class SimplePlantUMLPlugin {
    + transform(syntaxTree: AST): AST
}
```


## echarts

### basic bar chart

```echarts
xAxis:
  type: category
  data:
    - Mon
    - Tue
    - Wed
    - Thu
    - Fri
    - Sat
    - Sun
yAxis:
  type: value
series:
  - data:
      - 120
      - 200
      - 150
      - 80
      - 70
      - 110
      - 130
    type: bar
    showBackground: true
    backgroundStyle:
      color: 'rgba(180, 180, 180, 0.2)'
```

### multiple chart combined

```echarts
tooltip: {}
title:
  - text: 在线构建
    subtext: 总计 10887
    left: 25%
    textAlign: center
  - text: 各版本下载
    subtext: 总计 43263
    left: 75%
    textAlign: center
  - text: 主题下载
    subtext: 总计 9009
    left: 75%
    top: 50%
    textAlign: center
grid:
  - top: 50
    width: 50%
    bottom: 45%
    left: 10
    containLabel: true
  - top: 55%
    width: 50%
    bottom: 0
    left: 10
    containLabel: true
xAxis:
  - type: value
    max: 10887
    splitLine:
      show: false
  - type: value
    max: 10887
    gridIndex: 1
    splitLine:
      show: false
yAxis:
  - type: category
    data:
      - map
      - lines
      - bar
      - line
      - pie
      - scatter
      - candlestick
      - radar
      - heatmap
      - treemap
      - graph
      - boxplot
      - parallel
      - gauge
      - funnel
      - sankey
    axisLabel:
      interval: 0
      rotate: 30
    splitLine:
      show: false
  - gridIndex: 1
    type: category
    data:
      - geo
      - title
      - legend
      - tooltip
      - grid
      - markPoint
      - markLine
      - timeline
      - dataZoom
      - visualMap
      - toolbox
      - polar
    axisLabel:
      interval: 0
      rotate: 30
    splitLine:
      show: false
series:
  - type: bar
    stack: chart
    z: 3
    label:
      position: right
      show: true
      color: red
      fontWeight: bold
    data:
      - 3237
      - 2164
      - 7561
      - 7778
      - 7355
      - 2405
      - 1842
      - 2090
      - 1762
      - 1593
      - 2060
      - 1537
      - 1908
      - 2107
      - 1692
      - 1568
  - type: bar
    stack: chart
    silent: true
    itemStyle:
      color: '#eee'
    data:
      - 7650
      - 8723
      - 3326
      - 3109
      - 3532
      - 8482
      - 9045
      - 8797
      - 9125
      - 9294
      - 8827
      - 9350
      - 8979
      - 8780
      - 9195
      - 9319
  - type: bar
    stack: component
    xAxisIndex: 1
    yAxisIndex: 1
    z: 3
    label:
      position: right
      show: true
      color: red
      fontWeight: bold
    data:
      - 2788
      - 9575
      - 9400
      - 9466
      - 9266
      - 3419
      - 2984
      - 2739
      - 2744
      - 2466
      - 3034
      - 1945
  - type: bar
    stack: component
    silent: true
    xAxisIndex: 1
    yAxisIndex: 1
    itemStyle:
      color: '#eee'
    data:
      - 8099
      - 1312
      - 1487
      - 1421
      - 1621
      - 7468
      - 7903
      - 8148
      - 8143
      - 8421
      - 7853
      - 8942
  - type: pie
    radius:
      - 0
      - 30%
    center:
      - 75%
      - 25%
    label:
      color: black
    data:
      - name: echarts.min
        value: 17365
        color: black
      - name: echarts.simple.min
        value: 4079
        color: black
      - name: echarts.common.min
        value: 6929
        color: black
      - name: echarts
        value: 14890
        color: black
  - type: pie
    radius:
      - 0
      - 30%
    center:
      - 75%
      - 75%
    label:
      color: black
    data:
      - name: dark
        value: 1594
      - name: infographic
        value: 925
      - name: shine
        value: 1608
      - name: roma
        value: 721
      - name: macarons
        value: 2179
      - name: vintage
        value: 1982
```



This same readme converted to pdf:

 * [README.sample1.pdf](https://github.com/tenuki/amd2pdf/blob/main/samples/README.sample1.pdf)
 * [README.sample2.pdf](https://github.com/tenuki/amd2pdf/blob/main/samples/README.sample2.pdf)
 
