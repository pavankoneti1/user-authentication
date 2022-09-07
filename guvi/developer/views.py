from django.shortcuts import render, loader, reverse
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from .models import DataBase

# Create your views here.

pk = 0
def home(request):
    return HttpResponseRedirect('signup')

def signup(request):
    template = loader.get_template('signup.html')
    mymembers = DataBase.objects.values('user')
    context={
        1: mymembers
    }
    emails=[]
    for i in context[1]:
        emails.append(i['user'])

    if request.method == 'POST':
        #password validation
        p = request.POST.get('p')
        p1 = request.POST.get('pc')
        spl = '~!@#$%^&*(){}[]:;"/?>.<,+-_=|'
        num = '0123456789'
        cn, cs, cc = False, False, False
        valid = False
        for i in p:
            if i in spl:
                cs = True
            elif i in num:
                cn = True
            elif (i >= 'A' and i <= 'Z'):
                cc = True
            if all([cn, cs, cc]):
                valid = True
                break

        #age calculation
        d = request.POST.get('date', 0)
        today = datetime.date.today()
        age = today.year - int(d[:4]) - ((today.month, today.day) < (int(d[5:7]), int(d[8:])))
        e = request.POST.get('user',None)
        valid1 = e not in emails
        if p == p1 and valid and valid1:
            f = request.POST.get('first',None)
            l = request.POST.get('last',None)
            # e = request.POST['user']
            c = request.POST.get('mobile', None)
            d = request.POST.get('date',None)

            if d is None:
                age=0
            member = DataBase(user=e, first=f, last=l, contact=c, dob=d, age=age, password=p)
            member.save()
            return HttpResponseRedirect(reverse('login'))
        elif not valid1:
            return HttpResponse(template.render({'context':'username already taken try another'}, request))

        elif p!=p1:
            print('no match')
            return HttpResponse(template.render({'context':'passwords didn\'t match'}, request))
        elif not valid:
            return HttpResponse(template.render({'context':'should be minimum 6 characters , include atleast 1 special symbol(!,@,#,$,...) ,1 upper case and 1 numeric number '}, request))
    else:
        return HttpResponse(template.render({}, request))


def TaskList(request):
    mymembers = DataBase.objects.filter(id=pk).values()
    # mymembers = DataBase.objects.all().values()
    template = loader.get_template('task_list.html')
    context = {
        'mymembers': mymembers,
    }

    return HttpResponse(template.render(context, request))


def login(request):
    global pk
    mymembers = DataBase.objects.values('id', 'user','password')
    template = loader.get_template('task_list.html')
    context = {
        'mymembers': mymembers,
    }
    if request.method == 'POST':
        u = request.POST.get('user')
        p = request.POST.get('password')
        ps = False
        for i in context['mymembers']:
            if i['user'] == u:
                if i['password'] == p:
                    ps = True
                    pk = i['id']
                    print(pk)
                    break
        if ps:
            return HttpResponseRedirect(reverse('profile'), context)
        else:
            return HttpResponse(render(request, 'login.html' , {'context':'invalid credentials'}))


    else:
        return HttpResponse(render(request, 'login.html'))

def profile( request):
    mymembers = DataBase.objects.filter(id=pk).values()
    context = {
        'mymembers': mymembers,
    }
    context = dict(context)
    return  HttpResponse(render(request, 'profile.html', context))


def edit(request):
    template = loader.get_template('edit.html')
    member = DataBase.objects.get(id=pk)
    f1 = member.first
    l1 = member.last
    c1 = member.contact
    d1 = member.dob
    age = member.age

    if request.method == 'POST':
        print('it is if in edit')
        # password validation
        p = request.POST.get('p')
        p1 = request.POST.get('pc')
        spl = '~!@#$%^&*(){}[]:;"/?>.<,+-_=|'
        num = '0123456789'
        cn, cs, cc = False, False, False
        valid = False
        for i in p:
            if i in spl:
                cs = True
            elif i in num:
                cn = True
            elif i >= 'A' and i <= 'Z':
                cc = True
            if all([cn, cs, cc]):
                valid = True
                break

        # age calculation
        d = request.POST.get('dob')
        d = str(d)
        print(d, type(d))
        if isinstance(d, str) and d != '':
            today = datetime.date.today()
            age = today.year - int(d[:4]) - ((today.month, today.day) < (int(d[5:7]), int(d[8:])))
            print('age :', today)

        if p == p1 and valid :
            f = request.POST.get('first', None)
            l = request.POST.get('last', None)
            c = request.POST.get('mobile', None)
            d = request.POST.get('dob')
            checkDate = request.POST.get('dob')
            if datetime.date(int(checkDate[:4]), int(checkDate[5:7]), int(checkDate[8:10])) > datetime.date.today():
                return HttpResponse(template.render({'context' : 'date should not be greater than current date'}, request))

            if len(f.strip()) == 0:
                f = f1
            if len(l.strip()) == 0:
                l = l1
            if not isinstance(c, int):
                c = c1
            if len(d.strip()) == 0:
                d = d1

            # member = DataBase.objects.get(id = pk)
            member.first = f
            member.last = l
            member.contact = c
            member.password = p
            member.dob = d
            member.age = age
            member.save()
            return HttpResponseRedirect(reverse('profile'))

        elif p != p1:
            print('no match')
            return HttpResponse(template.render({'context': 'passwords didn\'t match'}, request))
        elif not valid:
            return HttpResponse(template.render({'context': 'should be minimum 6 characters , include atleast 1 special symbol(!,@,#,$,...) ,1 upper case and 1 numeric number '}, request))
    else:
        print('it is else')
        return HttpResponse(template.render({}, request))

