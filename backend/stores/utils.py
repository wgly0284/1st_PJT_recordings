# import os
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage, SystemMessage
# from dotenv import load_dotenv

# load_dotenv()

def generate_store_summary(store_name, reviews_list):
    """
    가게 이름과 리뷰 리스트를 받아 AI 요약 및 키워드를 반환합니다.
    (SSAFY GMS API 사용)
    """
    # ... (나머지 로직은 그대로 유지) ...
    # 1. 리뷰가 없거나 너무 적으면 분석 불가
    if not reviews_list:
        return {
            "summary": "아직 작성된 리뷰가 충분하지 않아 AI가 분석 중입니다. 😅",
            "keywords": ["리뷰환영", "첫리뷰도전"]
        }

#     # 2. 리뷰 텍스트 합치기
#     combined_reviews = "\n".join(reviews_list[:30]) 

#     # 3. LangChain 채팅 모델 초기화
#     chat = ChatOpenAI(
#         model_name="gpt-3.5-turbo",
#         openai_api_key=os.getenv("GMS_KEY"),
#         openai_api_base="https://gms.ssafy.io/gmsapi/api.openai.com/v1",
#         temperature=0.5
#     )

#     # 4. 프롬프트 엔지니어링
#     system_prompt = f"""
#     너는 '빵지순례'라는 빵집 추천 앱의 AI 어시스턴트야.
#     사용자들의 리뷰를 분석해서 다음 두 가지를 JSON 형식으로 대답해줘.
    
#     1. summary: 리뷰 내용을 종합해서 2~3문장으로 자연스럽게 요약 (친절하고 부드러운 말투). 맛, 분위기, 서비스 위주.
#     2. keywords: 리뷰에서 가장 많이 언급된 특징 3가지를 단어로 추출 (예: #겉바속촉).
    
#     분석할 가게 이름: {store_name}
#     """

#     user_prompt = f"다음 리뷰들을 분석해줘:\n{combined_reviews}"

#     try:
#         # 5. AI 호출
#         response = chat.invoke([
#             SystemMessage(content=system_prompt),
#             HumanMessage(content=user_prompt)
#         ])
        
#         # 6. 응답 파싱
#         content = response.content
        
#         import json
#         try:
#             result = json.loads(content)
#         except json.JSONDecodeError:
#             result = {
#                 "summary": content,
#                 "keywords": ["AI분석", "빵지순례"]
#             }
            
#         return result

#     except Exception as e:
#         print(f"OpenAI(GMS) Error: {e}")
#         return {
#             "summary": "현재 AI 서버가 혼잡하여 요약을 불러올 수 없습니다.",
#             "keywords": ["데이터분석"]
#         }