#coding:utf-8
from wand.image import Image
from wand.color import Color
from docx import Document
from docx.shared import Inches,Cm
import glob, os
def convert_pdf_to_jpg(filename):
    with Image(filename=filename) as img :
        img.format = 'png'
        img.compression_quality = 90
        img.background_color = Color("white")
        img.alpha_channel = 'remove'
#         print('pages = ', len(img.sequence))
        with img.convert('jpg') as converted:
            converted.save(filename=filename.split('\\')[-1][:-4]+'.jpg')





if __name__ == '__main__':
    print('Welcome!')
    # path = os.getcwd()
    list_file_path = glob.glob("*.pdf")
    for file in list_file_path:
        print('Convert file %s to jpeg image'%file)
        convert_pdf_to_jpg(file)

    list_file_path = glob.glob("*.jpg")

    document = Document()
    #changing the page margins
    sections = document.sections
    for section in sections:
        section.top_margin = Cm(1)
        section.bottom_margin = Cm(1)
        section.left_margin = Cm(1.5)
        section.right_margin = Cm(1.5)
    for picPath in list_file_path:
        print('Add image %s to word'%picPath)
        document.add_picture(picPath, width=Inches(7))
    document.save('demo_better.docx')

    print('Deleting intermediate jpeg images...')
    for f in list_file_path:
        os.remove(f)

    print('Finish!')

