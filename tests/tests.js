"use strict";
const assert = require("assert");
const stdmain = require("../amd2pdf/md2pdf.js").stdmain;
const chai = require('chai');
chai.use(require('chai-string'));
const expect = require('chai').expect;


const SampleDoc = `# Sample document
[[TOC]]
## Section 1
### Section 1.2
### Section 1.3
## Section 2
### Section 2.1`


const SampleOutput = `<h1 id="sample-document">Sample document</h1>
<p><div class="table-of-contents"><ul><li><a href="#section-1">Section 1</a> <a style="float:right; text-align: right" href="#section-1">xxx</a><ul><li><a href="#section-1.2">Section 1.2</a> <a style="float:right; text-align: right" href="#section-1.2">xxx</a></li><li><a href="#section-1.3">Section 1.3</a> <a style="float:right; text-align: right" href="#section-1.3">xxx</a></li></ul></li><li><a href="#section-2">Section 2</a> <a style="float:right; text-align: right" href="#section-2">xxx</a><ul><li><a href="#section-2.1">Section 2.1</a> <a style="float:right; text-align: right" href="#section-2.1">xxx</a></li></ul></li></ul></div></p>
<h2 id="section-1">Section 1</h2>
<h3 id="section-1.2">Section 1.2</h3>
<h3 id="section-1.3">Section 1.3</h3>
<h2 id="section-2">Section 2</h2>
<h3 id="section-2.1">Section 2.1</h3>
`

describe("Testing Markdown rendering", function () {
    it("Default settings produces default output", function (done) {
        assert.equal(stdmain(SampleDoc, (heading, link) => {
            return 'xxx';
        }), SampleOutput);
        done();
    });

    it("Check we get the links", function (done) {
        const links = [];
        stdmain(SampleDoc, (heading, link) => {
            links.push(link);
            return '';
        });

        assert.deepEqual(links, [
            '#section-1',
            '#section-1.2',
            '#section-1.3',
            '#section-2',
            '#section-2.1',
        ]);
        done();
    });

    it("All links are in the output twice", function (done) {
        const links = [];
        const result = stdmain(SampleDoc, (heading, link) => {
            links.push(link);
            return '';
        });

        for(const link_i of links) {
            // link is found twice, in the heading and in the page-number content
            assert.equal(
                (result.match(new RegExp(link_i+'"', 'g')) || []).length,  2) ;
            // link's without #-preffix is found three times
            assert.equal(
                (result.match(new RegExp(link_i.slice(1)+'"', 'g')) || []).length,  3) ;
        }
        done();
    });

    it("Super basic minimal markdown capability", function (done) {
        expect(stdmain('# main title')).to.startWith(`<h1 id="main-title">main title</h1>\n`);
        done();
    });

    it("BOM support", function (done) {
        expect(stdmain('\ufeff# main title')).to.startWith(`<h1 id="main-title">main title</h1>\n`);
        done();
    });
})
