# -*- coding: utf-8 -*-
"""
생년월일을 분석하여 별자리, 타로, 생일 특성 등을 제공하는 모듈
"""
from datetime import datetime
from typing import Dict, Optional
import calendar


class BirthdayAnalyzer:
    """생년월일 분석 클래스"""
    
    # 별자리 정보 (양력 기준)
    ZODIAC_SIGNS = {
        (1, 20): ('물병자리', 'Aquarius'),
        (2, 19): ('물고기자리', 'Pisces'),
        (3, 21): ('양자리', 'Aries'),
        (4, 20): ('황소자리', 'Taurus'),
        (5, 21): ('쌍둥이자리', 'Gemini'),
        (6, 21): ('게자리', 'Cancer'),
        (7, 23): ('사자자리', 'Leo'),
        (8, 23): ('처녀자리', 'Virgo'),
        (9, 23): ('천칭자리', 'Libra'),
        (10, 23): ('전갈자리', 'Scorpio'),
        (11, 22): ('사수자리', 'Sagittarius'),
        (12, 22): ('염소자리', 'Capricorn'),
    }
    
    # 타로 카드 (생일 숫자 기반)
    TAROT_CARDS = {
        1: ('마법사', 'The Magician', '새로운 시작, 의지력, 창조력'),
        2: ('여교황', 'The High Priestess', '직관, 내면의 지혜, 신비'),
        3: ('여황제', 'The Empress', '풍요, 창조성, 자연'),
        4: ('황제', 'The Emperor', '권위, 안정, 구조'),
        5: ('교황', 'The Hierophant', '전통, 가르침, 영성'),
        6: ('연인', 'The Lovers', '사랑, 선택, 조화'),
        7: ('전차', 'The Chariot', '의지, 승리, 통제'),
        8: ('힘', 'Strength', '인내, 용기, 내적 힘'),
        9: ('은둔자', 'The Hermit', '성찰, 지혜, 내적 탐구'),
        10: ('운명의 바퀴', 'Wheel of Fortune', '변화, 운명, 순환'),
        11: ('정의', 'Justice', '공정, 균형, 책임'),
        12: ('매달린 사람', 'The Hanged Man', '희생, 새로운 관점, 인내'),
        13: ('죽음', 'Death', '변화, 종료, 재생'),
        14: ('절제', 'Temperance', '균형, 조화, 인내'),
        15: ('악마', 'The Devil', '유혹, 속박, 해방'),
        16: ('탑', 'The Tower', '변화, 붕괴, 각성'),
        17: ('별', 'The Star', '희망, 영감, 치유'),
        18: ('달', 'The Moon', '직관, 환상, 잠재의식'),
        19: ('태양', 'The Sun', '기쁨, 성공, 활력'),
        20: ('심판', 'Judgement', '재생, 용서, 각성'),
        21: ('세계', 'The World', '완성, 성취, 여행'),
        22: ('바보', 'The Fool', '새로운 시작, 순수, 모험'),
    }
    
    def __init__(self, birth_date: str):
        """
        Args:
            birth_date: 'YYYY-MM-DD' 형식의 생년월일
        """
        try:
            self.birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("생년월일은 'YYYY-MM-DD' 형식이어야 합니다.")
        
        self.year = self.birth_date.year
        self.month = self.birth_date.month
        self.day = self.birth_date.day
    
    def get_zodiac_sign(self) -> Dict[str, str]:
        """별자리 정보 반환"""
        month_day = (self.month, self.day)
        
        # 별자리 경계일 처리
        for (m, d), (korean, english) in self.ZODIAC_SIGNS.items():
            if month_day < (m, d):
                # 이전 별자리 반환
                prev_month = m - 1 if m > 1 else 12
                prev_day = 31 if prev_month == 12 else calendar.monthrange(self.year, prev_month)[1]
                for (pm, pd), (pk, pe) in self.ZODIAC_SIGNS.items():
                    if (prev_month, prev_day) >= (pm, pd):
                        return {
                            'korean': pk,
                            'english': pe,
                            'month': prev_month,
                            'day': prev_day
                        }
        
        # 12월 말 ~ 1월 초 처리 (염소자리)
        if self.month == 12 and self.day >= 22:
            return {
                'korean': '염소자리',
                'english': 'Capricorn',
                'month': 12,
                'day': 22
            }
        elif self.month == 1 and self.day < 20:
            return {
                'korean': '염소자리',
                'english': 'Capricorn',
                'month': 12,
                'day': 22
            }
        
        # 기본값 (물병자리)
        return {
            'korean': '물병자리',
            'english': 'Aquarius',
            'month': 1,
            'day': 20
        }
    
    def get_tarot_card(self) -> Dict[str, str]:
        """생일 숫자 기반 타로 카드 반환"""
        # 생일 숫자를 1-22 범위로 변환
        birth_number = ((self.month + self.day) % 22) or 22
        
        korean, english, meaning = self.TAROT_CARDS.get(
            birth_number,
            ('바보', 'The Fool', '새로운 시작, 순수, 모험')
        )
        
        return {
            'korean': korean,
            'english': english,
            'meaning': meaning,
            'birth_number': birth_number
        }
    
    def get_birthday_characteristics(self) -> Dict:
        """생일 특성 분석"""
        # 요일
        weekday = calendar.day_name[self.birth_date.weekday()]
        weekday_korean = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일'][
            self.birth_date.weekday()
        ]
        
        # 계절
        if self.month in [12, 1, 2]:
            season = '겨울'
        elif self.month in [3, 4, 5]:
            season = '봄'
        elif self.month in [6, 7, 8]:
            season = '여름'
        else:
            season = '가을'
        
        # 생일 숫자 합
        birth_sum = sum(int(d) for d in f"{self.year}{self.month:02d}{self.day:02d}")
        life_path_number = birth_sum
        while life_path_number > 9 and life_path_number not in [11, 22, 33]:
            life_path_number = sum(int(d) for d in str(life_path_number))
        
        return {
            'weekday': weekday,
            'weekday_korean': weekday_korean,
            'season': season,
            'life_path_number': life_path_number,
            'birth_sum': birth_sum
        }
    
    def analyze(self) -> Dict:
        """전체 분석 결과 반환"""
        zodiac = self.get_zodiac_sign()
        tarot = self.get_tarot_card()
        characteristics = self.get_birthday_characteristics()
        
        return {
            'birth_date': self.birth_date.strftime('%Y-%m-%d'),
            'age': (datetime.now() - self.birth_date).days // 365,
            'zodiac': zodiac,
            'tarot': tarot,
            'characteristics': characteristics
        }


if __name__ == '__main__':
    # 테스트
    analyzer = BirthdayAnalyzer('1990-05-15')
    result = analyzer.analyze()
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))

