from django.shortcuts import render

def error404(request) -> render:
    return render(
        request=request,
        template_name='errors/error404.html',
        context={
            'error': 404
        }
    )
