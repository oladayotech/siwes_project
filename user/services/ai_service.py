# from google import genai
# from django.conf import settings


# client = genai.Client(
#     api_key=settings.GEMINI_API_KEY
# )

# def test_gemini():
#     response = client.models.generate_content(
#         model="gemini-3.8-flash",
#         contents="Say hello from my Django IT Support application."
#     )

#     return response.text

from google import genai
from django.conf import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def test_gemini():
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents="Reply with: Gemini connection successful."
        )

        return response.text

    except Exception as error:
        print(f"Error type: {type(error).__name__}")
        print(f"Error details: {error}")
        raise