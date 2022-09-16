from django.shortcuts import render
from django.core.mail import send_mail
from django.views.generic import ListView

# Create your views here.
def home_view(request):

    if request.POST:
        csrf, name, email, subject, message = request.POST.values()
        print(name)
        try:
            if request.is_secure():
                protocol = 'https://'
            else:
                protocol = 'http://'

            from templated_email import send_templated_mail
            send_templated_mail(
                template_name='contact_message',
                from_email=email,
                recipient_list=['contact@sofentng.org', 'admin@sofentng.org'],
                context={
                    'subject': subject,
                    'name': name,
                    'message': message,
                    'url': protocol + request.get_host()
                },
                # Optional:
                # cc=['cc@example.com'],
                # bcc=['bcc@example.com'],
                # headers={'My-Custom-Header':'Custom Value'},
                # template_prefix="my_emails/",
                # template_suffix="email",
            )
        except:
            print('error')
            return render(request, 'home/index.html', {'home': True, 'home_home': True, 'error': True})

    return render(request, 'home/index.html', {'home': True, 'home_home': True})

def about_view(request):
    return render(request, 'home/about.html', { 'about': True,})


class Xview(ListView):

    def get(self, request, *args, **kwargs):
        request.is_secure()
        return super().get(request, *args, **kwargs)