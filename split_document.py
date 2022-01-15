from PyPDF2 import PdfFileWriter, PdfFileReader
import argparse
import os

parser = argparse.ArgumentParser(description='Provide details of file to be parsed')

parser.add_argument("file")
parser.add_argument("write")

args = parser.parse_args()


if not os.path.isdir(args.write):
    os.mkdir(args.write)


inputpdf = PdfFileReader(open(args.file, "rb"))

for i in range(inputpdf.numPages):
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    
    with open(os.path.join(args.write, f"page{i}.pdf"), "wb") as outputStream:
        output.write(outputStream)
