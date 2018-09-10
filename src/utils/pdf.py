# from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
# from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure

from timer import watchdog_timer
import threading

import pandas as pd


def parse_layout(layout, container, idx=0, page_num=None, verbose=False):
    """Function to recursively parse the layout tree.
    Original script:
    https://stackoverflow.com/questions/25248140/how-does-one-obtain-the-location-of-text-in-a-pdf-with-pdfminer
    """
    for lt_obj in layout:
        idx += 1
        if verbose:
            print(lt_obj.__class__.__name__)
            print(lt_obj.bbox)
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            content = lt_obj.get_text()
            if verbose:
                print(lt_obj.get_text())
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
                        'lt_id': idx,
                        'page_num': page_num
                    }

                    container.append(layout_elem)

        elif isinstance(lt_obj, LTFigure):
            # skip figures for now
            pass
            # parse_layout(lt_obj, container, idx, page_num)  # Recursive


def pdf_to_df(fp):
    """Extracts text content from PDF and returns the content as a dataframe
    """
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


def get_extractable_pages(path, max_pages=50):
    """Return list of page numbers that will be extractable without error
    """

    pdf_file = open(path, 'rb')
    ok_pages = []  # container for extractable pages

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page_num in range(max_pages):

        while True:

            state = {'completed': False}
            watchdog = threading.Thread(target=watchdog_timer, args=(state,))
            watchdog.daemon = True
            watchdog.start()

            try:
                for page in PDFPage.get_pages(pdf_file, [page_num]):
                    interpreter.process_page(page)
                    layout = device.get_result()
                    if layout:
                        print(f"{page_num}: Hello World!")
                    else:
                        print("nothing?")
                    ok_pages.append(page_num)
                    state['completed'] = True
                break
            except KeyboardInterrupt:
                # this would be the place to log the timeout event
                print(f"Skipped page {page_num}")
                break
            except Exception as e:
                print("type error: " + str(e))
                break
            else:
                print("else?")
                break

    return ok_pages
