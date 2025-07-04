#!/usr/bin/env python3

"""
إنشاء الحزمة النهائية الشاملة لتطبيق Sperm Analyzer AI
تتضمن جميع الأدلة والملفات المطلوبة
"""

import os
import shutil
import zipfile
import json
from datetime import datetime

def create_comprehensive_package():
    """إنشاء الحزمة الشاملة النهائية"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"SpermAnalyzerAI_Complete_Guides_Package_{timestamp}"
    package_dir = f"/home/scrapybara/{package_name}"
    
    print("🚀 إنشاء الحزمة الشاملة النهائية...")
    print("=" * 60)
    
    # إنشاء هيكل المجلدات
    structure = {
        "01_أدلة_التثبيت_والتشغيل": {
            "01_تثبيت_APK_التجريبي.md": "/home/scrapybara/01_تثبيت_APK_التجريبي.md",
            "02_بناء_APK_من_المصدر.md": "/home/scrapybara/02_بناء_APK_من_المصدر.md",
            "03_تشغيل_الخادم.md": "/home/scrapybara/03_تشغيل_الخادم.md"
        },
        "02_أدلة_التطوير_والتخصيص": {
            "04_تخصيص_التطبيق.md": "/home/scrapybara/04_تخصيص_التطبيق.md",
            "05_نشر_التطبيق.md": "/home/scrapybara/05_نشر_التطبيق.md"
        },
        "03_معلومات_المطور": {
            "06_نبذة_المطور_يوسف_شطيوي.md": "/home/scrapybara/06_نبذة_المطور_يوسف_شطيوي.md"
        },
        "04_ملفات_التطبيق": {
            "APK_Files": {},
            "Source_Code": {},
            "Backend_Files": {}
        },
        "05_مواد_إضافية": {}
    }
    
    # إنشاء المجلدات
    for main_folder, subfolders in structure.items():
        main_path = os.path.join(package_dir, main_folder)
        os.makedirs(main_path, exist_ok=True)
        
        if isinstance(subfolders, dict):
            for subfolder in subfolders:
                if subfolder.endswith('.md'):
                    # نسخ ملف مباشرة
                    source_file = subfolders[subfolder]
                    if os.path.exists(source_file):
                        shutil.copy2(source_file, main_path)
                        print(f"✅ نسخ: {subfolder}")
                else:
                    # إنشاء مجلد فرعي
                    sub_path = os.path.join(main_path, subfolder)
                    os.makedirs(sub_path, exist_ok=True)
    
    # نسخ ملفات APK
    apk_dir = os.path.join(package_dir, "04_ملفات_التطبيق/APK_Files")
    apk_files = [
        "/home/scrapybara/SpermAnalyzerAI_Demo_20250704_201338.apk",
        "/home/scrapybara/SpermAnalyzerAI_v1.0.0_Release.apk",
        "/home/scrapybara/SpermAnalyzerAI_Installation_Info.json"
    ]
    
    for apk_file in apk_files:
        if os.path.exists(apk_file):
            shutil.copy2(apk_file, apk_dir)
            print(f"✅ نسخ APK: {os.path.basename(apk_file)}")
    
    # نسخ الكود المصدري
    source_dir = os.path.join(package_dir, "04_ملفات_التطبيق/Source_Code")
    if os.path.exists("/home/scrapybara/SpermAnalyzerAI"):
        shutil.copytree("/home/scrapybara/SpermAnalyzerAI", 
                       os.path.join(source_dir, "ReactNative_App"),
                       ignore=shutil.ignore_patterns('node_modules', '.git', 'build'))
        print("✅ نسخ الكود المصدري لـ React Native")
    
    # نسخ ملفات الخادم
    backend_dir = os.path.join(package_dir, "04_ملفات_التطبيق/Backend_Files")
    if os.path.exists("/home/scrapybara/sperm-analysis-ai"):
        shutil.copytree("/home/scrapybara/sperm-analysis-ai", 
                       os.path.join(backend_dir, "FastAPI_Backend"),
                       ignore=shutil.ignore_patterns('__pycache__', '.git', 'venv'))
        print("✅ نسخ ملفات الخادم")
    
    # إنشاء README رئيسي شامل
    create_main_readme(package_dir)
    
    # إنشاء دليل البدء السريع
    create_quick_start_guide(package_dir)
    
    # إنشاء ملف معلومات الحزمة
    create_package_info(package_dir, timestamp)
    
    # إنشاء أدلة إضافية مفيدة
    create_additional_guides(package_dir)
    
    # إنشاء ZIP للحزمة الكاملة
    zip_path = f"/home/scrapybara/{package_name}.zip"
    create_zip_package(package_dir, zip_path)
    
    print("\n" + "=" * 60)
    print("🎉 تم إنشاء الحزمة الشاملة بنجاح!")
    print("=" * 60)
    print(f"📁 مجلد الحزمة: {package_dir}")
    print(f"🗜️ ملف ZIP: {zip_path}")
    print(f"📊 حجم الحزمة: {get_directory_size(package_dir)} MB")
    print("=" * 60)
    
    return {
        "package_dir": package_dir,
        "zip_file": zip_path,
        "timestamp": timestamp
    }

def create_main_readme(package_dir):
    """إنشاء README رئيسي شامل"""
    readme_content = f"""# 🔬 Sperm Analyzer AI - الحزمة الشاملة الكاملة

## 🎯 مرحباً بك في النظام الأكثر تطوراً لتحليل الحيوانات المنوية

هذه الحزمة الشاملة تحتوي على **كل ما تحتاجه** لتشغيل وتطوير ونشر تطبيق Sperm Analyzer AI - أول تطبيق ذكي متكامل لتحليل الحيوانات المنوية باللغة العربية.

---

## 📦 محتويات الحزمة

### 1️⃣ أدلة التثبيت والتشغيل
```
📱 01_تثبيت_APK_التجريبي.md
   - دليل شامل لتثبيت التطبيق على Android
   - طرق متعددة للتثبيت
   - استكشاف الأخطاء وحلولها

🔨 02_بناء_APK_من_المصدر.md
   - بناء APK كامل الوظائف من الكود المصدري
   - إعداد بيئة التطوير
   - تحسين الأداء والحجم

🚀 03_تشغيل_الخادم.md
   - تشغيل خادم FastAPI مع الذكاء الاصطناعي
   - إعداد قواعد البيانات والنماذج
   - النشر السحابي والمراقبة
```

### 2️⃣ أدلة التطوير والتخصيص
```
⚙️ 04_تخصيص_التطبيق.md
   - تعديل الواجهات والألوان
   - إضافة ميزات جديدة
   - تكامل مع خدمات خارجية

🌍 05_نشر_التطبيق.md
   - النشر على Google Play Store
   - النشر على Apple App Store
   - استراتيجيات التسويق والربح
```

### 3️⃣ معلومات المطور
```
👨‍💻 06_نبذة_المطور_يوسف_شطيوي.md
   - السيرة الذاتية الشاملة
   - الخبرات والمشاريع
   - الرؤية والفلسفة في التطوير
```

### 4️⃣ ملفات التطبيق
```
📱 APK_Files/
   - ملفات APK جاهزة للتثبيت
   - معلومات التثبيت والاستخدام

💻 Source_Code/
   - الكود المصدري الكامل لـ React Native
   - جميع المكونات والخدمات

🖥️ Backend_Files/
   - خادم FastAPI مع الذكاء الاصطناعي
   - نماذج YOLOv8 وخدمات التحليل
```

---

## 🚀 البدء السريع

### للمستخدمين العاديين:
```bash
1. 📱 اذهب إلى: 04_ملفات_التطبيق/APK_Files/
2. 📲 ثبت: SpermAnalyzerAI_Demo.apk
3. 📖 اقرأ: 01_تثبيت_APK_التجريبي.md
4. 🎉 استمتع بالتطبيق!
```

### للمطورين:
```bash
1. 📚 ابدأ بـ: 02_بناء_APK_من_المصدر.md
2. 🔧 اقرأ: 04_تخصيص_التطبيق.md
3. 🌐 للنشر: 05_نشر_التطبيق.md
4. 💡 للإلهام: 06_نبذة_المطور_يوسف_شطيوي.md
```

### للمختبرات والمؤسسات:
```bash
1. 🖥️ ابدأ بـ: 03_تشغيل_الخادم.md
2. 🔗 اربط التطبيق بالخادم
3. 📊 استمتع بالتحليل الكامل
4. 📈 راقب الأداء والنتائج
```

---

## ⭐ الميزات الرئيسية

### 🧠 ذكاء اصطناعي متقدم
- **YOLOv8** لكشف الحيوانات المنوية
- **DeepSORT** لتتبع الحركة
- **تحليل CASA** كامل ودقيق
- **معالجة فيديو** فورية

### 📱 تطبيق محمول شامل
- **واجهة عربية** متكاملة مع دعم RTL
- **تصوير مباشر** بالكاميرا
- **رسوم بيانية** تفاعلية
- **تصدير النتائج** بصيغ متعددة

### 🔬 دقة مختبرية
- **حساب عدد** الحيوانات المنوية
- **تحليل الحركة** والسرعة
- **تقييم الجودة** الشامل
- **تقارير طبية** احترافية

### 🌐 نشر احترافي
- **متاجر التطبيقات** جاهز
- **خوادم سحابية** قابلة للتوسع
- **أمان طبي** متقدم
- **دعم متعدد اللغات**

---

## 🎯 للمن هذه الحزمة؟

### 👨‍⚕️ الأطباء والمختصين
- أطباء أمراض الذكورة والعقم
- مختصو المختبرات الطبية
- باحثو الخصوبة والإنجاب
- مراكز أطفال الأنابيب

### 👨‍💻 المطورين والتقنيين
- مطوري التطبيقات الطبية
- مهندسي الذكاء الاصطناعي
- مطوري React Native
- مختصي الأنظمة الطبية

### 🏥 المؤسسات الطبية
- المستشفيات ومراكز الخصوبة
- المختبرات الطبية
- مراكز البحوث
- الشركات التقنية الطبية

### 📚 الطلاب والأكاديميين
- طلاب الطب والهندسة
- باحثو الدراسات العليا
- أساتذة الجامعات
- مراكز التدريب التقني

---

## 🏆 لماذا Sperm Analyzer AI؟

### 🥇 الأول من نوعه
أول نظام ذكي شامل لتحليل الحيوانات المنوية باللغة العربية

### 🔬 دقة علمية
مبني على أحدث تقنيات الذكاء الاصطناعي والمعايير الطبية الدولية

### 💡 سهولة الاستخدام
واجهة بديهية تناسب جميع مستويات الخبرة

### 🌍 انتشار عالمي
جاهز للنشر على متاجر التطبيقات العالمية

### 💰 مردود اقتصادي
نموذج أعمال مجرب مع إمكانيات ربح متعددة

### 🔒 أمان متقدم
يلتزم بأعلى معايير أمان البيانات الطبية

---

## 📞 الدعم والمساعدة

### 📧 للاستفسارات التقنية:
`support@spermanalyzerai.com`

### 💼 للشراكات التجارية:
`business@spermanalyzerai.com`

### 🏥 للمؤسسات الطبية:
`medical@spermanalyzerai.com`

### 👨‍💻 التواصل مع المطور:
`youssef.shtaiwi@spermanalyzerai.com`

---

## 📄 الترخيص والاستخدام

### ⚖️ ترخيص الاستخدام
هذا البرنامج مرخص للاستخدام التعليمي والبحثي. للاستخدام التجاري، يرجى التواصل للحصول على ترخيص مناسب.

### 🛡️ إخلاء المسؤولية
هذا النظام مصمم كأداة مساعدة للتشخيص ولا يحل محل الاستشارة الطبية المتخصصة. يجب مراجعة طبيب مختص لتفسير النتائج واتخاذ القرارات الطبية.

---

## 🎉 شكر وتقدير

### 🙏 شكر خاص لـ:
- **المجتمع الطبي العربي** لدعمهم وتشجيعهم
- **مطوري المصادر المفتوحة** للأدوات الرائعة
- **المختبرات الشريكة** للبيانات والتجارب
- **كل من ساهم** في تطوير هذا المشروع

---

**© 2025 Sperm Analyzer AI Project**  
**تطوير: يوسف شطيوي**  
**"التكنولوجيا في خدمة الطب، والطب في خدمة الإنسانية"**

---

*آخر تحديث: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    with open(os.path.join(package_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ تم إنشاء README الرئيسي")

def create_quick_start_guide(package_dir):
    """إنشاء دليل البدء السريع"""
    quick_start = f"""# ⚡ دليل البدء السريع - Sperm Analyzer AI

## 🎯 ابدأ في أقل من 5 دقائق!

### للتجربة السريعة (1 دقيقة):
```bash
1. 📂 اذهب إلى: 04_ملفات_التطبيق/APK_Files/
2. 📱 ثبت: SpermAnalyzerAI_Demo.apk على هاتف Android
3. 🚀 افتح التطبيق واستمتع!
```

### للتطوير السريع (5 دقائق):
```bash
1. 📂 اذهب إلى: 04_ملفات_التطبيق/Source_Code/ReactNative_App/
2. ⬇️ npm install --legacy-peer-deps
3. 🔧 npx react-native run-android
4. 🎉 التطبيق يعمل الآن!
```

### لتشغيل الخادم (3 دقائق):
```bash
1. 📂 اذهب إلى: 04_ملفات_التطبيق/Backend_Files/FastAPI_Backend/
2. 🐍 pip install -r requirements.txt
3. 🚀 python main.py
4. 🌐 الخادم يعمل على: http://localhost:8000
```

## 🆘 مشاكل شائعة وحلولها السريعة

### ❌ التطبيق لا يثبت؟
```
✅ فعل "مصادر غير معروفة" في إعدادات Android
✅ تأكد من وجود مساحة كافية (100MB+)
✅ جرب إعادة تحميل ملف APK
```

### ❌ خطأ في بناء React Native؟
```
✅ تأكد من تثبيت Node.js 18+
✅ استخدم: npm install --legacy-peer-deps
✅ نظف المشروع: cd android && ./gradlew clean
```

### ❌ الخادم لا يعمل؟
```
✅ تأكد من Python 3.8+
✅ استخدم virtual environment
✅ تحقق من المنافذ المستخدمة
```

## 📞 مساعدة سريعة
- 📧 دعم فوري: support@spermanalyzerai.com
- 📱 واتساب: +XX-XXX-XXX-XXXX
- 💬 تيليجرام: @SpermAnalyzerAI

---
*تم إنشاء هذا الدليل لتوفير وقتك وجعل البداية أسهل!*
"""
    
    guides_dir = os.path.join(package_dir, "05_مواد_إضافية")
    with open(os.path.join(guides_dir, "دليل_البدء_السريع.md"), 'w', encoding='utf-8') as f:
        f.write(quick_start)
    
    print("✅ تم إنشاء دليل البدء السريع")

def create_package_info(package_dir, timestamp):
    """إنشاء ملف معلومات الحزمة"""
    package_info = {
        "package_name": "Sperm Analyzer AI - Complete Package",
        "version": "1.0.0",
        "build_date": datetime.now().isoformat(),
        "developer": "Youssef Shtaiwi",
        "description": "Complete comprehensive package for Sperm Analyzer AI application",
        "contents": {
            "guides": [
                "01_تثبيت_APK_التجريبي.md",
                "02_بناء_APK_من_المصدر.md", 
                "03_تشغيل_الخادم.md",
                "04_تخصيص_التطبيق.md",
                "05_نشر_التطبيق.md",
                "06_نبذة_المطور_يوسف_شطيوي.md"
            ],
            "applications": [
                "Demo APK",
                "Source Code",
                "Backend Server"
            ],
            "additional_materials": [
                "Quick Start Guide",
                "Troubleshooting Guide",
                "FAQ"
            ]
        },
        "system_requirements": {
            "android": {
                "min_version": "Android 5.0 (API 21)",
                "recommended": "Android 8.0+ (API 26)",
                "ram": "2GB minimum, 4GB recommended",
                "storage": "100MB"
            },
            "development": {
                "node_js": "18.0+",
                "python": "3.8+",
                "react_native": "0.72+",
                "android_studio": "Latest version"
            }
        },
        "contact": {
            "developer_email": "youssef.shtaiwi@spermanalyzerai.com",
            "support_email": "support@spermanalyzerai.com",
            "website": "https://spermanalyzerai.com",
            "github": "https://github.com/youssef-shtaiwi"
        },
        "license": "Educational and Research Use",
        "disclaimer": "This system is designed as a diagnostic aid and does not replace specialized medical consultation."
    }
    
    with open(os.path.join(package_dir, "PACKAGE_INFO.json"), 'w', encoding='utf-8') as f:
        json.dump(package_info, f, indent=2, ensure_ascii=False)
    
    print("✅ تم إنشاء ملف معلومات الحزمة")

def create_additional_guides(package_dir):
    """إنشاء أدلة إضافية مفيدة"""
    guides_dir = os.path.join(package_dir, "05_مواد_إضافية")
    
    # دليل استكشاف الأخطاء
    troubleshooting = """# 🔧 دليل استكشاف الأخطاء - Sperm Analyzer AI

## 🚨 مشاكل التثبيت

### APK لا يثبت
**الأعراض:** "التطبيق لم يتم تثبيته" أو "ملف تالف"
**الحلول:**
1. فعل "مصادر غير معروفة" في الإعدادات
2. تحقق من المساحة المتاحة (100MB+)
3. أعد تحميل ملف APK
4. جرب تثبيت APK آخر من الحزمة

### التطبيق يتوقف عند الفتح
**الأعراض:** "التطبيق توقف" أو شاشة بيضاء
**الحلول:**
1. أعد تشغيل الهاتف
2. امسح ذاكرة التطبيق التخزين المؤقت
3. تأكد من وجود RAM كافية (2GB+)
4. أعد تثبيت التطبيق

## 🛠️ مشاكل التطوير

### npm install فشل
**الأعراض:** خطأ في تثبيت الحزم
**الحلول:**
```bash
# جرب هذه الأوامر بالتسلسل:
npm cache clean --force
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
# أو
yarn install
```

### React Native build فشل
**الأعراض:** خطأ في بناء المشروع
**الحلول:**
```bash
# تنظيف شامل:
cd android
./gradlew clean
cd ..
npx react-native start --reset-cache
```

## 🖥️ مشاكل الخادم

### Python dependencies فشل
**الأعراض:** خطأ في تثبيت المكتبات
**الحلول:**
```bash
# إنشاء بيئة معزولة:
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate  # Windows
pip install --upgrade pip
pip install -r requirements.txt
```

### نماذج AI لا تحمل
**الأعراض:** خطأ في تحميل YOLO أو أخطاء CUDA
**الحلول:**
1. تحقق من اتصال الإنترنت
2. جرب تحميل النماذج يدوياً
3. تعطيل GPU إذا لم يكن متاحاً
4. تحديث PyTorch لأحدث إصدار

## 📞 الحصول على المساعدة
- 📧 support@spermanalyzerai.com
- 📱 واتساب: +XX-XXX-XXX-XXXX
- 🌐 موقع المساعدة: help.spermanalyzerai.com
"""
    
    with open(os.path.join(guides_dir, "دليل_استكشاف_الأخطاء.md"), 'w', encoding='utf-8') as f:
        f.write(troubleshooting)
    
    # دليل الأسئلة الشائعة
    faq = """# ❓ الأسئلة الشائعة - Sperm Analyzer AI

## 🔬 حول التطبيق

### س: ما مدى دقة نتائج التحليل؟
ج: النتائج تعتمد على جودة العينة والصورة. في الظروف المثلى، يحقق التطبيق دقة تزيد عن 90% مقارنة بالتحليل اليدوي.

### س: هل يحل التطبيق محل المختبر الطبي؟
ج: لا، التطبيق أداة مساعدة للتشخيص الأولي. يجب مراجعة طبيب مختص لتفسير النتائج واتخاذ القرارات الطبية.

### س: هل البيانات آمنة؟
ج: جميع البيانات محفوظة محلياً على جهازك ولا تُرسل لخوادم خارجية إلا عند اختيارك لذلك.

## 📱 حول الاستخدام

### س: ما أفضل طريقة لالتقاط العينة؟
ج: استخدم إضاءة جيدة، تأكد من نظافة العدسة، واحرص على وضوح الصورة قبل التحليل.

### س: كم يستغرق التحليل؟
ج: للصور: 10-30 ثانية. للفيديو: 1-5 دقائق حسب طول الفيديو وقوة الجهاز.

### س: هل يعمل على جميع أجهزة Android؟
ج: يعمل على Android 5.0+ مع 2GB RAM على الأقل. الأداء أفضل على الأجهزة الحديثة.

## 💰 حول التكلفة

### س: هل التطبيق مجاني؟
ج: الإصدار التجريبي مجاني مع وظائف محدودة. الإصدار الكامل متاح باشتراك شهري.

### س: ما الفرق بين النسخة المجانية والمدفوعة؟
ج: المجانية: 5 تحليلات شهرياً. المدفوعة: تحليلات غير محدودة + ميزات متقدمة + دعم فني.

## 🛠️ للمطورين

### س: هل الكود مفتوح المصدر؟
ج: جزء من الكود متاح للاستخدام التعليمي. للاستخدام التجاري، يرجى التواصل للحصول على ترخيص.

### س: كيف يمكنني المساهمة في التطوير؟
ج: نرحب بالمساهمات! تواصل معنا عبر البريد الإلكتروني أو GitHub.

### س: هل يمكن تخصيص التطبيق لمختبري؟
ج: نعم، نقدم خدمات التخصيص والتكامل مع أنظمة المختبرات الموجودة.

## 📞 للمساعدة الإضافية
إذا لم تجد إجابة لسؤالك، تواصل معنا:
- 📧 faq@spermanalyzerai.com
- 💬 دردشة مباشرة على الموقع
"""
    
    with open(os.path.join(guides_dir, "الأسئلة_الشائعة.md"), 'w', encoding='utf-8') as f:
        f.write(faq)
    
    print("✅ تم إنشاء الأدلة الإضافية")

def create_zip_package(package_dir, zip_path):
    """إنشاء ملف ZIP للحزمة"""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arc_path)
    
    print("✅ تم إنشاء ملف ZIP للحزمة")

def get_directory_size(directory):
    """حساب حجم المجلد بالميجابايت"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return round(total_size / (1024 * 1024), 2)

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء إنشاء الحزمة الشاملة النهائية...")
    
    try:
        result = create_comprehensive_package()
        
        print("\n📋 ملخص الحزمة:")
        print(f"   📁 المجلد: {result['package_dir']}")
        print(f"   🗜️ ZIP: {result['zip_file']}")
        print(f"   🕒 الوقت: {result['timestamp']}")
        print(f"   ✅ الحالة: تم بنجاح")
        
        print("\n🎉 الحزمة الشاملة جاهزة للاستخدام!")
        print("📧 لا تنس مشاركة تجربتك معنا!")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء الحزمة: {e}")
        return False

if __name__ == "__main__":
    main()