from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure

import pandas as pd


def parse_layout(layout, container, idx=0):
    """Function to recursively parse the layout tree.
    Original script: https://stackoverflow.com/questions/25248140/how-does-one-obtain-the-location-of-text-in-a-pdf-with-pdfminer
    """
    for lt_obj in layout:
        idx += 1
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            
            content = lt_obj.get_text()
            
            content_lines = content.split('\n')
            for line in content_lines:
                line = line.strip()
                if len(line) > 0:
                    layout_elem = {
                        'x_start': lt_obj.bbox[0],
                        'y_start': lt_obj.bbox[1],
                        'x_end': lt_obj.bbox[2],
                        'y_end': lt_obj.bbox[3],
                        'lt_type': lt_obj.__class__.__name__,
                        'lt_text': line,
                        'lt_id': idx
                    }

                    container.append(layout_elem)
            
        elif isinstance(lt_obj, LTFigure):
            parse_layout(lt_obj, idx)  # Recursive



def pdf_to_df(fp):
    """Extracts text content from PDF and returns the content as a dataframe
    """
    # parser = PDFParser(fp)
    pdf_file = open(fp, 'rb')

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    layouts = []
    for page in PDFPage.get_pages(pdf_file):
        interpreter.process_page(page)
        layout = device.get_result()
        parse_layout(layout, layouts)

    layouts_df = pd.DataFrame(data=layouts)
    return layouts_df