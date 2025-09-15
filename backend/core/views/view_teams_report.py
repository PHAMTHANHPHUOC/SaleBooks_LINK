from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
import requests
import json
from datetime import datetime, timedelta
from django.db.models import Count
from core.models.VisitCounter import VisitLog, VisitCounter
from core.models.SanPham import SanPham, SanPhamView
from .utils import get_visit_stats, get_country_stats
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def get_webhook_url() -> str:
    return getattr(settings, 'TEAMS_WEBHOOK_URL', '')

def detect_webhook_type(webhook_url: str) -> str:
    # 'incoming' for Teams Incoming Webhook; 'flow' for Power Automate flow
    if 'webhook.office.com' in webhook_url or 'office.com/webhook' in webhook_url:
        return 'incoming'
    if 'powerautomate' in webhook_url or 'flow.microsoft' in webhook_url or 'environment.api.powerplatform.com' in webhook_url:
        return 'flow'
    # fallback to explicit setting or default to 'incoming'
    explicit = getattr(settings, 'TEAMS_WEBHOOK_TYPE', '').strip().lower()
    return explicit or 'incoming'

def adapt_payload_for_webhook(message: dict, webhook_type: str) -> dict:
    # Incoming Webhook accepts MessageCard/Adaptive Card directly.
    if webhook_type == 'incoming':
        return message
    # Power Automate manual trigger usually expects a custom schema.
    # Wrap minimal fields so Flow can map them, while still passing full card if needed.
    return {
        'summary': message.get('summary', 'SaleBooks KDP Report'),
        'text': f"📊 {message.get('summary', '')}",
        'raw': message
    }

def get_daily_stats():
    """Lấy thống kê trong ngày"""
    try:
        today = datetime.now().date()
        
        # Thống kê truy cập
        visit_stats = get_visit_stats('home')
        logger.info(f"Visit stats: {visit_stats}")
        
        # Thống kê theo quốc gia hôm nay
        country_stats = get_country_stats('home')
        today_countries = country_stats.get('today', [])
        logger.info(f"Country stats: {len(today_countries)} countries")
        
        # Top sản phẩm hôm nay
        today_products = (
            SanPhamView.objects.filter(created_at__date=today)
            .values("san_pham__id", "san_pham__ten_san_pham", "san_pham__anh_dai_dien")
            .annotate(so_luot=Count("id"))
            .order_by("-so_luot")[:5]
        )
        
        top_products = [
            {
                "ten": v["san_pham__ten_san_pham"],
                "so_luot": v["so_luot"]
            }
            for v in today_products
        ]
        logger.info(f"Top products: {len(top_products)} products")
        
        return {
            'visit_stats': visit_stats,
            'country_stats': today_countries,
            'top_products': top_products,
            'date': today.strftime('%d/%m/%Y')
        }
    except Exception as e:
        logger.error(f"Error in get_daily_stats: {str(e)}")
        # Trả về dữ liệu mặc định nếu có lỗi
        return {
            'visit_stats': {
                'total_visits': 0,
                'today_visits': 0,
                'unique_today': 0
            },
            'country_stats': [],
            'top_products': [],
            'date': datetime.now().date().strftime('%d/%m/%Y')
        }

def create_teams_message(stats):
    """Tạo message cho Microsoft Teams"""
    try:
        # Tạo danh sách top quốc gia
        country_list = ""
        if stats.get('country_stats'):
            for i, country in enumerate(stats['country_stats'][:5], 1):
                flag = get_country_flag(country.get('country_code', 'UN'))
                country_list += f"{i}. {flag} {country.get('country_name', 'Unknown')}: {country.get('visits', 0)} lượt\n"
        
        # Tạo danh sách top sản phẩm
        product_list = ""
        if stats.get('top_products'):
            for i, product in enumerate(stats['top_products'], 1):
                product_list += f"{i}. {product.get('ten', 'Unknown')}: {product.get('so_luot', 0)} lượt xem\n"
    
        # Tạo message card
        message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": f"Báo cáo thống kê ngày {stats.get('date', 'N/A')}",
            "originator": "SaleBooks KDP System",
            "sections": [{
                "activityTitle": f"📊 Báo cáo thống kê ngày {stats.get('date', 'N/A')}",
                "activitySubtitle": "Tổng hợp lượt truy cập và sản phẩm hot từ SaleBooks KDP",
                "activityImage": "https://img.icons8.com/color/96/000000/analytics.png",
                "facts": [
                    {
                        "name": "👥 Tổng lượt truy cập",
                        "value": f"{stats.get('visit_stats', {}).get('total_visits', 0):,}"
                    },
                    {
                        "name": "📅 Lượt truy cập hôm nay",
                        "value": f"{stats.get('visit_stats', {}).get('today_visits', 0):,}"
                    },
                    {
                        "name": "👤 Người dùng duy nhất hôm nay",
                        "value": f"{stats.get('visit_stats', {}).get('unique_today', 0):,}"
                    },
                    {
                        "name": "🌍 Số quốc gia truy cập",
                        "value": f"{len(stats.get('country_stats', []))}"
                    }
                ],
                "markdown": True
            }]
        }
    
        # Thêm section top quốc gia nếu có
        if stats.get('country_stats'):
            message["sections"].append({
                "activityTitle": "🌍 Top quốc gia truy cập hôm nay",
                "text": country_list or "Chưa có dữ liệu"
            })
        
        # Thêm section top sản phẩm nếu có
        if stats.get('top_products'):
            message["sections"].append({
                "activityTitle": "🏆 Top sản phẩm hot hôm nay",
                "text": product_list or "Chưa có dữ liệu"
            })
        
        # Thêm thông tin thời gian
        message["sections"].append({
            "activityTitle": "⏰ Thông tin báo cáo",
            "facts": [
                {
                    "name": "Thời gian tạo báo cáo",
                    "value": datetime.now().strftime('%H:%M:%S %d/%m/%Y')
                },
                {
                    "name": "Nguồn dữ liệu",
                    "value": "SaleBooks KDP - Hệ thống thống kê"
                }
            ]
        })
        
        return message
    except Exception as e:
        logger.error(f"Error creating Teams message: {str(e)}")
        # Trả về message đơn giản nếu có lỗi
        return {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "FF0000",
            "summary": "Báo cáo thống kê - Có lỗi",
            "sections": [{
                "activityTitle": "❌ Lỗi khi tạo báo cáo",
                "activitySubtitle": "Không thể tạo báo cáo thống kê",
                "text": f"Lỗi: {str(e)}"
            }]
        }

def get_country_flag(country_code):
    """Lấy emoji flag cho quốc gia"""
    flags = {
        'VN': '🇻🇳', 'US': '🇺🇸', 'JP': '🇯🇵', 'KR': '🇰🇷', 'CN': '🇨🇳',
        'TH': '🇹🇭', 'SG': '🇸🇬', 'MY': '🇲🇾', 'ID': '🇮🇩', 'PH': '🇵🇭',
        'IN': '🇮🇳', 'AU': '🇦🇺', 'GB': '🇬🇧', 'DE': '🇩🇪', 'FR': '🇫🇷',
        'IT': '🇮🇹', 'ES': '🇪🇸', 'BR': '🇧🇷', 'CA': '🇨🇦', 'RU': '🇷🇺',
        'Unknown': '🌐'
    }
    return flags.get(country_code, '🌐')

@api_view(['POST'])
@csrf_exempt
def send_daily_report(request):
    """API gửi báo cáo thống kê hàng ngày vào Microsoft Teams"""
    try:
        logger.info("Bắt đầu gửi báo cáo thống kê...")
        
        # Lấy thống kê
        stats = get_daily_stats()
        logger.info(f"Đã lấy thống kê: {stats}")
        
        # Tạo message
        message = create_teams_message(stats)
        logger.info(f"Đã tạo message: {message}")
        
        # Gửi đến Teams
        webhook_url = get_webhook_url()
        # Cho phép override qua body để test nếu chưa cấu hình env
        try:
            if not webhook_url and request.body:
                body = json.loads(request.body)
                webhook_url = body.get('webhook_url') or webhook_url
        except Exception:
            pass
        webhook_type = detect_webhook_type(webhook_url)
        if not webhook_url:
            logger.error("TEAMS_WEBHOOK_URL rỗng - chưa cấu hình trong môi trường")
            return JsonResponse({'status': 'error', 'message': 'Chưa cấu hình TEAMS_WEBHOOK_URL'}, status=500)

        logger.info(f"Đang gửi đến Teams webhook: {webhook_url} (type={webhook_type})")
        logger.info(f"Message payload: {json.dumps(message, ensure_ascii=False, indent=2)}")
        payload = adapt_payload_for_webhook(message, webhook_type)

        response = requests.post(
            webhook_url,
            json=payload,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'SaleBooks-KDP-Report/1.0'
            },
            timeout=30
        )
        
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response text: {response.text}")
        
        if response.status_code in [200, 202]:
            logger.info("Báo cáo đã được gửi thành công đến Microsoft Teams")
            return JsonResponse({
                'status': 'success',
                'message': 'Báo cáo đã được gửi thành công đến Microsoft Teams',
                'data': {
                    'stats': stats,
                    'message_card': message,
                    'webhook_url': webhook_url,
                    'webhook_type': webhook_type,
                    'provider_response': {
                        'status_code': response.status_code,
                        'text': response.text
                    }
                }
            })
        else:
            logger.error(f"Lỗi khi gửi báo cáo: {response.status_code} - {response.text}")
            return JsonResponse({
                'status': 'error',
                'message': f'Lỗi khi gửi báo cáo: {response.status_code}',
                'error': response.text,
                'data': {
                    'stats': stats,
                    'message_card': message,
                    'webhook_url': webhook_url,
                    'webhook_type': webhook_type
                }
            }, status=500)
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Lỗi kết nối khi gửi báo cáo: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Lỗi kết nối khi gửi báo cáo',
            'error': str(e)
        }, status=500)
        
    except Exception as e:
        logger.error(f"Lỗi không xác định khi gửi báo cáo: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'status': 'error',
            'message': 'Lỗi không xác định khi gửi báo cáo',
            'error': str(e)
        }, status=500)

@api_view(['GET'])
def get_report_preview(request):
    """API xem trước báo cáo trước khi gửi"""
    try:
        logger.info("Tạo preview báo cáo...")
        stats = get_daily_stats()
        logger.info(f"Stats: {stats}")
        message = create_teams_message(stats)
        logger.info(f"Message: {message}")
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'stats': stats,
                'message': message,
                'webhook_url': get_webhook_url(),
                'webhook_type': detect_webhook_type(get_webhook_url() or '')
            }
        })
        
    except Exception as e:
        logger.error(f"Lỗi khi tạo preview báo cáo: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'status': 'error',
            'message': 'Lỗi khi tạo preview báo cáo',
            'error': str(e)
        }, status=500)

@api_view(['GET'])
def test_report(request):
    """API test đơn giản để kiểm tra"""
    try:
        return JsonResponse({
            'status': 'success',
            'message': 'API hoạt động bình thường',
            'data': {
                'timestamp': datetime.now().isoformat(),
                'test': True
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@api_view(['GET'])
def test_teams_message(request):
    """API test để xem format message Teams"""
    try:
        stats = get_daily_stats()
        message = create_teams_message(stats)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Message format for Teams',
            'data': {
                'stats': stats,
                'teams_message': message,
                'webhook_url': get_webhook_url(),
                'webhook_type': detect_webhook_type(get_webhook_url() or '')
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@api_view(['POST'])
@csrf_exempt
def send_custom_report(request):
    """API gửi báo cáo tùy chỉnh với dữ liệu từ request"""
    try:
        data = json.loads(request.body)
        report_type = data.get('type', 'daily')  # daily, weekly, monthly
        
        # Lấy thống kê theo loại báo cáo
        if report_type == 'daily':
            stats = get_daily_stats()
        else:
            # Có thể mở rộng cho weekly, monthly
            stats = get_daily_stats()
        
        # Tạo message
        message = create_teams_message(stats)
        
        # Gửi đến Teams
        webhook_url = get_webhook_url()
        webhook_type = detect_webhook_type(webhook_url)
        if not webhook_url:
            return JsonResponse({'status': 'error', 'message': 'Chưa cấu hình TEAMS_WEBHOOK_URL'}, status=500)
        payload = adapt_payload_for_webhook(message, webhook_type)
        response = requests.post(
            webhook_url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            return JsonResponse({
                'status': 'success',
                'message': f'Báo cáo {report_type} đã được gửi thành công',
                'data': stats
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': f'Lỗi khi gửi báo cáo: {response.status_code}',
                'error': response.text
            }, status=500)
            
    except Exception as e:
        logger.error(f"Lỗi khi gửi báo cáo tùy chỉnh: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Lỗi khi gửi báo cáo tùy chỉnh',
            'error': str(e)
        }, status=500)
