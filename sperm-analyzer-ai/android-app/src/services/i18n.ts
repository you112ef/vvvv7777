/**
 * Internationalization Configuration
 * Support for English and Arabic with RTL
 */

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import { getLocales } from 'react-native-localize';

// Translation resources
const resources = {
  en: {
    translation: {
      // Navigation
      home: 'Home',
      camera: 'Camera',
      analysis: 'Analysis',
      results: 'Results',
      settings: 'Settings',
      
      // Home Screen
      welcome: 'Welcome to Sperm Analyzer AI',
      subtitle: 'Revolutionary AI-Powered Fertility Diagnostics',
      startAnalysis: 'Start Analysis',
      viewResults: 'View Results',
      
      // Camera Screen
      takePhoto: 'Take Photo',
      recordVideo: 'Record Video',
      selectFromGallery: 'Select from Gallery',
      cameraPermission: 'Camera permission required',
      
      // Analysis Screen
      analyzing: 'Analyzing...',
      uploadMedia: 'Upload Media',
      processingVideo: 'Processing Video',
      processingImage: 'Processing Image',
      analysisComplete: 'Analysis Complete',
      
      // Results Screen
      spermCount: 'Sperm Count',
      motility: 'Motility',
      progressive: 'Progressive',
      nonProgressive: 'Non-Progressive',
      immotile: 'Immotile',
      concentration: 'Concentration',
      
      // CASA Metrics
      vcl: 'VCL (Curvilinear Velocity)',
      vsl: 'VSL (Straight Line Velocity)',
      vap: 'VAP (Average Path Velocity)',
      lin: 'LIN (Linearity)',
      str: 'STR (Straightness)',
      wob: 'WOB (Wobble)',
      alh: 'ALH (Amplitude Lateral Head)',
      bcf: 'BCF (Beat Cross Frequency)',
      
      // Settings
      language: 'Language',
      theme: 'Theme',
      about: 'About',
      version: 'Version',
      developer: 'Developer',
      
      // Common
      ok: 'OK',
      cancel: 'Cancel',
      save: 'Save',
      delete: 'Delete',
      share: 'Share',
      export: 'Export',
      loading: 'Loading...',
      error: 'Error',
      success: 'Success',
      
      // Units
      micrometersPerSecond: 'μm/s',
      micrometers: 'μm',
      hertz: 'Hz',
      percentage: '%',
      perMilliliter: '/ml',
      
      // Messages
      noResults: 'No results available',
      analysisError: 'Analysis failed. Please try again.',
      fileNotSupported: 'File format not supported',
      processingComplete: 'Processing completed successfully',
    }
  },
  ar: {
    translation: {
      // Navigation
      home: 'الرئيسية',
      camera: 'الكاميرا',
      analysis: 'التحليل',
      results: 'النتائج',
      settings: 'الإعدادات',
      
      // Home Screen
      welcome: 'مرحباً بك في محلل الحيوانات المنوية بالذكاء الاصطناعي',
      subtitle: 'تشخيص الخصوبة الثوري بالذكاء الاصطناعي',
      startAnalysis: 'بدء التحليل',
      viewResults: 'عرض النتائج',
      
      // Camera Screen
      takePhoto: 'التقاط صورة',
      recordVideo: 'تسجيل فيديو',
      selectFromGallery: 'اختيار من المعرض',
      cameraPermission: 'مطلوب إذن الكاميرا',
      
      // Analysis Screen
      analyzing: 'جاري التحليل...',
      uploadMedia: 'رفع الوسائط',
      processingVideo: 'معالجة الفيديو',
      processingImage: 'معالجة الصورة',
      analysisComplete: 'اكتمل التحليل',
      
      // Results Screen
      spermCount: 'عدد الحيوانات المنوية',
      motility: 'الحركة',
      progressive: 'متقدمة',
      nonProgressive: 'غير متقدمة',
      immotile: 'غير متحركة',
      concentration: 'التركيز',
      
      // CASA Metrics
      vcl: 'السرعة المنحنية',
      vsl: 'السرعة المستقيمة',
      vap: 'متوسط سرعة المسار',
      lin: 'الخطية',
      str: 'الاستقامة',
      wob: 'التذبذب',
      alh: 'سعة الحركة الجانبية',
      bcf: 'تردد عبور النبضة',
      
      // Settings
      language: 'اللغة',
      theme: 'المظهر',
      about: 'حول',
      version: 'الإصدار',
      developer: 'المطور',
      
      // Common
      ok: 'موافق',
      cancel: 'إلغاء',
      save: 'حفظ',
      delete: 'حذف',
      share: 'مشاركة',
      export: 'تصدير',
      loading: 'جاري التحميل...',
      error: 'خطأ',
      success: 'نجح',
      
      // Units
      micrometersPerSecond: 'ميكرومتر/ثانية',
      micrometers: 'ميكرومتر',
      hertz: 'هرتز',
      percentage: '%',
      perMilliliter: '/مل',
      
      // Messages
      noResults: 'لا توجد نتائج متاحة',
      analysisError: 'فشل التحليل. يرجى المحاولة مرة أخرى.',
      fileNotSupported: 'تنسيق الملف غير مدعوم',
      processingComplete: 'اكتملت المعالجة بنجاح',
    }
  }
};

// Get device locale
const deviceLocale = getLocales()[0];
const isRTL = deviceLocale?.languageCode === 'ar';

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: deviceLocale?.languageCode || 'en',
    fallbackLng: 'en',
    
    interpolation: {
      escapeValue: false,
    },
    
    react: {
      useSuspense: false,
    },
  });

export default i18n;
export { isRTL };
