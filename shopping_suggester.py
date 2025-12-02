# -*- coding: utf-8 -*-
"""
생년월일 기반 오늘의 쇼핑 아이템 추천 모듈
네이버 쇼핑 API 연동
"""
import hashlib
import requests
from datetime import datetime
from typing import Dict, Optional, List
import urllib.parse


class ShoppingSuggester:
    """생년월일과 날짜 기반 쇼핑 아이템 추천 클래스"""
    
    # 카테고리별 쇼핑 아이템
    SHOPPING_ITEMS = {
        '패션': [
            '니트', '코트', '가디건', '스웨터', '후드티', '청바지', '슬랙스',
            '운동화', '부츠', '스니커즈', '가방', '지갑', '시계', '선글라스',
            '목도리', '장갑', '모자', '스카프', '벨트', '반지', '목걸이', '귀걸이'
        ],
        '뷰티': [
            '립스틱', '파운데이션', '마스크팩', '세럼', '에센스', '크림',
            '선크림', '클렌징폼', '토너', '로션', '향수', '네일아트', '마스카라',
            '아이섀도', '블러셔', '하이라이터', '컨실러', '프라이머', '미스트'
        ],
        '라이프': [
            '캔들', '디퓨저', '인센스', '플랜터', '화분', '책', '노트북',
            '태블릿', '이어폰', '스피커', '블루투스 이어폰', '무선 충전기',
            '텀블러', '보온병', '머그컵', '그릇', '수저세트', '행주', '수건'
        ],
        '푸드': [
            '초콜릿', '과자', '커피', '차', '녹차', '홍차', '허브티',
            '건강식품', '비타민', '프로틴', '견과류', '건과일', '꿀', '잼',
            '시리얼', '그래놀라', '요거트', '치즈', '와인', '맥주'
        ],
        '홈데코': [
            '쿠션', '담요', '커튼', '램프', '조명', '액자', '그림',
            '인테리어 소품', '거울', '식탁보', '매트', '러그', '카펫',
            '벽지', '스티커', '포스터', '식물', '화분', '가드닝 도구'
        ],
        '취미': [
            '책', '만화', '보드게임', '퍼즐', '레고', '피규어', '인형',
            '악기', '기타', '피아노', '우쿨렐레', '카메라', '드론',
            '자전거', '운동기구', '요가매트', '덤벨', '러닝화'
        ]
    }
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        """
        Args:
            client_id: 네이버 API Client ID
            client_secret: 네이버 API Client Secret
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_url = "https://openapi.naver.com/v1/search/shop.json"
    
    def _search_naver_shopping(self, query: str) -> Optional[Dict]:
        """
        네이버 쇼핑 API로 상품 검색
        
        Args:
            query: 검색어
        
        Returns:
            첫 번째 상품 정보 또는 None
        """
        if not self.client_id or not self.client_secret:
            return None
        
        try:
            headers = {
                'X-Naver-Client-Id': self.client_id,
                'X-Naver-Client-Secret': self.client_secret
            }
            
            params = {
                'query': query,
                'display': 1,  # 첫 번째 결과만
                'start': 1
            }
            
            response = requests.get(self.api_url, headers=headers, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('items') and len(data['items']) > 0:
                item = data['items'][0]
                return {
                    'title': item.get('title', '').replace('<b>', '').replace('</b>', ''),
                    'link': item.get('link', ''),
                    'image': item.get('image', ''),
                    'lprice': item.get('lprice', ''),
                    'hprice': item.get('hprice', ''),
                    'mallName': item.get('mallName', ''),
                    'productId': item.get('productId', ''),
                    'productType': item.get('productType', ''),
                    'brand': item.get('brand', ''),
                    'maker': item.get('maker', ''),
                    'category1': item.get('category1', ''),
                    'category2': item.get('category2', ''),
                    'category3': item.get('category3', ''),
                    'category4': item.get('category4', '')
                }
        except Exception as e:
            print(f"네이버 쇼핑 API 호출 오류: {e}")
            return None
        
        return None
    
    def suggest_shopping_items(self, birth_date: str, date_str: Optional[str] = None, num_items: int = 1) -> List[Dict]:
        """
        생년월일과 날짜 기반으로 오늘의 쇼핑 아이템 추천
        
        Args:
            birth_date: 생년월일 (YYYY-MM-DD)
            date_str: 날짜 (YYYY-MM-DD), None이면 오늘 날짜
            num_items: 추천할 아이템 개수 (기본 3개)
        
        Returns:
            쇼핑 아이템 리스트 (각 아이템은 name, category, search_url 포함)
        """
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # 날짜와 생년월일을 조합하여 시드 생성
        seed_str = f"{date_str}_{birth_date}_shopping"
        seed_hash = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
        
        # 생년월일에서 정보 추출
        birth_dt = datetime.strptime(birth_date, '%Y-%m-%d')
        month = birth_dt.month
        day = birth_dt.day
        
        # 계절 결정
        if month in [12, 1, 2]:
            season = '겨울'
        elif month in [3, 4, 5]:
            season = '봄'
        elif month in [6, 7, 8]:
            season = '여름'
        else:
            season = '가을'
        
        # 카테고리 선택 (시드 기반)
        categories = list(self.SHOPPING_ITEMS.keys())
        selected_items = []
        
        # 첫 번째 아이템만 선택 (네이버 API 호출)
        category_idx = seed_hash % len(categories)
        category = categories[category_idx]
        
        # 해당 카테고리에서 아이템 선택
        items = self.SHOPPING_ITEMS[category]
        item_idx = seed_hash % len(items)
        item_name = items[item_idx]
        
        # 네이버 쇼핑 API로 실제 상품 검색
        product_data = self._search_naver_shopping(item_name)
        
        if product_data:
            # API에서 받은 실제 상품 정보 사용
            selected_items.append({
                'name': product_data.get('title', item_name),
                'category': category,
                'link': product_data.get('link', ''),
                'image': product_data.get('image', ''),
                'price': product_data.get('lprice', ''),
                'mallName': product_data.get('mallName', ''),
                'brand': product_data.get('brand', ''),
                'search_query': item_name,  # 원본 검색어
                'date': date_str
            })
        else:
            # API 호출 실패 시 기본 검색 URL 사용
            search_url = f"https://search.shopping.naver.com/search/all?query={urllib.parse.quote(item_name)}"
            selected_items.append({
                'name': item_name,
                'category': category,
                'link': search_url,
                'search_query': item_name,
                'date': date_str
            })
        
        return selected_items


if __name__ == '__main__':
    # 테스트
    suggester = ShoppingSuggester()
    items = suggester.suggest_shopping_items('1990-05-15')
    for item in items:
        print(f"{item['category']}: {item['name']} - {item['search_url']}")

