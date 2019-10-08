from django.shortcuts import render


def landing_page(request):
    print ('hellooooo!!!')
    return render(request, 'i2amparis_main/landing_page.html')