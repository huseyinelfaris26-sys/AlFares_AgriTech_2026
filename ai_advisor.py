# -*- coding: utf-8 -*-
"""
المستشار الزراعي الذكي
يدعم: Gemini / OpenAI / وضع عدم الاتصال (FAISS فقط)
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from .vector_search import vector_db

# تحميل متغيرات البيئة
load_dotenv()

AI_PROVIDER = os.getenv("AI_PROVIDER", "offline").lower()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


class AIAdvisor:
    def __init__(self):
        self.provider = "offline"
        self.model = None
        self._init_provider()

    def _init_provider(self):
        """تهيئة مزود الذكاء الاصطناعي حسب الإعدادات"""
        if AI_PROVIDER == "gemini" and GOOGLE_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=GOOGLE_API_KEY)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.provider = "gemini"
                print("✅ تم تفعيل Gemini بنجاح")
            except Exception as e:
                print(f"⚠️ تعذر تفعيل Gemini: {e}")
                self.provider = "offline"

        elif AI_PROVIDER == "openai" and OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.model = OpenAI(api_key=OPENAI_API_KEY)
                self.provider = "openai"
                print("✅ تم تفعيل OpenAI بنجاح")
            except Exception as e:
                print(f"⚠️ تعذر تفعيل OpenAI: {e}")
                self.provider = "offline"
        else:
            print("ℹ️ يعمل في الوضع المحلي (بدون اتصال بمخدمات الذكاء الاصطناعي)")
            self.provider = "offline"

    def ask(self, question: str) -> Dict:
        """استفسار شامل يبحث في قاعدة المعرفة ثم يجيب"""
        # البحث أولاً في قاعدة المعرفة المحلية
        knowledge_results = vector_db.semantic_search(question, top_k=3)
        
        context = ""
        if knowledge_results:
            context = "بناءً على معلومات من قاعدة البيانات:\n"
            for idx, item in enumerate(knowledge_results, 1):
                context += f"{idx}. [{item.get('category', 'عام')}] {item['question']}\nالجواب: {item['answer']}\n\n"

        # إذا كان هناك مزود ذكاء اصطناعي، استخدمه لصياغة إجابة أفضل
        if self.provider != "offline":
            ai_answer = self._call_ai(question, context)
            return {
                "answer": ai_answer,
                "source": self.provider,
                "local_results": knowledge_results,
                "confidence": "high" if knowledge_results else "medium"
            }
        
        # إجابة من قاعدة المعرفة فقط
        if knowledge_results:
            main_answer = knowledge_results[0]['answer']
            return {
                "answer": main_answer,
                "source": "local_knowledge",
                "local_results": knowledge_results,
                "confidence": "medium"
            }
        
        return {
            "answer": "⚠️ عذراً، لا أملك معلومات كافية حول هذا الموضوع حالياً. يمكنك إضافة المعلومة لقاعدة البيانات ليتمكن النظام من الإجابة لاحقاً.",
            "source": "none",
            "local_results": [],
            "confidence": "low"
        }

    def _call_ai(self, question: str, context: str) -> str:
        """استدعاء مزود الذكاء الاصطناعي"""
        system_prompt = """أنت مستشار زراعي عربي متخصص. أجب بلغة عربية واضحة ومبسطة.
استخدم المعلومات المتاحة أولاً، ثم أضف معرفتك العامة. إذا لم تتوفر معلومات، فقل ذلك باحترام."""
        
        full_prompt = f"{system_prompt}\n\n{context}\n\nسؤال المستخدم: {question}"

        try:
            if self.provider == "gemini":
                response = self.model.generate_content(full_prompt)
                return response.text
            
            elif self.provider == "openai":
                response = self.model.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"خطأ في استدعاء الذكاء الاصطناعي: {e}")
            if context:
                return f"⚠️ تعذر الاتصال بالذكاء الاصطناعي، إليك ما وجدته:\n\n{context}"
            return "⚠️ حدث خطأ في الاتصال، يرجى التحقق من مفتاح API أو العمل في الوضع المحلي."

    def diagnose(self, symptoms: str) -> Dict:
        """تشخيص أولي بناءً على الأعراض"""
        question = f"تشخيص: {symptoms}"
        result = self.ask(question)
        
        if result["source"] == "local_knowledge" and not result["local_results"]:
            result["answer"] = """⚠️ هذا تشخيص أولي واسترشادي فقط وليس بديلاً عن خبير.
أنصحك بالتواصل مع مهندس زراعي أو مرشد محلي لفحص النبات والتربة على الطبيعة.

📋 نصائح عامة:
• تحقق من لون الأوراق ونموه
• افحص التربة هل جافة أم رطبة جداً
• ابحث عن علامات آفات أو حشرات
• قارن بالمحاصيل السليمة في منطقتك"""
        
        result["warning"] = "تنبيه: هذه معلومات إرشادية وليست بديلاً عن استشارة مختص."
        return result

    def add_knowledge(self, category: str, question: str, answer: str) -> Dict:
        """إضافة معرفة جديدة للنظام"""
        success = vector_db.add_knowledge(category, question, answer)
        return {"success": success, "message": "✅ تمت الإضافة بنجاح"}

    def get_status(self) -> Dict:
        """حالة النظام"""
        return {
            "provider": self.provider,
            "knowledge_count": len(vector_db.get_all_knowledge()),
            "gemini_available": self.provider == "gemini",
            "openai_available": self.provider == "openai",
            "offline_mode": self.provider == "offline"
        }


# كائن جاهز للاستخدام
advisor = AIAdvisor()
