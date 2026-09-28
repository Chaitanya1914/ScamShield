import docx
import sys

def read_docx(filename):
    doc = docx.Document(filename)
    for paragraph in doc.paragraphs:
        print(paragraph.text)

if __name__ == '__main__':
    read_docx(sys.argv[1])
