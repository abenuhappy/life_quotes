// 생년월일 기반 명언/시 시스템 Frontend

const API_BASE = '';

// 사용자 ID (로컬 스토리지에서 가져오거나 생성)
let userId = localStorage.getItem('userId') || 'user_' + Date.now();
if (!localStorage.getItem('userId')) {
    localStorage.setItem('userId', userId);
}

// 현재 표시 중인 데이터 저장 (공유용)
let currentQuote = null;
let currentColor = null;
let currentDrink = null;
let currentBirthDate = null;
let lastLoadedDate = null; // 마지막으로 로드한 날짜
let midnightTimer = null; // 자정 타이머
let dateCheckInterval = null; // 날짜 확인 인터벌

// DOM 요소
const birthdayForm = document.getElementById('birthdayForm');
const birthdaySection = document.getElementById('birthdaySection');
const quoteSection = document.getElementById('quoteSection');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');
const birthdayMessage = document.getElementById('birthdayMessage');


// 한국시간(KST) 기준 현재 시간 가져오기
function getKSTNow() {
    const now = new Date();
    // UTC 시간을 가져와서 KST(UTC+9)로 변환
    const utcTime = now.getTime() + (now.getTimezoneOffset() * 60 * 1000);
    const kstOffset = 9 * 60 * 60 * 1000; // 9시간을 밀리초로 변환
    return new Date(utcTime + kstOffset);
}

// 자정까지 남은 시간 계산 (밀리초) - 한국시간 기준
function getMillisecondsUntilMidnight() {
    const now = getKSTNow();
    const midnight = new Date(now);
    midnight.setHours(24, 0, 0, 0); // 다음 자정
    return midnight.getTime() - now.getTime();
}

// 자정 자동 새로고침 설정
function setupMidnightAutoRefresh() {
    // 기존 타이머가 있으면 제거
    if (midnightTimer) {
        clearTimeout(midnightTimer);
    }
    
    const msUntilMidnight = getMillisecondsUntilMidnight();
    
    console.log(`자정 자동 새로고침 설정: ${Math.floor(msUntilMidnight / 1000 / 60)}분 후`);
    
    midnightTimer = setTimeout(() => {
        console.log('자정 도달! 자동으로 새로운 명언을 불러옵니다...');
        loadDailyQuote();
        
        // 다음 자정을 위해 다시 설정
        setupMidnightAutoRefresh();
    }, msUntilMidnight);
}

// 한국시간 기준 오늘 날짜 가져오기 (YYYY-MM-DD)
function getKSTToday() {
    const kstNow = getKSTNow();
    const year = kstNow.getFullYear();
    const month = String(kstNow.getMonth() + 1).padStart(2, '0');
    const day = String(kstNow.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// 날짜 확인 및 자동 업데이트 - 한국시간 기준
function checkDateAndUpdate() {
    const today = getKSTToday(); // 한국시간 기준 오늘 날짜
    
    // 날짜가 바뀌었으면 자동 업데이트
    if (lastLoadedDate && lastLoadedDate !== today) {
        console.log(`날짜가 변경되었습니다 (${lastLoadedDate} → ${today}). 자동으로 업데이트합니다.`);
        loadDailyQuote();
    }
}

// 날짜 확인 인터벌 설정 (1분마다 확인)
function setupDateCheckInterval() {
    // 기존 인터벌이 있으면 제거
    if (dateCheckInterval) {
        clearInterval(dateCheckInterval);
    }
    
    // 1분마다 날짜 확인
    dateCheckInterval = setInterval(() => {
        checkDateAndUpdate();
    }, 60 * 1000); // 1분 = 60,000ms
}

// 초기화
document.addEventListener('DOMContentLoaded', async () => {
    // 저장된 생년월일 확인
    const saved = await checkSavedBirthday();
    if (saved) {
        birthdaySection.style.display = 'none';
        quoteSection.style.display = 'block';
        // 헤더 및 메뉴 표시
        const headerSection = document.getElementById('headerSection');
        const topMenu = document.getElementById('topMenu');
        if (headerSection) {
            headerSection.style.display = 'block';
        }
        if (topMenu) {
            topMenu.style.display = 'flex';
        }
        updateSubtitle();
        loadDailyQuote();
    }
    
    // 생년월일 정보 가져오기 (공유용)
    try {
        const response = await fetch(`${API_BASE}/api/birthday/${userId}`);
        const data = await response.json();
        if (data.success && data.data.birth_date) {
            currentBirthDate = data.data.birth_date;
        }
    } catch (error) {
        console.error('생년월일 조회 오류:', error);
    }
    
    // 자정 자동 새로고침 설정
    setupMidnightAutoRefresh();
    
    // 날짜 확인 인터벌 설정
    setupDateCheckInterval();
    
    
    // 페이지가 보일 때 포커스 이벤트로 날짜 확인 (탭 전환 시)
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) {
            checkDateAndUpdate();
        }
    });
    
    // 탭 메뉴 클릭 시 해당 섹션으로 스크롤 및 active 상태 관리
    const tabItems = document.querySelectorAll('.tab-item');
    let activeTab = '오늘의 한 줄'; // 기본 활성 탭
    
    tabItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            const targetId = item.getAttribute('data-target');
            const tabName = item.getAttribute('data-tab');
            const targetElement = document.getElementById(targetId);
            
            // 모든 탭에서 active 클래스 제거
            tabItems.forEach(tab => tab.classList.remove('active'));
            // 클릭한 탭에 active 클래스 추가
            item.classList.add('active');
            activeTab = tabName;
            
            if (targetElement) {
                // 요소가 표시되어 있는지 확인
                if (targetElement.style.display === 'none') {
                    // 요소가 숨겨져 있으면 표시
                    targetElement.style.display = 'block';
                }
                
                // 부드러운 스크롤
                const offsetTop = targetElement.offsetTop;
                const headerOffset = 100; // 헤더와 메뉴 높이 고려
                const elementPosition = offsetTop - headerOffset;
                
                window.scrollTo({
                    top: elementPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // 초기 활성 탭 설정
    if (tabItems.length > 0) {
        tabItems[0].classList.add('active');
    }
});

// 생년월일 저장 확인
async function checkSavedBirthday() {
    try {
        const response = await fetch(`${API_BASE}/api/birthday/${userId}`);
        const data = await response.json();
        if (data.success && data.data.birth_date) {
            updateSubtitle(data.data.birth_date);
            return true;
        }
        return false;
    } catch (error) {
        console.error('생년월일 확인 오류:', error);
        return false;
    }
}

// 서브타이틀 업데이트
async function updateSubtitle(birthDate = null) {
    const subtitle = document.getElementById('subtitle');
    
    if (!birthDate) {
        // 생년월일 가져오기
        try {
            const response = await fetch(`${API_BASE}/api/birthday/${userId}`);
            const data = await response.json();
            if (data.success && data.data.birth_date) {
                birthDate = data.data.birth_date;
            } else {
                subtitle.textContent = '생년월일에 맞춘 매일 다른 명언 또는 시를 제공합니다';
                return;
            }
        } catch (error) {
            subtitle.textContent = '생년월일에 맞춘 매일 다른 명언 또는 시를 제공합니다';
            return;
        }
    }
    
    // 생년월일 포맷팅 (yy년 m월 d일)
    try {
        const date = new Date(birthDate);
        const year = date.getFullYear().toString().slice(-2); // 마지막 2자리
        const month = date.getMonth() + 1; // 0부터 시작하므로 +1
        const day = date.getDate();
        
        subtitle.innerHTML = `${year}년 ${month}월 ${day}일생을 위한 오늘의 메시지<br>당신에게 오늘 필요한 한 줄이에요`;
    } catch (error) {
        subtitle.innerHTML = '생년월일에 맞춘 매일 다른 명언 또는 시를 제공합니다';
    }
}

// 생년월일 저장
birthdayForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const birthDate = document.getElementById('birthDate').value;
    if (!birthDate) {
        showMessage(birthdayMessage, '생년월일을 입력해주세요.', 'error');
        return;
    }
    
    // 공유용 데이터 저장
    currentBirthDate = birthDate;
    
    showLoading(true);
    hideMessage(birthdayMessage);
    
    try {
        const response = await fetch(`${API_BASE}/api/birthday`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: userId,
                birth_date: birthDate
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(birthdayMessage, '생년월일이 저장되었습니다! 새로운 명언을 불러옵니다...', 'success');
            setTimeout(() => {
                birthdaySection.style.display = 'none';
                quoteSection.style.display = 'block';
                updateSubtitle(birthDate);
                // 헤더 및 메뉴 표시
                const headerSection = document.getElementById('headerSection');
                const topMenu = document.getElementById('topMenu');
                if (headerSection) {
                    headerSection.style.display = 'block';
                }
                if (topMenu) {
                    topMenu.style.display = 'flex';
                }
                // 생년월일 변경 시 즉시 새로운 명언 로드
                loadDailyQuote();
            }, 500);
        } else {
            showMessage(birthdayMessage, data.error || '저장에 실패했습니다.', 'error');
        }
    } catch (error) {
        showMessage(birthdayMessage, '오류가 발생했습니다: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
});

// 오늘의 명언/시 로드
async function loadDailyQuote() {
    showLoading(true);
    hideError();
    
    try {
        const response = await fetch(`${API_BASE}/api/daily?user_id=${userId}`);
        const data = await response.json();
        
            if (data.success) {
            displayQuote(data.data.quote);
            // 생년월일 분석 숨김 처리
            // if (data.data.analysis) {
            //     displayAnalysis(data.data.analysis);
            // }
            if (data.data.color) {
                displayColor(data.data.color);
            }
            if (data.data.drink) {
                displayDrink(data.data.drink);
            }
            if (data.data.flower) {
                displayFlower(data.data.flower);
            }
            if (data.data.shopping_items && data.data.shopping_items.length > 0) {
                displayShoppingItems(data.data.shopping_items);
            }
            
            // 헤더 및 메뉴 표시
            const headerSection = document.getElementById('headerSection');
            const topMenu = document.getElementById('topMenu');
            if (headerSection) {
                headerSection.style.display = 'block';
            }
            if (topMenu) {
                topMenu.style.display = 'flex';
            }
            
            // 로드한 날짜 저장 (한국시간 기준)
            const today = getKSTToday();
            lastLoadedDate = today;
            
            // 자정 타이머 재설정 (새로운 날짜가 로드되었으므로)
            setupMidnightAutoRefresh();
        } else {
            if (data.requires_birthday) {
                // 생년월일 입력 필요
                birthdaySection.style.display = 'block';
                quoteSection.style.display = 'none';
                showMessage(birthdayMessage, '생년월일을 먼저 입력해주세요.', 'error');
            } else {
                showError(data.error || '명언을 불러올 수 없습니다.');
            }
        }
    } catch (error) {
        showError('오류가 발생했습니다: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// 랜덤 명언/시 로드 (다른 한 줄 보기)
async function loadRandomQuote() {
    showLoading(true);
    hideError();
    
    try {
        // 랜덤 시드를 생성하여 다른 명언/시를 가져오기
        const randomSeed = Date.now() + Math.random();
        const response = await fetch(`${API_BASE}/api/quote?user_id=${userId}&random=${randomSeed}`);
        const data = await response.json();
        
        if (data.success) {
            displayQuote(data.data.quote);
            // 생년월일 분석 숨김 처리
            // if (data.data.analysis) {
            //     displayAnalysis(data.data.analysis);
            // }
            if (data.data.color) {
                displayColor(data.data.color);
            }
        } else {
            showError(data.error || '명언을 불러올 수 없습니다.');
        }
    } catch (error) {
        showError('오류가 발생했습니다: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// 명언 표시
function displayQuote(quote) {
    const quoteTextWrapper = document.getElementById('quoteTextWrapper');
    const quoteAuthor = document.getElementById('quoteAuthor');
    const quoteDate = document.getElementById('quoteDate');
    
    // 명언 텍스트를 줄바꿈으로 분리하여 각 줄을 별도의 p 태그로 표시
    const quoteLines = quote.text.split('\n').filter(line => line.trim() !== '');
    quoteTextWrapper.innerHTML = '';
    
    quoteLines.forEach(line => {
        const p = document.createElement('p');
        p.textContent = line.trim();
        quoteTextWrapper.appendChild(p);
    });
    
    // 작가 표시
    if (quote.author) {
        quoteAuthor.textContent = `- ${quote.author} -`;
    } else {
        quoteAuthor.textContent = '';
    }
    
    // 날짜 표시 (우측 하단)
    const today = getKSTToday();
    quoteDate.textContent = today;
    
    // 공유용 데이터 저장
    currentQuote = quote;
}

// 컬러 표시 및 화면 톤 변경
function displayColor(color) {
    const colorCard = document.getElementById('colorCard');
    const colorContent = document.getElementById('colorContent');
    
    // 의미 텍스트를 짧은 설명과 긴 설명으로 분리
    const meaning = color.meaning || '';
    // 첫 번째 문장을 짧은 설명으로, 나머지를 긴 설명으로
    const sentences = meaning.split(/[.。]/).filter(s => s.trim() !== '');
    let shortDesc = sentences.length > 0 ? sentences[0].trim() : meaning;
    let longDesc = sentences.length > 1 ? sentences.slice(1).join('. ').trim() : '';
    
    // "입니다"로 끝나는 경우 처리
    if (shortDesc && !shortDesc.endsWith('입니다') && !shortDesc.endsWith('.')) {
        shortDesc += '입니다';
    }
    
    colorContent.innerHTML = `
        <div class="color-inner-card">
            <h3 class="color-name">${color.name}</h3>
            <p class="color-short-desc">${shortDesc}</p>
            ${longDesc ? `<p class="color-long-desc">${longDesc}</p>` : ''}
        </div>
    `;
    
    colorCard.style.display = 'block';
    
    // 공유용 데이터 저장
    currentColor = color;
    
    // 화면 톤 변경
    applyColorTheme(color);
}

// 오늘의 꽃 표시
function displayFlower(flower) {
    const flowerCard = document.getElementById('flowerCard');
    const flowerContent = document.getElementById('flowerContent');
    
    flowerContent.innerHTML = `
        <div class="bg-white border-2 border-gray-100 rounded-2xl p-6 text-center">
            <div class="text-6xl mb-3">${flower.emoji || '🌺'}</div>
            <h3 class="text-gray-900 mb-1">${flower.name || ''}</h3>
            <p class="text-xs text-gray-600 mb-3">${flower.source || ''}</p>
            <p class="text-xs text-gray-500">${flower.meaning || ''}</p>
        </div>
    `;
    
    flowerCard.style.display = 'block';
}

// 추천 쇼핑 아이템 표시
function displayShoppingItems(items) {
    const shoppingCard = document.getElementById('shoppingCard');
    const shoppingContent = document.getElementById('shoppingContent');
    
    if (!items || items.length === 0) {
        shoppingCard.style.display = 'none';
        return;
    }
    
    // 첫 번째 아이템만 사용
    const item = items[0];
    
    // 가격 정보 처리
    const price = item.price ? parseInt(item.price) : null;
    const formattedPrice = price ? `${price.toLocaleString()}원` : '';
    
    // 이미지가 있으면 이미지 사용, 없으면 기본 이모지
    const imageHTML = item.image 
        ? `<img src="${item.image}" alt="${item.name}" class="shopping-item-image" onerror="this.style.display='none'">`
        : '<div class="text-3xl">🛍️</div>';
    
    shoppingContent.innerHTML = `
        <div class="bg-white border-2 border-gray-100 rounded-2xl p-6">
            <a href="${item.link}" target="_blank" rel="noopener noreferrer" class="shopping-item-link-wrapper">
                <div class="flex gap-4 items-center">
                    <div class="w-16 h-16 bg-gradient-to-b from-blue-100 to-blue-200 rounded-lg flex-shrink-0 flex items-center justify-center">
                        ${imageHTML}
                    </div>
                    <div class="flex-1">
                        <h3 class="text-gray-900 text-sm mb-1">${item.name || ''}</h3>
                        ${formattedPrice ? `
                            <div class="flex items-center gap-2 mb-1">
                                <span class="text-gray-900">${formattedPrice}</span>
                            </div>
                        ` : ''}
                        ${item.mallName ? `<p class="text-xs text-gray-400">${item.mallName}</p>` : ''}
                    </div>
                </div>
            </a>
        </div>
    `;
    
    shoppingCard.style.display = 'block';
}

// 오늘의 한잔 표시
function displayDrink(drink) {
    const drinkCard = document.getElementById('drinkCard');
    const drinkContent = document.getElementById('drinkContent');
    
    // description을 문장 단위로 분리
    const descriptionParts = drink.description ? drink.description.split(/[.!?]\s*/).filter(s => s.trim()) : [];
    const shortDesc = descriptionParts.length > 0 ? descriptionParts[0] : '';
    const longDesc = descriptionParts.length > 1 ? descriptionParts.slice(1).join('. ') : '';
    
    // 커피/차에 따른 아이콘 색상 결정
    const iconColor = drink.type === 'coffee' ? 'bg-green-300' : 'bg-blue-300';
    
    drinkContent.innerHTML = `
        <div class="bg-white border-2 border-gray-100 rounded-2xl p-6 text-center">
            <div class="w-20 h-20 mx-auto mb-3 bg-gradient-to-br from-amber-800 to-amber-900 rounded-full flex items-center justify-center">
                <div class="w-12 h-12 ${iconColor} rounded-full flex items-center justify-center">
                    <span style="font-size: 1.5rem;">${drink.emoji || '☕'}</span>
                </div>
            </div>
            <h3 class="text-gray-900 mb-1">${drink.name || ''}</h3>
            <p class="text-xs text-gray-500 mb-1">${drink.type_korean || ''}</p>
            ${shortDesc ? `<p class="text-xs text-gray-600">${shortDesc}</p>` : ''}
            ${longDesc ? `<p class="text-xs text-gray-500 mt-3">${longDesc}</p>` : ''}
        </div>
    `;
    
    drinkCard.style.display = 'block';
    
    // 공유용 데이터 저장
    currentDrink = drink;
}

// 컬러에 맞춰 화면 톤 변경
function applyColorTheme(color) {
    const hex = color.hex;
    const rgb = color.rgb || hexToRgb(hex);
    
    if (!rgb) return;
    
    // 컬러의 밝기 계산 (0-255)
    // 인간의 눈이 인지하는 밝기 가중치 사용
    const brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000;
    const isLight = brightness > 128; // 밝기 기준값
    
    // 컬러 카드는 원본 hex 그대로 유지 (변경 없음)
    
    // UI 톤 결정
    let uiGradient1, uiGradient2;
    
    if (isLight) {
        // LIGHT 컬러면 UI는 중간 톤
        // 원본보다 약간 어둡게, 하지만 너무 어둡지 않게
        uiGradient1 = adjustBrightness(hex, -0.15); // 약간 어둡게
        uiGradient2 = adjustBrightness(hex, -0.25); // 조금 더 어둡게
    } else {
        // DARK 컬러면 UI는 밝은 톤
        // 원본보다 훨씬 밝게
        uiGradient1 = adjustBrightness(hex, 0.4); // 많이 밝게
        uiGradient2 = adjustBrightness(hex, 0.2); // 조금 밝게
    }
    
    // CSS 변수 설정
    const root = document.documentElement;
    root.style.setProperty('--theme-color', hex); // 원본 컬러 유지
    root.style.setProperty('--theme-gradient-1', uiGradient1);
    root.style.setProperty('--theme-gradient-2', uiGradient2);
    root.style.setProperty('--theme-rgb', `${rgb[0]}, ${rgb[1]}, ${rgb[2]}`);
    
    // 배경 그라데이션 적용 (UI 톤 사용)
    document.body.style.background = `linear-gradient(135deg, ${uiGradient1} 0%, ${uiGradient2} 100%)`;
    
    // 컨테이너 배경 조정
    const container = document.querySelector('.container');
    if (container) {
        if (isLight) {
            // 밝은 컬러면 약간 투명한 흰색
            container.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
        } else {
            // 어두운 컬러면 더 불투명한 흰색 (가독성 향상)
            container.style.backgroundColor = 'rgba(255, 255, 255, 0.98)';
        }
    }
}

// HEX를 RGB로 변환
function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? [
        parseInt(result[1], 16),
        parseInt(result[2], 16),
        parseInt(result[3], 16)
    ] : null;
}

// 밝기 조정
function adjustBrightness(hex, percent) {
    const rgb = hexToRgb(hex);
    if (!rgb) return hex;
    
    const r = Math.max(0, Math.min(255, Math.round(rgb[0] + (rgb[0] * percent))));
    const g = Math.max(0, Math.min(255, Math.round(rgb[1] + (rgb[1] * percent))));
    const b = Math.max(0, Math.min(255, Math.round(rgb[2] + (rgb[2] * percent))));
    
    return `rgb(${r}, ${g}, ${b})`;
}

// 분석 정보 표시
function displayAnalysis(analysis) {
    const analysisCard = document.getElementById('analysisCard');
    const analysisContent = document.getElementById('analysisContent');
    
    analysisContent.innerHTML = `
        <div class="analysis-item">
            <h4>별자리</h4>
            <p>${analysis.zodiac.korean} (${analysis.zodiac.english})</p>
        </div>
        <div class="analysis-item">
            <h4>타로 카드</h4>
            <p>${analysis.tarot.korean}</p>
            <p style="font-size: 0.9em; margin-top: 5px; color: #999;">${analysis.tarot.meaning}</p>
        </div>
        <div class="analysis-item">
            <h4>생일 특성</h4>
            <p>${analysis.characteristics.season} 계절</p>
            <p>${analysis.characteristics.weekday_korean} 출생</p>
        </div>
        <div class="analysis-item">
            <h4>생명수</h4>
            <p>${analysis.characteristics.life_path_number}</p>
        </div>
    `;
    
    analysisCard.style.display = 'block';
}

// 다른 한 줄 보기 버튼
document.getElementById('refreshBtn').addEventListener('click', () => {
    loadRandomQuote();
});

// 생년월일 수정 버튼
document.getElementById('editBirthdayBtn').addEventListener('click', async () => {
    // 저장된 생년월일 가져오기
    try {
        const response = await fetch(`${API_BASE}/api/birthday/${userId}`);
        const data = await response.json();
        
        if (data.success && data.data.birth_date) {
            // 기존 생년월일을 입력 필드에 설정
            document.getElementById('birthDate').value = data.data.birth_date;
            currentBirthDate = data.data.birth_date;
        }
    } catch (error) {
        console.error('생년월일 조회 오류:', error);
    }
    
    // 생년월일 입력 섹션 표시
    quoteSection.style.display = 'none';
    birthdaySection.style.display = 'block';
    hideMessage(birthdayMessage);
    // 서브타이틀을 기본 메시지로 변경
    document.getElementById('subtitle').textContent = '생년월일에 맞춘 매일 다른 명언 또는 시를 제공합니다';
    
    // 공유 메뉴 숨기기
    const shareMenu = document.getElementById('shareMenu');
    if (shareMenu) {
        shareMenu.style.display = 'none';
    }
});


// 유틸리티 함수
function showLoading(show) {
    loading.style.display = show ? 'block' : 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

function showMessage(element, message, type) {
    element.textContent = message;
    element.className = `message ${type}`;
    element.style.display = 'block';
}

function hideMessage(element) {
    element.style.display = 'none';
}

// 공유 메시지 생성
function generateShareMessage() {
    if (!currentQuote) {
        return '오늘의 한 줄을 확인해보세요!';
    }
    
    let message = `🌟 오늘, 나에게 들려주는 한 줄\n\n`;
    message += `"${currentQuote.text}"\n`;
    message += `- ${currentQuote.author}\n\n`;
    
    if (currentColor) {
        message += `🎨 오늘의 컬러: ${currentColor.name} ${currentColor.hex}\n`;
        if (currentColor.meaning) {
            message += `${currentColor.meaning}\n\n`;
        }
    }
    
    if (currentDrink) {
        message += `☕ 오늘의 한잔: ${currentDrink.emoji} ${currentDrink.name}\n`;
        message += `${currentDrink.description}\n\n`;
    }
    
    message += `\n${window.location.href}`;
    
    return message;
}

// 공유 URL 생성 (공유 가능한 링크)
function generateShareUrl() {
    const params = new URLSearchParams();
    
    if (currentBirthDate) {
        params.append('birth_date', currentBirthDate);
    }
    
    if (currentQuote) {
        params.append('quote_text', encodeURIComponent(currentQuote.text));
        params.append('quote_author', encodeURIComponent(currentQuote.author));
        params.append('quote_type', currentQuote.type);
    }
    
    if (currentColor) {
        params.append('color_name', encodeURIComponent(currentColor.name));
        params.append('color_hex', currentColor.hex);
    }
    
    if (currentDrink) {
        params.append('drink_name', encodeURIComponent(currentDrink.name));
        params.append('drink_emoji', currentDrink.emoji);
    }
    
    return `${window.location.origin}${window.location.pathname}?${params.toString()}`;
}

// Safari 브라우저 감지
function isSafari() {
    return /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
}

// URL 복사 함수 (Safari 호환)
function copyToClipboard(text) {
    return new Promise((resolve, reject) => {
        // Clipboard API 시도 (HTTPS 환경에서만 작동)
        if (navigator.clipboard && navigator.clipboard.writeText && (location.protocol === 'https:' || location.hostname === 'localhost')) {
            navigator.clipboard.writeText(text)
                .then(() => resolve(true))
                .catch(() => {
                    // Clipboard API 실패 시 execCommand로 대체
                    fallbackCopyToClipboard(text, resolve, reject);
                });
        } else {
            // execCommand 사용 (Safari 포함 모든 브라우저)
            fallbackCopyToClipboard(text, resolve, reject);
        }
    });
}

// execCommand를 사용한 복사 (Safari 호환)
function fallbackCopyToClipboard(text, resolve, reject) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.top = '0';
    textArea.style.left = '0';
    textArea.style.width = '2em';
    textArea.style.height = '2em';
    textArea.style.padding = '0';
    textArea.style.border = 'none';
    textArea.style.outline = 'none';
    textArea.style.boxShadow = 'none';
    textArea.style.background = 'transparent';
    textArea.style.opacity = '0';
    textArea.readOnly = true;
    textArea.setAttribute('readonly', '');
    
    document.body.appendChild(textArea);
    
    // Safari에서 선택이 제대로 작동하도록
    if (isSafari()) {
        textArea.contentEditable = true;
        textArea.readOnly = false;
        const range = document.createRange();
        range.selectNodeContents(textArea);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        textArea.setSelectionRange(0, 999999);
    } else {
        textArea.select();
        textArea.setSelectionRange(0, 999999);
    }
    
    try {
        const successful = document.execCommand('copy');
        document.body.removeChild(textArea);
        if (successful) {
            resolve(true);
        } else {
            reject(new Error('execCommand copy failed'));
        }
    } catch (err) {
        document.body.removeChild(textArea);
        reject(err);
    }
}

// 공유 버튼 클릭 이벤트 - 바로 URL 복사
document.getElementById('shareBtn').addEventListener('click', async (e) => {
    e.stopPropagation();
    
    const shareUrl = generateShareUrl();
    
    try {
        // 단축 URL 생성
        showLoading(true);
        const response = await fetch(`${API_BASE}/api/shorten-url`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: shareUrl
            })
        });
        
        const data = await response.json();
        showLoading(false);
        
        const urlToCopy = (data.success && data.data.short_url) ? data.data.short_url : shareUrl;
        
        // URL 복사 시도
        try {
            await copyToClipboard(urlToCopy);
            alert('URL이 복사되었습니다.');
        } catch (error) {
            console.error('URL 복사 실패:', error);
            // 복사 실패 시 사용자에게 URL 표시
            alert(`URL 복사에 실패했습니다. 아래 URL을 직접 복사해주세요:\n\n${urlToCopy}`);
        }
    } catch (error) {
        showLoading(false);
        console.error('단축 URL 생성 실패:', error);
        // 단축 URL 생성 실패 시 원본 URL 복사
        try {
            await copyToClipboard(shareUrl);
            alert('URL이 복사되었습니다.');
        } catch (copyError) {
            console.error('URL 복사 실패:', copyError);
            alert(`URL 복사에 실패했습니다. 아래 URL을 직접 복사해주세요:\n\n${shareUrl}`);
        }
    }
});

// URL 복사하기 (공유 메뉴에서 사용 - 현재는 사용하지 않지만 유지)
document.getElementById('copyUrlBtn')?.addEventListener('click', async () => {
    const shareUrl = generateShareUrl();
    
    try {
        // 단축 URL 생성
        showLoading(true);
        const response = await fetch(`${API_BASE}/api/shorten-url`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: shareUrl
            })
        });
        
        const data = await response.json();
        showLoading(false);
        
        if (data.success && data.data.short_url) {
            const shortUrl = data.data.short_url;
            
            // 단축 URL 복사
            try {
                // Clipboard API 사용 (최신 브라우저)
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    await navigator.clipboard.writeText(shortUrl);
                    alert('URL이 복사되었습니다.');
                } else {
                    // 구형 브라우저를 위한 대체 방법
                    const textArea = document.createElement('textarea');
                    textArea.value = shortUrl;
                    textArea.style.position = 'fixed';
                    textArea.style.left = '-999999px';
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                    alert('URL이 복사되었습니다.');
                }
            } catch (error) {
                console.error('URL 복사 실패:', error);
                // 복사 실패 시 사용자에게 URL 표시
                alert(`URL 복사에 실패했습니다. 아래 URL을 직접 복사해주세요:\n\n${shortUrl}`);
            }
        } else {
            // 단축 URL 생성 실패 시 원본 URL 복사
            try {
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    await navigator.clipboard.writeText(shareUrl);
                    alert('URL이 복사되었습니다.');
                } else {
                    const textArea = document.createElement('textarea');
                    textArea.value = shareUrl;
                    textArea.style.position = 'fixed';
                    textArea.style.left = '-999999px';
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                    alert('URL이 복사되었습니다.');
                }
            } catch (error) {
                console.error('URL 복사 실패:', error);
                alert(`URL 복사에 실패했습니다. 아래 URL을 직접 복사해주세요:\n\n${shareUrl}`);
            }
        }
    } catch (error) {
        showLoading(false);
        console.error('단축 URL 생성 실패:', error);
        // 단축 URL 생성 실패 시 원본 URL 복사
        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                await navigator.clipboard.writeText(shareUrl);
                alert('URL이 복사되었습니다.');
            } else {
                const textArea = document.createElement('textarea');
                textArea.value = shareUrl;
                textArea.style.position = 'fixed';
                textArea.style.left = '-999999px';
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                alert('URL이 복사되었습니다.');
            }
        } catch (copyError) {
            console.error('URL 복사 실패:', copyError);
            alert(`URL 복사에 실패했습니다. 아래 URL을 직접 복사해주세요:\n\n${shareUrl}`);
        }
    }
    
    // 공유 메뉴 닫기
    const shareMenu = document.getElementById('shareMenu');
    if (shareMenu) {
        shareMenu.style.display = 'none';
    }
});

// URL 복사 성공 메시지 표시
function showCopySuccess() {
    // 기존 메시지 제거
    const existingMessage = document.getElementById('copySuccessMessage');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // 성공 메시지 생성
    const message = document.createElement('div');
    message.id = 'copySuccessMessage';
    message.className = 'copy-success-message';
    message.textContent = 'URL이 복사되었습니다!';
    
    // 버튼 그룹 근처에 추가
    const buttonGroup = document.querySelector('.button-group');
    if (buttonGroup) {
        buttonGroup.parentNode.insertBefore(message, buttonGroup.nextSibling);
        
        // 3초 후 자동 제거
        setTimeout(() => {
            message.remove();
        }, 3000);
    }
}

// 외부 클릭 시 공유 메뉴 닫기
document.addEventListener('click', (e) => {
    const shareMenu = document.getElementById('shareMenu');
    const shareBtn = document.getElementById('shareBtn');
    const copyUrlBtn = document.getElementById('copyUrlBtn');
    
    if (shareMenu && shareBtn) {
        // 공유 메뉴나 공유 버튼 외부 클릭 시 메뉴 닫기
        if (!shareMenu.contains(e.target) && !shareBtn.contains(e.target) && e.target !== copyUrlBtn) {
            shareMenu.style.display = 'none';
        }
    }
});


