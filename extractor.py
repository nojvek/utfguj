import pdfquery
from pyquery import PyQuery as pq
from lxml import etree
import urllib


def pdf2xml(path):
	pdf = pdfquery.PDFQuery(path + ".pdf");
	pdf.load()
	pdf.tree.write(path + ".xml", pretty_print=True, encoding='utf-8')
	print pdf.tree


if __name__ == "__main__":
	pdf2xml("pdfs/ratnavali");
	#xml2html("pdfs/fagva_eng")
