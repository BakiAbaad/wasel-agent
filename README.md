# wasel-agent (scaffold) — Local AI Agent for code & project help (MVP)

ملخص
هذا scaffold يوفّر PoC لوكيل ذكاء اصطناعي محلي-أول يمكنه فهرسة كود مشروع محلي، البحث الدلالي في الكود، وتقديم إجابات سياقية عبر LLM (اختياري: OpenAI).

المتطلّبات
- Python 3.11+ (أو 3.10)
- pip
- (اختياري) Docker & docker-compose
- (اختياري) مفتاح OpenAI في حال رغبت باستدعاء GPT عبر API

ملفات مهمة
- app/main.py        -> تطبيق FastAPI (endpoints: /api/index, /api/search, /api/chat)
- requirements.txt   -> تبعيات بايثون
- docker-compose.yml -> لتشغيل الخدمة في حاوية (اختياري)
- app/static/index.html -> واجهة ويب بسيطة للدردشة/البحث
- .env.example       -> مثال لملف إعدادات

تشغيل محلي (طريقة سريعة)
1) افتح موجه الأوامر داخل مجلد المشروع.
2) أنشئ بيئة افتراضية:
   python -m venv .venv
   .venv\Scripts\activate      # على Windows
3) ثبّت الحزم:
   pip install -r requirements.txt
4) انسخ .env.example إلى .env وأضف OPENAI_API_KEY إن أردت استخدام LLM خارجي.
5) شغّل الخادم:
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
6) افتح المتصفح:
   http://localhost:8000/static/index.html

تدفق العمل البسيط
- استخدم زر "Index repo" وأدخل مسار المشروع الذي تريد فهرسته، مثل: ../wasel-wrt-ai
- ثم اكتب سؤالك في مربع المحادثة. إن كان لديك OPENAI_API_KEY سيتم استخدام OpenAI، وإلا سيعتمد على السياق المسترجع فقط.

نصائح أمنية قبل التشغيل على سيرفر
- لا ترفع .env إلى repo
- استخدم Vault أو GitHub Secrets عند النشر
- فعّل GitHub Actions + Dependabot + CodeQL لاحقًا

