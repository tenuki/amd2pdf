import io
import xml
from xml.sax.saxutils import XMLGenerator

SAMPLE = """<p>Another markdown to pdf project. This time including indexed toc generation.</p>
<div class="toc">
<ul>
<li><a href="#another-markdown-to-pdf-tool-md2pdf">Another markdown to pdf tool: md2pdf</a><ul>
<li><a href="#requirements">Requirements</a><ul>
<li><a href="#wkhtmltopdf">wkhtmltopdf</a></li>
<li><a href="#poppers-pdftohtml">popper's pdftohtml</a></li>
<li><a href="#nodejs">Nodejs</a></li>
</ul>
</li>
<li><a href="#usage">Usage</a><ul>
<li><a href="#environment-options">Environment options</a><ul>
<li><a href="#headers-and-footers">Headers and footers</a><ul>
<li><a href="#special-variables">Special variables</a></li>
</ul>
</li>
<li><a href="#other-parameters">Other Parameters</a></li>
<li><a href="#toc-levels">TOC levels</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="#examples">Examples</a></li>
<li><a href="#some-exemplary-text">Some exemplary text</a></li>
<li><a href="#pikchr-diagrams">Pikchr diagrams!</a></li>
</ul>
</li>
<li><a href="#impossible-trident-pikchr-script">Impossible trident pikchr script</a></li>
<li><a href="#httpsenwikipediaorgwikiimpossible_trident">https://en.wikipedia.org/wiki/Impossible_trident</a></li>
<li><a href="#pikchr-script-by-kees-nuyt-license-creative-commons-by-nc-sa">pikchr script by Kees Nuyt, license Creative Commons BY-NC-SA</a></li>
<li><a href="#httpscreativecommonsorglicensesby-nc-sa40">https://creativecommons.org/licenses/by-nc-sa/4.0/</a><ul>
<li><a href="#syntax-highlighting">Syntax highlighting</a></li>
<li><a href="#plantuml">Plantuml</a><ul>
<li><a href="#standard-image-output">standard image output</a></li>
<li><a href="#vectorial-output">vectorial output</a></li>
<li><a href="#text-output">text output</a></li>
</ul>
</li>
<li><a href="#echarts">echarts</a><ul>
<li><a href="#basic-bar-chart">basic bar chart</a></li>
<li><a href="#multiple-chart-combined">multiple chart combined</a></li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
<h2 id="requirements">Requirements</h2>
<h3 id="wkhtmltopdf">wkhtmltopdf</h3>
"""
RESULT = """<?xml version="1.0" encoding="iso-8859-1"?>
<x><p>Another markdown to pdf project. This time including indexed toc generation.</p>
<div class="toc">
<ul>
<li><a href="#another-markdown-to-pdf-tool-md2pdf">Another markdown to pdf tool: md2pdf<a style="float:right; text-align: right" href="">iiiii</a></a><ul>
<li><a href="#requirements">Requirements<a style="float:right; text-align: right" href="">iiiii</a></a><ul>
<li><a href="#wkhtmltopdf">wkhtmltopdf<a style="float:right; text-align: right" href="">iiiii</a></a></li>
<li><a href="#poppers-pdftohtml">popper's pdftohtml<a style="float:right; text-align: right" href="">iiiii</a></a></li>
<li><a href="#nodejs">Nodejs<a style="float:right; text-align: right" href="">iiiii</a></a></li>
</ul>
</li>
<li><a href="#usage">Usage<a style="float:right; text-align: right" href="">iiiii</a></a><ul>
<li><a href="#environment-options">Environment options<a style="float:right; text-align: right" href="">iiiii</a></a><ul>
<li><a href="#headers-and-footers">Headers and footers<a style="float:right; text-align: right" href="">iiiii</a></a><ul>
<li><a href="#special-variables">Special variables<a style="float:right; text-align: right" href="">iiiii</a></a></li>
</ul>
</li>
<li><a href="#other-parameters">Other Parameters<a style="float:right; text-align: right" href="">iiiii</a></a></li>
<li><a href="#toc-levels">TOC levels<a style="float:right; text-align: right" href="">iiiii</a></a></li>
</ul>
</li>
</ul>
</li>
<li><a href="#examples">Examples<a style="float:right; text-align: right" href="">iiiii</a></a></li>
<li><a href="#some-exemplary-text">Some exemplary text<a style="float:right; text-align: right" href="">iiiii</a></a></li>
<li><a href="#pikchr-diagrams">Pikchr diagrams!<a style="float:right; text-align: right" href="">iiiii</a></a></li>
</ul>
</li>
<li><a href="#impossible-trident-pikchr-script">Impossible trident pikchr script<a style="float:right; text-align: right" href="">iiiii</a></a></li>
<li><a href="#httpsenwikipediaorgwikiimpossible_trident">https://en.wikipedia.org/wiki/Impossible_trident<a style="float:right; text-align: right" href="">iiiii</a></a></li>
<li><a href="#pikchr-script-by-kees-nuyt-license-creative-commons-by-nc-sa">pikchr script by Kees Nuyt, license Creative Commons BY-NC-SA<a style="float:right; text-align: right" href="">iiiii</a></a></li>
<li><a href="#httpscreativecommonsorglicensesby-nc-sa40">https://creativecommons.org/licenses/by-nc-sa/4.0/<a style="float:right; text-align: right" href="">iiiii</a></a><ul>
<li><a href="#syntax-highlighting">Syntax highlighting<a style="float:right; text-align: right" href="">iiiii</a></a></li>
<li><a href="#plantuml">Plantuml<a style="float:right; text-align: right" href="">iiiii</a></a><ul>
<li><a href="#standard-image-output">standard image output<a style="float:right; text-align: right" href="">iiiii</a></a></li>
<li><a href="#vectorial-output">vectorial output<a style="float:right; text-align: right" href="">iiiii</a></a></li>
<li><a href="#text-output">text output<a style="float:right; text-align: right" href="">iiiii</a></a></li>
</ul>
</li>
<li><a href="#echarts">echarts<a style="float:right; text-align: right" href="">iiiii</a></a><ul>
<li><a href="#basic-bar-chart">basic bar chart<a style="float:right; text-align: right" href="">iiiii</a></a></li>
<li><a href="#multiple-chart-combined">multiple chart combined<a style="float:right; text-align: right" href="">iiiii</a></a></li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
<h2 id="requirements">Requirements</h2>
<h3 id="wkhtmltopdf">wkhtmltopdf</h3>
</x>"""

Tag = lambda name, data: '<'+name+'>' + data + '</'+name+'>'


class Generator:
    def generate_for(self, name, attrs):
        pass


class XMLFilterByDepth(XMLGenerator):
    _stack = []

    def __init__(self, depth_check_func, out=None, encoding="iso-8859-1",
                 short_empty_elements=False, prevent_doc=False):
        super().__init__(out, encoding, short_empty_elements)
        self.prevent_doc = prevent_doc
        self.depth_check_func = depth_check_func

    def startElement(self, name, attrs):
        # detection and stack handling
        self._stack.append((name, attrs))
        if self.depth_check_func(self.depth-1):
            return super().startElement(name, attrs)

    def endElement(self, name):
        self._stack.pop()
        if self.depth_check_func(self.depth):
            return super().endElement(name)

    @property
    def depth(self):
        return len(self._stack)

    def startDocument(self):
        if self.prevent_doc:
            return
        return super().startDocument()

    def endDocument(self):
        if self.prevent_doc:
            return
        return super().endDocument()


class XMLPatcher(XMLGenerator):
    _state = False
    _stack = []
    _user_stack = []
    _writing = False

    def __init__(self, generator: Generator, out=None, encoding="iso-8859-1",
                 short_empty_elements=False, prevent_doc=False):
        super().__init__(out, encoding, short_empty_elements)
        self.prevent_doc = prevent_doc
        self.generator = generator

    def startElement(self, name, attrs):
        # detection and stack handling
        if not self._state:
            if 'class' in attrs and attrs['class'] == 'toc':
                self._state = True
        else:
            self._stack.append(name)
            # print('-->', self._stack)
            self._user_stack.append((name, attrs))
        return super().startElement(name, attrs)

    def inject(self, a_string):
        self._writing = True
        try:
            xml.sax.parseString(a_string, self)
        finally:
            self._writing = False

    def endElement(self, name):
        inject = False
        if self._state and (not self._writing) and name == "a":
            _name, _attr = self._user_stack[-1]
            # print("->", _attr['href'])
            inject = True

        # detection and stack handling
        if self._state:
            x = self._stack.pop()
            self._user_stack.pop()  # print('<--', self._stack, x)

        if self._stack == []:
            self._state = False

        ret = super().endElement(name)
        if inject:
            self.inject(self.generator.generate_for(_name, _attr))
        return ret

    def startDocument(self):
        if self.prevent_doc:
            return
        if not self._writing:
            return super().startDocument()

    def endDocument(self):
        if self.prevent_doc:
            return
        if not self._writing:
            return super().endDocument()


class FixedGenerator(Generator):
    def __init__(self, content):
        self.content = content

    def generate_for(self, name, attrs):
        return self.content


def parseXMLandGet(source, proc):
    bb = io.BytesIO()
    xml.sax.parseString(source, proc)
    return bb.getvalue()


def GenerateDummyToc(data: str, prevent_doc=True):
    custom = '<a style="float:right; text-align: right" href="">iiiii</a>'
    bb = io.BytesIO()
    xml.sax.parseString(Tag('x', data), XMLPatcher(FixedGenerator(custom), bb,
                                                   prevent_doc=prevent_doc))
    return bb.getvalue()


def FilterLowest():
    bb = io.BytesIO()
    xml.sax.parseString(Tag('x', Tag('y', 'hello world!')),
                        XMLFilterByDepth(lambda lvl: lvl != 0, bb,
                                         prevent_doc=True))
    return bb.getvalue()


def proc_toc(data: str):
    class LinkHrefGenerator(Generator):
        def __init__(self, content):
            self.content = content

        def generate_for(self, name, attrs):
            href_src = attrs['href']
            return self.content % href_src

    custom = '<a style="float:right; text-align: right" href="%s">iiiii</a>'
    bb, bb2 = io.BytesIO(), io.BytesIO()
    xml.sax.parseString(Tag('x', data), XMLPatcher(LinkHrefGenerator(custom), bb,
                                                   encoding='utf-8',
                                                   prevent_doc=True))
    c1 = bb.getvalue()
    xml.sax.parseString(c1, XMLFilterByDepth(lambda lvl: lvl != 0, bb2,
                                             encoding='utf-8',
                                             prevent_doc=True))
    return bb2.getvalue()


if __name__ == "__main__":
    result = GenerateDummyToc(SAMPLE, False)
    print(result.decode('latin-1').strip() == RESULT)
    result = GenerateDummyToc(SAMPLE)
    print(result.decode('latin-1').strip() == RESULT.replace(
        '<?xml version="1.0" encoding="iso-8859-1"?>', '').strip())

    result = FilterLowest()
    print(result==b'<y>hello world!</y>')

    result = proc_toc(SAMPLE)
    print(result)

