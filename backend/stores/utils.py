import os
import json
import traceback
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

# .env 파일 로드 (manage.py가 있는 루트 경로에 .env가 있어야 함)
load_dotenv()

def generate_store_summary(store_name, reviews_list):
    """
    가게 이름과 리뷰 리스트를 받아 AI 요약 및 키워드를 반환합니다.
    (SSAFY GMS API - gpt-4o 사용)
    """
    print(f"🔍 [AI 분석 시작] 가게: {store_name}, 리뷰 수: {len(reviews_list) if reviews_list else 0}")

    # 1. 리뷰 데이터 검증
    if not reviews_list:
        print("⚠️ [AI 분석 중단] 리뷰 데이터가 없음")
        return {
            "summary": "아직 작성된 리뷰가 충분하지 않아 AI가 분석 중입니다. 😅",
            "keywords": ["리뷰환영", "첫리뷰도전"]
        }

    # 2. API 키 검증
    api_key = os.getenv("GMS_KEY")
    if not api_key:
        print("🚨 [CRITICAL ERROR] .env 파일에서 'GMS_KEY'를 찾을 수 없습니다!")
        return {
            "summary": "서버 설정 오류: API 키가 확인되지 않습니다.",
            "keywords": ["시스템오류"]
        }

    # 3. 리뷰 텍스트 합치기 (최대 30개, 너무 길면 잘릴 수 있음)
    combined_reviews = "\n".join(reviews_list[:30]) 

    try:
        # 4. LangChain 채팅 모델 초기화 (API 명세 반영)
        # curl 예시: https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions
        # LangChain base_url: https://gms.ssafy.io/gmsapi/api.openai.com/v1 (뒤에 /chat/completions는 자동생성)
        chat = ChatOpenAI(
            model="gpt-4o",  # [수정] gpt-4o 사용
            api_key=api_key,
            base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1",
            temperature=0.5
        )

        # 5. 프롬프트 엔지니어링
        # (curl 예시의 role: "developer"는 LangChain의 SystemMessage와 동일한 역할)
        system_prompt = f"""
        너는 '브레드피아'라는 빵집 추천 앱의 AI 어시스턴트야.
        사용자들의 리뷰를 분석해서 다음 두 가지를 JSON 형식으로 대답해줘.
        JSON 외에 다른 말은 절대 하지 마.
        
        형식:
        {{
            "summary": "리뷰 내용을 종합해서 2~3문장으로 자연스럽게 요약 (친절하고 부드러운 말투). 맛, 분위기, 서비스 위주.",
            "keywords": ["키워드1", "키워드2", "키워드3"]
        }}
        
        분석할 가게 이름: {store_name}
        """

        user_prompt = f"다음 리뷰들을 분석해줘:\n{combined_reviews}"

        print("🚀 [AI 요청 보냄] 응답 대기 중... (Model: gpt-4o)")
        
        # 6. AI 호출
        response = chat.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        print(f"✅ [AI 응답 도착] {response.content[:50]}...")

        # 7. 응답 파싱
        content = response.content.strip()
        
        # 가끔 AI가 코드 블록(```json ... ```)을 포함할 경우 제거
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "")
        elif content.startswith("```"):
            content = content.replace("```", "")

        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            print(f"⚠️ [JSON 파싱 실패] 원본 응답: {content}")
            result = {
                "summary": content,
                "keywords": ["AI분석", "빵지순례"]
            }
            
        return result

    except Exception as e:
        print("\n" + "="*50)
        print("🚨 [AI 처리 중 에러 발생]")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        print("-" * 20)
        traceback.print_exc()
        print("="*50 + "\n")
        
        return {
            "summary": "현재 AI 서버 연결에 문제가 발생했습니다. 잠시 후 다시 시도해주세요.",
            "keywords": ["데이터분석", "오류발생"]
        }