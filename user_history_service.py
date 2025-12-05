# -*- coding: utf-8 -*-
"""
사용자 히스토리 및 선호도 관리 서비스
"""
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Set
import pytz

# 한국시간대 설정
KST = pytz.timezone('Asia/Seoul')

def get_kst_now():
    """한국시간(KST) 기준 현재 시간 반환"""
    return datetime.now(KST)


class UserHistoryService:
    """사용자 히스토리 및 선호도 관리 클래스"""
    
    def __init__(self, data_folder: str = 'data'):
        self.data_folder = data_folder
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
    
    def _get_history_file_path(self, user_id: str) -> str:
        """사용자 히스토리 파일 경로 반환"""
        return os.path.join(self.data_folder, f'{user_id}_history.json')
    
    def _load_history(self, user_id: str) -> Dict:
        """사용자 히스토리 로드"""
        file_path = self._get_history_file_path(user_id)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._get_default_history()
        return self._get_default_history()
    
    def _save_history(self, user_id: str, history: Dict):
        """사용자 히스토리 저장"""
        file_path = self._get_history_file_path(user_id)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def _get_default_history(self) -> Dict:
        """기본 히스토리 구조 반환"""
        return {
            'viewed_quotes': [],  # 본 명언 목록 (텍스트 해시)
            'viewed_colors': [],  # 본 컬러 목록 (컬러 이름)
            'viewed_drinks': [],  # 본 음료 목록 (음료 이름)
            'viewed_flowers': [],  # 본 꽃 목록 (꽃 이름)
            'viewed_greetings': [],  # 본 인사말 목록 (인사말 텍스트 해시)
            'viewed_shopping': [],  # 본 쇼핑 아이템 목록 (아이템 제목 해시)
            'last_updated': get_kst_now().isoformat()
        }
    
    def record_view(self, user_id: str, content_type: str, content_id: str):
        """
        콘텐츠 조회 기록
        
        Args:
            user_id: 사용자 ID
            content_type: 콘텐츠 타입 ('quote', 'color', 'drink', 'flower', 'greeting', 'shopping')
            content_id: 콘텐츠 식별자 (텍스트 해시 또는 이름)
        """
        history = self._load_history(user_id)
        view_key = f'viewed_{content_type}s'
        
        if view_key not in history:
            history[view_key] = []
        
        # 중복 방지
        if content_id not in history[view_key]:
            history[view_key].append(content_id)
            # 최근 100개만 유지 (메모리 절약)
            if len(history[view_key]) > 100:
                history[view_key] = history[view_key][-100:]
        
        history['last_updated'] = get_kst_now().isoformat()
        self._save_history(user_id, history)
    
    def get_viewed_items(self, user_id: str, content_type: str) -> List[str]:
        """본 콘텐츠 목록 반환"""
        history = self._load_history(user_id)
        view_key = f'viewed_{content_type}s'
        return history.get(view_key, [])
    
    def is_viewed(self, user_id: str, content_type: str, content_id: str) -> bool:
        """콘텐츠를 이미 본 적이 있는지 확인"""
        viewed = self.get_viewed_items(user_id, content_type)
        return content_id in viewed
    
    def should_avoid(self, user_id: str, content_type: str, content_id: str) -> bool:
        """콘텐츠를 피해야 하는지 확인 (이미 본 경우)"""
        # 이미 본 경우 피하기 (변화 주기 관리)
        if self.is_viewed(user_id, content_type, content_id):
            return True
        
        return False
    
    def get_content_hash(self, text: str) -> str:
        """텍스트를 해시하여 고유 ID 생성"""
        import hashlib
        return hashlib.md5(text.encode('utf-8')).hexdigest()[:16]
    
    def get_full_history(self, user_id: str) -> Dict:
        """전체 히스토리 반환 (public 메서드)"""
        return self._load_history(user_id)
    
    def clear_history(self, user_id: str, content_type: Optional[str] = None):
        """
        히스토리 초기화
        
        Args:
            user_id: 사용자 ID
            content_type: 콘텐츠 타입 (None이면 전체 초기화)
        """
        history = self._load_history(user_id)
        
        if content_type is None:
            # 전체 초기화
            history = self._get_default_history()
        else:
            # 특정 타입만 초기화
            view_key = f'viewed_{content_type}s'
            if view_key in history:
                history[view_key] = []
        
        history['last_updated'] = get_kst_now().isoformat()
        self._save_history(user_id, history)


if __name__ == '__main__':
    # 테스트
    service = UserHistoryService()
    user_id = 'test_user'
    
    # 조회 기록
    service.record_view(user_id, 'quote', 'quote_hash_123')
    service.record_view(user_id, 'color', '빨간색')
    
    # 피드백 기록
    service.record_feedback(user_id, 'quote', 'quote_hash_456', 'like')
    service.record_feedback(user_id, 'color', '파란색', 'dislike')
    
    # 조회
    print("본 명언:", service.get_viewed_items(user_id, 'quote'))
    print("선호도:", service.get_preferences(user_id, 'quote'))
    print("피해야 하는가:", service.should_avoid(user_id, 'color', '파란색'))

