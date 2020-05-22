# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render

from .forms import FeedbackForm
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail


def feedback_form(request):
    # if request.user.is_authenticated():
    #     username = request.user.username
        username = "test"
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                form.save()
                # This can be used to send an email to inform us about the newly submitted feedback.
                action = form.cleaned_data['service']
                details = form.cleaned_data['details']
                print(details)
                rating = str(form.cleaned_data['rating'])
                email_text = 'User: "' + str(username) + '" submitted his/her feedback on BDO Platform, regarding action: "' + str(
                    action) + '".\nComment: "' + str(details) + '"\nRating: ' + str(rating) + '/5 stars.'
                ''' Begin reCAPTCHA validation '''
                recaptcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'

                values = {
                    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                    'response': recaptcha_response
                }
                data = urllib.parse.urlencode(values).encode()
                req = urllib.request.Request(url, data=data)
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())
                ''' End reCAPTCHA validation '''
                # send_mail(str(username) + "'s Feedback on BDO Platform", email_text, 'noreply@epu.ntua.gr', ['iam@paris-reinforce.eu'],
                #           fail_silently=False)
                # print email_text
                return render(request, 'feedback_form/thanks.html')
        else:
            form = FeedbackForm()
        return render(request, 'feedback_form/feedback_form.html', {'form': form, 'user':username})
    # else:
    #     raise PermissionDenied