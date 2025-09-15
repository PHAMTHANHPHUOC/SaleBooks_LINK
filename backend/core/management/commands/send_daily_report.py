from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import requests
import json
import logging
from core.views.view_teams_report import get_daily_stats, create_teams_message

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Gửi báo cáo thống kê hàng ngày vào Microsoft Teams'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            help='Chạy ở chế độ test (không gửi thực tế)',
        )
        parser.add_argument(
            '--time',
            type=str,
            help='Thời gian gửi báo cáo (format: HH:MM)',
        )

    def handle(self, *args, **options):
        test_mode = options['test']
        report_time = options.get('time')
        
        self.stdout.write(
            self.style.SUCCESS(f'🚀 Bắt đầu gửi báo cáo thống kê...')
        )
        
        try:
            # Lấy thống kê
            stats = get_daily_stats()
            
            # Tạo message
            message = create_teams_message(stats)
            
            if test_mode:
                self.stdout.write(
                    self.style.WARNING('🧪 CHẠY Ở CHẾ ĐỘ TEST - Không gửi thực tế')
                )
                self.stdout.write('📊 Dữ liệu báo cáo:')
                self.stdout.write(f'  - Ngày: {stats["date"]}')
                self.stdout.write(f'  - Tổng lượt truy cập: {stats["visit_stats"]["total_visits"]:,}')
                self.stdout.write(f'  - Lượt truy cập hôm nay: {stats["visit_stats"]["today_visits"]:,}')
                self.stdout.write(f'  - Người dùng duy nhất: {stats["visit_stats"]["unique_today"]:,}')
                self.stdout.write(f'  - Số quốc gia: {len(stats["country_stats"])}')
                self.stdout.write(f'  - Top sản phẩm: {len(stats["top_products"])}')
                
                self.stdout.write('\n📤 Message sẽ được gửi:')
                self.stdout.write(json.dumps(message, indent=2, ensure_ascii=False))
                
                return
            
            # Gửi đến Teams
            TEAMS_WEBHOOK_URL = "https://defaultc8a25e62e9734b2ead55aeea08f862.89.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/eafa71ada5c843709d4c3685c58cc8c3/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=o24fzuiefrQEh_NZLCv4KHoV-iWwWF9HbmqB-STtwu0"
            
            response = requests.post(
                TEAMS_WEBHOOK_URL,
                json=message,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                self.stdout.write(
                    self.style.SUCCESS('✅ Báo cáo đã được gửi thành công đến Microsoft Teams!')
                )
                self.stdout.write(f'📊 Thống kê gửi:')
                self.stdout.write(f'  - Ngày: {stats["date"]}')
                self.stdout.write(f'  - Tổng lượt truy cập: {stats["visit_stats"]["total_visits"]:,}')
                self.stdout.write(f'  - Lượt truy cập hôm nay: {stats["visit_stats"]["today_visits"]:,}')
                self.stdout.write(f'  - Người dùng duy nhất: {stats["visit_stats"]["unique_today"]:,}')
                self.stdout.write(f'  - Số quốc gia: {len(stats["country_stats"])}')
                self.stdout.write(f'  - Top sản phẩm: {len(stats["top_products"])}')
                
                logger.info(f"Báo cáo hàng ngày đã được gửi thành công - {stats['date']}")
                
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Lỗi khi gửi báo cáo: {response.status_code}')
                )
                self.stdout.write(f'Chi tiết lỗi: {response.text}')
                logger.error(f"Lỗi khi gửi báo cáo: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Lỗi kết nối: {str(e)}')
            )
            logger.error(f"Lỗi kết nối khi gửi báo cáo: {str(e)}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Lỗi không xác định: {str(e)}')
            )
            logger.error(f"Lỗi không xác định khi gửi báo cáo: {str(e)}")
