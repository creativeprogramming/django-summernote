from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.utils import simplejson
from django_summernote.models import Attachment
from django_summernote.settings import summernote_config


def editor(request, id):
    return render(request, 'django_summernote/editor.html', {
        'id': id,
        'toolbar': simplejson.dumps(summernote_config['toolbar']),
        'url': {
            'upload_attachment': reverse_lazy('django_summernote-upload_attachment'),
        },
    })


def upload_attachment(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST method is allowed')

    if not request.FILES.getlist('files'):
        return HttpResponseBadRequest('No files were requested')

    try:
        attachments = []

        for file in request.FILES.getlist('files'):
            attachment = Attachment()
            attachment.file = file
            attachment.name = file.name

            if file.size > summernote_config['attachment_filesize_limit']:
                return HttpResponseBadRequest('File size exceeds the limit allowed and cannot be saved')

            attachment.save()
            attachments.append(attachment)

        return render(request, 'django_summernote/upload_attachment.json', {
            'attachments': attachments,
        })
    except IOError:
        return HttpResponseServerError('Failed to save attachment')
