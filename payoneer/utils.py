from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

from xhtml2pdf import pisa

def render_to_pdf(template_src, context={}):

    template = get_template(template_src)

    html  = template.render(context)
#    print("\n\nUtility.py\n\n{}\n\n{}\n\n".format(html,context))
#    return HttpResponse(html)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None