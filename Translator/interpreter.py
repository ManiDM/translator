interpreter_lang_texts =	{
  "en": "Touch the microphone of your language to start speaking",
  "bn": "কথা বলতে শুরু করতে আপনার ভাষার মাইক্রোফোনটি স্পর্শ করুন",
  "zh": "触摸您所用语言的麦克风即可开始讲话",
  "ar": "المس ميكروفون لغتك لبدء التحدث",
  "fr": "Touchez le microphone de votre langue pour commencer à parler",
  "hi": "बोलना शुरू करने के लिए अपनी भाषा के माइक्रोफ़ोन को स्पर्श करें",
  "id": "Sentuh mikrofon bahasa Anda untuk mulai berbicara",
  "pt": "Toque no microfone do seu idioma para começar a falar",
  "ru": "Коснитесь микрофона своего языка, чтобы начать говорить",
  "es": "Toca el micrófono de tu idioma para empezar a hablar."
}
interpreter_lang_names = {
  "en": "English",
  "bn": "বাংলা",
  "zh": "中国人",
  "ar": "عربى",
  "fr": "français",
  "hi": "हिंदी",
  "id": "Indonesia",
  "pt": "português",
  "ru": "русский",
  "es": "español"
}

def interpreter_lang_name(text):
	return interpreter_lang_names[text]
def interpreter_lang_text(text):
	return interpreter_lang_texts[text]
