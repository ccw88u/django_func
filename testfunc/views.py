# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.utils.http import cookie_date
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.translation import check_for_language, activate, to_locale

import time
# Create your views here.

def index(request):
    return render(request, 'testfunc/index.html')
    ##return HttpResponse('No cookie')

## 設定cookie
def set_c(request, key, value):
    response = HttpResponse('Set your lucku number as 8')
    response.set_cookie(key, value)
    return response

## 讀取cookie
def get_c(request):
    if 'lucky_number' in request.COOKIES:
        return HttpResponse('Your lucky number is {0}'.format(request.COOKIE['lucky_number']))

    else:        
        return HttpResponse('No cookie')

def ps(fn,fv=''):
    print(fn, fv)

## 設定cookie值
def setcookienumber(request):        

    lucky_number = 'No cookie'
    if request.method == "POST" and 'lucky_number' in request.POST.keys():
        print('set cookie page')
        lucky_number_get = request.POST['lucky_number']
        ps('lucky_number_get', lucky_number_get)
        set_c(request, 'lucky_number', lucky_number_get)

        ##設定完cookie後，導向某個功能
        response = HttpResponseRedirect('/testfunc/setcookienumber')

        # set the login cookie for the edx marketing site
        # we want this cookie to be accessed via javascript
        # so httponly is set to None
  
        if request.session.get_expire_at_browser_close():
            max_age = None
            expires = None
        else:
            max_age = request.session.get_expiry_age()
            ps('max_age', max_age)
            expires_time = time.time() + max_age
            expires = cookie_date(expires_time)

        ps('settings.SESSION_COOKIE_DOMAIN', settings.SESSION_COOKIE_DOMAIN)
        ps('expires', expires)

        response.set_cookie('lucky_number', lucky_number_get,
                            max_age=max_age,
                            expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                            path='/',
                            secure=None,
                            httponly=None)
        return response
        

    print('request.COOKIES.keys()', request.COOKIES)
    if 'lucky_number' in request.COOKIES:
        lucky_number = request.COOKIES['lucky_number']
        ps('lucky_number', lucky_number)

      
    ##HttpRequest.session.set_test_cookie()
    #HttpRequest.Session.test_cookie_worked()
    return render(request, 'testfunc/setcookienumber.html', {'lucky_number':lucky_number})

    
    
## 設定session
def setsession(request):

    ps('set session')
    lucky_number = ''
    if request.method == "POST" and 'lucky_number' in request.POST.keys():
        ps('set session post')
        lucky_number_get = request.POST['lucky_number']  
        request.session['lucky_number'] = lucky_number_get
        response = HttpResponseRedirect('/testfunc/setsession')
        return response

    if 'lucky_number' in request.session:
        lucky_number = request.session['lucky_number']

    ##ps('request.session', request.session)
    session_key = request.session.session_key

    ps('session_key', session_key)
    ps('lucky_number', lucky_number)

    sid = request.COOKIES['sessionid']
    ##ps('sid', sid)
    s = Session.objects.get(pk=sid)
    ps('=============ssssssssssss=============', s)
    cookie_session_key = s

    return render(request, 'testfunc/setsession.html', {'lucky_number':lucky_number, 'session_key':session_key, 'cookie_session_key': cookie_session_key})
    #return render(request, 'testfunc/setsession.html', {'lucky_number':lucky_number, 'session_key':session_key})


## 顯示訊息檔案
def languagedisp(request):

    
    from django.utils.translation import LANGUAGE_SESSION_KEY          # >= Django 1.8

    
    if request.method == "POST" and 'language_code' in request.POST.keys():

        response = HttpResponseRedirect('/testfunc/languagedisp')
        lang_code = request.POST['language_code']
        #ps('do language switch', lang_code)
        #ps('request.LANGUAGE_CODE', request.LANGUAGE_CODE)
        ##request.LANGUAGE_CODE = lang_code

        if lang_code and check_for_language(lang_code):
            print('----------set lang_code----------', lang_code)
            request.session[LANGUAGE_SESSION_KEY] = lang_code
            request.session['django_language'] = lang_code
        
        return response

    extra_context = {}
    #extra_context['cookie_title'] = _('cookie title')
    extra_context['cookie_title'] = ugettext('cookie title')
    extra_context['author_title'] = _('author_title')
    extra_context['select_language'] = _('select language')
    ps('extra_context', extra_context)
    
    return render(request, 'testfunc/languagedisp.html', extra_context)



def set_language(request):
    from django.utils.http import is_safe_url
    from django.utils.translation import LANGUAGE_SESSION_KEY          # >= Django 1.8
    """
    Redirect to a given url while setting the chosen language in the
    session or cookie. The url and the language code need to be
    specified in the request parameters.

    Since this view changes how the user will see the rest of the site, it must
    only be accessed as a POST request. If called as a GET request, it will
    redirect to the page in the request (the 'next' parameter) without changing
    any state.
    """
    #return render(request, 'fly/test.html', extra_context)
    next = request.REQUEST.get('next')
    if not is_safe_url(url=next, host=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=next, host=request.get_host()):
            next = '/'
    response = HttpResponseRedirect(next)
    if request.method == 'POST':
        lang_code = request.POST.get('language', None)
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
                request.session[LANGUAGE_SESSION_KEY] = lang_code      # >= Django 1.8
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
            # logger locale language
            #logger(request, 'Locale %s' % (lang_code))

    return response

## 測試cache key 存放秒數事宜
from django.core.cache import cache
def memorycachetest(request):

    formcache = 'no'
    if 'my_key' in cache:
        my_keyV = cache.get('my_key')  
        formcache = 'yes'
    else:
        formcache = 'no'
        cache.set('my_key', 'hello, world!', 5)   ## 5 代表5秒數
        my_keyV = cache.get('my_key')

    return render(request, 'testfunc/memorycachetest.html', {'my_key':my_keyV, 'formcache':formcache})

## 測試頁面cache 機制
from django.views.decorators.cache import cache_page
#@cache_page(60 * 15)    60 * 15 = 900 秒，代表15分鐘
@cache_page(10 * 1)      ##測試頁面cache 10 秒
def newspage(request):    
    print('this is new read')    
    return render(request, 'testfunc/newspage.html')