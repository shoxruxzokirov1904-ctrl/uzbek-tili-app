from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import json
import random
from datetime import datetime
import os

# Ekran o'lchamini mobil telefon uchun sozlash
Window.size = (360, 640)  # Standard mobil o'lcham

class RoundedButton(Button):
    """Yumaloq burchakli tugma"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    
    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*get_color_from_hex('#3498db'))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[20])

class LessonCard(BoxLayout):
    """Dars kartasi"""
    def __init__(self, lesson_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(5)
        self.padding = dp(10)
        self.size_hint_y = None
        self.height = dp(120)
        
        # Kartaning asosiy rangi
        with self.canvas.before:
            Color(*get_color_from_hex('#ffffff'))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
            Color(*get_color_from_hex('#3498db'))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[15], width=dp(2))
        
        # Dars ma'lumotlari
        title_label = Label(
            text=lesson_data['title'],
            font_size=sp(18),
            bold=True,
            color=get_color_from_hex('#2c3e50'),
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(title_label)
        
        desc_label = Label(
            text=lesson_data['description'],
            font_size=sp(12),
            color=get_color_from_hex('#7f8c8d'),
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(desc_label)
        
        # Progress va holat
        progress_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30)
        )
        
        progress_label = Label(
            text=f"Ball: {lesson_data.get('score', 0)}",
            font_size=sp(12),
            color=get_color_from_hex('#f39c12')
        )
        progress_layout.add_widget(progress_label)
        
        status_label = Label(
            text="✅ Tugatilgan" if lesson_data.get('completed') else "⭕ Davom etmoqda",
            font_size=sp(12),
            color=get_color_from_hex('#2ecc71') if lesson_data.get('completed') else get_color_from_hex('#e74c3c')
        )
        progress_layout.add_widget(status_label)
        
        self.add_widget(progress_layout)

class HomeScreen(Screen):
    """Bosh sahifa"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Sarlavha
        title = Label(
            text="🎓 O'zbek Tilim",
            font_size=sp(32),
            bold=True,
            color=get_color_from_hex('#2c3e50'),
            size_hint_y=None,
            height=dp(60)
        )
        layout.add_widget(title)
        
        # Statistikalar
        stats_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(120))
        
        stats = [
            ("Umumiy ball", "250", "#3498db"),
            ("Kunlik streyk", "5 kun", "#e74c3c"),
            ("Bajarilgan darslar", "3", "#2ecc71"),
            ("O'rganilgan so'zlar", "45", "#f39c12")
        ]
        
        for text, value, color in stats:
            stat_box = BoxLayout(orientation='vertical', padding=dp(10))
            with stat_box.canvas.before:
                Color(*get_color_from_hex(color))
                RoundedRectangle(pos=stat_box.pos, size=stat_box.size, radius=[10])
            
            stat_label = Label(
                text=text,
                font_size=sp(12),
                color=get_color_from_hex('#ffffff'),
                size_hint_y=None,
                height=dp(20)
            )
            stat_box.add_widget(stat_label)
            
            value_label = Label(
                text=value,
                font_size=sp(24),
                bold=True,
                color=get_color_from_hex('#ffffff'),
                size_hint_y=None,
                height=dp(40)
            )
            stat_box.add_widget(value_label)
            
            stats_layout.add_widget(stat_box)
        
        layout.add_widget(stats_layout)
        
        # Navigatsiya tugmalari
        nav_buttons = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, height=dp(300))
        
        buttons = [
            ("📚 Darslar", self.goto_lessons, "#3498db"),
            ("📖 Lug'at", self.goto_vocabulary, "#2ecc71"),
            ("📝 Test", self.goto_quiz, "#e74c3c"),
            ("📊 Statistika", self.goto_stats, "#f39c12"),
            ("⚙️ Sozlamalar", self.goto_settings, "#9b59b6")
        ]
        
        for text, callback, color in buttons:
            btn = Button(
                text=text,
                font_size=sp(18),
                background_normal='',
                background_color=get_color_from_hex(color),
                size_hint_y=None,
                height=dp(50)
            )
            btn.bind(on_press=callback)
            nav_buttons.add_widget(btn)
        
        layout.add_widget(nav_buttons)
        
        # Kunlik maqsad
        daily_goal = Label(
            text="Kunlik maqsad: 10 ta yangi so'z o'rganing",
            font_size=sp(14),
            italic=True,
            color=get_color_from_hex('#95a5a6')
        )
        layout.add_widget(daily_goal)
        
        self.add_widget(layout)
    
    def goto_lessons(self, instance):
        self.manager.current = 'lessons'
    
    def goto_vocabulary(self, instance):
        self.manager.current = 'vocabulary'
    
    def goto_quiz(self, instance):
        self.manager.current = 'quiz'
    
    def goto_stats(self, instance):
        self.manager.current = 'stats'
    
    def goto_settings(self, instance):
        self.manager.current = 'settings'

class LessonsScreen(Screen):
    """Darslar sahifasi"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'lessons'
        
        layout = BoxLayout(orientation='vertical')
        
        # Sarlavha va orqaga tugmasi
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        
        back_btn = Button(
            text="←",
            font_size=sp(24),
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            background_color=get_color_from_hex('#3498db')
        )
        back_btn.bind(on_press=self.goto_home)
        header.add_widget(back_btn)
        
        title = Label(
            text="📚 Darslar",
            font_size=sp(24),
            bold=True,
            color=get_color_from_hex('#2c3e50')
        )
        header.add_widget(title)
        
        layout.add_widget(header)
        
        # Darslar ro'yxati
        scroll = ScrollView()
        lessons_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20), size_hint_y=None)
        lessons_layout.bind(minimum_height=lessons_layout.setter('height'))
        
        # Namuna darslar
        sample_lessons = [
            {
                'title': "Salomlashish",
                'description': "Asosiy salomlar va tanishish",
                'score': 85,
                'completed': True
            },
            {
                'title': "Oilaviy so'zlar",
                'description': "Oila a'zolari va qarindoshlar",
                'score': 70,
                'completed': True
            },
            {
                'title': "Raqamlar",
                'description': "1 dan 100 gacha raqamlar",
                'score': 0,
                'completed': False
            },
            {
                'title': "Vaqt so'zlari",
                'description': "Kun, oy, fasllar",
                'score': 0,
                'completed': False
            },
            {
                'title': "Ovqatlanish",
                'description': "Restoranda buyurtma berish",
                'score': 0,
                'completed': False
            }
        ]
        
        for lesson in sample_lessons:
            card = LessonCard(lesson_data=lesson)
            card.bind(on_touch_down=lambda instance, touch, l=lesson: self.open_lesson(l) 
                     if instance.collide_point(*touch.pos) else None)
            lessons_layout.add_widget(card)
        
        scroll.add_widget(lessons_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def goto_home(self, instance):
        self.manager.current = 'home'
    
    def open_lesson(self, lesson):
        """Darsni ochish"""
        popup = Popup(
            title=lesson['title'],
            content=Label(text=f"Darsni boshlashni xohlaysizmi?\n\n{lesson['description']}"),
            size_hint=(0.8, 0.4)
        )
        
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        start_btn = Button(text="Boshlash", background_color=get_color_from_hex('#2ecc71'))
        start_btn.bind(on_press=lambda x: self.start_lesson(lesson, popup))
        btn_layout.add_widget(start_btn)
        
        cancel_btn = Button(text="Bekor qilish", background_color=get_color_from_hex('#e74c3c'))
        cancel_btn.bind(on_press=popup.dismiss)
        btn_layout.add_widget(cancel_btn)
        
        popup.content = BoxLayout(orientation='vertical')
        popup.content.add_widget(Label(text=f"Darsni boshlashni xohlaysizmi?\n\n{lesson['description']}"))
        popup.content.add_widget(btn_layout)
        
        popup.open()
    
    def start_lesson(self, lesson, popup):
        """Darsni boshlash"""
        popup.dismiss()
        # Bu yerda dars oynasiga o'tish kerak
        # Soddalik uchun xabar chiqaramiz
        from kivy.uix.popup import Popup
        Popup(
            title="Dars boshlandi",
            content=Label(text=f"{lesson['title']} darsini o'qiyapsiz..."),
            size_hint=(0.8, 0.4)
        ).open()

class VocabularyScreen(Screen):
    """Lug'at sahifasi"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'vocabulary'
        
        layout = BoxLayout(orientation='vertical')
        
        # Sarlavha va orqaga tugmasi
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        
        back_btn = Button(
            text="←",
            font_size=sp(24),
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            background_color=get_color_from_hex('#2ecc71')
        )
        back_btn.bind(on_press=self.goto_home)
        header.add_widget(back_btn)
        
        title = Label(
            text="📖 Lug'at",
            font_size=sp(24),
            bold=True,
            color=get_color_from_hex('#2c3e50')
        )
        header.add_widget(title)
        
        layout.add_widget(header)
        
        # Qidiruv paneli
        search_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), padding=dp(10))
        
        self.search_input = TextInput(
            hint_text="So'z qidirish...",
            multiline=False,
            size_hint_x=0.7
        )
        search_layout.add_widget(self.search_input)
        
        search_btn = Button(
            text="Qidirish",
            size_hint_x=0.3,
            background_color=get_color_from_hex('#3498db')
        )
        search_btn.bind(on_press=self.search_word)
        search_layout.add_widget(search_btn)
        
        layout.add_widget(search_layout)
        
        # Lug'at ro'yxati
        scroll = ScrollView()
        self.words_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20), size_hint_y=None)
        self.words_layout.bind(minimum_height=self.words_layout.setter('height'))
        
        # Namuna so'zlar
        sample_words = [
            {"uzbek": "salom", "english": "hello", "category": "asosiy"},
            {"uzbek": "raxmat", "english": "thank you", "category": "asosiy"},
            {"uzbek": "kechirasiz", "english": "excuse me", "category": "asosiy"},
            {"uzbek": "ota", "english": "father", "category": "oila"},
            {"uzbek": "ona", "english": "mother", "category": "oila"},
            {"uzbek": "bir", "english": "one", "category": "raqamlar"},
            {"uzbek": "ikki", "english": "two", "category": "raqamlar"},
            {"uzbek": "bugun", "english": "today", "category": "vaqt"}
        ]
        
        self.display_words(sample_words)
        
        scroll.add_widget(self.words_layout)
        layout.add_widget(scroll)
        
        # Yangi so'z qo'shish tugmasi
        add_btn = Button(
            text="+ Yangi so'z qo'shish",
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#9b59b6')
        )
        add_btn.bind(on_press=self.add_new_word)
        layout.add_widget(add_btn)
        
        self.add_widget(layout)
    
    def goto_home(self, instance):
        self.manager.current = 'home'
    
    def display_words(self, words):
        """So'zlarni ko'rsatish"""
        self.words_layout.clear_widgets()
        
        for word in words:
            word_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
            
            with word_box.canvas.before:
                Color(*get_color_from_hex('#ecf0f1'))
                RoundedRectangle(pos=word_box.pos, size=word_box.size, radius=[10])
            
            # O'zbekcha so'z
            uz_label = Label(
                text=word['uzbek'],
                font_size=sp(16),
                bold=True,
                color=get_color_from_hex('#2c3e50'),
                size_hint_x=0.3
            )
            word_box.add_widget(uz_label)
            
            # Inglizcha tarjima
            en_label = Label(
                text=word['english'],
                font_size=sp(16),
                color=get_color_from_hex('#3498db'),
                size_hint_x=0.4
            )
            word_box.add_widget(en_label)
            
            # Kategoriya
            cat_label = Label(
                text=word['category'],
                font_size=sp(12),
                color=get_color_from_hex('#95a5a6'),
                size_hint_x=0.3
            )
            word_box.add_widget(cat_label)
            
            self.words_layout.add_widget(word_box)
    
    def search_word(self, instance):
        """So'z qidirish"""
        query = self.search_input.text.lower()
        if query:
            # Bu yerda haqiqiy qidiruv logikasi bo'ladi
            # Hozircha faqat xabar chiqaramiz
            from kivy.uix.popup import Popup
            Popup(
                title="Qidiruv natijasi",
                content=Label(text=f"'{query}' so'zi qidirilmoqda..."),
                size_hint=(0.8, 0.3)
            ).open()
    
    def add_new_word(self, instance):
        """Yangi so'z qo'shish"""
        popup = Popup(
            title="Yangi so'z qo'shish",
            size_hint=(0.9, 0.6)
        )
        
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Input maydonlari
        uz_input = TextInput(hint_text="O'zbekcha so'z", multiline=False)
        en_input = TextInput(hint_text="Inglizcha tarjima", multiline=False)
        cat_input = TextInput(hint_text="Kategoriya", multiline=False)
        
        content.add_widget(uz_input)
        content.add_widget(en_input)
        content.add_widget(cat_input)
        
        # Tugmalar
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        
        save_btn = Button(text="Saqlash", background_color=get_color_from_hex('#2ecc71'))
        save_btn.bind(on_press=lambda x: self.save_word(popup, uz_input.text, en_input.text, cat_input.text))
        btn_layout.add_widget(save_btn)
        
        cancel_btn = Button(text="Bekor qilish", background_color=get_color_from_hex('#e74c3c'))
        cancel_btn.bind(on_press=popup.dismiss)
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        popup.content = content
        popup.open()
    
    def save_word(self, popup, uz_word, en_word, category):
        """So'zni saqlash"""
        # Bu yerda so'zni saqlash logikasi bo'ladi
        popup.dismiss()
        from kivy.uix.popup import Popup
        Popup(
            title="Muvaffaqiyat",
            content=Label(text=f"'{uz_word}' so'zi saqlandi!"),
            size_hint=(0.8, 0.3)
        ).open()

class QuizScreen(Screen):
    """Test sahifasi"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'quiz'
        self.current_question = 0
        self.score = 0
        
        self.layout = BoxLayout(orientation='vertical')
        
        # Sarlavha va orqaga tugmasi
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        
        back_btn = Button(
            text="←",
            font_size=sp(24),
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            background_color=get_color_from_hex('#e74c3c')
        )
        back_btn.bind(on_press=self.goto_home)
        header.add_widget(back_btn)
        
        self.title_label = Label(
            text="📝 Test",
            font_size=sp(24),
            bold=True,
            color=get_color_from_hex('#2c3e50')
        )
        header.add_widget(self.title_label)
        
        self.layout.add_widget(header)
        
        # Progress bar
        self.progress_bar = ProgressBar(max=100, size_hint_y=None, height=dp(20))
        self.layout.add_widget(self.progress_bar)
        
        # Savol va javoblar uchun container
        self.content_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        self.layout.add_widget(self.content_layout)
        
        # Namuna test savollari
        self.questions = [
            {
                "question": "'Hello' so'zi o'zbekchada nima degani?",
                "options": ["Salom", "Xayr", "Rahmat", "Yaxshi"],
                "answer": "Salom"
            },
            {
                "question": "'Thank you' so'zi o'zbekchada nima degani?",
                "options": ["Salom", "Xayr", "Rahmat", "Yaxshi"],
                "answer": "Rahmat"
            },
            {
                "question": "'Ota' so'zi ingliz tilida nima degani?",
                "options": ["Mother", "Father", "Brother", "Sister"],
                "answer": "Father"
            }
        ]
        
        self.show_question()
        self.add_widget(self.layout)
    
    def goto_home(self, instance):
        self.manager.current = 'home'
    
    def show_question(self):
        """Savolni ko'rsatish"""
        self.content_layout.clear_widgets()
        
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            
            # Progress yangilash
            progress = ((self.current_question + 1) / len(self.questions)) * 100
            self.progress_bar.value = progress
            
            # Savol matni
            question_label = Label(
                text=question['question'],
                font_size=sp(20),
                bold=True,
                color=get_color_from_hex('#2c3e50'),
                size_hint_y=None,
                height=dp(100)
            )
            self.content_layout.add_widget(question_label)
            
            # Javob variantlari
            self.selected_answer = None
            for option in question['options']:
                btn = ToggleButton(
                    text=option,
                    group='answers',
                    font_size=sp(16),
                    size_hint_y=None,
                    height=dp(60)
                )
                btn.bind(on_press=lambda instance, opt=option: self.select_answer(opt))
                self.content_layout.add_widget(btn)
            
            # Keyingi tugmasi
            next_btn = Button(
                text="Keyingi" if self.current_question < len(self.questions) - 1 else "Testni tugatish",
                size_hint_y=None,
                height=dp(50),
                background_color=get_color_from_hex('#3498db')
            )
            next_btn.bind(on_press=self.next_question)
            self.content_layout.add_widget(next_btn)
        else:
            # Test natijalari
            self.show_results()
    
    def select_answer(self, answer):
        """Javobni tanlash"""
        self.selected_answer = answer
    
    def next_question(self, instance):
        """Keyingi savolga o'tish"""
        if self.selected_answer:
            # Javobni tekshirish
            question = self.questions[self.current_question]
            if self.selected_answer == question['answer']:
                self.score += 1
            
            self.current_question += 1
            self.show_question()
        else:
            from kivy.uix.popup import Popup
            Popup(
                title="Diqqat!",
                content=Label(text="Iltimos, javob tanlang!"),
                size_hint=(0.8, 0.3)
            ).open()
    
    def show_results(self):
        """Test natijalarini ko'rsatish"""
        self.content_layout.clear_widgets()
        
        total = len(self.questions)
        percentage = (self.score / total) * 100
        
        # Natija xabari
        result_text = f"Test tugadi!\n\nNatija: {self.score}/{total}\n({percentage:.1f}%)"
        
        if percentage >= 90:
            result_text += "\n\nA'lo natija! 🎉"
        elif percentage >= 70:
            result_text += "\n\nYaxshi natija! 👍"
        elif percentage >= 50:
            result_text += "\n\nQoniqarli natija! 😊"
        else:
            result_text += "\n\nYana urinib ko'ring! 💪"
        
        result_label = Label(
            text=result_text,
            font_size=sp(24),
            bold=True,
            color=get_color_from_hex('#2c3e50')
        )
        self.content_layout.add_widget(result_label)
        
        # Tugmalar
        btn_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(150))
        
        restart_btn = Button(
            text="Qayta boshlash",
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#2ecc71')
        )
        restart_btn.bind(on_press=self.restart_quiz)
        btn_layout.add_widget(restart_btn)
        
        home_btn = Button(
            text="Bosh menyu",
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#3498db')
        )
        home_btn.bind(on_press=self.goto_home)
        btn_layout.add_widget(home_btn)
        
        self.content_layout.add_widget(btn_layout)
    
    def restart_quiz(self, instance):
        """Testni qayta boshlash"""
        self.current_question = 0
        self.score = 0
        self.show_question()

class StatsScreen(Screen):
    """Statistika sahifasi"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'stats'
        
        layout = BoxLayout(orientation='vertical')
        
        # Sarlavha va orqaga tugmasi
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        
        back_btn = Button(
            text="←",
            font_size=sp(24),
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            background_color=get_color_from_hex('#f39c12')
        )
        back_btn.bind(on_press=self.goto_home)
        header.add_widget(back_btn)
        
        title = Label(
            text="📊 Statistika",
            font_size=sp(24),
            bold=True,
            color=get_color_from_hex('#2c3e50')
        )
        header.add_widget(title)
        
        layout.add_widget(header)
        
        # Statistikalar
        scroll = ScrollView()
        stats_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint_y=None)
        stats_layout.bind(minimum_height=stats_layout.setter('height'))
        
        stats_data = [
            ("Umumiy ball", "250", "#3498db"),
            ("Kunlik streyk", "5 kun", "#e74c3c"),
            ("Bajarilgan darslar", "3", "#2ecc71"),
            ("O'rganilgan so'zlar", "45", "#f39c12"),
            ("Testlarda o'rtacha", "85%", "#9b59b6"),
            ("O'rtacha vaqt", "15 daqiqa/kun", "#1abc9c"),
            ("Boshlangan sana", "2024-01-15", "#34495e"),
            ("Reyting", "O'rta", "#d35400")
        ]
        
        for label, value, color in stats_data:
            stat_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
            
            with stat_box.canvas.before:
                Color(*get_color_from_hex('#f8f9fa'))
                RoundedRectangle(pos=stat_box.pos, size=stat_box.size, radius=[10])
                Color(*get_color_from_hex(color))
                RoundedRectangle(pos=[stat_box.pos[0], stat_box.pos[1]], 
                               size=[dp(5), stat_box.size[1]])
            
            label_widget = Label(
                text=label,
                font_size=sp(16),
                color=get_color_from_hex('#2c3e50'),
                size_hint_x=0.6
            )
            stat_box.add_widget(label_widget)
            
            value_widget = Label(
                text=value,
                font_size=sp(18),
                bold=True,
                color=get_color_from_hex(color),
                size_hint_x=0.4
            )
            stat_box.add_widget(value_widget)
            
            stats_layout.add_widget(stat_box)
        
        scroll.add_widget(stats_layout)
        layout.add_widget(scroll)
        
        # Eksport tugmasi
        export_btn = Button(
            text="Natijalarni saqlash",
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#2c3e50')
        )
        layout.add_widget(export_btn)
        
        self.add_widget(layout)
    
    def goto_home(self, instance):
        self.manager.current = 'home'

class SettingsScreen(Screen):
    """Sozlamalar sahifasi"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'settings'
        
        layout = BoxLayout(orientation='vertical')
        
        # Sarlavha va orqaga tugmasi
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        
        back_btn = Button(
            text="←",
            font_size=sp(24),
            size_hint_x=None,
            width=dp(50),
            background_normal='',
            background_color=get_color_from_hex('#9b59b6')
        )
        back_btn.bind(on_press=self.goto_home)
        header.add_widget(back_btn)
        
        title = Label(
            text="⚙️ Sozlamalar",
            font_size=sp(24),
            bold=True,
            color=get_color_from_hex('#2c3e50')
        )
        header.add_widget(title)
        
        layout.add_widget(header)
        
        # Sozlamalar ro'yxati
        scroll = ScrollView()
        settings_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint_y=None)
        settings_layout.bind(minimum_height=settings_layout.setter('height'))
        
        settings = [
            ("Til", ["O'zbekcha", "Inglizcha", "Ruscha"]),
            ("Ovoz", ["Yoqilgan", "O'chirilgan"]),
            ("Mavzu", ["Och", "Qorong'i"]),
            ("Qiyinlik darajasi", ["Oson", "O'rta", "Qiyin"]),
            ("Bildirishnomalar", ["Yoqilgan", "O'chirilgan"]),
            ("Avtomatik saqlash", ["Yoqilgan", "O'chirilgan"])
        ]
        
        for setting_name, options in settings:
            setting_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80))
            
            # Sozlama nomi
            name_label = Label(
                text=setting_name,
                font_size=sp(16),
                color=get_color_from_hex('#2c3e50'),
                size_hint_y=None,
                height=dp(30)
            )
            setting_box.add_widget(name_label)
            
            # Tugma guruhi
            btn_group = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(40))
            
            for i, option in enumerate(options):
                btn = ToggleButton(
                    text=option,
                    group=setting_name,
                    state='down' if i == 0 else 'normal',
                    size_hint_x=1/len(options)
                )
                btn_group.add_widget(btn)
            
            setting_box.add_widget(btn_group)
            settings_layout.add_widget(setting_box)
        
        scroll.add_widget(settings_layout)
        layout.add_widget(scroll)
        
        # Saqlash tugmasi
        save_btn = Button(
            text="Sozlamalarni saqlash",
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#2ecc71')
        )
        save_btn.bind(on_press=self.save_settings)
        layout.add_widget(save_btn)
        
        self.add_widget(layout)
    
    def goto_home(self, instance):
        self.manager.current = 'home'
    
    def save_settings(self, instance):
        from kivy.uix.popup import Popup
        Popup(
            title="Muvaffaqiyat",
            content=Label(text="Sozlamalar saqlandi!"),
            size_hint=(0.8, 0.3)
        ).open()

class UzbekTiliApp(App):
    def build(self):
        self.title = "O'zbek Tilim"
        
        # Ekran menejeri
        sm = ScreenManager()
        
        # Ekranlarni qo'shish
        sm.add_widget(HomeScreen())
        sm.add_widget(LessonsScreen())
        sm.add_widget(VocabularyScreen())
        sm.add_widget(QuizScreen())
        sm.add_widget(StatsScreen())
        sm.add_widget(SettingsScreen())
        
        return sm

def sp(value):
    """Pikselni ekran o'lchamiga moslashtirish"""
    from kivy.metrics import sp
    return sp(value)

if __name__ == '__main__':
    UzbekTiliApp().run()