# coding=utf-8
from time import sleep
from docx2txt import process
from os import listdir, mkdir
from shutil import rmtree
from string import printable
from os.path import isfile, join, splitext, exists
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from pdfminer.pdfparser import PDFSyntaxError
from FilesConverter import odt_get_text
from Configuration_Files import config

class Docxer:
    def __init__(self):
        self.name = ""

    @staticmethod
    def get_folder(path):
        try:
            files = [f for f in listdir(path) if isfile(join(path, f))]
            print "Found (%d) Files: %s" % (len(files), str(files))
            return files
        except Exception as err:
            print "ERROR: " + str(err)
            return [""]

    def run_files(self, dirs, ready_files, output=""):
        sleep(1)
        if exists(output):
            try:
                rmtree(output)
            except Exception as err:
                print "Unable to access folder"
                exit(0)
        sleep(1)
        try:
            mkdir(output)
        except Exception as err:
            sleep(1)
            mkdir(output)
        for filer in ready_files:
            extension = splitext(dirs + filer)[1]
            print "\r\rConverting: %s to" % filer,
            if "docx" in extension and config.run_docx:
                try:
                    to_write = str(self.process_doxc(dirs + filer).encode('ascii', 'ignore'))
                except (IOError, Exception):
                    to_write = "N?A"
                    print "Couldn't read DOCX: " + filer
            elif "pdf" in extension and config.run_pdf:
                try:
                    to_write = str(self.process_pdf(dirs + filer))
                except (PDFSyntaxError, Exception):
                    to_write = "N?A"
                    print "Couldn't read PDF: " + filer
            elif "odt" in extension and config.run_odt:
                try:
                    to_write = str(odt_get_text(dirs + filer).encode('ascii', 'ignore'))
                except (IOError, Exception):
                    to_write = "N?A"
                    print "Couldn't read ODT: " + filer
            else:
                try:
                    tofile = open(dirs + filer)
                    to_write = str(tofile.read())
                    tofile.close()
                except IOError:
                    print "Couldn't read file: " + filer
                    to_write = "N?A"
            # Only print printable
            sleep(0.1)
            try:
                printa = set(printable)
                to_write = to_write.replace(" ", "(<<&=SPACE=&>>)").replace("", "")
                to_write = filter(lambda x: x in printa, to_write).replace("\t", "")
                to_write = to_write.replace("(<<&=SPACE=&>>)", " ").strip()
                file_loc = str(output + (filer[:filer.rfind(".")]) + ".txt")
                print file_loc
                new_file = open(file_loc, 'w')
                new_file.write(to_write)
                new_file.close()
            except Exception as err:
                print "Error writing the file"
        sleep(1)
        print "Done..."

    @staticmethod
    def process_pdf(path):
        print "Processing pdf"
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = file(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)
        text = retstr.getvalue()
        fp.close()
        device.close()
        retstr.close()
        return text

    def process_doxc(self, files):
        self.name = file
        return process(str(files))