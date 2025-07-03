import speech_recognition as sr
import os
import psutil 
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  
import pyttsx3  

WAKE_WORD = "بيكاتشو" 


engine = pyttsx3.init()

# دالة للتفاعل الصوتي
def speak(text):
    engine.say(text)
    engine.runAndWait()


def open_application(command):
    if " يوتيوب" in command:
        os.system("start chrome https://www.youtube.com") 
        speak("تم فتح يوتيوب")


    elif "افتح الحاسبة" in command:
        os.system("start calc")  
        speak("تم فتح الآلة الحاسبة")
    else:
        speak("لم أتمكن من فتح التطبيق المطلوب.")


def calculate(command):
    try:
        result = eval(command)  
        speak(f"نتيجة العملية هي {result}")
    except:
        speak("عذرًا، لم أتمكن من فهم العملية الحسابية.")


def check_battery():
    battery = psutil.sensors_battery()
    percent = battery.percent
    speak(f"مستوى شحن البطارية هو {percent}%")
    print(f"مستوى شحن البطارية هو {percent}%")


def check_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, 0, None)
    volume = interface.GetMasterVolumeLevelScalar()  # الحصول على مستوى الصوت
    speak(f"مستوى الصوت الحالي هو {int(volume*100)}%")
    print(f"مستوى الصوت الحالي هو {int(volume*100)}%")

# دالة للاستماع للأوامر
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("انتظر الامر...قل بيكاتشو لتفعيل المساعد")
        recognizer.adjust_for_ambient_noise(source)  # ضبط حساسية الميكروفون ضد الضجيج
        while True:
            try:
                #audio = recognizer.listen(source, timeout=5)  # يسمع لمدة 5 ثوانٍ
                audio = recognizer.listen(source) 
                text = recognizer.recognize_google(audio, language="ar-SA")  
                print(f"سمعت: {text}")
                if WAKE_WORD in text.lower():  
                    speak("✅ المساعد مستعد لاستقبال الأوامر!")
                    command = text.lower().replace(WAKE_WORD, "").strip()  
                    
                    return command
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                speak("❌ خطأ في الاتصال بخدمة التعرف على الصوت!")
                break 


def execute_command(command):
    if "يوتيوب" in command or "حاسبة" in command:
        open_application(command)
    elif "حساب" in command or "+" in command or "-" in command or "*" in command or "/" in command:
        calculate(command)
    elif "شحن" in command:
        check_battery()
    elif "صوت" in command:
        check_volume()
    else:
        speak("عذرًا، لم أفهم الأمر.")


# تشغيل المساعد الصوتي
def start_assistant():
    speak("المساعد الصوتي جاهز. قل بيكاتشو لتفعيل المساعد.")
    while True:
        command = listen_command()  # الانتظار للأمر من المستخدم
        if command:
            execute_command(command)  # تنفيذ الأمر عند سماعه

# بدء المساعد
if __name__ == "__main__":
    start_assistant()