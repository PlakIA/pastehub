from django.shortcuts import render


def handler401(request, exception):
    return render(
        request=request,
        template_name="errors/401.html",
        status=401,
    )


def handler404(request, exception):
    return render(
        request=request,
        template_name="errors/404.html",
        status=404,
    )


def handler405(request, exception):
    return render(
        request=request,
        template_name="errors/405.html",
        status=405,
    )


def handler500(request):
    return render(
        request=request,
        template_name="errors/500.html",
        status=500,
    )


__all__ = ["handler404", "handler405"]
