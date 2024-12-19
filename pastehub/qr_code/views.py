from io import BytesIO

from django.http import HttpResponse, HttpResponseNotFound
from qrcode import constants, QRCode


__all__ = ["qr_code_download", "qr_code_preview"]


def qr_code_preview(request, url):
    qr = QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(str(url))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


def qr_code_download(request, format_image, url):
    if format_image.lower() == "png":
        qr = QRCode(
            version=1,
            error_correction=constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(url))
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, kind=format_image)
        response = HttpResponse(
            buffer.getvalue(),
            content_type=f"image/{format_image}",
        )
        response["Content-Disposition"] = (
            f"attachment; filename=qr_code.{format_image.lower()}"
        )
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        return response

    return HttpResponseNotFound()
