# -*- coding: utf-8 -*-

from claims.models import Claims
from django.db.models import Count, Max
from django.http import HttpResponse

def index(request):
    CLAIM_STATUS_NEW = 1
    """ This function handles users' claims on spelling error.
    It saves all information into Claims model. It doesn't check
    the fields' length. """
    if (request.is_ajax()):
        record = Claims(ctx_left=request.POST.get('ctx_left', ''),
                        selected=request.POST.get('selected', 'None'),
                        ctx_right=request.POST.get('ctx_right', ''),
                        email=request.POST.get('email', 'unknown@hz.ru'),
                        status=CLAIM_STATUS_NEW,
                        notify='true' == request.POST.get('notify', None),
                        comment=request.POST.get('comment', 'No comments...'),
                        url=request.META.get('HTTP_REFERER', ''))
        record.save()
        return HttpResponse('<result>ok</result>', mimetype="text/xml")
    else:
        return HttpResponse('<result>error</result>', mimetype="text/xml")
