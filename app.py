# -*- coding: utf-8 -*-
"""
생년월일 기반 매일 명언/시 제공 시스템
Flask Backend
"""
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
import os
import json
import hashlib
import string
import random
from datetime import datetime
import pytz
from quote_fetcher import QuoteFetcher
from birthday_analyzer import BirthdayAnalyzer
from color_suggester import ColorSuggester
from drink_suggester import DrinkSuggester
from shopping_suggester import ShoppingSuggester

# 한국시간대 설정
KST = pytz.timezone('Asia/Seoul')

def get_kst_now():
    """한국시간(KST) 기준 현재 시간 반환"""
    return datetime.now(KST)

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
CORS(app)

# 개발 모드 설정
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# 데이터 저장 폴더
DATA_FOLDER = 'data'
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# 단축 URL 저장 파일
SHORT_URL_FILE = os.path.join(DATA_FOLDER, 'short_urls.json')

# 단축 URL 데이터 로드
def load_short_urls():
    """단축 URL 매핑 데이터 로드"""
    if os.path.exists(SHORT_URL_FILE):
        try:
            with open(SHORT_URL_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

# 단축 URL 데이터 저장
def save_short_urls(data):
    """단축 URL 매핑 데이터 저장"""
    with open(SHORT_URL_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 짧은 코드 생성
def generate_short_code(url, length=6):
    """URL에서 짧은 코드 생성"""
    # URL 해시 생성
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    # 랜덤 문자 추가하여 더 짧은 코드 생성
    chars = string.ascii_letters + string.digits
    random_part = ''.join(random.choice(chars) for _ in range(length))
    # 해시와 랜덤 조합
    short_code = (url_hash[:3] + random_part)[:length]
    return short_code

# 명언 수집기 초기화
quote_fetcher = QuoteFetcher()
color_suggester = ColorSuggester()
drink_suggester = DrinkSuggester()

# 네이버 쇼핑 API 키 설정 (환경 변수 또는 직접 설정)
NAVER_CLIENT_ID = os.environ.get('NAVER_CLIENT_ID', '6uQXc6h4TnSMVS_h5ooY')
NAVER_CLIENT_SECRET = os.environ.get('NAVER_CLIENT_SECRET', 'zBXyXbIxN4')
shopping_suggester = ShoppingSuggester(
    client_id=NAVER_CLIENT_ID,
    client_secret=NAVER_CLIENT_SECRET
)

# 사용자별 생년월일 저장 (실제로는 DB 사용 권장)
user_birthdays = {}


@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@app.route('/api/birthday', methods=['POST'])
def save_birthday():
    """생년월일 저장"""
    try:
        data = request.json
        user_id = data.get('user_id', 'default')
        birth_date = data.get('birth_date')
        
        if not birth_date:
            return jsonify({
                'success': False,
                'error': '생년월일이 필요합니다.'
            }), 400
        
        # 생년월일 검증
        try:
            datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'error': '생년월일 형식이 올바르지 않습니다. (YYYY-MM-DD)'
            }), 400
        
        # 저장
        user_birthdays[user_id] = birth_date
        
        # 파일로도 저장 (영구 보존)
        file_path = os.path.join(DATA_FOLDER, f'{user_id}_birthday.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({'birth_date': birth_date, 'saved_at': get_kst_now().isoformat()}, f, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'message': '생년월일이 저장되었습니다.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/birthday/<user_id>', methods=['GET'])
def get_birthday(user_id):
    """생년월일 조회"""
    try:
        # 파일에서 먼저 확인
        file_path = os.path.join(DATA_FOLDER, f'{user_id}_birthday.json')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                birth_date = data.get('birth_date')
        else:
            birth_date = user_birthdays.get(user_id)
        
        if not birth_date:
            return jsonify({
                'success': False,
                'error': '저장된 생년월일이 없습니다.'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'birth_date': birth_date
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_birthday():
    """생년월일 분석"""
    try:
        data = request.json
        birth_date = data.get('birth_date')
        user_id = data.get('user_id', 'default')
        
        if not birth_date:
            # 저장된 생년월일 사용
            file_path = os.path.join(DATA_FOLDER, f'{user_id}_birthday.json')
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    saved_data = json.load(f)
                    birth_date = saved_data.get('birth_date')
            
            if not birth_date:
                return jsonify({
                    'success': False,
                    'error': '생년월일이 필요합니다.'
                }), 400
        
        # 생년월일 분석
        analyzer = BirthdayAnalyzer(birth_date)
        analysis = analyzer.analyze()
        
        return jsonify({
            'success': True,
            'data': analysis
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/quote', methods=['GET'])
def get_quote():
    """매일 명언/시 조회 (랜덤 옵션 지원)"""
    try:
        user_id = request.args.get('user_id', 'default')
        date_str = request.args.get('date')  # 선택적: 특정 날짜
        random_seed = request.args.get('random')  # 랜덤 시드 (다른 한 줄 보기용)
        
        # 생년월일 가져오기
        birth_date = None
        file_path = os.path.join(DATA_FOLDER, f'{user_id}_birthday.json')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                birth_date = data.get('birth_date')
        
        # 랜덤 시드가 있으면 랜덤 명언/시 제공
        if random_seed:
            quote = quote_fetcher.fetch_random_quote(birth_date, random_seed)
        else:
            # 명언 가져오기 (생년월일 포함)
            quote = quote_fetcher.fetch_daily_quote(date_str, birth_date)
        
        # 생년월일이 있으면 분석 정보도 함께 반환
        analysis = None
        if birth_date:
            try:
                analyzer = BirthdayAnalyzer(birth_date)
                analysis = analyzer.analyze()
            except:
                pass
        
        return jsonify({
            'success': True,
            'data': {
                'quote': quote,
                'analysis': analysis
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/daily', methods=['GET'])
def get_daily():
    """생년월일 기반 오늘의 명언/시 (통합 API)"""
    try:
        user_id = request.args.get('user_id', 'default')
        
        # 생년월일 가져오기
        birth_date = None
        file_path = os.path.join(DATA_FOLDER, f'{user_id}_birthday.json')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                birth_date = data.get('birth_date')
        
        if not birth_date:
            return jsonify({
                'success': False,
                'error': '생년월일을 먼저 입력해주세요.',
                'requires_birthday': True
            }), 400
        
        # 생년월일 분석
        try:
            analyzer = BirthdayAnalyzer(birth_date)
            analysis = analyzer.analyze()
        except Exception as e:
            print(f"생년월일 분석 오류: {e}")
            analysis = None
        
        # 오늘의 명언/시 (생년월일 포함)
        try:
            quote = quote_fetcher.fetch_daily_quote(birth_date=birth_date)
        except Exception as e:
            print(f"명언 가져오기 오류: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': f'명언을 가져오는 중 오류가 발생했습니다: {str(e)}'
            }), 500
        
        # 오늘의 컬러 추천
        try:
            color = color_suggester.suggest_color(birth_date)
        except Exception as e:
            print(f"컬러 추천 오류: {e}")
            color = None
        
        # 오늘의 한잔 추천
        try:
            drink = drink_suggester.suggest_drink(birth_date)
        except Exception as e:
            print(f"음료 추천 오류: {e}")
            drink = None
        
        # 오늘의 쇼핑 아이템 추천 (items[0]만 사용)
        try:
            shopping_items = shopping_suggester.suggest_shopping_items(birth_date, num_items=1)
        except Exception as e:
            print(f"쇼핑 아이템 추천 오류: {e}")
            import traceback
            traceback.print_exc()
            shopping_items = []
        
        return jsonify({
            'success': True,
            'data': {
                'quote': quote,
                'analysis': analysis,
                'color': color,
                'drink': drink,
                'shopping_items': shopping_items,
                'date': get_kst_now().strftime('%Y-%m-%d')
            }
        })
    except ValueError as e:
        print(f"ValueError: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        print(f"예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'서버 오류가 발생했습니다: {str(e)}'
        }), 500


@app.route('/api/shorten-url', methods=['POST'])
def shorten_url():
    """URL 단축"""
    try:
        data = request.get_json()
        original_url = data.get('url')
        
        if not original_url:
            return jsonify({
                'success': False,
                'error': 'URL이 필요합니다.'
            }), 400
        
        # 기존 단축 URL 확인
        short_urls = load_short_urls()
        
        # 이미 단축된 URL이 있는지 확인
        for code, url_data in short_urls.items():
            if url_data.get('original_url') == original_url:
                short_code = code
                short_url = f"{request.host_url}s/{short_code}"
                return jsonify({
                    'success': True,
                    'data': {
                        'short_url': short_url,
                        'original_url': original_url,
                        'code': short_code
                    }
                })
        
        # 새로운 단축 코드 생성
        short_code = generate_short_code(original_url)
        
        # 중복 확인 및 재생성
        max_attempts = 10
        attempts = 0
        while short_code in short_urls and attempts < max_attempts:
            short_code = generate_short_code(original_url + str(random.random()))
            attempts += 1
        
        # 단축 URL 저장
        short_urls[short_code] = {
            'original_url': original_url,
            'created_at': get_kst_now().isoformat()
        }
        save_short_urls(short_urls)
        
        # 단축 URL 생성
        short_url = f"{request.host_url}s/{short_code}"
        
        return jsonify({
            'success': True,
            'data': {
                'short_url': short_url,
                'original_url': original_url,
                'code': short_code
            }
        })
    except Exception as e:
        print(f"URL 단축 오류: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'URL 단축 중 오류가 발생했습니다: {str(e)}'
        }), 500


@app.route('/s/<short_code>')
def redirect_short_url(short_code):
    """단축 URL 리다이렉트"""
    try:
        short_urls = load_short_urls()
        
        if short_code in short_urls:
            original_url = short_urls[short_code].get('original_url')
            if original_url:
                return redirect(original_url, code=302)
        
        # 단축 URL이 없으면 메인 페이지로 리다이렉트
        return redirect('/', code=302)
    except Exception as e:
        print(f"리다이렉트 오류: {e}")
        return redirect('/', code=302)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    print(f"생년월일 기반 명언/시 시스템이 시작됩니다.")
    print(f"브라우저에서 http://localhost:{port} 접속하세요.")
    app.run(host='0.0.0.0', port=port, debug=True)

