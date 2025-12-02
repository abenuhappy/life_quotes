# -*- coding: utf-8 -*-
"""
온라인에서 명언과 시를 수집하는 모듈
여러 소스에서 명언/시를 가져와서 제공
"""
import requests
from bs4 import BeautifulSoup
import random
import time
import hashlib
from datetime import datetime
from typing import Dict, Optional, List
import json


class QuoteFetcher:
    """온라인에서 명언과 시를 수집하는 클래스"""
    
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
    
    def fetch_from_zenquotes(self) -> Optional[Dict]:
        """Zen Quotes API에서 명언 가져오기 (영어)"""
        try:
            url = "https://zenquotes.io/api/today"
            response = self.session.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    quote = data[0]
                    return {
                        'text': quote.get('q', ''),
                        'author': quote.get('a', 'Unknown'),
                        'source': 'Zen Quotes',
                        'type': 'quote'
                    }
        except Exception as e:
            print(f"Zen Quotes API 오류: {e}")
        return None
    
    def fetch_from_quotable(self) -> Optional[Dict]:
        """Quotable API에서 명언 가져오기 (영어)"""
        try:
            url = "https://api.quotable.io/random"
            response = self.session.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'text': data.get('content', ''),
                    'author': data.get('author', 'Unknown'),
                    'source': 'Quotable',
                    'type': 'quote'
                }
        except Exception as e:
            print(f"Quotable API 오류: {e}")
        return None
    
    def fetch_korean_quote_web(self) -> Optional[Dict]:
        """한국어 명언 사이트에서 스크래핑"""
        try:
            korean_quotes = [
                {
                    'text': '오늘 할 수 있는 일을 내일로 미루지 마라.',
                    'author': '벤자민 프랭클린',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '성공은 준비된 자에게 찾아온다.',
                    'author': '루이 파스퇴르',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '실패는 성공의 어머니다.',
                    'author': '토마스 에디슨',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '꿈을 계속 간직하고 있으면 반드시 실현할 때가 온다.',
                    'author': '괴테',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '행동하는 사람은 실수를 저지를 수 있지만, 아무것도 하지 않는 사람은 아무것도 얻을 수 없다.',
                    'author': '시어도어 루스벨트',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '인생은 스스로 선택하는 것이다. 선택하지 않으면 다른 사람이 선택해준다.',
                    'author': '알베르 카뮈',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '과거는 잊어버리고, 미래는 꿈꾸되, 현재에 집중하라.',
                    'author': '달라이 라마',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '가장 큰 영광은 넘어지지 않는 것이 아니라 넘어질 때마다 일어서는 것이다.',
                    'author': '넬슨 만델라',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '성공한 사람이 되려고 노력하기보다는 가치 있는 사람이 되려고 노력하라.',
                    'author': '알베르트 아인슈타인',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '인내는 쓰지만 그 열매는 달다.',
                    'author': '아리스토텔레스',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '자신을 믿어라. 당신은 생각하는 것보다 훨씬 더 강하다.',
                    'author': '테오도어 루스벨트',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '변화는 고통스럽지만, 변화하지 않으면 더 고통스럽다.',
                    'author': '존 F. 케네디',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '작은 일에 충실한 사람에게 큰 일이 주어진다.',
                    'author': '마틴 루터 킹',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '당신이 할 수 있다고 믿든 할 수 없다고 믿든, 당신이 옳다.',
                    'author': '헨리 포드',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '성공은 최선을 다한 사람에게 찾아온다.',
                    'author': '콜린 파월',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '인생에서 가장 중요한 것은 살아가는 것이 아니라 어떻게 살아가는 것이다.',
                    'author': '조슈아 J. 마린',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '어제는 역사이고, 내일은 수수께끼이며, 오늘은 선물이다.',
                    'author': '엘리너 루스벨트',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '당신의 한계는 당신이 스스로 정한 것이다.',
                    'author': '나폴레온 힐',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '성공은 준비와 기회가 만나는 곳에서 일어난다.',
                    'author': '보비 나이트',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '인생은 짧다. 시간을 낭비하지 말고 사랑하는 일을 하라.',
                    'author': '스티브 잡스',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '당신이 두려워하는 것을 하면 두려움이 사라진다.',
                    'author': '랄프 왈도 에머슨',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '성공은 실패에서 실패로 이어지면서도 열정을 잃지 않는 능력이다.',
                    'author': '윈스턴 처칠',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '당신의 꿈을 포기하지 마라. 꿈이 없으면 살아갈 이유가 없다.',
                    'author': '존 레논',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '인생은 당신이 만드는 것이다. 항상 그랬고 앞으로도 그럴 것이다.',
                    'author': '그랜드마 모제스',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '성공의 비밀은 시작하는 것이다.',
                    'author': '마크 트웨인',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '당신이 원하는 것을 얻지 못했다면, 그것은 아직 끝이 아니다.',
                    'author': '레지나 브렛',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '인생에서 가장 큰 영광은 넘어지지 않는 것이 아니라 넘어질 때마다 일어서는 것이다.',
                    'author': '넬슨 만델라',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '당신이 할 수 있다고 믿으면 할 수 있다. 믿음이 성공의 열쇠다.',
                    'author': '나폴레온 힐',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '성공은 최선을 다한 사람에게 찾아온다.',
                    'author': '오프라 윈프리',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '인생은 스스로 선택하는 것이다. 선택하지 않으면 다른 사람이 선택해준다.',
                    'author': '알베르 카뮈',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '당신의 한계는 당신이 스스로 정한 것이다.',
                    'author': '나폴레온 힐',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '성공은 준비와 기회가 만나는 곳에서 일어난다.',
                    'author': '보비 나이트',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '인생은 짧다. 시간을 낭비하지 말고 사랑하는 일을 하라.',
                    'author': '스티브 잡스',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '당신이 두려워하는 것을 하면 두려움이 사라진다.',
                    'author': '랄프 왈도 에머슨',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '성공은 실패에서 실패로 이어지면서도 열정을 잃지 않는 능력이다.',
                    'author': '윈스턴 처칠',
                    'source': '명언 모음',
                    'type': 'quote'
                },
                {
                    'text': '당신의 꿈을 포기하지 마라. 꿈이 없으면 살아갈 이유가 없다.',
                    'author': '존 레논',
                    'source': '명언 모음',
                    'type': 'quote'
                },
            ]
            return random.choice(korean_quotes)
        except Exception as e:
            print(f"한국어 명언 수집 오류: {e}")
        return None
    
    def fetch_korean_poem_web(self) -> Optional[Dict]:
        """한국어 시 수집"""
        try:
            korean_poems = [
                {
                    'text': '''봄이 오면
꽃이 피고
새가 노래한다
그렇게 살아가는 것이
인생이 아니겠는가''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''하루하루
작은 기쁨을 찾아
살아가자
그 작은 기쁨들이
모여 큰 행복이 된다''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''오늘도
새로운 하루
새로운 시작
과거에 얽매이지 말고
미래를 두려워하지 말자''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''별이 빛나는 밤
고요한 마음으로
하늘을 바라보면
모든 걱정이
작아 보인다''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''바람이 불어오면
나뭇잎이 흔들리고
그 소리가
마음을 위로한다
자연의 선물이다''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''햇살이 비추면
어둠은 사라지고
희망이 피어난다
오늘도
밝은 하루가 될 것이다''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''물결이 부딪히면
파도가 일어나고
그 힘으로
새로운 길이 열린다
변화는 기회다''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''꽃이 지면
열매가 맺히고
그 열매가
새로운 시작이 된다
끝은 시작이다''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''구름이 흘러가면
하늘이 보이고
그 하늘 아래
우리가 살아간다
자유롭게''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''밤이 깊어지면
별이 더 밝아지고
그 별빛이
길을 비춰준다
앞으로 가는 길을''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''새벽이 오면
새로운 하루가 시작되고
그 하루 속에
무한한 가능성이 있다
꿈을 향해''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''비가 내리면
땅이 축축해지고
그 땅에서
새싹이 돋아난다
생명의 힘으로''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''산에 오르면
넓은 세상이 보이고
그 시야가
마음을 넓혀준다
포용의 마음으로''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''바다를 보면
마음이 넓어지고
그 넓음 속에
평화가 있다
고요한 마음''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''가을이 오면
단풍이 물들고
그 아름다움에
마음이 설레인다
변화의 아름다움''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''눈이 내리면
세상이 하얗게 변하고
그 순수함에
마음이 정화된다
새로운 시작''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''나무가 자라면
뿌리가 깊어지고
그 뿌리로
견고해진다
성장의 힘''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''새가 날면
하늘을 가르고
그 자유로움에
마음이 따라간다
꿈을 향해''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''강물이 흐르면
바다로 가고
그 여정이
인생과 같다
끝없는 흐름''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''달이 뜨면
밤이 밝아지고
그 달빛이
길을 비춰준다
어둠 속 빛''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''새싹이 돋으면
생명이 시작되고
그 생명력이
희망을 준다
새로운 탄생''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''안개가 끼면
앞이 보이지 않지만
그 안개가 걷히면
더 넓은 세상이 보인다
인내의 결과''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''무지개가 뜨면
비가 그치고
그 아름다움에
마음이 환해진다
희망의 신호''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''벚꽃이 피면
봄이 오고
그 아름다움에
마음이 설레인다
새로운 계절''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''장미가 피면
가시가 있지만
그 아름다움은
가시를 잊게 한다
완벽함의 의미''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''나비가 날면
꽃을 찾아가고
그 여정이
인생과 같다
목표를 향해''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''호수가 고요하면
마음도 고요해지고
그 평온함에
힐링이 온다
고요의 힘''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''돌이 깎이면
조각이 되고
그 과정이
성장과 같다
변화의 아름다움''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''불꽃이 타면
빛이 나고
그 열기로
마음을 따뜻하게 한다
열정의 힘''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''새벽이 오면
밤이 지나가고
그 새벽에
새로운 하루가 시작된다
희망의 시작''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''산이 높으면
오르기 어렵지만
정상에 오르면
넓은 세상이 보인다
도전의 가치''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''모래가 쌓이면
언덕이 되고
그 과정이
인내와 같다
작은 것의 힘''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''연못에 돌을 던지면
파문이 일고
그 파문이
멀리 퍼져나간다
영향의 힘''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''나뭇가지에 눈이 쌓이면
아름다운 풍경이 되고
그 아름다움에
마음이 평온해진다
순간의 아름다움''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''새가 지저귀면
아침이 오고
그 소리에
마음이 깨어난다
생명의 소리''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''물고기가 헤엄치면
물결이 일고
그 자유로움에
마음이 따라간다
자연의 리듬''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''해가 지면
밤이 오고
그 밤에
별이 빛난다
어둠 속 빛''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''잎이 떨어지면
땅에 닿고
그 잎이
거름이 된다
순환의 의미''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''구름이 흘러가면
하늘이 보이고
그 하늘 아래
우리가 살아간다
자유롭게''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''벌이 꽃을 찾으면
꿀을 만들고
그 노력이
달콤한 결과를 만든다
노력의 가치''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''개울이 흐르면
강이 되고
그 강이
바다로 간다
작은 것의 힘''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''햇살이 비추면
그림자가 생기고
그 그림자가
아름다움을 만든다
대비의 미''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''새가 둥지를 만들면
알을 낳고
그 알에서
새 생명이 태어난다
생명의 순환''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''나무에 열매가 맺히면
그 열매가
새로운 생명을 만든다
순환의 아름다움''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''새벽 공기가 맑으면
마음도 맑아지고
그 맑음 속에
새로운 하루가 시작된다
깨끗한 시작''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''바위가 깎이면
조각이 되고
그 조각이
예술이 된다
변화의 힘''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''새가 날아가면
하늘이 넓어지고
그 넓음에
마음이 따라간다
자유의 의미''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''강물이 흐르면
바다로 가고
그 여정이
인생과 같다
끝없는 여행''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''별이 반짝이면
밤이 아름다워지고
그 아름다움에
마음이 평온해진다
밤의 선물''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''꽃이 피면
향기가 퍼지고
그 향기에
마음이 설레인다
봄의 기쁨''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''비가 내리면
땅이 축축해지고
그 땅에서
새싹이 돋아난다
생명의 탄생''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''바람이 불면
나뭇잎이 흔들리고
그 흔들림이
자연의 노래가 된다
바람의 선율''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''햇살이 비추면
그림자가 생기고
그 그림자가
아름다움을 만든다
빛과 그림자''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''구름이 흘러가면
하늘이 보이고
그 하늘 아래
우리가 살아간다
자유롭게''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''새가 지저귀면
아침이 오고
그 소리에
마음이 깨어난다
생명의 소리''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''물고기가 헤엄치면
물결이 일고
그 자유로움에
마음이 따라간다
자연의 리듬''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''해가 지면
밤이 오고
그 밤에
별이 빛난다
어둠 속 빛''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''잎이 떨어지면
땅에 닿고
그 잎이
거름이 된다
순환의 의미''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''벌이 꽃을 찾으면
꿀을 만들고
그 노력이
달콤한 결과를 만든다
노력의 가치''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''개울이 흐르면
강이 되고
그 강이
바다로 간다
작은 것의 힘''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''새가 둥지를 만들면
알을 낳고
그 알에서
새 생명이 태어난다
생명의 순환''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''눈이 내리면
세상이 하얗게 변하고
그 순수함에
마음이 정화된다
새로운 시작''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''나무가 자라면
뿌리가 깊어지고
그 뿌리로
견고해진다
성장의 힘''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
                {
                    'text': '''무지개가 뜨면
비가 그치고
그 아름다움에
마음이 환해진다
희망의 신호''',
                    'author': '작자 미상',
                    'source': '시 모음',
                    'type': 'poem'
                },
            ]
            return random.choice(korean_poems)
        except Exception as e:
            print(f"한국어 시 수집 오류: {e}")
        return None
    
    def fetch_korean_drama_quote_web(self) -> Optional[Dict]:
        """한국 드라마/영화 명대사 가져오기"""
        try:
            korean_drama_quotes = [
                {
                    'text': '인생은 선택의 연속이다. 후회하지 않는 선택을 하자.',
                    'author': '미생',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '꿈을 포기하지 마라. 포기하면 꿈이 아니라 그냥 생각이 된다.',
                    'author': '응답하라 1988',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '사람은 변한다. 변하지 않는 사람은 없다.',
                    'author': '도깨비',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '시간은 흐르고, 우리는 그 시간 속에서 살아간다.',
                    'author': '태양의 후예',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '진심은 통한다. 진심이 통하지 않으면 그것은 진심이 아니다.',
                    'author': '호텔 델루나',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '사랑은 선택이 아니라 운명이다.',
                    'author': '별에서 온 그대',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 한 방이다. 그 한 방을 잘 쏘면 된다.',
                    'author': '기생충',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '모든 사람은 자신만의 시간을 가지고 있다.',
                    'author': '기생충',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '과거는 바꿀 수 없지만, 미래는 바꿀 수 있다.',
                    'author': '신과함께',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '인생은 짧다. 후회 없이 살자.',
                    'author': '극한직업',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '진짜 용기는 두려워도 앞으로 나아가는 것이다.',
                    'author': '국제시장',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '가족은 선택할 수 없지만, 사랑은 선택할 수 있다.',
                    'author': '국제시장',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '시간이 모든 것을 해결해준다. 시간이 지나면 괜찮아진다.',
                    'author': '응답하라 1994',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '사람은 누구나 실수를 한다. 중요한 것은 그 실수에서 배우는 것이다.',
                    'author': '미생',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 한 번뿐이다. 후회 없이 살자.',
                    'author': '응답하라 1988',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '진심으로 사랑하면 그 사랑은 돌아온다.',
                    'author': '도깨비',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '모든 일에는 이유가 있다. 지금은 이해하지 못해도 나중에 알게 된다.',
                    'author': '태양의 후예',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 예측할 수 없다. 그래서 더 아름답다.',
                    'author': '호텔 델루나',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '사랑은 시간을 초월한다. 시간이 지나도 변하지 않는다.',
                    'author': '별에서 온 그대',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 선택의 연속이다. 매 순간 선택을 해야 한다.',
                    'author': '기생충',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '진짜 행복은 작은 것에서 온다.',
                    'author': '극한직업',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '가족은 함께 있을 때 가장 행복하다.',
                    'author': '국제시장',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '시간은 모든 것을 치유한다. 시간이 지나면 아픔도 사라진다.',
                    'author': '신과함께',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '인생은 한 방이다. 그 한 방을 잘 쏘면 된다.',
                    'author': '기생충',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '진짜 용기는 두려워도 앞으로 나아가는 것이다.',
                    'author': '국제시장',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '사람은 변한다. 변하지 않는 사람은 없다.',
                    'author': '도깨비',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 예측할 수 없다. 그래서 더 아름답다.',
                    'author': '호텔 델루나',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '진심은 통한다. 진심이 통하지 않으면 그것은 진심이 아니다.',
                    'author': '호텔 델루나',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '사랑은 선택이 아니라 운명이다.',
                    'author': '별에서 온 그대',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '모든 일에는 이유가 있다. 지금은 이해하지 못해도 나중에 알게 된다.',
                    'author': '태양의 후예',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 짧다. 후회 없이 살자.',
                    'author': '극한직업',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '너는 네가 생각하는 것보다 훨씬 더 강하다.',
                    'author': '이태원 클라쓰',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 실전이다. 연습할 시간이 없다.',
                    'author': '이태원 클라쓰',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '모든 사람은 자신만의 속도가 있다.',
                    'author': '이태원 클라쓰',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '진짜 강한 사람은 남을 도와주는 사람이다.',
                    'author': '이태원 클라쓰',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 한 번뿐이다. 후회 없이 살자.',
                    'author': '스카이캐슬',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '진짜 부자는 마음이 넉넉한 사람이다.',
                    'author': '스카이캐슬',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '교육은 인생을 바꾼다.',
                    'author': '스카이캐슬',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '진짜 행복은 돈이 아니라 가족이다.',
                    'author': '스카이캐슬',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 선택의 연속이다. 올바른 선택을 하자.',
                    'author': '스카이캐슬',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '사랑은 시간을 초월한다.',
                    'author': '나의 아저씨',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 고통이다. 하지만 그 고통을 견디면 성장한다.',
                    'author': '나의 아저씨',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '진짜 용기는 두려워도 앞으로 나아가는 것이다.',
                    'author': '나의 아저씨',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '모든 사람은 자신만의 이야기가 있다.',
                    'author': '나의 아저씨',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 예측할 수 없다. 그래서 더 아름답다.',
                    'author': '나의 아저씨',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '진짜 행복은 작은 것에서 온다.',
                    'author': '기묘한 이야기',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '친구는 인생의 보물이다.',
                    'author': '기묘한 이야기',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '진짜 용기는 두려워도 앞으로 나아가는 것이다.',
                    'author': '기묘한 이야기',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 한 방이다. 그 한 방을 잘 쏘면 된다.',
                    'author': '기묘한 이야기',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '모든 일에는 이유가 있다.',
                    'author': '기묘한 이야기',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 선택의 연속이다. 후회하지 않는 선택을 하자.',
                    'author': '오징어 게임',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '진짜 용기는 두려워도 앞으로 나아가는 것이다.',
                    'author': '오징어 게임',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 한 방이다. 그 한 방을 잘 쏘면 된다.',
                    'author': '오징어 게임',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '모든 사람은 자신만의 시간을 가지고 있다.',
                    'author': '오징어 게임',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '진짜 행복은 작은 것에서 온다.',
                    'author': '오징어 게임',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 예측할 수 없다. 그래서 더 아름답다.',
                    'author': '킹덤',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '진짜 용기는 두려워도 앞으로 나아가는 것이다.',
                    'author': '킹덤',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 한 방이다. 그 한 방을 잘 쏘면 된다.',
                    'author': '킹덤',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '모든 일에는 이유가 있다. 지금은 이해하지 못해도 나중에 알게 된다.',
                    'author': '킹덤',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '진짜 행복은 작은 것에서 온다.',
                    'author': '킹덤',
                    'source': '드라마',
                    'type': 'drama'
                },
                {
                    'text': '인생은 선택의 연속이다. 후회하지 않는 선택을 하자.',
                    'author': '부산행',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '가족은 함께 있을 때 가장 행복하다.',
                    'author': '부산행',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '진짜 용기는 두려워도 앞으로 나아가는 것이다.',
                    'author': '부산행',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '인생은 한 방이다. 그 한 방을 잘 쏘면 된다.',
                    'author': '부산행',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '모든 사람은 자신만의 시간을 가지고 있다.',
                    'author': '부산행',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '진짜 행복은 작은 것에서 온다.',
                    'author': '암살',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '인생은 예측할 수 없다. 그래서 더 아름답다.',
                    'author': '암살',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '진짜 용기는 두려워도 앞으로 나아가는 것이다.',
                    'author': '암살',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '인생은 한 방이다. 그 한 방을 잘 쏘면 된다.',
                    'author': '암살',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '모든 일에는 이유가 있다. 지금은 이해하지 못해도 나중에 알게 된다.',
                    'author': '암살',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '진짜 행복은 작은 것에서 온다.',
                    'author': '베테랑',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '인생은 선택의 연속이다. 후회하지 않는 선택을 하자.',
                    'author': '베테랑',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '진짜 용기는 두려워도 앞으로 나아가는 것이다.',
                    'author': '베테랑',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '인생은 한 방이다. 그 한 방을 잘 쏘면 된다.',
                    'author': '베테랑',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '모든 사람은 자신만의 시간을 가지고 있다.',
                    'author': '베테랑',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '진짜 행복은 작은 것에서 온다.',
                    'author': '신과함께',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '인생은 예측할 수 없다. 그래서 더 아름답다.',
                    'author': '신과함께',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '진짜 용기는 두려워도 앞으로 나아가는 것이다.',
                    'author': '신과함께',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '인생은 한 방이다. 그 한 방을 잘 쏘면 된다.',
                    'author': '신과함께',
                    'source': '영화',
                    'type': 'drama'
                },
                {
                    'text': '모든 일에는 이유가 있다. 지금은 이해하지 못해도 나중에 알게 된다.',
                    'author': '신과함께',
                    'source': '영화',
                    'type': 'drama'
                },
            ]
            
            return random.choice(korean_drama_quotes)
        except Exception as e:
            print(f"한국 드라마/영화 명대사 수집 오류: {e}")
        return None
    
    def fetch_quote(self, prefer_korean: bool = True, prefer_poem: bool = False) -> Dict:
        """
        명언 또는 시를 가져오기
        여러 소스를 시도하여 성공한 것을 반환
        
        Args:
            prefer_korean: 한국어 우선 여부
            prefer_poem: 시 우선 여부 (True면 시를 우선적으로 선택)
        """
        sources = []
        
        if prefer_korean:
            if prefer_poem:
                # 시를 우선적으로
                sources.extend([
                    self.fetch_korean_poem_web,
                    self.fetch_korean_quote_web,
                ])
            else:
                # 명언과 시를 랜덤하게
                korean_sources = [self.fetch_korean_quote_web, self.fetch_korean_poem_web]
                random.shuffle(korean_sources)  # 랜덤 순서
                sources.extend(korean_sources)
        
        # 영어 소스
        sources.extend([
            self.fetch_from_zenquotes,
            self.fetch_from_quotable,
        ])
        
        # 각 소스를 시도
        for source_func in sources:
            result = source_func()
            if result:
                return result
            time.sleep(0.5)  # API 호출 간격
        
        # 모든 소스 실패 시 기본 명언 반환
        return {
            'text': '오늘도 새로운 하루를 시작합니다. 작은 것부터 시작해보세요.',
            'author': '시스템',
            'source': '기본',
            'type': 'quote'
        }
    
    def fetch_daily_quote(self, date_str: Optional[str] = None, birth_date: Optional[str] = None) -> Dict:
        """
        날짜와 생년월일 기반으로 매일 다른 명언 가져오기
        같은 날짜와 생년월일이면 같은 명언 반환
        생년월일이 다르면 다른 명언 반환
        """
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # 날짜와 생년월일을 조합하여 시드 생성
        # 생년월일이 있으면 포함, 없으면 날짜만 사용
        if birth_date:
            seed_str = f"{date_str}_{birth_date}"
        else:
            seed_str = date_str
        
        # 시드를 해시하여 정수로 변환 (더 안정적인 랜덤 시드)
        seed_hash = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
        random.seed(seed_hash)
        
        prefer_korean = True
        
        # 시, 명언, 명대사를 랜덤하게 선택 (시드 기반)
        # 시드의 마지막 숫자로 결정 (0: 시, 1: 명언, 2: 명대사)
        seed_mod = seed_hash % 3
        prefer_poem = (seed_mod == 0)  # 33% 확률로 시 선택
        
        quote = self.fetch_quote(prefer_korean=prefer_korean, prefer_poem=prefer_poem)
        quote['date'] = date_str
        
        return quote
    
    def fetch_random_quote(self, birth_date: Optional[str] = None, random_seed: Optional[str] = None) -> Dict:
        """
        랜덤 명언/시 가져오기 (다른 한 줄 보기용)
        
        Args:
            birth_date: 생년월일 (선택적)
            random_seed: 랜덤 시드 (선택적, 없으면 현재 시간 사용)
        """
        if random_seed is None:
            random_seed = str(time.time())
        
        # 랜덤 시드 생성
        if birth_date:
            seed_str = f"{random_seed}_{birth_date}"
        else:
            seed_str = random_seed
        
        # 시드를 해시하여 정수로 변환
        seed_hash = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
        random.seed(seed_hash)
        
        prefer_korean = True
        
        # 시, 명언, 명대사를 랜덤하게 선택
        seed_mod = seed_hash % 3
        prefer_poem = (seed_mod == 0)  # 33% 확률로 시 선택
        
        quote = self.fetch_quote(prefer_korean=prefer_korean, prefer_poem=prefer_poem)
        quote['date'] = datetime.now().strftime('%Y-%m-%d')
        
        return quote


if __name__ == '__main__':
    # 테스트
    fetcher = QuoteFetcher()
    quote = fetcher.fetch_daily_quote()
    print(json.dumps(quote, ensure_ascii=False, indent=2))

