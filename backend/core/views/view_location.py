from django.http import JsonResponse
from django.contrib.gis.geoip2 import GeoIP2
import geoip2

def get_location(request):
    ip = request.GET.get("ip")
    if not ip:
        # fallback nếu không truyền ip
        ip = request.META.get("REMOTE_ADDR", "")

    try:
        reader = geoip2.database.Reader('GeoLite2-City.mmdb')
        response = reader.city(ip)
        return JsonResponse({
            "ip": ip,
            "city": response.city.name,
            "country": response.country.name,
            "latitude": response.location.latitude,
            "longitude": response.location.longitude,
        })
    except Exception as e:
        return JsonResponse({"error": str(e), "ip": ip})



def get_client_ip(request):
    """Lấy IP thật từ request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
