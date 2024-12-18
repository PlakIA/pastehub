from django.shortcuts import render


def handler404(request, exception):
    return render(
        request=request,
        template_name="404.html",
        status=404,
    )


__all__ = ["handler404"]
