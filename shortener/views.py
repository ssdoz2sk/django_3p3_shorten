from django.contrib.auth import get_user
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from ipware import get_client_ip
from shortener.forms import ShortenForm
from shortener.models import Shorten
from shortener.units.encode_url import encode_url


def get_url_code(url):
    code_split_step = 8
    while True:
        codes = encode_url(url, code_split_step)
        for code in codes:
            short = Shorten.objects \
                           .filter(code=code) \
                           .first()
            if not short:
                return code

        code_split_step += 1


def landingPage(request):
    return render(request, 'landing.html')

def shorten_redirect(request, code):
    recode = Shorten.objects.filter(code=code).first()
    if not recode:
        return redirect('landingPage')
    recode.counter += 1
    recode.save()

    return HttpResponseRedirect(recode.url)

@csrf_exempt
def shorten(request):
    if request.method == 'POST':
        form = ShortenForm(request.POST)
    elif request.method == 'GET':
        form = ShortenForm(request.GET)
    else:
        form = ShortenForm()

    if form.is_valid():
        url = form.cleaned_data['url']
        client_ip, is_routable = get_client_ip(request)

        user = get_user(request)

        if user.is_anonymous:
            user = None

        already_generated = Shorten.objects \
                                   .filter(url=url) \
                                   .filter(create_user=user) \
                                   .first()

        if already_generated:
            shorten_url = already_generated
        else:
            shorten_url = form.save(commit=False)

            shorten_url.code = get_url_code(url)
            shorten_url.create_user = user
            shorten_url.create_ip = client_ip
            shorten_url.save()

        response = HttpResponse(shorten_url, status=201, content_type='application/json')
        response['Location'] = shorten_url.short_url
    else:
        response = HttpResponse(status=400)

    return response


@csrf_exempt
def history(request):
    if request.user.is_authenticated():
        return HttpResponse(status=401)

    shorten_urls = Shorten.objects.filter(creater_user=request.user).order_by('create_at')

    return HttpResponse(shorten_urls, content_type='application/json')

