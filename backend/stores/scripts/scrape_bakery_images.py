"""
Google 이미지 검색을 통해 빵집 이미지를 수집하는 스크립트

사용 전 준비사항:
1. pip install selenium
2. Chrome 브라우저 설치
3. ChromeDriver 설치 (또는 자동 다운로드)

주의:
- 학교 프로젝트/비상업적 용도로만 사용
- 과도한 요청은 IP 차단될 수 있음
- 이미지 저작권은 원작자에게 있음
"""

import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    """Chrome WebDriver 설정"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 백그라운드 실행
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    # ChromeDriver 자동 관리 (selenium 4.6+)
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_google_image_url(driver, store_name):
    """
    Google 이미지 검색에서 첫 번째 이미지 URL 가져오기

    Args:
        driver: Selenium WebDriver
        store_name: 검색할 가게 이름

    Returns:
        이미지 URL 또는 None
    """
    try:
        # Google 이미지 검색
        search_query = f"{store_name} 빵집 부산"
        search_url = f"https://www.google.com/search?q={search_query}&tbm=isch"

        driver.get(search_url)
        time.sleep(2)  # 페이지 로딩 대기

        # 첫 번째 이미지 클릭
        images = driver.find_elements(By.CSS_SELECTOR, 'img.rg_i')

        if not images or len(images) < 2:  # 첫 번째는 Google 로고
            print(f"  ❌ {store_name}: 이미지를 찾을 수 없음")
            return None

        # 두 번째 이미지 클릭 (첫 번째는 보통 로고)
        images[1].click()
        time.sleep(1)

        # 원본 이미지 URL 추출
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'img.n3VNCb'))
        )

        actual_images = driver.find_elements(By.CSS_SELECTOR, 'img.n3VNCb')

        for img in actual_images:
            src = img.get_attribute('src')
            if src and src.startswith('http') and 'gstatic' not in src:
                print(f"  ✅ {store_name}: 이미지 발견")
                return src

        print(f"  ⚠️ {store_name}: 유효한 이미지 URL 없음")
        return None

    except Exception as e:
        print(f"  ❌ {store_name} 오류: {str(e)}")
        return None


def scrape_and_update_fixture():
    """
    Google 이미지 검색으로 fixture 업데이트
    """
    fixture_path = 'stores/fixtures/busan_west_3gu_bakeries_fixture.json'

    # Fixture 파일 읽기
    with open(fixture_path, 'r', encoding='utf-8') as f:
        stores = json.load(f)

    print(f"총 {len(stores)}개 가게 처리 시작...\n")

    # WebDriver 초기화
    driver = setup_driver()

    try:
        success_count = 0
        fail_count = 0

        for i, store in enumerate(stores[:10], 1):  # 처음 10개만 테스트
            name = store['fields']['name']
            print(f"[{i}/10] {name}")

            # Google 이미지 검색
            image_url = get_google_image_url(driver, name)

            if image_url:
                store['fields']['preview_image'] = image_url
                success_count += 1
            else:
                # 실패하면 기본 이미지 유지
                fail_count += 1

            # API 과부하 방지
            time.sleep(3)

        print(f"\n✅ 성공: {success_count}개")
        print(f"❌ 실패: {fail_count}개")

        # 결과 저장
        with open(fixture_path, 'w', encoding='utf-8') as f:
            json.dump(stores, f, ensure_ascii=False, indent=2)

        print(f"\n완료! {fixture_path} 파일이 업데이트되었습니다.")

    finally:
        driver.quit()


if __name__ == '__main__':
    print("⚠️ 주의사항:")
    print("- 이 스크립트는 학교 프로젝트/비상업적 용도로만 사용하세요")
    print("- 과도한 요청은 IP 차단될 수 있습니다")
    print("- 수집된 이미지의 저작권은 원작자에게 있습니다\n")

    response = input("계속하시겠습니까? (y/n): ")

    if response.lower() == 'y':
        scrape_and_update_fixture()
    else:
        print("취소되었습니다.")
