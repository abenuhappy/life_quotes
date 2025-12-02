# -*- coding: utf-8 -*-
"""
생년월일 기반 오늘의 컬러 추천 모듈
"""
import hashlib
from datetime import datetime
from typing import Dict, Optional, Tuple


class ColorSuggester:
    """생년월일과 날짜 기반 컬러 추천 클래스"""
    
    # 별자리별 대표 컬러
    ZODIAC_COLORS = {
        '물병자리': {'name': '하늘색', 'hex': '#87CEEB', 'rgb': (135, 206, 235)},
        '물고기자리': {'name': '바다색', 'hex': '#4682B4', 'rgb': (70, 130, 180)},
        '양자리': {'name': '빨간색', 'hex': '#FF6B6B', 'rgb': (255, 107, 107)},
        '황소자리': {'name': '초록색', 'hex': '#51CF66', 'rgb': (81, 207, 102)},
        '쌍둥이자리': {'name': '노란색', 'hex': '#FFD93D', 'rgb': (255, 217, 61)},
        '게자리': {'name': '은색', 'hex': '#C0C0C0', 'rgb': (192, 192, 192)},
        '사자자리': {'name': '금색', 'hex': '#FFD700', 'rgb': (255, 215, 0)},
        '처녀자리': {'name': '베이지색', 'hex': '#F5DEB3', 'rgb': (245, 222, 179)},
        '천칭자리': {'name': '분홍색', 'hex': '#FFB6C1', 'rgb': (255, 182, 193)},
        '전갈자리': {'name': '진한 빨간색', 'hex': '#DC143C', 'rgb': (220, 20, 60)},
        '사수자리': {'name': '보라색', 'hex': '#9370DB', 'rgb': (147, 112, 219)},
        '염소자리': {'name': '갈색', 'hex': '#8B4513', 'rgb': (139, 69, 19)},
    }
    
    # 계절별 컬러 팔레트
    SEASON_COLORS = {
        '봄': [
            {'name': '벚꽃 핑크', 'hex': '#FFB6C1', 'rgb': (255, 182, 193)},
            {'name': '연두색', 'hex': '#90EE90', 'rgb': (144, 238, 144)},
            {'name': '하늘색', 'hex': '#87CEEB', 'rgb': (135, 206, 235)},
            {'name': '라벤더', 'hex': '#E6E6FA', 'rgb': (230, 230, 250)},
        ],
        '여름': [
            {'name': '바다색', 'hex': '#4682B4', 'rgb': (70, 130, 180)},
            {'name': '에메랄드', 'hex': '#50C878', 'rgb': (80, 200, 120)},
            {'name': '노란색', 'hex': '#FFD700', 'rgb': (255, 215, 0)},
            {'name': '코랄', 'hex': '#FF7F50', 'rgb': (255, 127, 80)},
        ],
        '가을': [
            {'name': '주황색', 'hex': '#FF8C00', 'rgb': (255, 140, 0)},
            {'name': '갈색', 'hex': '#8B4513', 'rgb': (139, 69, 19)},
            {'name': '버건디', 'hex': '#800020', 'rgb': (128, 0, 32)},
            {'name': '올리브', 'hex': '#808000', 'rgb': (128, 128, 0)},
        ],
        '겨울': [
            {'name': '네이비', 'hex': '#000080', 'rgb': (0, 0, 128)},
            {'name': '은색', 'hex': '#C0C0C0', 'rgb': (192, 192, 192)},
            {'name': '아이스 블루', 'hex': '#B0E0E6', 'rgb': (176, 224, 230)},
            {'name': '화이트', 'hex': '#FFFFFF', 'rgb': (255, 255, 255)},
        ],
    }
    
    # 타로 카드별 컬러
    TAROT_COLORS = {
        '마법사': {'name': '보라색', 'hex': '#9370DB', 'rgb': (147, 112, 219)},
        '여교황': {'name': '은색', 'hex': '#C0C0C0', 'rgb': (192, 192, 192)},
        '여황제': {'name': '분홍색', 'hex': '#FFB6C1', 'rgb': (255, 182, 193)},
        '황제': {'name': '빨간색', 'hex': '#FF6B6B', 'rgb': (255, 107, 107)},
        '교황': {'name': '금색', 'hex': '#FFD700', 'rgb': (255, 215, 0)},
        '연인': {'name': '핑크', 'hex': '#FF69B4', 'rgb': (255, 105, 180)},
        '전차': {'name': '주황색', 'hex': '#FF8C00', 'rgb': (255, 140, 0)},
        '힘': {'name': '빨간색', 'hex': '#DC143C', 'rgb': (220, 20, 60)},
        '은둔자': {'name': '회색', 'hex': '#808080', 'rgb': (128, 128, 128)},
        '운명의 바퀴': {'name': '금색', 'hex': '#FFD700', 'rgb': (255, 215, 0)},
        '정의': {'name': '하늘색', 'hex': '#87CEEB', 'rgb': (135, 206, 235)},
        '매달린 사람': {'name': '파란색', 'hex': '#4169E1', 'rgb': (65, 105, 225)},
        '죽음': {'name': '검은색', 'hex': '#000000', 'rgb': (0, 0, 0)},
        '절제': {'name': '청록색', 'hex': '#40E0D0', 'rgb': (64, 224, 208)},
        '악마': {'name': '진한 빨간색', 'hex': '#8B0000', 'rgb': (139, 0, 0)},
        '탑': {'name': '주황색', 'hex': '#FF4500', 'rgb': (255, 69, 0)},
        '별': {'name': '하늘색', 'hex': '#87CEEB', 'rgb': (135, 206, 235)},
        '달': {'name': '은색', 'hex': '#C0C0C0', 'rgb': (192, 192, 192)},
        '태양': {'name': '금색', 'hex': '#FFD700', 'rgb': (255, 215, 0)},
        '심판': {'name': '흰색', 'hex': '#FFFFFF', 'rgb': (255, 255, 255)},
        '세계': {'name': '에메랄드', 'hex': '#50C878', 'rgb': (80, 200, 120)},
        '바보': {'name': '노란색', 'hex': '#FFD93D', 'rgb': (255, 217, 61)},
    }
    
    def __init__(self):
        pass
    
    def suggest_color(self, birth_date: str, date_str: Optional[str] = None) -> Dict:
        """
        생년월일과 날짜 기반으로 오늘의 컬러 추천
        
        Args:
            birth_date: 생년월일 (YYYY-MM-DD)
            date_str: 날짜 (YYYY-MM-DD), None이면 오늘 날짜
        
        Returns:
            컬러 정보 딕셔너리
        """
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # 날짜와 생년월일을 조합하여 시드 생성
        seed_str = f"{date_str}_{birth_date}_color"
        seed_hash = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
        
        # 생년월일에서 정보 추출
        birth_dt = datetime.strptime(birth_date, '%Y-%m-%d')
        month = birth_dt.month
        
        # 계절 결정
        if month in [12, 1, 2]:
            season = '겨울'
        elif month in [3, 4, 5]:
            season = '봄'
        elif month in [6, 7, 8]:
            season = '여름'
        else:
            season = '가을'
        
        # 별자리 결정 (간단한 버전)
        zodiac_korean = self._get_zodiac_from_month_day(month, birth_dt.day)
        
        # 타로 카드 결정 (생일 숫자 기반)
        tarot_number = ((month + birth_dt.day) % 22) or 22
        tarot_name = self._get_tarot_name(tarot_number)
        
        # 컬러 선택 소스 결정 (시드 기반)
        source_type = seed_hash % 3  # 0: 별자리, 1: 계절, 2: 타로
        
        if source_type == 0 and zodiac_korean in self.ZODIAC_COLORS:
            # 별자리 컬러
            color = self.ZODIAC_COLORS[zodiac_korean].copy()
            color['source'] = f'{zodiac_korean}의 컬러'
        elif source_type == 1:
            # 계절 컬러
            season_palette = self.SEASON_COLORS.get(season, self.SEASON_COLORS['봄'])
            color_idx = seed_hash % len(season_palette)
            color = season_palette[color_idx].copy()
            color['source'] = f'{season} 계절의 컬러'
        else:
            # 타로 컬러
            if tarot_name in self.TAROT_COLORS:
                color = self.TAROT_COLORS[tarot_name].copy()
                color['source'] = f'{tarot_name} 카드의 컬러'
            else:
                # 기본 컬러
                color = {'name': '하늘색', 'hex': '#87CEEB', 'rgb': (135, 206, 235), 'source': '기본 컬러'}
        
        # 추가 정보
        color['date'] = date_str
        color['birth_date'] = birth_date
        color['meaning'] = self._get_color_meaning(color['name'])
        
        return color
    
    def _get_zodiac_from_month_day(self, month: int, day: int) -> str:
        """월과 일로 별자리 결정"""
        if (month == 1 and day >= 20) or (month == 2 and day < 19):
            return '물병자리'
        elif (month == 2 and day >= 19) or (month == 3 and day < 21):
            return '물고기자리'
        elif (month == 3 and day >= 21) or (month == 4 and day < 20):
            return '양자리'
        elif (month == 4 and day >= 20) or (month == 5 and day < 21):
            return '황소자리'
        elif (month == 5 and day >= 21) or (month == 6 and day < 21):
            return '쌍둥이자리'
        elif (month == 6 and day >= 21) or (month == 7 and day < 23):
            return '게자리'
        elif (month == 7 and day >= 23) or (month == 8 and day < 23):
            return '사자자리'
        elif (month == 8 and day >= 23) or (month == 9 and day < 23):
            return '처녀자리'
        elif (month == 9 and day >= 23) or (month == 10 and day < 23):
            return '천칭자리'
        elif (month == 10 and day >= 23) or (month == 11 and day < 22):
            return '전갈자리'
        elif (month == 11 and day >= 22) or (month == 12 and day < 22):
            return '사수자리'
        else:
            return '염소자리'
    
    def _get_tarot_name(self, number: int) -> str:
        """타로 카드 번호로 이름 반환"""
        tarot_names = [
            '마법사', '여교황', '여황제', '황제', '교황', '연인', '전차', '힘', '은둔자',
            '운명의 바퀴', '정의', '매달린 사람', '죽음', '절제', '악마', '탑', '별', '달',
            '태양', '심판', '세계', '바보'
        ]
        return tarot_names[number - 1] if 1 <= number <= 22 else '바보'
    
    def _get_color_meaning(self, color_name: str) -> str:
        """컬러 의미 반환"""
        meanings = {
            '빨간색': '열정과 에너지를 상징합니다. 오늘은 활기차게 보내세요.',
            '주황색': '창의성과 낙관을 나타냅니다. 새로운 아이디어가 떠오를 수 있습니다.',
            '노란색': '행복과 지혜를 의미합니다. 밝은 하루가 될 것입니다.',
            '초록색': '성장과 평화를 상징합니다. 안정적인 하루를 보낼 수 있습니다.',
            '파란색': '평온과 신뢰를 나타냅니다. 차분하게 하루를 시작하세요.',
            '보라색': '영감과 직관을 의미합니다. 내면의 목소리에 귀 기울여보세요.',
            '분홍색': '사랑과 친절함을 상징합니다. 주변 사람들과 따뜻한 하루를 보내세요.',
            '하늘색': '자유와 평화를 나타냅니다. 마음이 편안해지는 하루입니다.',
            '금색': '성공과 풍요를 의미합니다. 긍정적인 변화가 있을 수 있습니다.',
            '은색': '직관과 반성을 상징합니다. 깊이 생각해볼 시간입니다.',
            '갈색': '안정과 신뢰를 나타냅니다. 견고한 기반을 다지는 하루입니다.',
            '검은색': '신비와 변화를 의미합니다. 새로운 시작을 준비하는 시간입니다.',
            '흰색': '순수와 새로운 시작을 상징합니다. 깨끗한 마음으로 시작하세요.',
            '에메랄드': '성장과 조화를 나타냅니다. 균형 잡힌 하루가 될 것입니다.',
            '바다색': '평온과 깊이를 의미합니다. 마음의 여유를 느껴보세요.',
            '벚꽃 핑크': '사랑과 아름다움을 상징합니다. 감성적인 하루입니다.',
            '연두색': '새싹과 희망을 나타냅니다. 새로운 가능성이 열립니다.',
            '라벤더': '평화와 치유를 의미합니다. 마음을 정리하는 시간입니다.',
            '코랄': '활력과 열정을 상징합니다. 에너지 넘치는 하루입니다.',
            '버건디': '우아함과 깊이를 나타냅니다. 성숙한 하루입니다.',
            '올리브': '평화와 조화를 의미합니다. 안정적인 하루입니다.',
            '네이비': '신뢰와 안정을 상징합니다. 확고한 하루입니다.',
            '아이스 블루': '시원함과 평온을 나타냅니다. 차분한 하루입니다.',
            '핑크': '사랑과 친절함을 의미합니다. 따뜻한 하루입니다.',
            '진한 빨간색': '강렬한 열정을 상징합니다. 집중력이 높은 하루입니다.',
            '청록색': '균형과 조화를 나타냅니다. 안정적인 하루입니다.',
            '회색': '중립과 균형을 의미합니다. 객관적으로 생각해볼 시간입니다.',
        }
        return meanings.get(color_name, '오늘 하루를 긍정적으로 보내세요.')


if __name__ == '__main__':
    # 테스트
    suggester = ColorSuggester()
    color = suggester.suggest_color('1990-05-15')
    import json
    print(json.dumps(color, ensure_ascii=False, indent=2))

