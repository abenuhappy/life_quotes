# -*- coding: utf-8 -*-
import hashlib
from datetime import datetime
import pytz
from typing import Dict, Optional

KST = pytz.timezone('Asia/Seoul')

def get_kst_now():
    return datetime.now(KST)

class GreetingSuggester:
    """오늘의 인사말 제안 클래스"""
    
    # 카테고리별 인사말 데이터
    GREETINGS = {
        '반가움': [
            {
                'language': '한국어',
                'text': '안녕하세요',
                'pronunciation': None,
                'meaning': '처음 만나거나 만날 때 하는 인사말'
            },
            {
                'language': '영어',
                'text': 'Hello',
                'pronunciation': '헬로',
                'meaning': '안녕하세요'
            },
            {
                'language': '일본어',
                'text': 'こんにちは',
                'pronunciation': '곤니치와',
                'meaning': '안녕하세요'
            },
            {
                'language': '중국어',
                'text': '你好',
                'pronunciation': '니하오',
                'meaning': '안녕하세요'
            },
            {
                'language': '스페인어',
                'text': 'Hola',
                'pronunciation': '올라',
                'meaning': '안녕하세요'
            },
            {
                'language': '프랑스어',
                'text': 'Bonjour',
                'pronunciation': '봉주르',
                'meaning': '안녕하세요'
            },
            {
                'language': '독일어',
                'text': 'Guten Tag',
                'pronunciation': '구텐 타크',
                'meaning': '안녕하세요'
            },
            {
                'language': '이탈리아어',
                'text': 'Ciao',
                'pronunciation': '차오',
                'meaning': '안녕하세요'
            },
            {
                'language': '러시아어',
                'text': 'Привет',
                'pronunciation': '프리뱃',
                'meaning': '안녕하세요'
            },
            {
                'language': '아랍어',
                'text': 'مرحبا',
                'pronunciation': '마르하바',
                'meaning': '안녕하세요'
            },
        ],
        '고마움': [
            {
                'language': '한국어',
                'text': '감사합니다',
                'pronunciation': None,
                'meaning': '고마움을 표현하는 말'
            },
            {
                'language': '영어',
                'text': 'Thank you',
                'pronunciation': '땡큐',
                'meaning': '감사합니다'
            },
            {
                'language': '일본어',
                'text': 'ありがとう',
                'pronunciation': '아리가또',
                'meaning': '감사합니다'
            },
            {
                'language': '중국어',
                'text': '谢谢',
                'pronunciation': '셰셰',
                'meaning': '감사합니다'
            },
            {
                'language': '스페인어',
                'text': 'Gracias',
                'pronunciation': '그라시아스',
                'meaning': '감사합니다'
            },
            {
                'language': '프랑스어',
                'text': 'Merci',
                'pronunciation': '메르시',
                'meaning': '감사합니다'
            },
            {
                'language': '독일어',
                'text': 'Danke',
                'pronunciation': '단케',
                'meaning': '감사합니다'
            },
            {
                'language': '이탈리아어',
                'text': 'Grazie',
                'pronunciation': '그라치에',
                'meaning': '감사합니다'
            },
            {
                'language': '러시아어',
                'text': 'Спасибо',
                'pronunciation': '스파시바',
                'meaning': '감사합니다'
            },
            {
                'language': '아랍어',
                'text': 'شكرا',
                'pronunciation': '슈크란',
                'meaning': '감사합니다'
            },
        ],
        '위로': [
            {
                'language': '한국어',
                'text': '힘내세요',
                'pronunciation': None,
                'meaning': '어려운 상황에서 용기를 북돋아주는 말'
            },
            {
                'language': '영어',
                'text': 'Hang in there',
                'pronunciation': '행 인 데어',
                'meaning': '힘내세요'
            },
            {
                'language': '일본어',
                'text': '頑張って',
                'pronunciation': '간밧떼',
                'meaning': '힘내세요'
            },
            {
                'language': '중국어',
                'text': '加油',
                'pronunciation': '지아요우',
                'meaning': '힘내세요'
            },
            {
                'language': '스페인어',
                'text': 'Ánimo',
                'pronunciation': '아니모',
                'meaning': '힘내세요'
            },
            {
                'language': '프랑스어',
                'text': 'Courage',
                'pronunciation': '쿠라주',
                'meaning': '용기를 내세요'
            },
            {
                'language': '독일어',
                'text': 'Kopf hoch',
                'pronunciation': '코프 호흐',
                'meaning': '고개를 들어, 힘내세요'
            },
            {
                'language': '이탈리아어',
                'text': 'Coraggio',
                'pronunciation': '코라지오',
                'meaning': '용기를 내세요'
            },
            {
                'language': '러시아어',
                'text': 'Держись',
                'pronunciation': '데르지스',
                'meaning': '버티세요'
            },
            {
                'language': '아랍어',
                'text': 'قوة',
                'pronunciation': '쿠와',
                'meaning': '힘내세요'
            },
        ],
        '첫만남': [
            {
                'language': '한국어',
                'text': '처음 뵙겠습니다',
                'pronunciation': None,
                'meaning': '처음 만날 때 하는 정중한 인사말'
            },
            {
                'language': '영어',
                'text': 'Nice to meet you',
                'pronunciation': '나이스 투 밋 유',
                'meaning': '만나서 반갑습니다'
            },
            {
                'language': '일본어',
                'text': 'はじめまして',
                'pronunciation': '하지메마시떼',
                'meaning': '처음 뵙겠습니다'
            },
            {
                'language': '중국어',
                'text': '很高兴认识你',
                'pronunciation': '헨 가오싱 런스 니',
                'meaning': '만나서 반갑습니다'
            },
            {
                'language': '스페인어',
                'text': 'Mucho gusto',
                'pronunciation': '무초 구스토',
                'meaning': '만나서 반갑습니다'
            },
            {
                'language': '프랑스어',
                'text': 'Enchanté',
                'pronunciation': '앙샹떼',
                'meaning': '만나서 반갑습니다'
            },
            {
                'language': '독일어',
                'text': 'Freut mich',
                'pronunciation': '프로이트 미히',
                'meaning': '만나서 반갑습니다'
            },
            {
                'language': '이탈리아어',
                'text': 'Piacere',
                'pronunciation': '피아체레',
                'meaning': '만나서 반갑습니다'
            },
            {
                'language': '러시아어',
                'text': 'Очень приятно',
                'pronunciation': '오첸 프리야트노',
                'meaning': '만나서 반갑습니다'
            },
            {
                'language': '아랍어',
                'text': 'تشرفنا',
                'pronunciation': '타샤라프나',
                'meaning': '만나서 반갑습니다'
            },
        ],
        '사랑': [
            {
                'language': '한국어',
                'text': '사랑해요',
                'pronunciation': None,
                'meaning': '사랑을 표현하는 말'
            },
            {
                'language': '영어',
                'text': 'I love you',
                'pronunciation': '아이 러브 유',
                'meaning': '사랑해요'
            },
            {
                'language': '일본어',
                'text': '愛してる',
                'pronunciation': '아이시떼루',
                'meaning': '사랑해요'
            },
            {
                'language': '중국어',
                'text': '我爱你',
                'pronunciation': '워 아이 니',
                'meaning': '사랑해요'
            },
            {
                'language': '스페인어',
                'text': 'Te amo',
                'pronunciation': '떼 아모',
                'meaning': '사랑해요'
            },
            {
                'language': '프랑스어',
                'text': 'Je t\'aime',
                'pronunciation': '주 땀',
                'meaning': '사랑해요'
            },
            {
                'language': '독일어',
                'text': 'Ich liebe dich',
                'pronunciation': '이히 리베 디히',
                'meaning': '사랑해요'
            },
            {
                'language': '이탈리아어',
                'text': 'Ti amo',
                'pronunciation': '티 아모',
                'meaning': '사랑해요'
            },
            {
                'language': '러시아어',
                'text': 'Я тебя люблю',
                'pronunciation': '야 떼뱌 류블류',
                'meaning': '사랑해요'
            },
            {
                'language': '아랍어',
                'text': 'أحبك',
                'pronunciation': '우헵빅',
                'meaning': '사랑해요'
            },
        ],
        '칭찬': [
            {
                'language': '한국어',
                'text': '잘하셨어요',
                'pronunciation': None,
                'meaning': '칭찬과 격려의 말'
            },
            {
                'language': '영어',
                'text': 'Well done',
                'pronunciation': '웰 던',
                'meaning': '잘했어요'
            },
            {
                'language': '일본어',
                'text': 'よくできました',
                'pronunciation': '요쿠데키마시타',
                'meaning': '잘했어요'
            },
            {
                'language': '중국어',
                'text': '做得好',
                'pronunciation': '주오 더 하오',
                'meaning': '잘했어요'
            },
            {
                'language': '스페인어',
                'text': 'Bien hecho',
                'pronunciation': '비엔 에초',
                'meaning': '잘했어요'
            },
            {
                'language': '프랑스어',
                'text': 'Bravo',
                'pronunciation': '브라보',
                'meaning': '훌륭해요'
            },
            {
                'language': '독일어',
                'text': 'Gut gemacht',
                'pronunciation': '구트 게마흐트',
                'meaning': '잘했어요'
            },
            {
                'language': '이탈리아어',
                'text': 'Ben fatto',
                'pronunciation': '벤 파토',
                'meaning': '잘했어요'
            },
            {
                'language': '러시아어',
                'text': 'Молодец',
                'pronunciation': '몰로데츠',
                'meaning': '훌륭해요'
            },
            {
                'language': '아랍어',
                'text': 'ممتاز',
                'pronunciation': '맘타즈',
                'meaning': '훌륭해요'
            },
        ],
        '용기': [
            {
                'language': '한국어',
                'text': '당신은 할 수 있어요',
                'pronunciation': None,
                'meaning': '용기를 북돋아주는 말'
            },
            {
                'language': '영어',
                'text': 'You can do it',
                'pronunciation': '유 캔 두 잇',
                'meaning': '당신은 할 수 있어요'
            },
            {
                'language': '일본어',
                'text': 'あなたならできる',
                'pronunciation': '아나타나라 데키루',
                'meaning': '당신이라면 할 수 있어요'
            },
            {
                'language': '중국어',
                'text': '你可以的',
                'pronunciation': '니 케이 이 더',
                'meaning': '당신은 할 수 있어요'
            },
            {
                'language': '스페인어',
                'text': 'Tú puedes',
                'pronunciation': '투 푸에데스',
                'meaning': '당신은 할 수 있어요'
            },
            {
                'language': '프랑스어',
                'text': 'Tu peux le faire',
                'pronunciation': '튜 푸 르 페르',
                'meaning': '당신은 할 수 있어요'
            },
            {
                'language': '독일어',
                'text': 'Du schaffst das',
                'pronunciation': '두 샤프스트 다스',
                'meaning': '당신은 할 수 있어요'
            },
            {
                'language': '이탈리아어',
                'text': 'Ce la puoi fare',
                'pronunciation': '체 라 푸오이 파레',
                'meaning': '당신은 할 수 있어요'
            },
            {
                'language': '러시아어',
                'text': 'Ты можешь',
                'pronunciation': '티 모제시',
                'meaning': '당신은 할 수 있어요'
            },
            {
                'language': '아랍어',
                'text': 'يمكنك ذلك',
                'pronunciation': '유민쿠 달리크',
                'meaning': '당신은 할 수 있어요'
            },
        ],
    }
    
    def __init__(self):
        pass
    
    def suggest_greeting(self, birth_date: str, date_str: Optional[str] = None) -> Dict:
        """
        생년월일과 날짜 기반으로 오늘의 인사말 제안
        
        Args:
            birth_date: 생년월일 (YYYY-MM-DD)
            date_str: 날짜 (YYYY-MM-DD), None이면 오늘
        
        Returns:
            인사말 정보 딕셔너리
        """
        if date_str is None:
            date_str = get_kst_now().strftime('%Y-%m-%d')
        
        # 날짜와 생년월일을 조합하여 시드 생성
        seed_str = f"{date_str}_{birth_date}_greeting"
        seed_hash = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
        
        # 카테고리 선택 (생년월일의 일자 기반)
        birth_dt = datetime.strptime(birth_date, '%Y-%m-%d')
        day = birth_dt.day
        categories = list(self.GREETINGS.keys())
        category_index = (day + seed_hash) % len(categories)
        category = categories[category_index]
        
        # 해당 카테고리의 인사말 중 하나 선택
        greetings_in_category = self.GREETINGS[category]
        greeting_index = seed_hash % len(greetings_in_category)
        greeting = greetings_in_category[greeting_index].copy()
        
        # 추가 정보
        greeting['category'] = category
        greeting['date'] = date_str
        greeting['birth_date'] = birth_date
        
        return greeting

