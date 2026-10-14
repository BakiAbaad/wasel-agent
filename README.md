# wasel-agent (scaffold) — Local AI Agent for code & project help (MVP)

ملخص
هذا scaffold يوفّر PoC لوكيل ذكاء اصطناعي محلي-أول يمكنه فهرسة كود مشروع محلي، البحث الدلالي في الكود، وتقديم إجابات سياقية عبر LLM (اختياري: OpenAI).

المتطلّبات
- Python 3.11+
- pip
- (اختياري) Docker & docker-compose
- (اختياري) مفتاح OpenAI

تشغيل محلي
1) افتح موجه الأوامر داخل مجلد المشروع.
2) أنشئ بيئة افتراضية:
   python -m venv .venv
   .venv\Scripts\activate
3) ثبّت الحزم:
   pip install -r requirements.txt
4) انسخ .env.example إلى .env وادخل مفتاح OpenAI إن رغبت:
   OPENAI_API_KEY=sk-...
5) شغّل الخادم:
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
6) افتح المتصفح:
   http://localhost:8000/static/index.html

الوظيفة الأساسية
- Index repo: فهرسة مجلد مشروع محلي
- Search: البحث الدلالي داخل المشروع
- Chat: سؤال الوكيل عن المشروع، مع استخدام السياق المسترجع

ملاحظات أمنية
- لا ترفع .env إلى المستودع
- استخدم GitHub Secrets / Vault عند النشر
- فعّل CI Security checks لاحقًا: Dependabot، CodeQL، Semgrep، Trivy
