from weasyprint import HTML


class PDFAdapter():

    @classmethod
    def html_to_pdf(cls, html_code: str, path: str):
        HTML(string=html_code).write_pdf(target=path, zoom=1)

