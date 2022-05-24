from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import *
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.db.models import Q

# Create your views here.

decs = [csrf_exempt, never_cache]


class homeview(ListView):
    template_name = 'home.html'
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        exclude = SaleProduct.objects.values('product')
        counts = Product.objects.all().count()
        val = int(counts / 4)
        queryset = Product.objects.exclude(product_id__in=exclude).order_by('product_id')[val:]
        return queryset

    def get_context_data(self, **kwargs):
        context = super(homeview, self).get_context_data(**kwargs)
        context['sales'] = SaleProduct.objects.all()
        if self.request.user.is_authenticated:
            context['cart'] = Cart.objects.filter(added_by=self.request.user).count()
            return context
        else:
            print(context['sales'])
            return context


@method_decorator(decs, name='dispatch')
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'login.html')

    def post(self, request):
        email = request.POST['logemail']
        password = request.POST['logpass']
        userlog = authenticate(request, email=email, password=password)
        if userlog is not None:
            login(request, userlog)
            return redirect('products')
        else:
            messages.error(request, "Credentials you Provide are incorrect or email is not registered")
            return redirect('Login')


class Aboutview(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(added_by=self.request.user).count()
            return render(request, 'about.html', {'cart': cart})
        else:
            return render(request, 'about.html')


@method_decorator(decs, name='dispatch')
class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'register.html')

    def post(self, request):
        fname = request.POST['reg_fname']
        lname = request.POST['reg_lname']
        email = request.POST['reg_email']
        password = request.POST['reg_pass']
        userexist = CustomUser.objects.filter(email=email).exists()
        if userexist:
            messages.error(request, "User with this email already exists")
            return redirect('register')
        else:
            usersave = CustomUser(first_name=fname, last_name=lname, email=email, password=password)
            usersave.set_password(password)
            usersave.save()
            return redirect('Login')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ProductView(LoginRequiredMixin, ListView):
    template_name = 'products.html'
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        exclude = SaleProduct.objects.values('product')
        queryset = Product.objects.exclude(product_id__in=exclude).order_by('product_id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['sales'] = SaleProduct.objects.all()
        context['cart'] = Cart.objects.filter(added_by=self.request.user).count()
        Incart = Cart.objects.filter(added_by=self.request.user).values_list('product_added').order_by(
            'product_added')
        incartlist = []
        for i in Incart:
            for j in i:
                incartlist.append(j)
        context['incart'] = incartlist
        print(context['incart'])
        print(context['sales'])
        print(context['cart'])
        return context


@method_decorator(decs, name='dispatch')
class ContactView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(added_by=self.request.user).count()
            return render(request, 'contact.html', {'cart': cart})
        else:
            return render(request, 'contact.html')

    def post(self, request):
        name = request.POST['cname']
        email = request.POST['cemail']
        number = request.POST['cnumber']
        subject = request.POST['csubject']
        message = request.POST['cmessage']
        message = Mail(
            from_email='{}'.format(email),
            to_emails='rajat8146925479@gmail.com',
            subject='{}'.format(subject),
            html_content='<strong>Email By:{0} , senders number:{1}, message:{2}</strong>'.format(name, number,
                                                                                                  message))
        try:
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            messages.success(request, "message is sent to CU Granite")
            return redirect('contact')
        except Exception as e:
            messages.success(request, "message not sent retry or provide correct email")
            return redirect('contact')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class Cartview(LoginRequiredMixin, ListView):
    model = Cart
    context_object_name = 'cart'
    template_name = 'cartview.html'

    def get_context_data(self, **kwargs):
        context = super(Cartview, self).get_context_data(**kwargs)
        context['cart'] = Cart.objects.filter(added_by=self.request.user).count()
        qyery = Cart.objects.values_list('product_added').filter(added_by=self.request.user)
        context['products'] = Product.objects.exclude(~Q(product_id__in=qyery)).order_by('product_id')
        Incart = Cart.objects.filter(added_by=self.request.user).values_list('product_added').order_by(
            'product_added')
        incartlist = []
        for i in Incart:
            for j in i:
                incartlist.append(j)
        context['incart'] = incartlist
        sales = SaleProduct.objects.values_list('product')
        salelist = []
        for i in sales:
            for j in i:
                salelist.append(j)
        print(salelist)
        context['sales'] = salelist
        print(context['incart'])
        print(context['products'])
        return context


decart = [login_required(login_url='/login/'), never_cache, csrf_exempt]


@method_decorator(decart, name='dispatch')
class Removecart(View):
    def post(self, request):
        delcart = request.POST['delcart']
        mod = Cart.objects.filter(added_by=request.user).get(product_added=delcart)
        mod.delete()
        return redirect('/products/')


@method_decorator(decart, name='dispatch')
class Addcart(View):
    def post(self, request):
        adcart = request.POST['adcart']
        product_added = Product.objects.get(pk=adcart)
        cart = Cart(added_by=request.user, product_added=product_added)
        cart.save()
        return redirect('/products/')


ai = [login_required(login_url='/login/')]


class SearchView(ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = 'products'

    def get_queryset(self):
        filters = self.request.GET.get('product')
        if filters == 'all' or filters == 'None' or filters == 'none':
            new_context = Product.objects.all()
            return new_context
        new_context = Product.objects.filter(product_name__contains=filters.capitalize()).exists()
        print(filters)
        print(new_context)
        if new_context:
            new_context = Product.objects.filter(product_name__contains=filters.capitalize())
            return new_context
        else:
            new_context = None
            return new_context

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['cart'] = Cart.objects.filter(added_by=self.request.user).count()
        else:
            context['cart'] = 0
        context['sales'] = SaleProduct.objects.all()
        exclude = SaleProduct.objects.values('product')
        product = self.request.GET.get('product')
        context['product'] = product
        context['search']=self.request.GET.get('product')
        if self.request.user.is_authenticated:
            Incart = Cart.objects.filter(added_by=self.request.user).values_list('product_added').order_by(
                'product_added')
            incartlist = []
            for i in Incart:
                for j in i:
                    incartlist.append(j)
            context['incart'] = incartlist
        context['all'] = Product.objects.exclude(product_id__in=exclude)

        return context


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
