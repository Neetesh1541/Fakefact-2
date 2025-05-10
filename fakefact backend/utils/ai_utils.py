import google.generativeai as genai
import language_tool_python
import re
import base64

# Configure Gemini API
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel('gemini-1.5-pro')

# Language Tool
tool = language_tool_python.LanguageTool('en-US')

def auto_correct_text(text):
    matches = tool.check(text)
    return language_tool_python.utils.correct(text, matches)

def ai_call(prompt):
    try:
        response = model.generate_content(prompt)
        text = response.text
        match = re.search(r'(\d{1,3})%', text)
        if match:
            percentage = match.group(1)
            explanation = text.split(match.group(0))[0].strip()
            return {"percentage": percentage, "explanation": explanation}
        return {"message": text}
    except Exception as e:
        return {"error": str(e)}

def ai_image_check(prompt_text, mime_type, base64_img):
    try:
        response = model.generate_content(
            contents=[{
                "role": "user",
                "parts": [
                    {"text": prompt_text},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": base64_img
                        }
                    },
                ]
            }]
        )
        return {"message": response.text}
    except Exception as e:
        return {"error": str(e)}
