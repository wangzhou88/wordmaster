import sys
import os
from utils.audio import audio_manager

# Apply Kivy compatibility patch for Python 3.11+
kivy_compat_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kivy_compat.py')
if os.path.exists(kivy_compat_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("kivy_compat", kivy_compat_path)
    kivy_compat = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kivy_compat)

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.utils import get_color_from_hex
import io
from datetime import datetime, timedelta

# 设置中文字体支持
from kivy.core.text import LabelBase

# 尝试注册多种中文字体
fonts_to_try = [
    ('msyh', 'msyh.ttc'),      # 微软雅黑
    ('msyhbd', 'msyhbd.ttc'),  # 微软雅黑粗体
    ('simhei', 'simhei.ttf'),  # 黑体
    ('simsun', 'simsun.ttc'),  # 宋体
    ('kaiti', 'kaiti.ttc'),    # 楷体
]

DEFAULT_FONT = 'Arial'
for font_name, font_file in fonts_to_try:
    font_path = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Fonts', font_file)
    if os.path.exists(font_path):
        try:
            LabelBase.register(name=font_name, fn_regular=font_path)
            DEFAULT_FONT = font_name
            print(f"成功注册字体: {font_name}")
            break
        except Exception as e:
            print(f"注册字体 {font_name} 失败: {e}")
            continue

# 如果没有找到中文字体，使用默认字体
if DEFAULT_FONT == 'Arial':
    print("未找到中文字体，使用默认字体 Arial")
else:
    print(f"使用字体: {DEFAULT_FONT}")

# ===== 安卓适配优化配置 =====
ANDROID_CONFIG = {
    # 响应式尺寸设计（基于360dp宽度的手机屏幕）
    'base_width': 360,  # 基准宽度（dp）
    'screen_scale_factor': 1.0,  # 全局缩放因子
    
    # 按钮尺寸优化
    'button_height_normal': 48,    # 正常按钮高度（dp）
    'button_height_large': 56,     # 大按钮高度（dp）
    'button_height_small': 40,     # 小按钮高度（dp）
    
    # 文字尺寸优化
    'font_size_title': 20,         # 标题文字大小
    'font_size_subtitle': 16,      # 副标题文字大小
    'font_size_body': 14,          # 正文文字大小
    'font_size_large': 24,         # 大号文字
    'font_size_extra_large': 28,   # 超大号文字
    
    # 间距优化
    'spacing_small': 8,            # 小间距
    'spacing_normal': 12,          # 正常间距
    'spacing_large': 16,           # 大间距
    'spacing_extra_large': 20,     # 超大间距
    
    # 内边距优化
    'padding_small': 8,            # 小内边距
    'padding_normal': 16,          # 正常内边距
    'padding_large': 20,           # 大内边距
    
    # 卡片高度优化
    'card_height_small': 120,      # 小卡片高度
    'card_height_normal': 160,     # 正常卡片高度
    'card_height_large': 200,      # 大卡片高度
    
    # 导航栏优化
    'nav_height': 56,              # 导航栏高度
    'bottom_nav_height': 80,       # 底部导航高度
}

# 响应式尺寸计算函数
def get_scaled_size(size):
    """根据屏幕宽度计算缩放后的尺寸"""
    try:
        current_width = Window.width if hasattr(Window, 'width') else 360
        scale_factor = min(current_width / ANDROID_CONFIG['base_width'], 1.5)  # 最大放大1.5倍
        return int(size * scale_factor)
    except:
        return size

def get_scaled_font_size(size):
    """计算缩放后的字体大小"""
    try:
        current_width = Window.width if hasattr(Window, 'width') else 360
        scale_factor = min(current_width / ANDROID_CONFIG['base_width'], 1.2)  # 字体缩放稍微保守
        return int(size * scale_factor)
    except:
        return size

# 安卓优化的按钮创建函数
def create_android_button(text, size_hint_y=None, height=None, font_size=None, **kwargs):
    """创建适合安卓设备优化的按钮组件"""
    if height is None:
        height = get_scaled_size(ANDROID_CONFIG['button_height_normal'])
    if font_size is None:
        font_size = get_scaled_font_size(ANDROID_CONFIG['font_size_body'])
    
    # 如果用户没有指定背景色，使用默认颜色
    if 'background_color' not in kwargs:
        kwargs['background_color'] = CHILD_COLORS['primary']
    
    # 确保使用中文字体
    if 'font_name' not in kwargs:
        kwargs['font_name'] = DEFAULT_FONT
    
    btn = Button(
        text=text,
        font_size=font_size,
        size_hint_y=size_hint_y,
        height=height,
        color=(0, 0, 0, 1),
        **kwargs
    )
    return btn

# 安卓优化的标签创建函数
def create_android_label(text, font_size=None, **kwargs):
    """创建适合安卓设备优化的标签组件"""
    if font_size is None:
        font_size = get_scaled_font_size(ANDROID_CONFIG['font_size_body'])
    
    # 确保使用中文字体
    if 'font_name' not in kwargs:
        kwargs['font_name'] = DEFAULT_FONT
    
    label = Label(
        text=text,
        font_size=font_size,
        **kwargs
    )
    return label

PHONETIC_FONTS = [
    'Arial Unicode MS',
    'Cambria Math',
    'Consolas',
    'Courier New',
    'Lucida Console',
    'Segoe UI Symbol',
    'Lucida Sans Unicode',
    'Times New Roman',
    'Georgia',
    'DejaVu Sans',
    'DejaVu Sans Mono',
    'Charis SIL',
    'Doulos SIL',
]

PHONETIC_FONT = None
for font_name in PHONETIC_FONTS:
    for ext in ['.ttf', '.ttc', '.fon']:
        font_path = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Fonts', f'{font_name}{ext}')
        if os.path.exists(font_path):
            try:
                LabelBase.register(name='phonetic', fn_regular=font_path)
                PHONETIC_FONT = 'phonetic'
                print(f"音标字体注册成功: {font_name}")
                break
            except Exception as e:
                print(f"注册字体 {font_name} 失败: {e}")
                continue
        font_path_cjk = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Fonts', f'{font_name}.ttf')
        if os.path.exists(font_path_cjk):
            try:
                LabelBase.register(name='phonetic', fn_regular=font_path_cjk)
                PHONETIC_FONT = 'phonetic'
                print(f"音标字体注册成功: {font_name}")
                break
            except Exception as e:
                continue
    if PHONETIC_FONT is not None:
        break

if PHONETIC_FONT is None:
    PHONETIC_FONT = DEFAULT_FONT
    print(f"未找到专用音标字体，使用默认字体: {DEFAULT_FONT}")

CHILD_COLORS = {
    'background': (1.0, 0.95, 0.6, 1),        # 浅黄色背景
    'primary': (1.0, 0.60, 0.20, 1),         # 更鲜艳的橙色
    'secondary': (1.0, 0.95, 0.6, 1),        # 浅黄色辅助色
    'accent': (1.0, 0.95, 0.6, 1),           # 浅黄色强调色
    'warning': (1.0, 0.30, 0.30, 1),         # 更鲜艳的红色
    'card_bg': (1.0, 0.95, 0.6, 1),          # 淡黄色卡片背景
    'text': (0.05, 0.05, 0.05, 1),           # 更深的黑色文字，完全不透明
    'success': (1.0, 0.95, 0.6, 1),          # 浅黄色成功色
    'rating_some': (1.0, 0.60, 0.20, 1),     # 保持橙色
    'rating_vague': (1.0, 0.85, 0.25, 1),    # 更鲜艳的黄色
    'inactive': (1.0, 0.95, 0.6, 1),         # 浅黄色非激活状态
    'border': (1.0, 0.95, 0.6, 1),           # 浅黄色边框
    'info': (1.0, 0.95, 0.6, 1),             # 浅黄色信息色
}

def format_phonetic(phonetic_str):
    """格式化音标字符串，清理不需要的括号和引号"""
    if not phonetic_str:
        return ""
    import re
    cleaned = phonetic_str.strip()
    cleaned = re.sub(r'^\[|\]$', '', cleaned)
    cleaned = re.sub(r'^["\']|["\']$', '', cleaned)
    return cleaned

# 设置窗口背景
Window.clearcolor = CHILD_COLORS['background']


def create_label(text="", font_size=20, bold=False, **kwargs):
    kwargs['color'] = CHILD_COLORS['text']
    if 'font_name' not in kwargs:
        kwargs['font_name'] = DEFAULT_FONT
    return Label(text=text, font_size=font_size, bold=bold, **kwargs)


def create_button(text="", font_size=18, **kwargs):
    if 'background_color' not in kwargs:
        kwargs['background_color'] = CHILD_COLORS['primary']
    kwargs['color'] = (0, 0, 0, 1)
    return Button(text=text, font_name=DEFAULT_FONT, font_size=font_size, **kwargs)


def create_textinput(text="", font_size=18, **kwargs):
    kwargs['font_name'] = DEFAULT_FONT
    kwargs['font_size'] = font_size
    kwargs['write_tab'] = False
    # 设置默认背景颜色，确保在所有背景下都清晰可见
    if 'background_color' not in kwargs:
        kwargs['background_color'] = CHILD_COLORS['card_bg']  # 统一的卡片背景
    if 'foreground_color' not in kwargs:
        kwargs['foreground_color'] = (0, 0, 0, 1)  # 纯黑文字
    # 添加边框以增强可见性
    if 'border' not in kwargs:
        kwargs['border'] = (2, 2, 2, 2)
    return TextInput(text=text, **kwargs)


def create_spinner(text="", values=None, **kwargs):
    font_size = kwargs.pop('font_size', 16)
    spinner = Spinner(text=text, font_name=DEFAULT_FONT, font_size=font_size, **kwargs)
    if values:
        spinner.values = values
    return spinner


# 导入自定义模块
from models.database import db_manager
from models.word import Word
from models.dictionary import Dictionary
from models.learning import LearningRecord
from models.user import User
from utils.speech_recog import speech_recognizer

_buttons_cache = {}

def _get_rating_buttons():
    """获取记忆评级按钮（单例模式）"""
    if '_rating_buttons' not in _buttons_cache:
        _buttons_cache['_rating_buttons'] = [
            ('不认识', 0, CHILD_COLORS['warning']),
            ('有点印象', 1, CHILD_COLORS['rating_some']),
            ('模糊记忆', 2, CHILD_COLORS['rating_vague']),
            ('记得', 3, CHILD_COLORS['secondary']),
            ('非常熟悉', 4, CHILD_COLORS['accent']),
        ]
    return _buttons_cache['_rating_buttons']

_rating_button_callbacks = {}

def _get_rating_callback(rating):
    """获取记忆评级回调函数（单例模式）"""
    if rating not in _rating_button_callbacks:
        def callback(btn_instance):
            try:
                app = App.get_running_app()
                if app is None:
                    return
                root = app.root
                if root is None:
                    return
                if hasattr(root, 'current_screen'):
                    current = root.current_screen
                    if current and hasattr(current, 'rate_memory'):
                        current.rate_memory(rating)
            except Exception as e:
                print(f"Error in rating callback: {e}")
        _rating_button_callbacks[rating] = callback
    return _rating_button_callbacks[rating]

_screen_transition_cache = {}

_screen_widget_pool = {}

def _get_screen_transition(target_screen):
    """获取屏幕切换回调函数（单例模式）"""
    if target_screen not in _screen_transition_cache:
        def callback(btn_instance):
            App.get_running_app().root.current = target_screen
        _screen_transition_cache[target_screen] = callback
    return _screen_transition_cache[target_screen]

def _get_word_card_from_pool():
    """从池中获取单词卡片部件"""
    global _screen_widget_pool
    pool_key = 'word_card'
    if pool_key in _screen_widget_pool and _screen_widget_pool[pool_key]:
        return _screen_widget_pool[pool_key].pop()
    return None

def _return_word_card_to_pool(card):
    """将单词卡片部件返回池中"""
    global _screen_widget_pool
    pool_key = 'word_card'
    if pool_key not in _screen_widget_pool:
        _screen_widget_pool[pool_key] = []
    if len(_screen_widget_pool[pool_key]) < 20:
        _screen_widget_pool[pool_key].append(card)

_dictionary_button_callbacks = {}

def _get_dictionary_callback(action_type):
    """获取词典操作回调函数（单例模式）"""
    if action_type not in _dictionary_button_callbacks:
        def callback(btn_instance, dictionary):
            screen = None
            for screen in App.get_running_app().root.children:
                if hasattr(screen, action_type):
                    getattr(screen, action_type)(dictionary)
                    break
        _dictionary_button_callbacks[action_type] = callback
    return _dictionary_button_callbacks[action_type]

_test_type_callbacks = {}

def _get_test_type_callback(test_type, buttons_ref):
    """获取测试类型选择回调函数（单例模式）"""
    key = (test_type, id(buttons_ref))
    if key not in _test_type_callbacks:
        def callback(btn_instance):
            screen = None
            for screen in App.get_running_app().root.children:
                if hasattr(screen, 'set_test_type'):
                    screen.set_test_type(test_type, buttons_ref)
                    break
        _test_type_callbacks[key] = callback
    return _test_type_callbacks[key]

_widget_pool = {}

def get_widget_from_pool(widget_type, **kwargs):
    """从对象池获取小部件"""
    pool_key = widget_type
    if pool_key in _widget_pool and _widget_pool[pool_key]:
        widget = _widget_pool[pool_key].pop()
        for key, value in kwargs.items():
            if hasattr(widget, key):
                setattr(widget, key, value)
        return widget
    return None

def return_widget_to_pool(widget_type, widget):
    """将小部件返回对象池"""
    pool_key = widget_type
    if pool_key not in _widget_pool:
        _widget_pool[pool_key] = []
    if len(_widget_pool[pool_key]) < 10:
        _widget_pool[pool_key].append(widget)


class ChineseSpinner(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = DEFAULT_FONT
        self.font_size = 16

    def on_open(self):
        super().on_open()
        for i in range(5):
            Clock.schedule_once(self._apply_font_to_dropdown, 0.05 * (i + 1))

    def _apply_font_to_dropdown(self, dt):
        if self.dropdown:
            self._set_font_recursive(self.dropdown)

    def _set_font_recursive(self, widget):
        if hasattr(widget, 'font_name'):
            widget.font_name = DEFAULT_FONT
        if hasattr(widget, 'font_size'):
            widget.font_size = 16
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._set_font_recursive(child)


class LanguageSpinner(BoxLayout):
    current_value = None
    dropdown = None
    dropdown_open = False

    def __init__(self, text="英语", values=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = kwargs.get('size_hint_y', None)
        self.height = kwargs.get('height', 40)
        self.values = values or ("英语", "中文", "日语", "韩语")
        self.current_value = text
        self.dropdown = None

        self.btn = Button(
            text=text,
            font_name=DEFAULT_FONT,
            font_size=16,
            size_hint_y=None,
            height=self.height,
            halign='center'
        )
        self.btn.bind(on_press=self.toggle_dropdown)
        self.add_widget(self.btn)

        arrow = Label(
            text="▼",
            font_name=DEFAULT_FONT,
            font_size=12,
            size_hint_y=None,
            height=self.height,
            size_hint_x=None,
            width=30
        )
        self.add_widget(arrow)

    def toggle_dropdown(self, instance):
        if self.dropdown_open:
            self.close_dropdown()
        else:
            self.open_dropdown()

    def open_dropdown(self):
        if self.dropdown:
            self.close_dropdown()

        content_height = len(self.values) * 40 + 10
        self.dropdown = Popup(size_hint=(None, None), size=(self.btn.width, content_height))
        dropdown_layout = BoxLayout(orientation='vertical', padding=5, spacing=2)
        dropdown_layout.height = content_height

        for value in self.values:
            btn = Button(
                text=value,
                font_name=DEFAULT_FONT,
                font_size=16,
                size_hint_y=None,
                height=40
            )
            btn.bind(on_press=lambda x, v=value: self.select_value(v))
            dropdown_layout.add_widget(btn)

        self.dropdown.content = dropdown_layout
        self.dropdown.open()
        self.dropdown.bind(on_dismiss=self.on_dropdown_dismiss)
        self.dropdown_open = True

    def close_dropdown(self):
        if self.dropdown:
            self.dropdown.dismiss()
            self.dropdown = None
        self.dropdown_open = False

    def on_dropdown_dismiss(self, instance):
        self.dropdown_open = False

    def select_value(self, value):
        self.current_value = value
        self.btn.text = value
        self.close_dropdown()

    def get_text(self):
        return self.current_value

    text = property(get_text)


class Card(BoxLayout):
    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10
        
        # 添加白色背景，确保卡片可见
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*CHILD_COLORS['card_bg'], 1)  # 白色背景
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        # 绑定尺寸变化，更新背景
        self.bind(pos=self.update_bg, size=self.update_bg)
    
    def update_bg(self, instance, value):
        """更新卡片背景矩形大小"""
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size


# 创建默认用户
current_user = User.create_default_user()

# 主界面
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.build_ui()
    
    def add_cute_background(self):
        if hasattr(self, 'bg_color') and self.bg_color:
            self.remove_widget(self.bg_color)
        
        self.bg_color = Widget(size=self.size)
        with self.bg_color.canvas:
            Color(1.0, 0.95, 0.6, 1)
            Rectangle(pos=(0, 0), size=self.size)
        
        self.add_widget(self.bg_color, index=0)
    
    def update_canvas(self, instance, value):
        pass
    
    def build_ui(self):
        # 添加可爱背景
        self.add_cute_background()
        
        # ===== 主布局优化（安卓适配） =====
        layout = BoxLayout(orientation='vertical', 
                          padding=get_scaled_size(ANDROID_CONFIG['padding_normal']), 
                          spacing=get_scaled_size(ANDROID_CONFIG['spacing_normal']))
        
        # ===== 顶部状态栏优化 =====
        top_bar = BoxLayout(size_hint_y=None, 
                           height=get_scaled_size(ANDROID_CONFIG['nav_height']), 
                           spacing=get_scaled_size(ANDROID_CONFIG['spacing_small']))
        
        # 标题 - 使用响应式字体大小
        title_label = create_android_label(text="单词大师", 
                                          font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_title']), 
                                          bold=True)
        top_bar.add_widget(title_label)
        
        # 学习进度 - 添加错误处理和默认值
        try:
            stats = LearningRecord.get_learning_stats(current_user.id)
            progress_text = f"复习:{stats['need_review']} 已学:{stats['learned']}/{stats['total']}"
        except Exception as e:
            print(f"获取学习统计信息失败: {e}")
            progress_text = "复习:0 已学:0/0"
        
        progress_label = create_android_label(text=progress_text, 
                                            font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']))
        top_bar.add_widget(progress_label)
        
        layout.add_widget(top_bar)
        
        # ===== 功能卡片区域优化 =====
        cards_layout = GridLayout(cols=2, 
                                 spacing=get_scaled_size(ANDROID_CONFIG['spacing_normal']), 
                                 size_hint_y=1)
        
        # 学习卡片 - 优化高度和布局，减少20度高度
        learn_card = Card(size_hint_y=None, 
                         height=get_scaled_size(ANDROID_CONFIG['card_height_large'] - 20))
        learn_layout = BoxLayout(orientation='vertical', 
                                padding=get_scaled_size(ANDROID_CONFIG['padding_normal']))
        
        learn_layout.add_widget(create_android_label(text="[学习] 学习新词", 
                                                    font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_subtitle']), 
                                                    bold=True))
        learn_layout.add_widget(create_android_label(text="开始学习新单词", 
                                                    font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body'])))
        
        learn_btn = create_android_button(text="开始学习", 
                                         size_hint_y=None, 
                                         height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                         background_color=CHILD_COLORS['accent'])
        learn_btn.bind(on_press=self.go_to_learning)
        learn_layout.add_widget(learn_btn)
        learn_card.add_widget(learn_layout)
        cards_layout.add_widget(learn_card)
        
        # 复习卡片
        review_card = Card(size_hint_y=None, 
                          height=get_scaled_size(ANDROID_CONFIG['card_height_large'] - 20))
        review_layout = BoxLayout(orientation='vertical', 
                                 padding=get_scaled_size(ANDROID_CONFIG['padding_normal']))
        
        review_layout.add_widget(create_android_label(text="[复习] 复习单词", 
                                                    font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_subtitle']), 
                                                    bold=True))
        # 添加错误处理
        try:
            stats = LearningRecord.get_learning_stats(current_user.id)
            review_text = f"{stats['need_review']} 个单词需要复习"
        except Exception as e:
            print(f"获取复习统计信息失败: {e}")
            review_text = "0 个单词需要复习"
        
        review_layout.add_widget(create_android_label(text=review_text, 
                                                    font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body'])))
        
        review_btn = create_android_button(text="开始复习", 
                                          size_hint_y=None, 
                                          height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                          background_color=CHILD_COLORS['secondary'])
        review_btn.bind(on_press=self.go_to_review)
        review_layout.add_widget(review_btn)
        review_card.add_widget(review_layout)
        cards_layout.add_widget(review_card)
        
        # 测试卡片
        test_card = Card(size_hint_y=None, 
                        height=get_scaled_size(ANDROID_CONFIG['card_height_large'] - 20))
        test_layout = BoxLayout(orientation='vertical', 
                               padding=get_scaled_size(ANDROID_CONFIG['padding_normal']))
        
        test_layout.add_widget(create_android_label(text="[测试] 单词测试", 
                                                   font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_subtitle']), 
                                                   bold=True))
        test_layout.add_widget(create_android_label(text="测试你的单词掌握程度", 
                                                   font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body'])))
        
        test_btn = create_android_button(text="开始测试", 
                                        size_hint_y=None, 
                                        height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                        background_color=CHILD_COLORS['success'])
        test_btn.bind(on_press=self.go_to_test)
        test_layout.add_widget(test_btn)
        test_card.add_widget(test_layout)
        cards_layout.add_widget(test_card)
        
        # 语法练习卡片
        grammar_card = Card(size_hint_y=None, 
                           height=get_scaled_size(ANDROID_CONFIG['card_height_large'] - 20))
        grammar_layout = BoxLayout(orientation='vertical', 
                                  padding=get_scaled_size(ANDROID_CONFIG['padding_normal']))
        grammar_layout.add_widget(create_android_label(text="[语法] 语法练习", 
                                                      font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_subtitle']), 
                                                      bold=True))
        grammar_layout.add_widget(create_android_label(text="语法练习", 
                                                      font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body'])))
        
        grammar_btn = create_android_button(text="语法练习", 
                                           size_hint_y=None, 
                                           height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                           background_color=CHILD_COLORS['accent'])
        grammar_btn.bind(on_press=self.go_to_grammar)
        grammar_layout.add_widget(grammar_btn)
        grammar_card.add_widget(grammar_layout)
        cards_layout.add_widget(grammar_card)
        
        # ===== 底部导航栏优化 =====
        bottom_nav_container = BoxLayout(size_hint_y=None, 
                                        height=get_scaled_size(ANDROID_CONFIG['bottom_nav_height'] + 10),  # 增加高度
                                        spacing=get_scaled_size(ANDROID_CONFIG['spacing_small']),
                                        padding=[10, 5, 10, 10])  # 添加内边距
        
        # 添加背景和边框涂层
        with bottom_nav_container.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*CHILD_COLORS['background'], 1)  # 背景色
            self.nav_bg_rect = Rectangle(pos=bottom_nav_container.pos, size=bottom_nav_container.size)
            Color(*CHILD_COLORS['border'], 1)  # 边框色
            Rectangle(pos=(bottom_nav_container.x, bottom_nav_container.y - 2), 
                     size=(bottom_nav_container.width, 2))  # 顶部边框
        
        bottom_nav_container.bind(size=self._update_nav_background, pos=self._update_nav_background)
        
        bottom_nav = BoxLayout(spacing=get_scaled_size(ANDROID_CONFIG['spacing_small']))

        # 使用专门的导航按钮样式
        home_btn = create_android_button(text="首页", 
                                        font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                        size_hint_x=1.0)
        home_btn.bind(on_press=_get_screen_transition('main'))
        
        learn_nav_btn = create_android_button(text="学习", 
                                            font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                            size_hint_x=1.0)
        learn_nav_btn.bind(on_press=_get_screen_transition('learning'))
        
        review_nav_btn = create_android_button(text="复习", 
                                             font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                             size_hint_x=1.0)
        review_nav_btn.bind(on_press=_get_screen_transition('review'))
        
        test_nav_btn = create_android_button(text="测试", 
                                           font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                           size_hint_x=1.0)
        test_nav_btn.bind(on_press=_get_screen_transition('test'))
        
        dict_nav_btn = create_android_button(text="词库", 
                                           font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                           size_hint_x=1.0)
        dict_nav_btn.bind(on_press=_get_screen_transition('dictionary'))
        
        reading_nav_btn = create_android_button(text="阅读", 
                                              font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                              size_hint_x=1.0)
        reading_nav_btn.bind(on_press=_get_screen_transition('reading'))
        
        bottom_nav.add_widget(home_btn)
        bottom_nav.add_widget(learn_nav_btn)
        bottom_nav.add_widget(review_nav_btn)
        bottom_nav.add_widget(test_nav_btn)
        bottom_nav.add_widget(dict_nav_btn)
        bottom_nav.add_widget(reading_nav_btn)
        
        bottom_nav_container.add_widget(bottom_nav)
        
        # 将卡片区域添加到主布局（这里之前遗漏了！）
        layout.add_widget(cards_layout)
        layout.add_widget(bottom_nav_container)
        
        # 将主布局添加到屏幕
        self.add_widget(layout)
    
    def _update_nav_background(self, instance, value):
        """更新底部导航栏背景"""
        if hasattr(self, 'nav_bg_rect'):
            self.nav_bg_rect.pos = instance.pos
            self.nav_bg_rect.size = instance.size
    
    def go_to_learning(self, instance):
        self.manager.current = 'learning'
    
    def go_to_review(self, instance):
        self.manager.current = 'review'
    
    def go_to_test(self, instance):
        self.manager.current = 'test'
    
    def go_to_dictionary(self, instance):
        self.manager.current = 'dictionary'
    
    def go_to_reading(self, instance):
        self.manager.current = 'reading'
    
    def go_to_statistics(self, instance):
        self.manager.current = 'statistics'
    
    def go_to_vocabulary(self, instance):
        self.manager.current = 'vocabulary'
    
    def go_to_grammar(self, instance):
        self.manager.current = 'grammar'
    
    def open_settings(self, instance):
        # 这里可以实现设置弹窗
        popup = Popup(title="设置", title_font=DEFAULT_FONT, size_hint=(0.8, 0.8))
        
        settings_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 每日目标设置
        daily_target_layout = BoxLayout(size_hint_y=None, height=50)
        daily_target_layout.add_widget(create_label(text="每日学习目标"))
        
        # 保存按钮
        save_btn = create_button(text="保存设置", size_hint_y=None, height=50)
        save_btn.bind(on_press=lambda x: self.save_settings(popup, {'daily_target': int(daily_target_input.text)}))
        settings_layout.add_widget(save_btn)
        
        popup.content = settings_layout
        popup.open()
    
    def toggle_setting(self, setting_name, button):
        current_value = current_user.settings.get(setting_name, True)
        new_value = not current_value
        current_user.settings[setting_name] = new_value
        button.text = "开" if new_value else "关"
    
    def save_settings(self, popup, new_settings):
        current_user.update_settings(new_settings)
        popup.dismiss()

# 学习界面
class LearningScreen(Screen):
    _word_cache = {}
    _dictionary_cache = None
    
    def __init__(self, **kwargs):
        super(LearningScreen, self).__init__(**kwargs)
        self.current_word = None
        self.words = []
        self.current_index = 0
        self._data_loaded = False
        self._start_time = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 顶部标题栏
        top_bar = BoxLayout(size_hint_y=None, height=50)
        back_btn = create_button(text="< 返回", on_press=self.on_back)
        top_bar.add_widget(back_btn)
        
        self.progress_label = create_label(text="[进度] 0/0")
        top_bar.add_widget(self.progress_label)
        
        dict_btn = create_button(text="选择词库", on_press=self.show_dictionary_selection)
        top_bar.add_widget(dict_btn)
        
        layout.add_widget(top_bar)
        
        # 单词卡片
        self.word_card = Card(size_hint_y=1, padding=20)
        self.word_layout = BoxLayout(orientation='vertical', spacing=12)
        
        # 单词和音标分别显示
        word_phonetic_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=60, spacing=2)
        
        # 单词
        self.word_label = create_label(text="点击'开始学习'加载单词", font_size=28, bold=True, size_hint_y=None, height=30)
        word_phonetic_layout.add_widget(self.word_label)
        
        # 音标（使用专门字体）
        self.phonetic_label = create_label(text="", font_size=18, font_name=PHONETIC_FONT, 
                                         size_hint_y=None, height=25, color=(1.0, 0.95, 0.6, 1))
        word_phonetic_layout.add_widget(self.phonetic_label)
        
        # 发音按钮
        self.pronunciation_btn = create_button(text="🔊", font_size=24, size_hint_y=None, height=40, 
                                             background_color=CHILD_COLORS['accent'], on_press=self.play_pronunciation)
        self.pronunciation_btn.opacity = 0  # 初始隐藏
        self.pronunciation_btn.disabled = True
        
        word_header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        word_header_layout.add_widget(word_phonetic_layout)
        word_header_layout.add_widget(self.pronunciation_btn)
        self.word_layout.add_widget(word_header_layout)
        
        # 翻译
        self.translation_label = create_label(text="", font_size=24, shorten=True, text_size=(None, None), halign='left', valign='middle')
        self.word_layout.add_widget(self.translation_label)
        
        # 例句
        self.example_label = create_label(text="", font_size=16, italic=True, shorten=True, shorten_from='right', text_size=(None, None), size_hint_y=None, height=30)
        self.word_layout.add_widget(self.example_label)
        
        # 图片（延迟加载）
        self.word_image = Image(source="", size_hint_y=None, height=200, allow_stretch=True, keep_ratio=True)
        self.word_image.opacity = 0
        self.word_layout.add_widget(self.word_image)
        
        self.word_card.add_widget(self.word_layout)
        layout.add_widget(self.word_card)
        
        # 操作按钮
        buttons_layout = BoxLayout(spacing=10, size_hint_y=None, height=70)
        
        prev_btn = create_button(text="< 上一张", on_press=self.prev_word)
        buttons_layout.add_widget(prev_btn)
        
        self.show_btn = create_button(text="显示翻译", on_press=self.toggle_translation)
        buttons_layout.add_widget(self.show_btn)
        
        next_btn = create_button(text="下一张 >", on_press=self.next_word)
        buttons_layout.add_widget(next_btn)
        
        layout.add_widget(buttons_layout)
        
        self.add_widget(layout)
    
    def on_enter(self):
        if not self._data_loaded:
            Clock.schedule_once(lambda dt: self.load_words(), 0.1)
    
    def on_leave(self):
        pass
    
    def on_back(self, instance):
        if self._start_time and hasattr(current_user, 'id'):
            duration = int((datetime.now() - self._start_time).total_seconds())
            if duration > 5:
                LearningRecord.record_learning_time(current_user.id, duration, 'test')
        self.manager.current = 'main'
    
    def load_words(self):
        # 获取所有词库
        dictionaries = Dictionary.get_all()
        
        if not dictionaries:
            # 如果没有词库，显示提示
            self.word_label.text = "没有可用的词库"
            self.translation_label.text = "请先在词库管理中创建或导入词库"
            self.example_label.text = ""
            self.progress_label.text = "进度: 0/0"
            
            # 隐藏发音按钮
            self.pronunciation_btn.opacity = 0
            self.pronunciation_btn.disabled = True
            return
        
        # 使用第一个词库
        dictionary = dictionaries[0]
        
        # 获取词库中的所有单词
        self.words = Word.get_by_dictionary(dictionary.id)
        
        if not self.words:
            # 如果词库中没有单词，显示提示
            self.word_label.text = f"词库 '{dictionary.name}' 中没有单词"
            self.translation_label.text = "请先在词库管理中添加单词"
            self.example_label.text = ""
            self.progress_label.text = "进度: 0/0"
            
            # 隐藏发音按钮
            self.pronunciation_btn.opacity = 0
            self.pronunciation_btn.disabled = True
            return
        
        # 创建学习记录（如果不存在的话）
        LearningRecord.create_initial_records(current_user.id, dictionary.id)
        
        # 开始计时
        self._start_time = datetime.now()
        
        # 重置索引
        self.current_index = 0
        
        # 显示第一个单词
        self.show_word()
    
    def show_word(self):
        if not self.words or self.current_index < 0 or self.current_index >= len(self.words):
            return
        
        # 获取当前单词
        self.current_word = self.words[self.current_index]
        
        # 更新UI - 单词和音标分别显示
        self.word_label.text = self.current_word.word
        
        phonetic_text = format_phonetic(self.current_word.phonetic)
        if phonetic_text:
            self.phonetic_label.text = f"[{phonetic_text}]"
            self.phonetic_label.opacity = 1
        else:
            self.phonetic_label.text = ""
            self.phonetic_label.opacity = 0
        
        # 初始隐藏翻译
        self.translation_label.text = "点击'显示翻译'查看翻译"
        self.example_label.text = ""
        
        # 更新图片
        if self.current_word.image_path and os.path.exists(self.current_word.image_path):
            self.word_image.source = self.current_word.image_path
            self.word_image.opacity = 1
        else:
            self.word_image.opacity = 0
        
        # 更新进度
        self.progress_label.text = f"[进度] {self.current_index + 1}/{len(self.words)}"
        
        # 显示并启用发音按钮
        self.pronunciation_btn.opacity = 1
        self.pronunciation_btn.disabled = False
        
        # 预加载当前单词的发音
        if self.current_word and self.current_word.word:
            audio_manager.preload_word_audio(self.current_word.word, 'en')
    
    def toggle_translation(self, instance):
        if self.current_word:
            if self.translation_label.text == "点击'显示翻译'查看翻译":
                # 显示翻译
                self.translation_label.text = self.current_word.translation
                self.example_label.text = self.current_word.example or ""
                instance.text = "隐藏翻译"
            else:
                # 隐藏翻译
                self.translation_label.text = "点击'显示翻译'查看翻译"
                self.example_label.text = ""
                instance.text = "显示翻译"
    
    def prev_word(self, instance):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_word()
    
    def next_word(self, instance):
        if self.current_index < len(self.words) - 1:
            self.current_index += 1
            self.show_word()
    
    def play_pronunciation(self, instance):
        """播放当前单词的发音"""
        if self.current_word and self.current_word.word:
            try:
                # 使用有道词典TTS功能播放单词发音
                audio_path = audio_manager.get_word_audio_path(self.current_word.word, 'en')
                if audio_path:
                    audio_manager.play_audio(audio_path)
                else:
                    # 备用方案：使用gTTS直接播放
                    print("使用备用发音方案")
            except Exception as e:
                print(f"发音播放失败: {e}")
                # 可以显示一个提示消息
                pass
    
    def show_dictionary_selection(self, instance):
        # 这里可以实现词库选择弹窗
        popup = Popup(title="选择词库", title_font=DEFAULT_FONT, size_hint=(0.8, 0.8))
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 获取所有词库
        dictionaries = Dictionary.get_all()
        
        if not dictionaries:
            layout.add_widget(create_label(text="没有可用的词库"))
        else:
            # 词库列表
            for dictionary in dictionaries:
                dict_btn = create_button(text=f"{dictionary.name} ({dictionary.word_count}个单词)")
                dict_btn.bind(on_press=lambda x, d=dictionary: self.select_dictionary(popup, d))
                layout.add_widget(dict_btn)
        
        # 取消按钮
        cancel_btn = create_button(text="取消", size_hint_y=None, height=50)
        cancel_btn.bind(on_press=popup.dismiss)
        layout.add_widget(cancel_btn)
        
        popup.content = layout
        popup.open()
    
    def select_dictionary(self, popup, dictionary):
        # 获取词库中的所有单词
        self.words = Word.get_by_dictionary(dictionary.id)
        
        if not self.words:
            # 如果词库中没有单词，显示提示
            self.word_label.text = f"词库 '{dictionary.name}' 中没有单词"
            self.translation_label.text = "请先在词库管理中添加单词"
            self.example_label.text = ""
            self.progress_label.text = "进度: 0/0"
        else:
            # 创建学习记录（如果不存在的话）
            LearningRecord.create_initial_records(current_user.id, dictionary.id)
            
            # 重置索引
            self.current_index = 0
            
            # 显示第一个单词
            self.show_word()
        
        popup.dismiss()

# 复习界面
class ReviewScreen(Screen):
    _review_cache = None
    
    def __init__(self, **kwargs):
        super(ReviewScreen, self).__init__(**kwargs)
        self.review_items = []
        self.current_index = 0
        self.current_record = None
        self._data_loaded = False
        self._current_word_id = None
        self._pending_operation = False
        self._start_time = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 顶部标题栏
        top_bar = BoxLayout(size_hint_y=None, height=50)
        back_btn = create_button(text="返回", on_press=self.on_back)
        top_bar.add_widget(back_btn)
        
        self.progress_label = create_label(text="点击'刷新列表'加载复习单词", font_size=16)
        top_bar.add_widget(self.progress_label)
        
        refresh_btn = create_button(text="刷新列表", on_press=self.load_review_words)
        top_bar.add_widget(refresh_btn)
        
        layout.add_widget(top_bar)
        
        # 单词卡片
        self.word_card = Card(size_hint_y=1, padding=20)
        self.word_layout = BoxLayout(orientation='vertical', spacing=10)
        
        # 单词和音标分别显示
        word_phonetic_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=60, spacing=2)
        
        # 单词
        self.word_label = create_label(text="等待加载...", font_size=28, bold=True, size_hint_y=None, height=30)
        word_phonetic_layout.add_widget(self.word_label)
        
        # 音标（使用专门字体）
        self.phonetic_label = create_label(text="", font_size=18, font_name=PHONETIC_FONT, 
                                         size_hint_y=None, height=25, color=(1.0, 0.95, 0.6, 1))
        word_phonetic_layout.add_widget(self.phonetic_label)
        
        self.word_layout.add_widget(word_phonetic_layout)
        
        # 翻译
        self.translation_label = create_label(text="", font_size=24, shorten=True, text_size=(None, None), halign='left', valign='middle')
        self.word_layout.add_widget(self.translation_label)
        
        # 例句
        self.example_label = create_label(text="", font_size=16, italic=True, shorten=True, shorten_from='right', text_size=(None, None), size_hint_y=None, height=30)
        self.word_layout.add_widget(self.example_label)
        
        self.word_card.add_widget(self.word_layout)
        layout.add_widget(self.word_card)
        
        # 操作按钮
        buttons_layout = BoxLayout(spacing=10, size_hint_y=None, height=60)
        
        prev_btn = create_button(text="上一题", on_press=self.prev_word)
        buttons_layout.add_widget(prev_btn)
        
        next_btn = create_button(text="下一题", on_press=self.next_word)
        buttons_layout.add_widget(next_btn)
        
        layout.add_widget(buttons_layout)
        
        # 记忆评级按钮
        rating_layout = BoxLayout(spacing=5, size_hint_y=None, height=60)

        for text, rating, color in _get_rating_buttons():
            btn = create_button(text=text, background_color=color, on_press=_get_rating_callback(rating))
            rating_layout.add_widget(btn)

        layout.add_widget(rating_layout)
        
        self.add_widget(layout)
    
    def on_enter(self):
        if not self._data_loaded and self.review_items:
            Clock.schedule_once(lambda dt: self.show_word(), 0.1)
    
    def on_back(self, instance):
        if self._start_time and hasattr(current_user, 'id'):
            duration = int((datetime.now() - self._start_time).total_seconds())
            if duration > 5:
                LearningRecord.record_learning_time(current_user.id, duration, 'review')
        self.manager.current = 'main'
    
    def load_review_words(self, instance=None):
        # 开始计时
        self._start_time = datetime.now()
        
        # 获取需要复习的单词
        self.review_items = LearningRecord.get_review_words(current_user.id)
        
        if not self.review_items:
            # 如果没有需要复习的单词，显示提示
            self.word_label.text = "没有需要复习的单词"
            self.translation_label.text = "所有单词都已复习完成"
            self.example_label.text = ""
            self.progress_label.text = "进度: 0/0"
            return
        
        # 重置索引
        self.current_index = 0
        
        # 显示第一个单词
        self.show_word()
    
    def show_word(self):
        if not self.review_items or self.current_index < 0 or self.current_index >= len(self.review_items):
            return
        
        word, self.current_record = self.review_items[self.current_index]
        
        if self._current_word_id == word.id:
            return
        
        self._current_word_id = word.id
        
        # 单词和音标分别显示
        self.word_label.text = word.word
        
        phonetic_text = format_phonetic(word.phonetic)
        if phonetic_text:
            self.phonetic_label.text = f"[{phonetic_text}]"
            self.phonetic_label.opacity = 1
        else:
            self.phonetic_label.text = ""
            self.phonetic_label.opacity = 0
            
        self.translation_label.text = word.translation
        self.example_label.text = word.example or ""
        
        self.progress_label.text = f"进度: {self.current_index + 1}/{len(self.review_items)}"
    
    def rate_memory(self, rating):
        if self._pending_operation:
            return
        if not self.current_record:
            return
        
        self._pending_operation = True
        
        try:
            self.current_record.update_after_review(rating)
            
            if self.current_index < len(self.review_items) - 1:
                self.current_index += 1
                self._current_word_id = None
                self.show_word()
            else:
                self.word_label.text = "复习完成"
                self.translation_label.text = f"已完成所有 {len(self.review_items)} 个单词的复习"
                self.example_label.text = ""
                self.progress_label.text = "进度: 100%"
                self._current_word_id = None
                
                if self._start_time and hasattr(current_user, 'id'):
                    duration = int((datetime.now() - self._start_time).total_seconds())
                    if duration > 5:
                        LearningRecord.record_learning_time(current_user.id, duration, 'review')
        except Exception as e:
            print(f"Error in rate_memory: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self._pending_operation = False
    
    def prev_word(self, instance):
        if self._pending_operation:
            return
        if self.current_index > 0:
            self.current_index -= 1
            self._current_word_id = None
            self.show_word()
    
    def next_word(self, instance):
        if self._pending_operation:
            return
        if self.current_index < len(self.review_items) - 1:
            self.current_index += 1
            self._current_word_id = None
            self.show_word()

# 测试界面
class TestScreen(Screen):
    _test_cache = {}
    
    def __init__(self, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        self.current_dictionary = None
        self.test_words = []
        self.current_index = 0
        self.correct_count = 0
        self.test_type = "choice"
        self.user_answer = ""
        self._data_loaded = False
        self._start_time = None
        self.build_ui()
    
    def add_cute_background(self):
        from random import randint
        
        bg_layout = BoxLayout()
        bg_layout.bind(pos=self.update_canvas, size=self.update_canvas)
        
        with bg_layout.canvas:
            Color(1.0, 0.95, 0.6, 1)
            Rectangle(pos=(0, 0), size=self.size)
            
            colors = [
                (1.0, 0.75, 0.3, 0.2),
                (0.3, 0.85, 0.65, 0.2),
                (0.35, 0.75, 1.0, 0.2),
                (1.0, 0.5, 0.5, 0.18),
                (0.9, 0.7, 0.95, 0.18),
                (0.4, 0.9, 0.9, 0.15),
                (1.0, 0.8, 0.6, 0.15),
            ]
            
            left_positions = [
                (50, 400, 180, 180),
                (self.width * 0.15 if self.width > 0 else 120, 100, 140, 140),
                (80, 600, 120, 120),
                (30, 200, 100, 100),
            ]
            
            for i, (x, y, w, h) in enumerate(left_positions):
                Color(*colors[i % len(colors)])
                RoundedRectangle(pos=(x, y), size=(w, h), radius=[50])
            
            right_positions = [
                (self.width - 200 if self.width > 0 else 600, 450, 200, 200),
                (self.width - 150 if self.width > 0 else 650, 200, 150, 150),
                (self.width - 280 if self.width > 0 else 520, 650, 180, 180),
                (self.width - 100 if self.width > 0 else 700, 550, 120, 120),
            ]
            
            for i, (x, y, w, h) in enumerate(right_positions):
                Color(*colors[(i + 3) % len(colors)])
                RoundedRectangle(pos=(x, y), size=(w, h), radius=[50])
    
    def update_canvas(self, instance, value):
        pass
    
    def build_ui(self):
        self.add_cute_background()
        
        layout = BoxLayout(orientation='vertical', spacing=10)
        
        # 顶部标题栏 - 返回按钮在左，选择词库在右
        top_bar = BoxLayout(size_hint_y=None, height=50)
        
        # 返回按钮 - 左对齐，固定宽度
        back_btn = create_button(text="< 返回", size_hint_x=None, width=80, on_press=self.on_back)
        back_anchor = AnchorLayout(anchor_x='left', size_hint_x=0.3)
        back_anchor.add_widget(back_btn)
        top_bar.add_widget(back_anchor)
        
        # 进度标签 - 居中
        self.progress_label = create_label(text="准备测试")
        progress_anchor = AnchorLayout(anchor_x='center', size_hint_x=0.4)
        progress_anchor.add_widget(self.progress_label)
        top_bar.add_widget(progress_anchor)
        
        # 选择词库按钮 - 右对齐
        dict_btn = create_button(text="选择词库", size_hint_x=None, width=100, on_press=self.show_dictionary_selection)
        dict_anchor = AnchorLayout(anchor_x='right', size_hint_x=0.3)
        dict_anchor.add_widget(dict_btn)
        top_bar.add_widget(dict_anchor)
        
        layout.add_widget(top_bar)

        # 测试类型选择
        test_type_layout = BoxLayout(spacing=5, size_hint_y=None, height=50)

        choice_btn = create_button(text="选择题", background_color=CHILD_COLORS['accent'] if self.test_type == "choice" else CHILD_COLORS['inactive'])
        fill_btn = create_button(text="填空题", background_color=CHILD_COLORS['accent'] if self.test_type == "fill" else CHILD_COLORS['inactive'])

        buttons_ref = [choice_btn, fill_btn]
        choice_btn.bind(on_press=_get_test_type_callback("choice", buttons_ref))
        fill_btn.bind(on_press=_get_test_type_callback("fill", buttons_ref))

        test_type_layout.add_widget(choice_btn)
        test_type_layout.add_widget(fill_btn)

        layout.add_widget(test_type_layout)

        # 测试内容区域
        self.test_card = Card(size_hint_y=None, height=350, padding=20)
        self.test_layout = BoxLayout(orientation='vertical', spacing=10)

        # 问题
        self.question_label = create_label(text="请选择词库并点击开始测试", font_size=24)
        self.test_layout.add_widget(self.question_label)

        # 选项（选择题）
        self.options_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        self.test_layout.add_widget(self.options_layout)

        # 填空题输入框
        self.fill_input = create_textinput(text="", font_size=24, multiline=False, size_hint_y=None, height=50, opacity=0)
        self.test_layout.add_widget(self.fill_input)

        # 结果反馈
        self.result_label = create_label(text="", font_size=20)
        self.test_layout.add_widget(self.result_label)

        self.test_card.add_widget(self.test_layout)
        layout.add_widget(self.test_card)

        # 操作按钮
        buttons_layout = BoxLayout(spacing=10, size_hint_y=None, height=60)

        self.start_btn = create_button(text="开始测试", on_press=self.start_test)
        buttons_layout.add_widget(self.start_btn)

        self.submit_btn = create_button(text="提交答案", on_press=self.submit_answer, opacity=0)
        buttons_layout.add_widget(self.submit_btn)

        self.next_btn = create_button(text="下一题", on_press=self.next_question, opacity=0)
        buttons_layout.add_widget(self.next_btn)

        self.finish_btn = create_button(text="完成测试", on_press=self.finish_test, opacity=0)
        buttons_layout.add_widget(self.finish_btn)

        layout.add_widget(buttons_layout)

        self.add_widget(layout)
    
    def on_back(self, instance):
        if self._start_time and hasattr(current_user, 'id'):
            duration = int((datetime.now() - self._start_time).total_seconds())
            if duration > 5:
                LearningRecord.record_learning_time(current_user.id, duration, 'test')
        self.manager.current = 'main'
    
    def show_dictionary_selection(self, instance):
        # 词库选择弹窗
        popup = Popup(title="选择词库", title_font=DEFAULT_FONT, size_hint=(0.8, 0.8))
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 获取所有词库
        dictionaries = Dictionary.get_all()
        
        if not dictionaries:
            layout.add_widget(create_label(text="没有可用的词库"))
        else:
            # 词库列表
            for dictionary in dictionaries:
                dict_btn = create_button(text=f"{dictionary.name} ({dictionary.word_count}个单词")
                dict_btn.bind(on_press=lambda x, d=dictionary: self.select_dictionary(popup, d))
                layout.add_widget(dict_btn)
        
        # 取消按钮
        cancel_btn = create_button(text="取消", size_hint_y=None, height=50)
        cancel_btn.bind(on_press=popup.dismiss)
        layout.add_widget(cancel_btn)
        
        popup.content = layout
        popup.open()
    
    def select_dictionary(self, popup, dictionary):
        self.current_dictionary = dictionary
        self.question_label.text = f"已选择词库: {dictionary.name}\n点击'开始测试'开始测试"
        popup.dismiss()
    
    def set_test_type(self, test_type, buttons):
        self.test_type = test_type
        
        for btn in buttons:
            btn.background_color = CHILD_COLORS['inactive']
        
        for btn in buttons:
            if btn.text == {"choice": "选择题", "fill": "填空题"}[test_type]:
                btn.background_color = CHILD_COLORS['accent']
    
    def start_test(self, instance):
        if not self.current_dictionary:
            self.question_label.text = "请先选择词库"
            return
        
        # 开始计时
        self._start_time = datetime.now()
        
        # 获取词库中的所有单词
        all_words = Word.get_by_dictionary(self.current_dictionary.id)
        
        if not all_words:
            self.question_label.text = f"词库 '{self.current_dictionary.name}' 中没有单词"
            return
        
        # 随机选择10个单词（如果单词数量少于10，则全部使用）
        import random
        self.test_words = random.sample(all_words, min(10, len(all_words)))
        
        # 重置测试状态
        self.current_index = 0
        self.correct_count = 0
        
        # 隐藏开始按钮，显示提交按钮
        self.start_btn.opacity = 0
        self.submit_btn.opacity = 1
        
        # 显示第一题
        self.show_question()
    
    def show_question(self):
        if self.current_index >= len(self.test_words):
            self.finish_test(None)
            return
        
        current_word = self.test_words[self.current_index]
        
        self.progress_label.text = f"进度: {self.current_index + 1}/{len(self.test_words)}"
        
        self.result_label.text = ""
        
        if self.test_type == "choice":
            self.show_choice_question(current_word)
        elif self.test_type == "fill":
            self.show_fill_question(current_word)
    
    def show_choice_question(self, word):
        self.question_label.text = f"请选择 '{word.word}' 的正确翻译"
        
        all_words = Word.get_by_dictionary(word.dictionary_id)
        translations = [w.translation for w in all_words if w.id != word.id]
        
        import random
        wrong_options = random.sample(translations, min(3, len(translations)))
        
        all_options = wrong_options + [word.translation]
        
        random.shuffle(all_options)
        
        self.options_layout.clear_widgets()
        
        for option in all_options:
            option_btn = create_button(text=option, font_size=18, size_hint_y=None, height=60)
            option_btn.bind(on_press=lambda x, opt=option: self.select_option(opt))
            self.options_layout.add_widget(option_btn)
        
        self.options_layout.opacity = 1
        self.fill_input.opacity = 0
    
    def show_fill_question(self, word):
        self.question_label.text = f"请写出 '{word.translation}' 的英文单词"
        
        self.fill_input.text = ""
        
        self.options_layout.opacity = 0
        self.fill_input.opacity = 1
    
    def select_option(self, option):
        self.user_answer = option
        self.submit_answer(None)

    def submit_answer(self, instance):
        if self.current_index >= len(self.test_words):
            return
        
        current_word = self.test_words[self.current_index]
        
        if self.test_type == "choice":
            user_answer = self.user_answer
        else:  # fill
            user_answer = self.fill_input.text.strip()
        
        is_correct = False
        
        if self.test_type == "choice":
            is_correct = user_answer == current_word.translation
        else:  # fill
            is_correct = user_answer.lower() == current_word.word.lower()
        
        if is_correct:
            self.correct_count += 1
            self.result_label.text = f"正确! {current_word.word}"
            self.result_label.color = (0, 1, 0, 1)
        else:
            self.result_label.text = f"错误! 正确答案是 {current_word.word}"
            self.result_label.color = (1, 0, 0, 1)
        
        self.submit_btn.opacity = 0
        self.next_btn.opacity = 1
        
        if self.current_index == len(self.test_words) - 1:
            self.next_btn.text = "查看结果"
            self.finish_btn.opacity = 1
    
    def next_question(self, instance):
        if self.current_index == len(self.test_words) - 1:
            self.finish_test(None)
            return
        
        self.current_index += 1
        
        self.next_btn.opacity = 0
        self.submit_btn.opacity = 1
        
        self.show_question()
    
    def finish_test(self, instance):
        score = (self.correct_count / len(self.test_words)) * 100
        
        self.question_label.text = f"测试完成!\n得分: {score:.1f}%\n正确: {self.correct_count}/{len(self.test_words)}"
        
        self.submit_btn.opacity = 0
        self.next_btn.opacity = 0
        self.finish_btn.opacity = 0
        self.start_btn.opacity = 1
        self.start_btn.text = "重新测试"
        
        self.options_layout.opacity = 0
        self.fill_input.opacity = 0
        
        self.result_label.text = ""
        
        if self._start_time and hasattr(current_user, 'id'):
            duration = int((datetime.now() - self._start_time).total_seconds())
            if duration > 5:
                LearningRecord.record_learning_time(current_user.id, duration, 'test')
            
            if self.current_dictionary:
                LearningRecord.record_test_result(
                    current_user.id,
                    self.current_dictionary.id,
                    self.test_type,
                    len(self.test_words),
                    self.correct_count
                )

# 词库管理界面
class DictionaryScreen(Screen):
    def __init__(self, **kwargs):
        super(DictionaryScreen, self).__init__(**kwargs)
        self.current_dictionary = None
        self.build_ui()
    
    def toggle_info(self, dictionary):
        info_layout = getattr(self, f'info_{dictionary.id}', None)
        if info_layout is None:
            return
        
        current_height = info_layout.height
        if current_height > 1:
            info_layout.height = 0
            info_layout.opacity = 0
        else:
            info_layout.height = 30
            info_layout.opacity = 1
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 顶部标题栏（返回 + 新建词库）
        top_bar = BoxLayout(size_hint_y=None, height=50)
        
        back_btn = create_button(text="< 返回", size_hint_x=0.2, on_press=lambda x: setattr(self.manager, 'current', 'main'))
        top_bar.add_widget(back_btn)
        
        top_bar.add_widget(create_label(text="[词库] 词库管理", font_size=20, bold=True))
        
        new_dict_btn = create_button(text="+ 新建词库", size_hint_x=0.3, on_press=self.create_dictionary)
        
        top_bar.add_widget(new_dict_btn)
        
        layout.add_widget(top_bar)
        
        # 词库列表
        self.dictionary_list = ScrollView(size_hint_y=1)
        self.dictionary_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.dictionary_list.add_widget(self.dictionary_layout)
        layout.add_widget(self.dictionary_list)
        
        # 加载词库列表
        self.load_dictionaries()
        
        # 底部导航栏
        bottom_nav = BoxLayout(size_hint_y=None, height=80, spacing=5, padding=[0, 10, 0, 10])

        home_btn = create_button(text="首页", font_size=14)
        home_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))

        learn_nav_btn = create_button(text="学习", font_size=14)
        learn_nav_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'learning'))

        review_nav_btn = create_button(text="复习", font_size=14)
        review_nav_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'review'))

        test_nav_btn = create_button(text="测试", font_size=14)
        test_nav_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'test'))

        dict_nav_btn = create_button(text="词库", font_size=14, background_color=CHILD_COLORS['accent'])
        dict_nav_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'dictionary'))
        
        bottom_nav.add_widget(home_btn)
        bottom_nav.add_widget(learn_nav_btn)
        bottom_nav.add_widget(review_nav_btn)
        bottom_nav.add_widget(test_nav_btn)
        bottom_nav.add_widget(dict_nav_btn)
        
        layout.add_widget(bottom_nav)
        
        self.add_widget(layout)
    
    def load_dictionaries(self):
        # 清空列表
        self.dictionary_layout.clear_widgets()
        
        # 获取所有词库
        dictionaries = Dictionary.get_all()
        
        if not dictionaries:
            # 如果没有词库，显示提示
            return
        
        # 添加词库卡片
        for dictionary in dictionaries:
            card = Card(size_hint_y=None, height=130)
            card_layout = BoxLayout(orientation='vertical', padding=10, spacing=2)
            
            # 词库名称和折叠按钮
            header_layout = BoxLayout(spacing=10, size_hint_y=None, height=40)
            header_layout.add_widget(create_label(text=f"[词库] {dictionary.name}", font_size=20, bold=True))
            
            # 折叠箭头按钮
            toggle_btn = Button(text="▼", font_size=16, size_hint_x=None, width=40, background_color=CHILD_COLORS['secondary'])
            toggle_btn.bind(on_press=lambda x, d=dictionary: self.toggle_info(d))
            header_layout.add_widget(toggle_btn)
            
            # 保存展开状态
            if not hasattr(self, 'expanded_dicts'):
                self.expanded_dicts = {}
            self.expanded_dicts[dictionary.id] = False
            
            card_layout.add_widget(header_layout)
            
            # 折叠的信息区域（默认折叠）
            info_layout = BoxLayout(spacing=10, size_hint_y=None, height=0, opacity=0)
            info_layout.add_widget(create_label(text=f"[说明] {dictionary.description}", font_size=14, shorten=True, shorten_from='center'))
            info_layout.add_widget(create_label(text=f"[单词] {dictionary.word_count} 个单词", font_size=14))
            card_layout.add_widget(info_layout)
            setattr(self, f'info_{dictionary.id}', info_layout)
            
            # 操作按钮放在词库信息上方
            buttons_layout = BoxLayout(spacing=5, size_hint_y=None, height=40, size_hint_x=1)
            
            view_btn = create_button(text="查看", size_hint_x=0.25)
            view_btn.bind(on_press=lambda x, d=dictionary: self.view_words(d))
            
            import_btn = create_button(text="导入", size_hint_x=0.25)
            import_btn.bind(on_press=lambda x, d=dictionary: self.import_words(d))
            
            export_btn = create_button(text="导出", size_hint_x=0.25)
            export_btn.bind(on_press=lambda x, d=dictionary: self.export_words(d))
            
            delete_btn = create_button(text="删除", size_hint_x=0.25)
            delete_btn.bind(on_press=lambda x, d=dictionary: self.delete_dictionary(d))
            
            buttons_layout.add_widget(view_btn)
            buttons_layout.add_widget(import_btn)
            buttons_layout.add_widget(export_btn)
            buttons_layout.add_widget(delete_btn)
            
            card_layout.add_widget(buttons_layout)
            card.add_widget(card_layout)
            self.dictionary_layout.add_widget(card)
        
        # 动态调整GridLayout高度
        self.dictionary_layout.height = len(dictionaries) * 140 + 10
    
    def create_dictionary(self, instance):
        # 新建词库弹窗
        popup = Popup(title="新建词库", title_font=DEFAULT_FONT, size_hint=(0.8, 0.8))
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 词库名称
        layout.add_widget(create_label(text="词库名称:"))
        name_input = create_textinput(multiline=False)
        layout.add_widget(name_input)
        
        # 词库描述
        layout.add_widget(create_label(text="词库描述:"))
        desc_input = create_textinput(multiline=True)
        layout.add_widget(desc_input)

        # 语言选择
        layout.add_widget(create_label(text="语言:"))
        lang_input = LanguageSpinner(
            text="英语",
            values=("英语", "中文", "日语", "韩语", "法语", "德语", "西班牙语", "俄语"),
            size_hint_y=None,
            height=40
        )
        layout.add_widget(lang_input)
        
        # 按钮布局
        buttons_layout = BoxLayout(spacing=10, size_hint_y=None, height=50)
        
        create_btn = create_button(text="创建")
        create_btn.bind(on_press=lambda x: self.save_dictionary(popup, name_input.text, desc_input.text, lang_input.text))
        
        cancel_btn = create_button(text="取消")
        cancel_btn.bind(on_press=popup.dismiss)
        
        buttons_layout.add_widget(create_btn)
        buttons_layout.add_widget(cancel_btn)
        
        layout.add_widget(buttons_layout)
        
        popup.content = layout
        popup.open()
    
    def save_dictionary(self, popup, name, description, language):
        if not name:
            # 显示错误提示
            error_popup = Popup(title="错误", content=create_label(text="词库名称不能为空"), size_hint=(0.5, 0.5))
            error_popup.open()
            return
        
        # 创建新词库        dictionary = Dictionary(name=name, description=description, language=language)
        dictionary.save()
        
        # 刷新词库列表
        self.load_dictionaries()
        
        # 关闭弹窗
        popup.dismiss()
    
    def view_words(self, dictionary):
        # 查看单词弹窗
        popup = Popup(title=f"词库: {dictionary.name}", title_font=DEFAULT_FONT, size_hint=(0.9, 0.9))
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 搜索框
        search_layout = BoxLayout(size_hint_y=None, height=50)
        search_input = create_textinput(
            hint_text="搜索单词...", 
            multiline=False,
            background_color=CHILD_COLORS['card_bg'],  # 统一的卡片背景
            foreground_color=(0, 0, 0, 1),  # 纯黑文字
            hint_text_color=(1.0, 0.95, 0.6, 1),  # 浅黄色提示文字
            border=(2, 2, 2, 2)  # 增强边框
        )
        search_btn = create_button(
            text="搜索", 
            background_color=CHILD_COLORS['accent'],
            color=(0, 0, 0, 1)  # 黑色文字
        )
        search_btn.bind(on_press=lambda x: self.search_words(dictionary, search_input.text, word_list))
        search_layout.add_widget(search_input)
        search_layout.add_widget(search_btn)
        layout.add_widget(search_layout)
        
        # 添加单词按钮
        add_btn = create_button(text="添加单词", size_hint_y=None, height=50)
        add_btn.bind(on_press=lambda x: self.add_word(dictionary, popup))
        layout.add_widget(add_btn)
        
        # 单词列表
        word_list = ScrollView()
        word_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        word_list.add_widget(word_layout)
        
        # 加载单词
        self.load_words(dictionary, word_layout)
        
        layout.add_widget(word_list)
        
        # 关闭按钮
        close_btn = create_button(text="关闭", size_hint_y=None, height=50)
        close_btn.bind(on_press=popup.dismiss)
        layout.add_widget(close_btn)
        
        popup.content = layout
        popup.open()
    
    def load_words(self, dictionary, layout):
        existing_cards = []
        for child in layout.children[:]:
            if hasattr(child, 'word_id'):
                _return_word_card_to_pool(child)
            else:
                child.clear_widgets()
                child.parent = None
        
        layout.clear_widgets()
        
        words = Word.get_by_dictionary(dictionary.id)
        
        if not words:
            layout.add_widget(create_label(text="词库中没有单词", font_size=18))
            return
        
        for word in words:
            card = _get_word_card_from_pool()
            if card is None:
                card = Card(size_hint_y=None, height=100)
                card.word_id = word.id
                card_layout = BoxLayout(orientation='vertical', padding=5)
                card.add_widget(card_layout)
                
                word_row = BoxLayout(spacing=5, size_hint_y=None, height=30)
                card.word_row = word_row
                card_layout.add_widget(word_row)
                
                card.buttons_layout = BoxLayout(spacing=5, size_hint_y=None, height=30)
                card_layout.add_widget(card.buttons_layout)
            else:
                card.word_id = word.id
                card_layout = card.children[0]
                card.word_row = card_layout.children[1]
                card.buttons_layout = card_layout.children[0]
            
            card.word_row.clear_widgets()
            card.word_row.add_widget(create_label(text=word.word, font_size=18, bold=True))
            card.word_row.add_widget(create_label(text=word.translation, font_size=16))
            
            if card.buttons_layout.children:
                edit_btn, delete_btn = card.buttons_layout.children
                edit_btn.unbind(on_press=self.edit_word)
                delete_btn.unbind(on_press=self.delete_word)
            
            edit_btn = create_button(text="编辑", size_hint_x=0.5)
            edit_btn.bind(on_press=lambda x, w=word: self.edit_word(w))
            
            delete_btn = create_button(text="删除", size_hint_x=0.5)
            delete_btn.bind(on_press=lambda x, w=word, d=dictionary, l=layout: self.delete_word(w, d, l))
            
            card.buttons_layout.clear_widgets()
            card.buttons_layout.add_widget(edit_btn)
            card.buttons_layout.add_widget(delete_btn)
            
            layout.add_widget(card)
    
    def search_words(self, dictionary, keyword, layout):
        if not keyword:
            # 如果搜索关键词为空，显示所有单词
            self.load_words(dictionary, layout)
            return
        
        # 清空列表
        layout.clear_widgets()
        
        # 搜索单词
        words = Word.search(keyword, dictionary.id)
        
        if not words:
            # 如果没有找到单词，显示提示
            layout.add_widget(create_label(text=f"没有找到包含 '{keyword}' 的单词", font_size=18))
            return
        
        # 添加单词卡片（与load_words相同的代码）
        for word in words:
            card = Card(size_hint_y=None, height=100)
            card_layout = BoxLayout(orientation='vertical', padding=5)
            
            # 单词和翻译
            word_row = BoxLayout(spacing=10)
            word_row.add_widget(create_label(text=word.word, font_size=18, bold=True))
            word_row.add_widget(create_label(text=word.translation, font_size=16))
            card_layout.add_widget(word_row)
            
            # 音标
            if word.phonetic:
                card_layout.add_widget(create_label(text=format_phonetic(word.phonetic), font_name=PHONETIC_FONT, font_size=16))
            
            # 操作按钮
            buttons_layout = BoxLayout(spacing=5, size_hint_y=None, height=30)
            
            edit_btn = create_button(text="编辑", size_hint_x=0.5)
            edit_btn.bind(on_press=lambda x, w=word: self.edit_word(w))
            
            delete_btn = create_button(text="删除", size_hint_x=0.5)
            delete_btn.bind(on_press=lambda x, w=word, d=dictionary, l=layout: self.delete_word(w, d, l))
            
            buttons_layout.add_widget(edit_btn)
            buttons_layout.add_widget(delete_btn)
            
            card_layout.add_widget(buttons_layout)
            card.add_widget(card_layout)
            layout.add_widget(card)
    
    def add_word(self, dictionary, parent_popup):
        # 添加单词弹窗
        popup = Popup(title="添加单词", title_font=DEFAULT_FONT, size_hint=(0.8, 0.8))
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 单词
        layout.add_widget(create_label(text="单词:"))
        word_input = create_textinput(multiline=False)
        layout.add_widget(word_input)
        
        # 翻译
        layout.add_widget(create_label(text="翻译:"))
        translation_input = create_textinput(multiline=False)
        layout.add_widget(translation_input)
        
        # 音标
        layout.add_widget(create_label(text="音标:"))
        phonetic_input = create_textinput(multiline=False)
        layout.add_widget(phonetic_input)
        
        # 释义
        layout.add_widget(create_label(text="释义:"))
        definition_input = create_textinput(multiline=True)
        layout.add_widget(definition_input)
        
        # 例句
        layout.add_widget(create_label(text="例句:"))
        example_input = create_textinput(multiline=True)
        layout.add_widget(example_input)
        
        # 按钮布局
        buttons_layout = BoxLayout(spacing=10, size_hint_y=None, height=50)
        
        save_btn = create_button(text="保存")
        save_btn.bind(on_press=lambda x: self.save_word(popup, parent_popup, dictionary, word_input.text, translation_input.text, 
                                                       phonetic_input.text, definition_input.text, example_input.text))
        
        cancel_btn = create_button(text="取消")
        cancel_btn.bind(on_press=popup.dismiss)
        
        buttons_layout.add_widget(save_btn)
        buttons_layout.add_widget(cancel_btn)
        
        layout.add_widget(buttons_layout)
        
        popup.content = layout
        popup.open()
    
    def save_word(self, popup, parent_popup, dictionary, word, translation, phonetic, definition, example):
        if not word or not translation:
            # 显示错误提示
            error_popup = Popup(title="错误", title_font=DEFAULT_FONT, content=create_label(text="单词和翻译不能为空"), size_hint=(0.5, 0.5))
            error_popup.open()
            return
        
        # 创建新单词
        new_word = Word(
            word=word,
            translation=translation,
            phonetic=phonetic,
            definition=definition,
            example=example,
            dictionary_id=dictionary.id
        )
        new_word.save()
        
        # 刷新单词列表
        for child in parent_popup.content.children:
            if isinstance(child, ScrollView):
                for grandchild in child.children:
                    if isinstance(grandchild, GridLayout):
                        self.load_words(dictionary, grandchild)
        
        # 关闭弹窗
        popup.dismiss()
    
    def edit_word(self, word):
        # 编辑单词弹窗
        popup = Popup(title="编辑单词", size_hint=(0.8, 0.8))
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 单词
        layout.add_widget(create_label(text="单词:"))
        word_input = create_textinput(text=word.word, multiline=False)
        layout.add_widget(word_input)
        
        # 翻译
        layout.add_widget(create_label(text="翻译:"))
        translation_input = create_textinput(text=word.translation, multiline=False)
        layout.add_widget(translation_input)
        
        # 音标
        layout.add_widget(create_label(text="音标:"))
        phonetic_input = create_textinput(text=word.phonetic or "", multiline=False)
        layout.add_widget(phonetic_input)
        
        # 释义
        layout.add_widget(create_label(text="释义:"))
        definition_input = create_textinput(text=word.definition or "", multiline=True)
        layout.add_widget(definition_input)
        
        # 例句
        layout.add_widget(create_label(text="例句:"))
        example_input = create_textinput(text=word.example or "", multiline=True)
        layout.add_widget(example_input)
        
        # 按钮布局
        buttons_layout = BoxLayout(spacing=10, size_hint_y=None, height=50)
        
        save_btn = create_button(text="保存")
        save_btn.bind(on_press=lambda x: self.update_word(popup, word, word_input.text, translation_input.text, 
                                                         phonetic_input.text, definition_input.text, example_input.text))
        
        cancel_btn = create_button(text="取消")
        cancel_btn.bind(on_press=popup.dismiss)
        
        buttons_layout.add_widget(save_btn)
        buttons_layout.add_widget(cancel_btn)
        
        layout.add_widget(buttons_layout)
        
        popup.content = layout
        popup.open()
    
    def update_word(self, popup, word, new_word, new_translation, new_phonetic, new_definition, new_example):
        if not new_word or not new_translation:
            # 显示错误提示
            error_popup = Popup(title="错误", title_font=DEFAULT_FONT, content=create_label(text="单词和翻译不能为空"), size_hint=(0.5, 0.5))
            error_popup.open()
            return
        
        # 更新单词
        word.word = new_word
        word.translation = new_translation
        word.phonetic = new_phonetic
        word.definition = new_definition
        word.example = new_example
        word.save()
        
        # 关闭弹窗
        popup.dismiss()
        
        # 刷新单词列表（这里简化处理，实际应该找到对应的弹窗并刷新列表）
    
    def delete_word(self, word, dictionary, layout):
        # 确认删除弹窗
        popup = Popup(title="确认删除", size_hint=(0.5, 0.5))
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(create_label(text=f"确定要删除单词 '{word.word}' 吗？"))
        
        buttons_layout = BoxLayout(spacing=10, size_hint_y=None, height=50)
        
        delete_btn = create_button(text="删除", background_color=CHILD_COLORS['warning'])
        delete_btn.bind(on_press=lambda x: self.confirm_delete_word(popup, word, dictionary, layout))
        
        cancel_btn = create_button(text="取消")
        cancel_btn.bind(on_press=popup.dismiss)
        
        buttons_layout.add_widget(delete_btn)
        buttons_layout.add_widget(cancel_btn)
        
        layout.add_widget(buttons_layout)
        
        popup.content = layout
        popup.open()
    
    def confirm_delete_word(self, popup, word, dictionary, layout):
        # 删除单词
        word.delete()
        
        # 刷新单词列表
        self.load_words(dictionary, layout)
        
        # 关闭弹窗
        popup.dismiss()
    
    def import_words(self, dictionary):
        # 这里简化处理，实际应该使用文件选择器
        # 显示提示
        popup = Popup(title="导入单词", title_font=DEFAULT_FONT, content=create_label(text="请将词库文件放在 data/dictionaries 目录下\n支持的格式: txt, csv, json"), size_hint=(0.8, 0.8))
        popup.open()
    
    def export_words(self, dictionary):
        # 这里简化处理，实际应该使用文件保存对话框
        # 显示提示
        popup = Popup(title="导出单词", title_font=DEFAULT_FONT, content=create_label(text="词库将导出到 data/dictionaries 目录？"), size_hint=(0.8, 0.8))
        popup.open()
    
    def delete_dictionary(self, dictionary):
        # 确认删除弹窗
        popup = Popup(title="确认删除", title_font=DEFAULT_FONT, size_hint=(0.5, 0.5))
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(create_label(text=f"确定要删除词库'{dictionary.name}' 吗？\n此操作将删除词库中的所有单词"))
        
        buttons_layout = BoxLayout(spacing=10, size_hint_y=None, height=50)
        
        delete_btn = create_button(text="删除", background_color=CHILD_COLORS['warning'])
        delete_btn.bind(on_press=lambda x: self.confirm_delete_dictionary(popup, dictionary))
        
        cancel_btn = create_button(text="取消")
        cancel_btn.bind(on_press=popup.dismiss)
        
        buttons_layout.add_widget(delete_btn)
        buttons_layout.add_widget(cancel_btn)
        
        layout.add_widget(buttons_layout)
        
        popup.content = layout
        popup.open()
    
    def confirm_delete_dictionary(self, popup, dictionary):
        # 删除词库
        dictionary.delete()
        
        # 刷新词库列表
        self.load_dictionaries()
        
        # 关闭弹窗
        popup.dismiss()
    
    def import_yilin_vocabulary(self, instance):
        """导入译林版英语词汇到词典库"""
        try:
            # 创建主词库
            main_dict = Dictionary(
                name="译林版四年级英语",
                description="译林版小学英语四年级上册词汇表，按单元分类",
                language="英语"
            )
            main_dict.save()
            
            # 导入每个单元
            imported_units = 0
            total_words = 0
            
            for unit_key, unit_data in VOCABULARY_DATA.items():
                # 创建单元词库
                unit_dict = Dictionary(
                    name=f"译林版四年级英语 - {unit_data['title']}",
                    description=f"译林版小学英语四年级词汇 - {unit_data['title']}，共{len(unit_data['words'])}个单词",
                    language="英语"
                )
                unit_dict.save()
                
                # 导入该单元的单词
                words_imported = 0
                for word_data in unit_data['words']:
                    word = Word(
                        word=word_data['english'],
                        translation=word_data['chinese'],
                        phonetic=word_data['phonetic'],
                        dictionary_id=unit_dict.id,
                        definition=f"译林版四年级英语 - {unit_data['title']}"
                    )
                    word.save()
                    words_imported += 1
                    total_words += 1
                
                imported_units += 1
                print(f"已导入单元 {unit_data['title']}: {words_imported} 个单词")
            
            # 显示成功消息
            success_msg = f"成功导入译林版英语词汇！\n\n已导入 {imported_units} 个单元\n共 {total_words} 个单词"
            success_popup = Popup(
                title="导入成功", 
                content=create_label(text=success_msg, font_size=16),
                size_hint=(0.7, 0.6)
            )
            success_popup.open()
            
            # 刷新词库列表
            self.load_dictionaries()
            
        except Exception as e:
            # 显示错误消息
            error_msg = f"导入失败：\n{str(e)}"
            error_popup = Popup(
                title="导入失败", 
                content=create_label(text=error_msg, font_size=14),
                size_hint=(0.7, 0.6)
            )
            error_popup.open()
            print(f"Import error: {e}")
            import traceback
            traceback.print_exc()

# 统计界面
class StatisticsScreen(Screen):
    def __init__(self, **kwargs):
        super(StatisticsScreen, self).__init__(**kwargs)
        self._ui_built = False
        self._build_lock = False
    
    def build_ui(self):
        if self._ui_built or self._build_lock:
            return
        
        self._build_lock = True
        try:
            print(f"[DEBUG] StatisticsScreen.build_ui called, current_user exists: {hasattr(current_user, 'id')}")
            content = self._create_statistics_content()
            self.add_widget(content)
            self._ui_built = True
            print(f"[DEBUG] StatisticsScreen UI built successfully")
        except Exception as e:
            print(f"Error building StatisticsScreen UI: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self._build_lock = False
    
    def _create_statistics_content(self):
        try:
            print(f"[DEBUG] _create_statistics_content starting...")
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            
            # 顶部标题栏
            top_bar = BoxLayout(size_hint_y=None, height=50)
            top_bar.add_widget(create_button(text="返回", on_press=lambda x: setattr(self.manager, 'current', 'main')))
            top_bar.add_widget(create_label(text="学习统计", font_size=20, bold=True))
            layout.add_widget(top_bar)
            print(f"[DEBUG] Top bar created")
            
            # 统计卡片区域
            cards_layout = GridLayout(cols=2, spacing=10, size_hint_y=1)
            
            # 学习进度卡片
            progress_card = Card(size_hint_y=None, height=200)
            progress_layout = BoxLayout(orientation='vertical', padding=10)
            progress_layout.add_widget(create_label(text="学习进度", font_size=20, bold=True))
            
            # 获取学习统计
            stats = self._safe_get_learning_stats()
            print(f"[DEBUG] Learning stats: {stats}")
            
            # 计算进度百分比
            total = stats.get('total', 0) if stats else 0
            learned = stats.get('learned', 0) if stats else 0
            need_review = stats.get('need_review', 0) if stats else 0
            
            if total > 0:
                progress_percent = (learned / total) * 100
            else:
                progress_percent = 0
            
            # 进度条
            progress_bar_layout = BoxLayout(orientation='vertical', spacing=5)
            progress_bar_layout.add_widget(create_label(text=f"已学习 {learned}/{total} 个({progress_percent:.1f}%)"))
            
            # 进度条背景 - 使用简单标签占位
            progress_bar_bg = BoxLayout(size_hint_y=None, height=20, size_hint_x=1, padding=[0,0,0,0])
            progress_bar_bg.add_widget(Widget(size_hint_x=None, width=progress_bar_bg.width))
            progress_bar_layout.add_widget(progress_bar_bg)
            
            progress_layout.add_widget(progress_bar_layout)
            progress_layout.add_widget(create_label(text=f"今日待复习 {need_review} 个单词"))
            
            progress_card.add_widget(progress_layout)
            cards_layout.add_widget(progress_card)
            print(f"[DEBUG] Progress card created")
            
            # 记忆效果卡片
            memory_card = Card(size_hint_y=None, height=260)
            memory_layout = BoxLayout(orientation='vertical', padding=10)
            memory_layout.add_widget(create_label(text="记忆效果", font_size=20, bold=True))
            
            # 复习统计数据
            review_stats = self._safe_get_review_stats()
            today_reviewed = review_stats.get('today_reviewed', 0) if review_stats else 0
            today_avg_quality = review_stats.get('today_avg_quality', 0.0) if review_stats else 0.0
            stats_text = f"今日复习: {today_reviewed} 个 | 质量: {today_avg_quality:.1f}"
            memory_layout.add_widget(create_label(text=stats_text, font_size=12))
            print(f"[DEBUG] Review stats: {review_stats}")
            
            memory_card.add_widget(memory_layout)
            cards_layout.add_widget(memory_card)
            
            # 学习时间卡片
            time_card = Card(size_hint_y=None, height=250)
            time_layout = BoxLayout(orientation='vertical', padding=10)
            time_layout.add_widget(create_label(text="学习时间", font_size=20, bold=True))
            
            today_time = self._safe_get_today_learning_time()
            total_minutes = today_time.get('total_time', 0) // 60
            review_minutes = today_time.get('review_time', 0) // 60
            test_minutes = today_time.get('test_time', 0) // 60
            
            time_layout.add_widget(create_label(text=f"今日学习: {total_minutes}分钟", font_size=14))
            time_layout.add_widget(create_label(text=f"  - 复习: {review_minutes}分钟", font_size=12))
            time_layout.add_widget(create_label(text=f"  - 测试: {test_minutes}分钟", font_size=12))
            
            time_layout.add_widget(create_label(text=""))
            time_layout.add_widget(create_label(text="本周学习时间", font_size=14))
            
            weekly_time = self._safe_get_weekly_learning_time()
            weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            today_weekday = datetime.now().weekday()
            
            days_order = [(today_weekday - i) % 7 for i in range(6, -1, -1)]
            
            for i, weekday_idx in enumerate(days_order):
                date_str = (datetime.now() - timedelta(days=6-i)).strftime("%Y-%m-%d")
                minutes = weekly_time.get(date_str, 0) // 60
                time_layout.add_widget(create_label(text=f"  {weekdays[weekday_idx]}: {minutes}分钟", font_size=12))
            
            time_card.add_widget(time_layout)
            cards_layout.add_widget(time_card)
            
            # 测试成绩卡片
            score_card = Card(size_hint_y=None, height=200)
            score_layout = BoxLayout(orientation='vertical', padding=10)
            score_layout.add_widget(create_label(text="测试成绩", font_size=20, bold=True))
            
            test_stats = self._safe_get_test_stats()
            today_tests = test_stats.get('today_tests', 0)
            today_avg_score = test_stats.get('today_avg_score', 0.0)
            today_correct = test_stats.get('today_correct', 0)
            today_total = test_stats.get('today_total', 0)
            total_tests = test_stats.get('total_tests', 0)
            total_avg_score = test_stats.get('total_avg_score', 0.0)
            
            if today_tests > 0:
                score_layout.add_widget(create_label(text=f"今日测试: {today_tests} 次 | 正确: {today_correct}/{today_total}", font_size=12))
                score_layout.add_widget(create_label(text=f"今日平均分: {today_avg_score:.1f}分", font_size=12))
            else:
                score_layout.add_widget(create_label(text="今日暂无测试数据", font_size=12))
            
            score_layout.add_widget(create_label(text=""))
            score_layout.add_widget(create_label(text=f"总测试次数: {total_tests} 次", font_size=12))
            score_layout.add_widget(create_label(text=f"历史平均分: {total_avg_score:.1f}分", font_size=12))
            
            score_card.add_widget(score_layout)
            cards_layout.add_widget(score_card)
            
            scroll_view = ScrollView()
            scroll_view.add_widget(cards_layout)
            layout.add_widget(scroll_view)
            print(f"[DEBUG] All cards created, returning layout")
            
            return layout
        except Exception as e:
            print(f"[ERROR] Exception in _create_statistics_content: {e}")
            import traceback
            traceback.print_exc()
            # Return a simple fallback layout
            fallback = BoxLayout(orientation='vertical', padding=10)
            fallback.add_widget(create_label(text="统计加载失败"))
            fallback.add_widget(create_button(text="返回", on_press=lambda x: setattr(self.manager, 'current', 'main')))
            return fallback
    
    def _safe_get_learning_stats(self):
        try:
            if not hasattr(current_user, 'id'):
                return {'total': 0, 'learned': 0, 'need_review': 0}
            return LearningRecord.get_learning_stats(current_user.id) or {'total': 0, 'learned': 0, 'need_review': 0}
        except Exception as e:
            print(f"Error getting learning stats: {e}")
            return {'total': 0, 'learned': 0, 'need_review': 0}
    
    def _safe_get_review_stats(self):
        try:
            if not hasattr(current_user, 'id'):
                return {}
            return LearningRecord.get_review_stats(current_user.id) or {}
        except Exception as e:
            print(f"Error getting review stats: {e}")
            return {}
    
    def _safe_get_today_learning_time(self):
        try:
            if not hasattr(current_user, 'id'):
                return {'review_time': 0, 'test_time': 0, 'total_time': 0}
            return LearningRecord.get_today_learning_time(current_user.id) or {'review_time': 0, 'test_time': 0, 'total_time': 0}
        except Exception as e:
            print(f"Error getting today learning time: {e}")
            return {'review_time': 0, 'test_time': 0, 'total_time': 0}
    
    def _safe_get_weekly_learning_time(self):
        try:
            if not hasattr(current_user, 'id'):
                return {}
            return LearningRecord.get_weekly_learning_time(current_user.id) or {}
        except Exception as e:
            print(f"Error getting weekly learning time: {e}")
            return {}
    
    def _safe_get_test_stats(self):
        try:
            if not hasattr(current_user, 'id'):
                return {
                    'today_tests': 0, 'today_avg_score': 0, 'today_correct': 0, 'today_total': 0,
                    'total_tests': 0, 'total_avg_score': 0, 'weekly_tests': 0, 'weekly_avg_score': 0
                }
            return LearningRecord.get_test_stats(current_user.id) or {
                'today_tests': 0, 'today_avg_score': 0, 'today_correct': 0, 'today_total': 0,
                'total_tests': 0, 'total_avg_score': 0, 'weekly_tests': 0, 'weekly_avg_score': 0
            }
        except Exception as e:
            print(f"Error getting test stats: {e}")
            return {
                'today_tests': 0, 'today_avg_score': 0, 'today_correct': 0, 'today_total': 0,
                'total_tests': 0, 'total_avg_score': 0, 'weekly_tests': 0, 'weekly_avg_score': 0
            }
    
    def on_enter(self):
        if not self._ui_built:
            self.build_ui()
    
    def update_progress_bar(self, percent):
        try:
            if not hasattr(self, 'progress_rect') or self.progress_rect is None:
                return
            
            parent = self.progress_rect.parent
            if parent is None:
                return
            
            width = parent.width * (percent / 100)
            self.progress_rect.size = (width, 20)
        except Exception as e:
            print(f"Error updating progress bar: {e}")


# 语法专项练习界面
class GrammarScreen(Screen):
    def __init__(self, **kwargs):
        super(GrammarScreen, self).__init__(**kwargs)
        self.current_exercise = None
        self.exercise_type = None
        self.question_type = None
        self.current_question_index = 0
        self.total_questions = 5
        self.correct_answers = 0
        self.exercise_data = []
        self.answer_submitted = False  # 防止重复提交
        self.build_ui()
        
    def build_ui(self):
        # 添加可爱背景
        self.add_cute_background()
        
        # ===== 主布局优化（安卓适配） =====
        layout = BoxLayout(orientation='vertical', 
                          padding=get_scaled_size(ANDROID_CONFIG['padding_large']), 
                          spacing=get_scaled_size(ANDROID_CONFIG['spacing_normal']))
        
        # ===== 顶部导航栏优化 =====
        top_bar = BoxLayout(size_hint_y=None, 
                           height=get_scaled_size(ANDROID_CONFIG['nav_height']), 
                           spacing=get_scaled_size(ANDROID_CONFIG['spacing_small']))
        
        back_btn = create_android_button(text="< 返回", 
                                        font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                        size_hint_y=None, 
                                        height=get_scaled_size(ANDROID_CONFIG['button_height_normal']))
        back_btn.bind(on_press=self.go_back)
        top_bar.add_widget(back_btn)
        
        self.progress_label = create_android_label(text="语法专项练习", 
                                                  font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_title']), 
                                                  bold=True)
        top_bar.add_widget(self.progress_label)
        
        layout.add_widget(top_bar)
        
        # ===== 增加顶部间距，让内容下移 =====
        layout.add_widget(create_label(text="", size_hint_y=None, height=get_scaled_size(ANDROID_CONFIG['spacing_large'])))
        
        # ===== 语法分类选择区域优化（安卓适配） =====
        # 增加ScrollView高度，确保所有内容可见
        category_scroll = ScrollView(size_hint_y=1, size_hint_x=1)
        self.category_layout = BoxLayout(orientation='vertical', 
                                        size_hint_y=None, 
                                        padding=get_scaled_size(ANDROID_CONFIG['padding_normal']))
        self.category_layout.bind(minimum_height=self.category_layout.setter('height'))
        
        # 标题 - 使用响应式字体
        self.category_layout.add_widget(create_android_label(text="选择语法分类", 
                                                            font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_title']), 
                                                            bold=True))
        
        # 增加标题与按钮区域的间距
        self.category_layout.add_widget(create_label(text="", size_hint_y=None, 
                                                    height=get_scaled_size(ANDROID_CONFIG['spacing_normal'])))
        
        # ===== 分类按钮网格优化 =====
        buttons_grid = GridLayout(cols=2, 
                                 spacing=get_scaled_size(ANDROID_CONFIG['spacing_normal']), 
                                 size_hint_y=None, 
                                 height=get_scaled_size(480))
        
        # ===== 语法练习按钮优化（安卓适配） =====
        
        # 介词练习按钮
        preposition_btn = create_android_button(text="介词练习", 
                                               background_color=CHILD_COLORS['primary'], 
                                               font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                               size_hint_y=None, 
                                               height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                               on_press=lambda x: self.start_exercise('preposition'))
        buttons_grid.add_widget(preposition_btn)
        
        # 第三人称单数按钮
        third_person_btn = create_android_button(text="第三人称单数", 
                                                background_color=CHILD_COLORS['rating_vague'], 
                                                font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                                size_hint_y=None, 
                                                height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                                on_press=lambda x: self.start_exercise('third_person'))
        buttons_grid.add_widget(third_person_btn)
        
        # 动词练习按钮
        verb_btn = create_android_button(text="动词练习", 
                                        background_color=CHILD_COLORS['rating_vague'], 
                                        font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                        size_hint_y=None, 
                                        height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                        on_press=lambda x: self.start_exercise('verb'))
        buttons_grid.add_widget(verb_btn)
        
        # 动名词练习按钮
        gerund_btn = create_android_button(text="动名词练习", 
                                          background_color=CHILD_COLORS['warning'], 
                                          font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                          size_hint_y=None, 
                                          height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                          on_press=lambda x: self.start_exercise('gerund'))
        buttons_grid.add_widget(gerund_btn)
        
        # 情态动词练习按钮
        modal_btn = create_android_button(text="情态动词", 
                                         background_color=CHILD_COLORS['warning'], 
                                         font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                         size_hint_y=None, 
                                         height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                         on_press=lambda x: self.start_exercise('modal'))
        buttons_grid.add_widget(modal_btn)
        
        # Be动词练习按钮
        be_btn = create_android_button(text="Be动词", 
                                      background_color=CHILD_COLORS['primary'], 
                                      font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                      size_hint_y=None, 
                                      height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                      on_press=lambda x: self.start_exercise('be_verb'))
        buttons_grid.add_widget(be_btn)
        
        # 特殊疑问句练习按钮
        question_btn = create_android_button(text="特殊疑问句", 
                                            background_color=CHILD_COLORS['warning'], 
                                            font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                            size_hint_y=None, 
                                            height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                            on_press=lambda x: self.start_exercise('question'))
        buttons_grid.add_widget(question_btn)
        
        # 首字母填空练习按钮
        first_letter_btn = create_android_button(text="首字母填空\n专项练习", 
                                                background_color=CHILD_COLORS['rating_vague'], 
                                                font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                                size_hint_y=None, 
                                                height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                                on_press=lambda x: self.start_exercise('first_letter'))
        buttons_grid.add_widget(first_letter_btn)
        
        # 综合练习按钮
        comprehensive_btn = create_android_button(text="综合练习\n(随机500题)", 
                                                 background_color=CHILD_COLORS['rating_vague'], 
                                                 font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                                 size_hint_y=None, 
                                                 height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                                 on_press=lambda x: self.start_exercise('comprehensive'))
        buttons_grid.add_widget(comprehensive_btn)
        
        self.category_layout.add_widget(buttons_grid)
        category_scroll.add_widget(self.category_layout)
        layout.add_widget(category_scroll)
        
        # ===== 题目显示区域优化（安卓适配） =====
        self.question_layout = BoxLayout(orientation='vertical', 
                                        size_hint_y=None, 
                                        height=get_scaled_size(450), 
                                        spacing=get_scaled_size(ANDROID_CONFIG['spacing_normal']))
        self.question_layout.clear_widgets()
        
        # ===== 题目类型选择优化 =====
        self.question_type_layout = BoxLayout(size_hint_y=None, 
                                             height=get_scaled_size(ANDROID_CONFIG['button_height_large']), 
                                             spacing=get_scaled_size(ANDROID_CONFIG['spacing_small']))
        
        self.question_type_layout.add_widget(create_android_label(text="题目类型：", 
                                                                 font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body'])))
        
        choice_btn = create_android_button(text="选择题", 
                                          background_color=CHILD_COLORS['rating_some'], 
                                          font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                          size_hint_y=None, 
                                          height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                          on_press=lambda x: self.set_question_type('choice'))
        fill_btn = create_android_button(text="填空题", 
                                        background_color=CHILD_COLORS['rating_vague'], 
                                        font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                        size_hint_y=None, 
                                        height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                        on_press=lambda x: self.set_question_type('fill'))
        
        self.question_type_layout.add_widget(choice_btn)
        self.question_type_layout.add_widget(fill_btn)
        
        self.question_layout.add_widget(self.question_type_layout)
        
        # 题目内容区域
        self.content_layout = BoxLayout(orientation='vertical', 
                                       spacing=get_scaled_size(ANDROID_CONFIG['spacing_normal']))
        self.question_layout.add_widget(self.content_layout)
        
        # ===== 控制按钮区域优化 =====
        control_layout = BoxLayout(size_hint_y=None, 
                                  height=get_scaled_size(ANDROID_CONFIG['button_height_large'] + 20), 
                                  spacing=get_scaled_size(ANDROID_CONFIG['spacing_small']))
        
        self.submit_btn = create_android_button(text="提交答案", 
                                               background_color=CHILD_COLORS['rating_some'], 
                                               font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                               size_hint_y=None, 
                                               height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                               on_press=lambda x: self.submit_answer(x))
        self.next_btn = create_android_button(text="下一题", 
                                             background_color=CHILD_COLORS['rating_vague'], 
                                             font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                             size_hint_y=None, 
                                             height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                             on_press=lambda x: self.next_question(x))
        self.next_btn.disabled = True
        self.back_btn = create_android_button(text="返回上一级", 
                                             background_color=CHILD_COLORS['warning'], 
                                             font_size=get_scaled_font_size(ANDROID_CONFIG['font_size_body']),
                                             size_hint_y=None, 
                                             height=get_scaled_size(ANDROID_CONFIG['button_height_normal']),
                                             on_press=lambda x: self.back_to_category())
        
        control_layout.add_widget(self.submit_btn)
        control_layout.add_widget(self.next_btn)
        control_layout.add_widget(self.back_btn)
        
        self.question_layout.add_widget(control_layout)
        
        layout.add_widget(self.question_layout)
        # 确保题目布局可见
        self.question_layout.opacity = 1
        self.question_layout.disabled = False
        
        self.add_widget(layout)
        
    def add_cute_background(self):
        if hasattr(self, 'bg_color') and self.bg_color:
            self.remove_widget(self.bg_color)
        
        self.bg_color = Widget(size=self.size)
        with self.bg_color.canvas:
            Color(1.0, 0.95, 0.6, 1)
            Rectangle(pos=(0, 0), size=self.size)
        
        self.add_widget(self.bg_color, index=0)
    
    def go_back(self, instance):
        self.manager.current = 'main'
        
    def back_to_category(self):
        self.category_layout.opacity = 1
        self.category_layout.disabled = False
        self.question_layout.opacity = 0
        self.question_layout.disabled = True
        
        # 恢复题型选择区域显示
        self.question_type_layout.opacity = 1
        self.question_type_layout.disabled = False
        
    def start_exercise(self, exercise_type):
        self.exercise_type = exercise_type
        self.current_question_index = 0
        self.correct_answers = 0
        
        # 隐藏分类选择，显示题目区域
        self.category_layout.opacity = 0
        self.category_layout.disabled = True
        
        self.question_layout.opacity = 1
        self.question_layout.disabled = False
        
        # 更新进度标签
        self.progress_label.text = f"语法专项 - {self.get_exercise_name(exercise_type)}"
        
        # 首字母填空专项不需要题目类型选择
        if exercise_type == 'first_letter':
            # 隐藏题型选择区域
            self.question_type_layout.opacity = 0
            self.question_type_layout.disabled = True
            
            # 自动设置为首字母填空类型
            self.question_type = 'first_letter'
            self.load_questions()
            self.show_question()
        else:
            # 显示题型选择区域
            self.question_type_layout.opacity = 1
            self.question_type_layout.disabled = False
            
            # 显示题目类型选择
            self.show_question_type_selection()
        
    def get_exercise_name(self, exercise_type):
        names = {
            'preposition': '介词练习',
            'third_person': '第三人称单数',
            'verb': '动词练习',
            'gerund': '动名词练习',
            'modal': '情态动词',
            'be_verb': 'Be动词',
            'question': '特殊疑问句',
            'first_letter': '首字母填空专项练习',
            'comprehensive': '综合语法练习'
        }
        return names.get(exercise_type, exercise_type)
        
    def show_question_type_selection(self):
        self.content_layout.clear_widgets()
        self.content_layout.add_widget(create_label(text="请选择题目类型", font_size=18, bold=True))
        
        # 重置按钮状态
        self.submit_btn.disabled = True
        self.next_btn.disabled = True
        
    def set_question_type(self, question_type):
        self.question_type = question_type
        
        if question_type == 'fill' or question_type == 'first_letter':
            self.submit_btn.disabled = False
        else:
            self.submit_btn.disabled = True
            
        self.load_questions()
        self.show_question()
        
    def load_questions(self):
        # 根据语法类型加载题目数据
        if self.exercise_type == 'preposition':
            self.exercise_data = self.get_preposition_questions()
        elif self.exercise_type == 'third_person':
            self.exercise_data = self.get_third_person_questions()
        elif self.exercise_type == 'verb':
            self.exercise_data = self.get_verb_questions()
        elif self.exercise_type == 'gerund':
            self.exercise_data = self.get_gerund_questions()
        elif self.exercise_type == 'modal':
            self.exercise_data = self.get_modal_questions()
        elif self.exercise_type == 'be_verb':
            self.exercise_data = self.get_be_verb_questions()
        elif self.exercise_type == 'question':
            self.exercise_data = self.get_question_questions()
        elif self.exercise_type == 'first_letter':
            self.exercise_data = self.get_first_letter_questions()
        elif self.exercise_type == 'comprehensive':
            self.exercise_data = self.get_comprehensive_questions()
            import random
            random.shuffle(self.exercise_data)
        elif self.exercise_type == 'reading':
            self.exercise_data = self.get_reading_questions()
        else:
            self.exercise_data = []
        
        # 根据题目类型过滤（除首字母填空专项外）
        if self.question_type and self.exercise_data and self.exercise_type != 'first_letter':
            self.exercise_data = [q for q in self.exercise_data if q['type'] == self.question_type]
        
        # 确保至少有题目
        if not self.exercise_data:
            self.exercise_data = self.get_comprehensive_questions()
            if self.question_type and self.exercise_type != 'first_letter':
                self.exercise_data = [q for q in self.exercise_data if q['type'] == self.question_type]
                if not self.exercise_data:
                    # 如果过滤后没有题目，使用所有题目
                    self.exercise_data = self.get_comprehensive_questions()
            import random
            random.shuffle(self.exercise_data)
            
    def get_preposition_questions(self):
        """获取介词题库"""
        return [
            {'type': 'fill', 'question': 'The cat is _____ the table.', 'answer': 'on'},
            {'type': 'fill', 'question': 'She sits _____ the park every morning.', 'answer': 'in'},
            {'type': 'fill', 'question': 'The book is _____ my bag.', 'answer': 'in'},
        ]
    
    def get_reading_questions(self):
        """获取阅读理解题库 - 50篇适合小学生的英语文章"""
        return [
            # 选择题
            {'type': 'choice', 'question': 'The cat is _____ the table.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'on'},
            {'type': 'choice', 'question': 'She sits _____ the park every morning.', 'options': ['in', 'on', 'at', 'by'], 'answer': 'in'},
            {'type': 'choice', 'question': 'The book is _____ my bag.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'in'},
            {'type': 'choice', 'question': 'We will meet _____ 3 o\'clock.', 'options': ['in', 'on', 'at', 'by'], 'answer': 'at'},
            {'type': 'choice', 'question': 'The ball is _____ the box.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'in'},
            {'type': 'choice', 'question': 'My school is _____ the corner.', 'options': ['on', 'in', 'at', 'around'], 'answer': 'on'},
            {'type': 'choice', 'question': 'The dog is sleeping _____ the sofa.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'on'},
            {'type': 'choice', 'question': 'I live _____ Beijing with my parents.', 'options': ['on', 'in', 'at', 'to'], 'answer': 'in'},
            {'type': 'choice', 'question': 'The flowers are _____ the vase on the table.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'in'},
            {'type': 'choice', 'question': 'The train will arrive _____ noon tomorrow.', 'options': ['in', 'on', 'at', 'by'], 'answer': 'at'},
            {'type': 'choice', 'question': 'The children are playing _____ the garden.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'in'},
            {'type': 'choice', 'question': 'There is a picture _____ the wall.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'on'},
            {'type': 'choice', 'question': 'I go to school _____ foot every day.', 'options': ['by', 'on', 'in', 'with'], 'answer': 'by'},
            {'type': 'choice', 'question': 'She goes to work _____ car.', 'options': ['by', 'on', 'in', 'with'], 'answer': 'by'},
            {'type': 'choice', 'question': 'The moon is _____ the night sky.', 'options': ['on', 'in', 'at', 'in'], 'answer': 'in'},
            {'type': 'choice', 'question': 'The clock is _____ the wall.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'on'},
            {'type': 'choice', 'question': 'We will have a party _____ Saturday.', 'options': ['in', 'on', 'at', 'by'], 'answer': 'on'},
            {'type': 'choice', 'question': 'The shop is _____ the corner of the street.', 'options': ['on', 'in', 'at', 'around'], 'answer': 'on'},
            {'type': 'choice', 'question': 'She is _____ the bathroom.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'in'},
            {'type': 'choice', 'question': 'The children are _____ the playground.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'on'},
            {'type': 'choice', 'question': 'We will meet _____ the cinema.', 'options': ['in', 'on', 'at', 'by'], 'answer': 'at'},
            {'type': 'choice', 'question': 'The keys are _____ my pocket.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'in'},
            {'type': 'choice', 'question': 'The plane flies _____ the clouds.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'in'},
            {'type': 'choice', 'question': 'She is sitting _____ the window.', 'options': ['on', 'by', 'at', 'under'], 'answer': 'by'},
            {'type': 'choice', 'question': 'The meeting is _____ 2 PM.', 'options': ['in', 'on', 'at', 'by'], 'answer': 'at'},
            {'type': 'choice', 'question': 'We walked _____ the forest.', 'options': ['on', 'in', 'through', 'under'], 'answer': 'through'},
            {'type': 'choice', 'question': 'The bridge is _____ the river.', 'options': ['on', 'in', 'at', 'over'], 'answer': 'over'},
            {'type': 'choice', 'question': 'She is _____ the hospital.', 'options': ['on', 'in', 'at', 'to'], 'answer': 'at'},
            {'type': 'choice', 'question': 'The children are hiding _____ the tree.', 'options': ['on', 'in', 'at', 'behind'], 'answer': 'behind'},
            {'type': 'choice', 'question': 'We are waiting _____ the bus stop.', 'options': ['on', 'in', 'at', 'for'], 'answer': 'at'},
            {'type': 'choice', 'question': 'The cat jumped _____ the fence.', 'options': ['on', 'in', 'at', 'over'], 'answer': 'over'},
            # 填空题
            {'type': 'fill', 'question': 'The dog is sleeping _____ the sofa.', 'answer': 'on'},
            {'type': 'fill', 'question': 'I live _____ Beijing.', 'answer': 'in'},
            {'type': 'fill', 'question': 'The flowers are _____ the vase.', 'answer': 'in'},
            {'type': 'fill', 'question': 'The train will arrive _____ noon.', 'answer': 'at'},
            {'type': 'fill', 'question': 'The children are playing _____ the garden.', 'answer': 'in'},
            {'type': 'fill', 'question': 'Put the book _____ the table.', 'answer': 'on'},
            {'type': 'fill', 'question': 'My birthday is _____ July.', 'answer': 'in'},
            {'type': 'fill', 'question': 'We have class _____ Monday.', 'answer': 'on'},
            {'type': 'fill', 'question': 'The cat is hiding _____ the bed.', 'answer': 'under'},
            {'type': 'fill', 'question': 'I go to school _____ bus.', 'answer': 'by'},
            {'type': 'fill', 'question': 'The clock is _____ the wall.', 'answer': 'on'},
            {'type': 'fill', 'question': 'We will have a party _____ Saturday.', 'answer': 'on'},
            {'type': 'fill', 'question': 'She is _____ the bathroom.', 'answer': 'in'},
            {'type': 'fill', 'question': 'The children are _____ the playground.', 'answer': 'on'},
            {'type': 'fill', 'question': 'We will meet _____ the cinema.', 'answer': 'at'},
            {'type': 'fill', 'question': 'The keys are _____ my pocket.', 'answer': 'in'},
            {'type': 'fill', 'question': 'The plane flies _____ the clouds.', 'answer': 'in'},
            {'type': 'fill', 'question': 'She is sitting _____ the window.', 'answer': 'by'},
            {'type': 'fill', 'question': 'The meeting is _____ 2 PM.', 'answer': 'at'},
            {'type': 'fill', 'question': 'We walked _____ the forest.', 'answer': 'through'},
            {'type': 'fill', 'question': 'The bridge is _____ the river.', 'answer': 'over'},
            {'type': 'fill', 'question': 'She is _____ the hospital.', 'answer': 'at'},
            {'type': 'fill', 'question': 'The children are hiding _____ the tree.', 'answer': 'behind'},
            {'type': 'fill', 'question': 'We are waiting _____ the bus stop.', 'answer': 'at'},
            {'type': 'fill', 'question': 'The cat jumped _____ the fence.', 'answer': 'over'},
            {'type': 'fill', 'question': 'The picture is _____ the wall.', 'answer': 'on'},
            {'type': 'fill', 'question': 'I will be _____ home tomorrow.', 'answer': 'at'},
            {'type': 'fill', 'question': 'The birds are _____ the tree.', 'answer': 'in'},
            {'type': 'fill', 'question': 'She is standing _____ the door.', 'answer': 'by'},
            {'type': 'fill', 'question': 'The sun is _____ the sky.', 'answer': 'in'},
            {'type': 'fill', 'question': 'We sit _____ the first row.', 'answer': 'in'},
        ]
        
    def get_third_person_questions(self):
        return [
            # 选择题
            {'type': 'choice', 'question': 'He _____ to school every day.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'goes'},
            {'type': 'choice', 'question': 'She _____ English very well.', 'options': ['speak', 'speaks', 'speaking', 'spoke'], 'answer': 'speaks'},
            {'type': 'choice', 'question': 'My mother _____ cooking.', 'options': ['like', 'likes', 'liking', 'liked'], 'answer': 'likes'},
            {'type': 'choice', 'question': 'The cat _____ fish.', 'options': ['like', 'likes', 'liking', 'liked'], 'answer': 'likes'},
            {'type': 'choice', 'question': 'He _____ basketball very well.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'plays'},
            {'type': 'choice', 'question': 'My sister _____ music.', 'options': ['like', 'likes', 'liking', 'liked'], 'answer': 'likes'},
            {'type': 'choice', 'question': 'The teacher _____ us English.', 'options': ['teach', 'teaches', 'teaching', 'taught'], 'answer': 'teaches'},
            {'type': 'choice', 'question': 'Tom _____ his homework every day.', 'options': ['do', 'does', 'doing', 'did'], 'answer': 'does'},
            {'type': 'choice', 'question': 'She always _____ early.', 'options': ['wake', 'wakes', 'waking', 'woke'], 'answer': 'wakes'},
            {'type': 'choice', 'question': 'The bird _____ in the tree.', 'options': ['sing', 'sings', 'singing', 'sang'], 'answer': 'sings'},
            {'type': 'choice', 'question': 'My father _____ to work by car.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'goes'},
            {'type': 'choice', 'question': 'The sun _____ in the east.', 'options': ['rise', 'rises', 'rising', 'rose'], 'answer': 'rises'},
            {'type': 'choice', 'question': 'She _____ a letter to her friend.', 'options': ['write', 'writes', 'writing', 'wrote'], 'answer': 'writes'},
            {'type': 'choice', 'question': 'The clock _____ six o\'clock.', 'options': ['show', 'shows', 'showing', 'showed'], 'answer': 'shows'},
            {'type': 'choice', 'question': 'He _____ his teeth every morning.', 'options': ['brush', 'brushes', 'brushing', 'brushed'], 'answer': 'brushes'},
            {'type': 'choice', 'question': 'The dog _____ at the door.', 'options': ['bark', 'barks', 'barking', 'barked'], 'answer': 'barks'},
            {'type': 'choice', 'question': 'My grandmother _____ very tasty cookies.', 'options': ['make', 'makes', 'making', 'made'], 'answer': 'makes'},
            {'type': 'choice', 'question': 'The boy _____ his bicycle every weekend.', 'options': ['ride', 'rides', 'riding', 'rode'], 'answer': 'rides'},
            {'type': 'choice', 'question': 'She _____ her hair every day.', 'options': ['wash', 'washes', 'washing', 'washed'], 'answer': 'washes'},
            {'type': 'choice', 'question': 'The computer _____ very fast.', 'options': ['work', 'works', 'working', 'worked'], 'answer': 'works'},
            {'type': 'choice', 'question': 'He _____ a lot of water every day.', 'options': ['drink', 'drinks', 'drinking', 'drank'], 'answer': 'drinks'},
            {'type': 'choice', 'question': 'The train _____ to the city.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'goes'},
            {'type': 'choice', 'question': 'She _____ in a big company.', 'options': ['work', 'works', 'working', 'worked'], 'answer': 'works'},
            {'type': 'choice', 'question': 'The fish _____ in the water.', 'options': ['swim', 'swims', 'swimming', 'swam'], 'answer': 'swims'},
            {'type': 'choice', 'question': 'My friend _____ the piano beautifully.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'plays'},
            {'type': 'choice', 'question': 'The phone _____ on the table.', 'options': ['ring', 'rings', 'ringing', 'rang'], 'answer': 'rings'},
            {'type': 'choice', 'question': 'He _____ his room every Saturday.', 'options': ['tidy', 'tidies', 'tidying', 'tidied'], 'answer': 'tidies'},
            {'type': 'choice', 'question': 'The teacher _____ a story to the children.', 'options': ['tell', 'tells', 'telling', 'told'], 'answer': 'tells'},
            {'type': 'choice', 'question': 'She _____ to the radio every morning.', 'options': ['listen', 'listens', 'listening', 'listened'], 'answer': 'listens'},
            {'type': 'choice', 'question': 'The car _____ very smoothly.', 'options': ['run', 'runs', 'running', 'ran'], 'answer': 'runs'},
            # 填空题
            {'type': 'fill', 'question': 'My sister _____ music.', 'answer': 'likes'},
            {'type': 'fill', 'question': 'He always _____ early.', 'answer': 'gets up'},
            {'type': 'fill', 'question': 'The teacher _____ us English.', 'answer': 'teaches'},
            {'type': 'fill', 'question': 'She _____ her homework every day.', 'answer': 'does'},
            {'type': 'fill', 'question': 'My father _____ to work by car.', 'answer': 'goes'},
            {'type': 'fill', 'question': 'Tom _____ English very much.', 'answer': 'likes'},
            {'type': 'fill', 'question': 'She _____ a beautiful dress.', 'answer': 'wears'},
            {'type': 'fill', 'question': 'The cat _____ milk.', 'answer': 'drinks'},
            {'type': 'fill', 'question': 'He _____ football on Sundays.', 'answer': 'plays'},
            {'type': 'fill', 'question': 'She _____ Chinese food.', 'answer': 'eats'},
            {'type': 'fill', 'question': 'The dog _____ at the door.', 'answer': 'barks'},
            {'type': 'fill', 'question': 'My grandmother _____ cookies.', 'answer': 'makes'},
            {'type': 'fill', 'question': 'The boy _____ his bicycle.', 'answer': 'rides'},
            {'type': 'fill', 'question': 'She _____ her hair.', 'answer': 'washes'},
            {'type': 'fill', 'question': 'The computer _____ fast.', 'answer': 'works'},
            {'type': 'fill', 'question': 'He _____ water.', 'answer': 'drinks'},
            {'type': 'fill', 'question': 'The train _____ to the city.', 'answer': 'goes'},
            {'type': 'fill', 'question': 'She _____ in a company.', 'answer': 'works'},
            {'type': 'fill', 'question': 'The fish _____ in water.', 'answer': 'swims'},
            {'type': 'fill', 'question': 'My friend _____ the piano.', 'answer': 'plays'},
            {'type': 'fill', 'question': 'The phone _____ on the table.', 'answer': 'rings'},
            {'type': 'fill', 'question': 'He _____ his room.', 'answer': 'tidies'},
            {'type': 'fill', 'question': 'The teacher _____ a story.', 'answer': 'tells'},
            {'type': 'fill', 'question': 'She _____ to the radio.', 'answer': 'listens'},
            {'type': 'fill', 'question': 'The car _____ smoothly.', 'answer': 'runs'},
            {'type': 'fill', 'question': 'The baby _____ loudly.', 'answer': 'cries'},
            {'type': 'fill', 'question': 'He _____ his homework.', 'answer': 'finishes'},
            {'type': 'fill', 'question': 'She _____ the window.', 'answer': 'opens'},
            {'type': 'fill', 'question': 'The teacher _____ the board.', 'answer': 'writes on'},
            {'type': 'fill', 'question': 'He _____ a book.', 'answer': 'reads'},
            {'type': 'fill', 'question': 'She _____ to music.', 'answer': 'listens'},
        ]
        
    def get_verb_questions(self):
        return [
            # 选择题
            {'type': 'choice', 'question': 'I _____ to the store yesterday.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'went'},
            {'type': 'choice', 'question': 'She is _____ a book now.', 'options': ['read', 'reads', 'reading', 'readed'], 'answer': 'reading'},
            {'type': 'choice', 'question': 'They _____ basketball every weekend.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'play'},
            {'type': 'choice', 'question': 'We _____ dinner at 6 PM.', 'options': ['have', 'has', 'having', 'had'], 'answer': 'have'},
            {'type': 'choice', 'question': 'He _____ his teeth twice a day.', 'options': ['brush', 'brushes', 'brushing', 'brushed'], 'answer': 'brushes'},
            {'type': 'choice', 'question': 'Yesterday, I _____ to the park.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'went'},
            {'type': 'choice', 'question': 'She is _____ her homework right now.', 'options': ['do', 'does', 'doing', 'did'], 'answer': 'doing'},
            {'type': 'choice', 'question': 'They usually _____ football after school.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'play'},
            {'type': 'choice', 'question': 'We _____ breakfast together every morning.', 'options': ['have', 'has', 'having', 'had'], 'answer': 'have'},
            {'type': 'choice', 'question': 'He _____ his room every Sunday.', 'options': ['clean', 'cleans', 'cleaning', 'cleaned'], 'answer': 'cleans'},
            {'type': 'choice', 'question': 'I _____ my teeth every morning.', 'options': ['brush', 'brushes', 'brushing', 'brushed'], 'answer': 'brush'},
            {'type': 'choice', 'question': 'She is _____ a letter now.', 'options': ['write', 'writes', 'writing', 'wrote'], 'answer': 'writing'},
            {'type': 'choice', 'question': 'They _____ to the library yesterday.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'went'},
            {'type': 'choice', 'question': 'We are _____ a picture in art class.', 'options': ['draw', 'draws', 'drawing', 'drew'], 'answer': 'drawing'},
            {'type': 'choice', 'question': 'He always _____ his bag to school.', 'options': ['bring', 'brings', 'bringing', 'brought'], 'answer': 'brings'},
            {'type': 'choice', 'question': 'The children _____ in the garden yesterday.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'played'},
            {'type': 'choice', 'question': 'I am _____ a movie tonight.', 'options': ['watch', 'watches', 'watching', 'watched'], 'answer': 'watching'},
            {'type': 'choice', 'question': 'She _____ her friends last week.', 'options': ['visit', 'visits', 'visiting', 'visited'], 'answer': 'visited'},
            {'type': 'choice', 'question': 'We _____ to the beach every summer.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'go'},
            {'type': 'choice', 'question': 'He is _____ his bicycle now.', 'options': ['fix', 'fixes', 'fixing', 'fixed'], 'answer': 'fixing'},
            {'type': 'choice', 'question': 'The students _____ their homework yesterday.', 'options': ['finish', 'finishes', 'finishing', 'finished'], 'answer': 'finished'},
            {'type': 'choice', 'question': 'I am _____ for my exam tomorrow.', 'options': ['study', 'studies', 'studying', 'studied'], 'answer': 'studying'},
            {'type': 'choice', 'question': 'She _____ a beautiful song yesterday.', 'options': ['sing', 'sings', 'singing', 'sang'], 'answer': 'sang'},
            {'type': 'choice', 'question': 'They _____ games after school every day.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'play'},
            {'type': 'choice', 'question': 'We _____ to music last night.', 'options': ['listen', 'listens', 'listening', 'listened'], 'answer': 'listened'},
            {'type': 'choice', 'question': 'He _____ his face every morning.', 'options': ['wash', 'washes', 'washing', 'washed'], 'answer': 'washes'},
            {'type': 'choice', 'question': 'I am _____ my room now.', 'options': ['organize', 'organizes', 'organizing', 'organized'], 'answer': 'organizing'},
            {'type': 'choice', 'question': 'She _____ to work by bus.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'goes'},
            {'type': 'choice', 'question': 'We _____ lunch at school yesterday.', 'options': ['have', 'has', 'having', 'had'], 'answer': 'had'},
            {'type': 'choice', 'question': 'The teacher _____ us a story.', 'options': ['tell', 'tells', 'telling', 'told'], 'answer': 'told'},
            # 填空题
            {'type': 'fill', 'question': 'Yesterday, I _____ to the park.', 'answer': 'went'},
            {'type': 'fill', 'question': 'She is _____ her homework.', 'answer': 'doing'},
            {'type': 'fill', 'question': 'They _____ football every afternoon.', 'answer': 'play'},
            {'type': 'fill', 'question': 'We _____ breakfast together.', 'answer': 'have'},
            {'type': 'fill', 'question': 'He _____ his room every Sunday.', 'answer': 'cleans'},
            {'type': 'fill', 'question': 'She _____ to school yesterday.', 'answer': 'walked'},
            {'type': 'fill', 'question': 'I am _____ a book now.', 'answer': 'reading'},
            {'type': 'fill', 'question': 'They always _____ games after lunch.', 'answer': 'play'},
            {'type': 'fill', 'question': 'We _____ to music yesterday.', 'answer': 'listened'},
            {'type': 'fill', 'question': 'He _____ his face every morning.', 'answer': 'washes'},
            {'type': 'fill', 'question': 'The children _____ in the garden.', 'answer': 'played'},
            {'type': 'fill', 'question': 'I am _____ a movie tonight.', 'answer': 'watching'},
            {'type': 'fill', 'question': 'She _____ her friends last week.', 'answer': 'visited'},
            {'type': 'fill', 'question': 'We _____ to the beach every summer.', 'answer': 'go'},
            {'type': 'fill', 'question': 'He is _____ his bicycle now.', 'answer': 'fixing'},
            {'type': 'fill', 'question': 'The students _____ their homework.', 'answer': 'finished'},
            {'type': 'fill', 'question': 'I am _____ for my exam.', 'answer': 'studying'},
            {'type': 'fill', 'question': 'She _____ a beautiful song.', 'answer': 'sang'},
            {'type': 'fill', 'question': 'They _____ games after school.', 'answer': 'play'},
            {'type': 'fill', 'question': 'We _____ to music last night.', 'answer': 'listened'},
            {'type': 'fill', 'question': 'He _____ his face every morning.', 'answer': 'washes'},
            {'type': 'fill', 'question': 'I am _____ my room now.', 'answer': 'organizing'},
            {'type': 'fill', 'question': 'She _____ to work by bus.', 'answer': 'goes'},
            {'type': 'fill', 'question': 'We _____ lunch at school.', 'answer': 'had'},
            {'type': 'fill', 'question': 'The teacher _____ us a story.', 'answer': 'told'},
            {'type': 'fill', 'question': 'I _____ my teeth yesterday.', 'answer': 'brushed'},
            {'type': 'fill', 'question': 'She is _____ a letter now.', 'answer': 'writing'},
            {'type': 'fill', 'question': 'They _____ to the library.', 'answer': 'went'},
            {'type': 'fill', 'question': 'We are _____ a picture.', 'answer': 'drawing'},
            {'type': 'fill', 'question': 'He always _____ his bag.', 'answer': 'brings'},
            {'type': 'fill', 'question': 'I _____ to the store yesterday.', 'answer': 'went'},
        ]
        
    def get_gerund_questions(self):
        return [
            {'type': 'choice', 'question': 'I enjoy _____ music.', 'options': ['listen', 'listens', 'listening', 'listened'], 'answer': 'listening'},
            {'type': 'choice', 'question': 'She hates _____ early.', 'options': ['wake', 'wakes', 'waking', 'waked'], 'answer': 'waking'},
            {'type': 'choice', 'question': 'They are good at _____ games.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'playing'},
            {'type': 'choice', 'question': 'He dislikes _____ vegetables.', 'options': ['eat', 'eats', 'eating', 'ate'], 'answer': 'eating'},
            {'type': 'choice', 'question': 'We are interested in _____ stories.', 'options': ['read', 'reads', 'reading', 'readed'], 'answer': 'reading'},
            {'type': 'choice', 'question': 'My brother practices _____ the piano every day.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'playing'},
            {'type': 'choice', 'question': 'She avoids _____ in the rain.', 'options': ['walk', 'walks', 'walking', 'walked'], 'answer': 'walking'},
            {'type': 'choice', 'question': 'They keep _____ English every day.', 'options': ['study', 'studies', 'studying', 'studied'], 'answer': 'studying'},
            {'type': 'choice', 'question': 'He finishes _____ his homework at 9 PM.', 'options': ['do', 'does', 'doing', 'did'], 'answer': 'doing'},
            {'type': 'choice', 'question': 'I am considering _____ a new car.', 'options': ['buy', 'buys', 'buying', 'bought'], 'answer': 'buying'},
            {'type': 'choice', 'question': 'We are looking forward to _____ you soon.', 'options': ['see', 'sees', 'seeing', 'saw'], 'answer': 'seeing'},
            {'type': 'choice', 'question': 'She can\'t help _____ laughing.', 'options': ['laugh', 'laughs', 'laughing', 'laughed'], 'answer': 'laughing'},
            {'type': 'choice', 'question': 'They suggested _____ to the cinema.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'going'},
            {'type': 'choice', 'question': 'I am thinking about _____ a vacation.', 'options': ['take', 'takes', 'taking', 'took'], 'answer': 'taking'},
            {'type': 'choice', 'question': 'He is afraid of _____ spiders.', 'options': ['see', 'sees', 'seeing', 'saw'], 'answer': 'seeing'},
            {'type': 'choice', 'question': 'We are used to _____ early.', 'options': ['wake', 'wakes', 'waking', 'woke'], 'answer': 'waking'},
            {'type': 'choice', 'question': 'She is excited about _____ to the party.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'going'},
            {'type': 'choice', 'question': 'They are tired of _____ the same thing.', 'options': ['do', 'does', 'doing', 'did'], 'answer': 'doing'},
            {'type': 'choice', 'question': 'I am good at _____ puzzles.', 'options': ['solve', 'solves', 'solving', 'solved'], 'answer': 'solving'},
            {'type': 'choice', 'question': 'He is interested in _____ languages.', 'options': ['learn', 'learns', 'learning', 'learned'], 'answer': 'learning'},
            {'type': 'choice', 'question': 'We are proud of _____ you.', 'options': ['help', 'helps', 'helping', 'helped'], 'answer': 'helping'},
            {'type': 'choice', 'question': 'She dreams of _____ a doctor.', 'options': ['become', 'becomes', 'becoming', 'became'], 'answer': 'becoming'},
            {'type': 'choice', 'question': 'They are responsible for _____ the project.', 'options': ['manage', 'manages', 'managing', 'managed'], 'answer': 'managing'},
            {'type': 'choice', 'question': 'I am busy _____ for my exam.', 'options': ['study', 'studies', 'studying', 'studied'], 'answer': 'studying'},
            {'type': 'choice', 'question': 'He is famous for _____ stories.', 'options': ['write', 'writes', 'writing', 'wrote'], 'answer': 'writing'},
            {'type': 'choice', 'question': 'We are worried about _____ the test.', 'options': ['fail', 'fails', 'failing', 'failed'], 'answer': 'failing'},
            {'type': 'choice', 'question': 'She is expert in _____ problems.', 'options': ['solve', 'solves', 'solving', 'solved'], 'answer': 'solving'},
            {'type': 'choice', 'question': 'They are happy _____ the news.', 'options': ['hear', 'hears', 'hearing', 'heard'], 'answer': 'hearing'},
            {'type': 'choice', 'question': 'I am serious about _____ my goal.', 'options': ['achieve', 'achieves', 'achieving', 'achieved'], 'answer': 'achieving'},
            {'type': 'choice', 'question': 'He is crazy about _____ football.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'playing'},
            # 填空题
            {'type': 'fill', 'question': 'I like _____ in the morning.', 'answer': 'running'},
            {'type': 'fill', 'question': 'She is good at _____ pictures.', 'answer': 'drawing'},
            {'type': 'fill', 'question': 'They enjoy _____ with friends.', 'answer': 'playing'},
            {'type': 'fill', 'question': 'He dislikes _____ in the rain.', 'answer': 'walking'},
            {'type': 'fill', 'question': 'We are busy _____ our project.', 'answer': 'working on'},
            {'type': 'fill', 'question': 'They stopped _____ because it started to rain.', 'answer': 'playing'},
            {'type': 'fill', 'question': 'She suggested _____ to the park.', 'answer': 'going'},
            {'type': 'fill', 'question': 'I remember _____ her at the party.', 'answer': 'meeting'},
            {'type': 'fill', 'question': 'He admitted _____ the window.', 'answer': 'breaking'},
            {'type': 'fill', 'question': 'We are looking forward to _____ you.', 'answer': 'seeing'},
            {'type': 'fill', 'question': 'She can\'t help _____ laughing.', 'answer': 'laughing'},
            {'type': 'fill', 'question': 'They suggested _____ to the cinema.', 'answer': 'going'},
            {'type': 'fill', 'question': 'I am thinking about _____ a vacation.', 'answer': 'taking'},
            {'type': 'fill', 'question': 'He is afraid of _____ spiders.', 'answer': 'seeing'},
            {'type': 'fill', 'question': 'We are used to _____ early.', 'answer': 'waking'},
            {'type': 'fill', 'question': 'She is excited about _____ to the party.', 'answer': 'going'},
            {'type': 'fill', 'question': 'They are tired of _____ the same thing.', 'answer': 'doing'},
            {'type': 'fill', 'question': 'I am good at _____ puzzles.', 'answer': 'solving'},
            {'type': 'fill', 'question': 'He is interested in _____ languages.', 'answer': 'learning'},
            {'type': 'fill', 'question': 'We are proud of _____ you.', 'answer': 'helping'},
            {'type': 'fill', 'question': 'She dreams of _____ a doctor.', 'answer': 'becoming'},
            {'type': 'fill', 'question': 'They are responsible for _____ the project.', 'answer': 'managing'},
            {'type': 'fill', 'question': 'I am busy _____ for my exam.', 'answer': 'studying'},
            {'type': 'fill', 'question': 'He is famous for _____ stories.', 'answer': 'writing'},
            {'type': 'fill', 'question': 'We are worried about _____ the test.', 'answer': 'failing'},
            {'type': 'fill', 'question': 'She is expert in _____ problems.', 'answer': 'solving'},
            {'type': 'fill', 'question': 'They are happy _____ the news.', 'answer': 'hearing'},
            {'type': 'fill', 'question': 'I am serious about _____ my goal.', 'answer': 'achieving'},
            {'type': 'fill', 'question': 'He is crazy about _____ football.', 'answer': 'playing'},
        ]
        
    def get_modal_questions(self):
        return [
            {'type': 'choice', 'question': '_____ you help me with this problem?', 'options': ['Can', 'May', 'Must', 'Should'], 'answer': 'Can'},
            {'type': 'choice', 'question': 'It is raining. You _____ take an umbrella.', 'options': ['can', 'may', 'must', 'could'], 'answer': 'must'},
            {'type': 'choice', 'question': '_____ I borrow your pencil?', 'options': ['Can', 'Must', 'Should', 'Will'], 'answer': 'Can'},
            {'type': 'choice', 'question': 'You _____ finish your homework before watching TV.', 'options': ['can', 'may', 'must', 'could'], 'answer': 'must'},
            {'type': 'choice', 'question': 'She _____ speak English very well.', 'options': ['can', 'may', 'must', 'should'], 'answer': 'can'},
            {'type': 'choice', 'question': 'You _____ not run in the hallway.', 'options': ['can', 'may', 'must', 'mustn\'t'], 'answer': 'mustn\'t'},
            {'type': 'choice', 'question': '_____ I come in?', 'options': ['Can', 'May', 'Must', 'Should'], 'answer': 'May'},
            {'type': 'choice', 'question': 'We _____ be quiet in the library.', 'options': ['can', 'may', 'must', 'could'], 'answer': 'must'},
            {'type': 'choice', 'question': 'You _____ try again.', 'options': ['can', 'should', 'must', 'may'], 'answer': 'should'},
            {'type': 'choice', 'question': '_____ I use your phone?', 'options': ['Can', 'Must', 'Shall', 'Will'], 'answer': 'Can'},
            {'type': 'choice', 'question': 'He is very tired. He _____ go home now.', 'options': ['can', 'may', 'must', 'could'], 'answer': 'must'},
            {'type': 'choice', 'question': 'You _____ eat a lot of candy.', 'options': ['shouldn\'t', 'can', 'may', 'could'], 'answer': 'shouldn\'t'},
            {'type': 'choice', 'question': '_____ you please open the window?', 'options': ['Can', 'May', 'Must', 'Will'], 'answer': 'Can'},
            {'type': 'choice', 'question': 'We _____ protect the environment.', 'options': ['can', 'may', 'must', 'could'], 'answer': 'must'},
            {'type': 'choice', 'question': '_____ I help you with your bags?', 'options': ['Can', 'May', 'Must', 'Should'], 'answer': 'Can'},
            {'type': 'choice', 'question': 'You _____ believe in yourself.', 'options': ['can', 'may', 'must', 'could'], 'answer': 'must'},
            {'type': 'choice', 'question': '_____ I sit here?', 'options': ['Can', 'May', 'Must', 'Will'], 'answer': 'May'},
            {'type': 'choice', 'question': 'Students _____ listen to the teacher carefully.', 'options': ['can', 'may', 'must', 'could'], 'answer': 'must'},
            {'type': 'choice', 'question': 'You _____ be late for school.', 'options': ['can', 'may', 'must', 'mustn\'t'], 'answer': 'mustn\'t'},
            {'type': 'choice', 'question': '_____ we go to the park tomorrow?', 'options': ['Can', 'May', 'Must', 'Shall'], 'answer': 'Shall'},
            {'type': 'choice', 'question': 'She _____ have finished her work by now.', 'options': ['can', 'may', 'must', 'should'], 'answer': 'should'},
            {'type': 'choice', 'question': '_____ I know the answer to this question?', 'options': ['Can', 'May', 'Must', 'Will'], 'answer': 'Can'},
            {'type': 'choice', 'question': 'He _____ not be at home now.', 'options': ['can', 'may', 'must', 'might'], 'answer': 'might'},
            {'type': 'choice', 'question': 'You _____ do what you want to do.', 'options': ['can', 'may', 'must', 'should'], 'answer': 'can'},
            {'type': 'choice', 'question': '_____ I have another piece of cake?', 'options': ['Can', 'May', 'Must', 'Will'], 'answer': 'May'},
            {'type': 'choice', 'question': 'We _____ start the meeting now.', 'options': ['can', 'may', 'must', 'shall'], 'answer': 'shall'},
            {'type': 'choice', 'question': 'You _____ be more careful next time.', 'options': ['can', 'should', 'may', 'might'], 'answer': 'should'},
            {'type': 'choice', 'question': '_____ she be coming to the party?', 'options': ['Can', 'May', 'Must', 'Will'], 'answer': 'May'},
            {'type': 'choice', 'question': 'I _____ see what you mean.', 'options': ['can', 'may', 'must', 'could'], 'answer': 'can'},
            {'type': 'choice', 'question': '_____ they be waiting for us?', 'options': ['Can', 'May', 'Must', 'Should'], 'answer': 'May'},
            {'type': 'choice', 'question': 'You _____ not tell anyone about this.', 'options': ['can', 'may', 'must', 'mustn\'t'], 'answer': 'mustn\'t'},
            {'type': 'choice', 'question': '_____ we meet at the station tomorrow?', 'options': ['Can', 'May', 'Must', 'Shall'], 'answer': 'Shall'},
            {'type': 'choice', 'question': 'He _____ be studying in his room.', 'options': ['can', 'may', 'must', 'could'], 'answer': 'may'},
            {'type': 'choice', 'question': '_____ I borrow your umbrella?', 'options': ['Can', 'May', 'Must', 'Should'], 'answer': 'Can'},
            {'type': 'choice', 'question': 'You _____ wear a seatbelt in the car.', 'options': ['can', 'may', 'must', 'could'], 'answer': 'must'},
            {'type': 'choice', 'question': '_____ she come with us to the movies?', 'options': ['Can', 'May', 'Must', 'Will'], 'answer': 'May'},
            {'type': 'fill', 'question': 'I _____ swim very well. (can)', 'answer': 'can'},
            {'type': 'fill', 'question': 'You _____ finish your work today. (must)', 'answer': 'must'},
            {'type': 'fill', 'question': '_____ I use your pen? (can)', 'answer': 'Can'},
            {'type': 'fill', 'question': 'She _____ speak French. (can)', 'answer': 'can'},
            {'type': 'fill', 'question': 'You _____ be quiet in the library. (must)', 'answer': 'must'},
            {'type': 'fill', 'question': '_____ you help me? (can)', 'answer': 'Can'},
            {'type': 'fill', 'question': 'We _____ protect wild animals. (must)', 'answer': 'must'},
            {'type': 'fill', 'question': '_____ I come in? (may)', 'answer': 'May'},
            {'type': 'fill', 'question': 'You _____ try your best. (should)', 'answer': 'should'},
            {'type': 'fill', 'question': 'He _____ go home early yesterday. (could)', 'answer': 'could'},
            {'type': 'fill', 'question': '_____ I have another try? (can)', 'answer': 'Can'},
            {'type': 'fill', 'question': 'She _____ have finished her homework. (must)', 'answer': 'must'},
            {'type': 'fill', 'question': '_____ we start the class now? (shall)', 'answer': 'Shall'},
            {'type': 'fill', 'question': 'You _____ be more careful. (should)', 'answer': 'should'},
            {'type': 'fill', 'question': '_____ he be coming to the meeting? (may)', 'answer': 'May'},
            {'type': 'fill', 'question': '_____ you understand what I mean? (can)', 'answer': 'Can'},
            {'type': 'fill', 'question': 'They _____ be waiting for us. (may)', 'answer': 'may'},
            {'type': 'fill', 'question': '_____ we meet at the park? (shall)', 'answer': 'Shall'},
            {'type': 'fill', 'question': '_____ I borrow your book? (may)', 'answer': 'May'},
            {'type': 'fill', 'question': 'She _____ be very tired now. (must)', 'answer': 'must'},
            {'type': 'fill', 'question': '_____ you do me a favor? (can)', 'answer': 'Can'},
            {'type': 'fill', 'question': 'We _____ be more careful next time. (should)', 'answer': 'should'},
            {'type': 'fill', 'question': '_____ I have some water? (may)', 'answer': 'May'},
            {'type': 'fill', 'question': 'He _____ have finished the project. (must)', 'answer': 'must'},
            {'type': 'fill', 'question': '_____ we go to the beach tomorrow? (shall)', 'answer': 'Shall'},
            {'type': 'fill', 'question': '_____ you speak English fluently? (can)', 'answer': 'Can'},
            {'type': 'fill', 'question': 'They _____ be having dinner now. (may)', 'answer': 'may'},
            {'type': 'fill', 'question': '_____ I sit next to you? (may)', 'answer': 'May'},
            {'type': 'fill', 'question': 'You _____ not forget to do your homework. (must)', 'answer': 'must'},
            {'type': 'fill', 'question': '_____ we start the game? (shall)', 'answer': 'Shall'},
        ]
        
    def get_be_verb_questions(self):
        return [
            {'type': 'choice', 'question': 'I _____ a student.', 'options': ['am', 'is', 'are', 'be'], 'answer': 'am'},
            {'type': 'choice', 'question': 'She _____ a teacher.', 'options': ['am', 'is', 'are', 'be'], 'answer': 'is'},
            {'type': 'choice', 'question': 'They _____ friends.', 'options': ['am', 'is', 'are', 'be'], 'answer': 'are'},
            {'type': 'choice', 'question': 'He _____ playing football now.', 'options': ['am', 'is', 'are', 'be'], 'answer': 'is'},
            {'type': 'choice', 'question': 'We _____ having dinner.', 'options': ['am', 'is', 'are', 'be'], 'answer': 'are'},
            {'type': 'choice', 'question': 'The book _____ on the table.', 'options': ['am', 'is', 'are', 'be'], 'answer': 'is'},
            {'type': 'choice', 'question': 'I _____ born in 2015.', 'options': ['am', 'was', 'were', 'be'], 'answer': 'was'},
            {'type': 'choice', 'question': 'She _____ happy yesterday.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'was'},
            {'type': 'choice', 'question': 'They _____ at home last night.', 'options': ['was', 'were', 'is', 'are'], 'answer': 'were'},
            {'type': 'choice', 'question': 'I _____ a child then.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'was'},
            {'type': 'choice', 'question': 'She _____ hungry now.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'is'},
            {'type': 'choice', 'question': 'We _____ good friends.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'are'},
            {'type': 'choice', 'question': 'The flowers _____ beautiful last spring.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'were'},
            {'type': 'choice', 'question': 'He _____ a doctor when he grows up.', 'options': ['am', 'is', 'are', 'will be'], 'answer': 'will be'},
            {'type': 'choice', 'question': 'I _____ to the park tomorrow.', 'options': ['am', 'is', 'are', 'will go'], 'answer': 'will go'},
            {'type': 'choice', 'question': 'The sky _____ blue today.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'is'},
            {'type': 'choice', 'question': 'My parents _____ at work yesterday.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'were'},
            {'type': 'choice', 'question': 'It _____ a sunny day tomorrow.', 'options': ['am', 'is', 'are', 'will be'], 'answer': 'will be'},
            {'type': 'choice', 'question': 'The children _____ in the classroom.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'are'},
            {'type': 'choice', 'question': 'I _____ doing my homework.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'am'},
            {'type': 'choice', 'question': 'The dogs _____ sleeping in the yard.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'are'},
            {'type': 'choice', 'question': 'She _____ very tired last night.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'was'},
            {'type': 'choice', 'question': 'We _____ ready for the trip.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'are'},
            {'type': 'choice', 'question': 'The cat _____ hiding under the bed.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'is'},
            {'type': 'choice', 'question': 'They _____ studying English last year.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'were'},
            {'type': 'choice', 'question': 'The car _____ parked outside.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'is'},
            {'type': 'choice', 'question': 'I _____ very excited about the concert.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'am'},
            {'type': 'choice', 'question': 'She _____ the best student in class.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'is'},
            {'type': 'choice', 'question': 'The students _____ taking a test now.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'are'},
            {'type': 'choice', 'question': 'We _____ late for school yesterday.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'were'},
            {'type': 'choice', 'question': 'It _____ very cold last winter.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'was'},
            {'type': 'choice', 'question': 'The teacher _____ explaining the lesson.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'is'},
            {'type': 'choice', 'question': 'They _____ going to the movies tomorrow.', 'options': ['am', 'is', 'are', 'will be'], 'answer': 'will be'},
            {'type': 'choice', 'question': 'I _____ watching TV last night.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'was'},
            {'type': 'choice', 'question': 'The windows _____ open in the morning.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'are'},
            {'type': 'choice', 'question': 'She _____ wearing a red dress.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'is'},
            {'type': 'choice', 'question': 'We _____ having a meeting this afternoon.', 'options': ['am', 'is', 'are', 'will be'], 'answer': 'will be'},
            {'type': 'choice', 'question': 'The bird _____ singing in the tree.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'is'},
            {'type': 'choice', 'question': 'They _____ living in Beijing last year.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'were'},
            {'type': 'choice', 'question': 'I _____ very busy this week.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'am'},
            {'type': 'choice', 'question': 'The door _____ locked last night.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'was'},
            {'type': 'choice', 'question': 'We _____ planning our vacation.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'are'},
            {'type': 'choice', 'question': 'She _____ the tallest girl in the class.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'is'},
            {'type': 'choice', 'question': 'The computers _____ working properly.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'are'},
            {'type': 'choice', 'question': 'I _____ reading a book now.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'am'},
            {'type': 'choice', 'question': 'They _____ playing basketball yesterday.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'were'},
            {'type': 'choice', 'question': 'The music _____ very loud last night.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'was'},
            {'type': 'choice', 'question': 'We _____ going to the party tonight.', 'options': ['am', 'is', 'are', 'will be'], 'answer': 'will be'},
            {'type': 'choice', 'question': 'She _____ cooking dinner for us.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'is'},
            {'type': 'choice', 'question': 'The children _____ sleeping in their rooms.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'are'},
            {'type': 'choice', 'question': 'I _____ very happy today.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'am'},
            {'type': 'choice', 'question': 'They _____ having a great time at the party.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'are'},
            {'type': 'choice', 'question': 'The sun _____ shining brightly this morning.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'is'},
            {'type': 'choice', 'question': 'We _____ waiting for the bus.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'are'},
            {'type': 'choice', 'question': 'She _____ wearing a beautiful dress.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'is'},
            {'type': 'choice', 'question': 'The garden _____ full of flowers in spring.', 'options': ['am', 'is', 'are', 'was'], 'answer': 'was'},
            {'type': 'choice', 'question': 'I _____ going to visit my grandmother tomorrow.', 'options': ['am', 'is', 'are', 'will be'], 'answer': 'will be'},
            {'type': 'choice', 'question': 'The students _____ studying hard for the exam.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'are'},
            {'type': 'choice', 'question': 'They _____ living in a big house last year.', 'options': ['am', 'is', 'are', 'were'], 'answer': 'were'},
            {'type': 'fill', 'question': 'I _____ a student. (am)', 'answer': 'am'},
            {'type': 'fill', 'question': 'She _____ a teacher. (is)', 'answer': 'is'},
            {'type': 'fill', 'question': 'They _____ friends. (are)', 'answer': 'are'},
            {'type': 'fill', 'question': 'He _____ playing now. (is)', 'answer': 'is'},
            {'type': 'fill', 'question': 'We _____ happy yesterday. (were)', 'answer': 'were'},
            {'type': 'fill', 'question': 'I _____ born in 2015. (was)', 'answer': 'was'},
            {'type': 'fill', 'question': 'She _____ hungry now. (is)', 'answer': 'is'},
            {'type': 'fill', 'question': 'They _____ at school. (are)', 'answer': 'are'},
            {'type': 'fill', 'question': 'It _____ a nice day. (is)', 'answer': 'is'},
            {'type': 'fill', 'question': 'The book _____ on the desk. (is)', 'answer': 'is'},
            {'type': 'fill', 'question': 'We _____ studying English last year. (were)', 'answer': 'were'},
            {'type': 'fill', 'question': 'I _____ reading a book now. (am)', 'answer': 'am'},
            {'type': 'fill', 'question': 'She _____ wearing a red dress. (is)', 'answer': 'is'},
            {'type': 'fill', 'question': 'They _____ playing basketball yesterday. (were)', 'answer': 'were'},
            {'type': 'fill', 'question': 'It _____ very cold last winter. (was)', 'answer': 'was'},
            {'type': 'fill', 'question': 'We _____ going to the party tonight. (will be)', 'answer': 'will be'},
            {'type': 'fill', 'question': 'She _____ cooking dinner for us. (is)', 'answer': 'is'},
            {'type': 'fill', 'question': 'The children _____ sleeping in their rooms. (are)', 'answer': 'are'},
            {'type': 'fill', 'question': 'I _____ very happy today. (am)', 'answer': 'am'},
            {'type': 'fill', 'question': 'They _____ having a great time. (are)', 'answer': 'are'},
            {'type': 'fill', 'question': 'The sun _____ shining brightly. (is)', 'answer': 'is'},
            {'type': 'fill', 'question': 'We _____ waiting for the bus. (are)', 'answer': 'are'},
            {'type': 'fill', 'question': 'She _____ the tallest girl in class. (is)', 'answer': 'is'},
            {'type': 'fill', 'question': 'The garden _____ full of flowers. (was)', 'answer': 'was'},
            {'type': 'fill', 'question': 'I _____ going to visit my grandmother. (will be)', 'answer': 'will be'},
            {'type': 'fill', 'question': 'The students _____ studying hard. (are)', 'answer': 'are'},
            {'type': 'fill', 'question': 'They _____ living in a big house. (were)', 'answer': 'were'},
            {'type': 'fill', 'question': 'The music _____ very loud last night. (was)', 'answer': 'was'},
            {'type': 'fill', 'question': 'We _____ having a meeting this afternoon. (will be)', 'answer': 'will be'},
            {'type': 'fill', 'question': 'The teacher _____ explaining the lesson. (is)', 'answer': 'is'},
            {'type': 'fill', 'question': 'They _____ going to the movies tomorrow. (will be)', 'answer': 'will be'},
            {'type': 'fill', 'question': 'I _____ watching TV last night. (was)', 'answer': 'was'},
            {'type': 'fill', 'question': 'The windows _____ open in the morning. (are)', 'answer': 'are'},
            {'type': 'fill', 'question': 'She _____ very excited about the concert. (is)', 'answer': 'is'},
            {'type': 'fill', 'question': 'We _____ ready for the trip. (are)', 'answer': 'are'},
            {'type': 'fill', 'question': 'The cat _____ hiding under the bed. (is)', 'answer': 'is'},
            {'type': 'fill', 'question': 'They _____ studying English last year. (were)', 'answer': 'were'},
            {'type': 'fill', 'question': 'The car _____ parked outside. (is)', 'answer': 'is'},
            {'type': 'fill', 'question': 'I _____ very busy this week. (am)', 'answer': 'am'},
            {'type': 'fill', 'question': 'The door _____ locked last night. (was)', 'answer': 'was'},
            {'type': 'fill', 'question': 'We _____ planning our vacation. (are)', 'answer': 'are'},
            {'type': 'fill', 'question': 'The computers _____ working properly. (are)', 'answer': 'are'},
            {'type': 'fill', 'question': 'The bird _____ singing in the tree. (is)', 'answer': 'is'},
            {'type': 'fill', 'question': 'They _____ living in Beijing last year. (were)', 'answer': 'were'},
            {'type': 'fill', 'question': 'The garden _____ beautiful in spring. (was)', 'answer': 'was'},
        ]
        
    def get_question_questions(self):
        return [
            {'type': 'choice', 'question': '_____ is your name?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ do you live?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'Where'},
            {'type': 'choice', 'question': '_____ is your birthday?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'When'},
            {'type': 'choice', 'question': '_____ is that girl?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'Who'},
            {'type': 'choice', 'question': '_____ do you go to school?', 'options': ['Where', 'What', 'How', 'When'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ many books do you have?', 'options': ['Where', 'What', 'How', 'When'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ is this?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ are you from?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'Where'},
            {'type': 'choice', 'question': '_____ do you eat breakfast?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'When'},
            {'type': 'choice', 'question': '_____ is your teacher?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'Who'},
            {'type': 'choice', 'question': '_____ color is your pen?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ do you like English?', 'options': ['Where', 'What', 'Why', 'When'], 'answer': 'Why'},
            {'type': 'choice', 'question': '_____ is the weather like today?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ old are you?', 'options': ['Where', 'What', 'How', 'When'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ do you do on weekends?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ time is it now?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ does she go to work?', 'options': ['Where', 'What', 'How', 'When'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ are you doing?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ is your phone number?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ did you go on vacation?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'Where'},
            {'type': 'choice', 'question': '_____ is the capital of France?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ do you study English?', 'options': ['Where', 'What', 'How', 'When'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ is your favorite movie?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ are you looking for?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ did she arrive at the party?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'When'},
            {'type': 'choice', 'question': '_____ are those people?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'Who'},
            {'type': 'choice', 'question': '_____ much does this cost?', 'options': ['Where', 'What', 'How', 'When'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ do you want to be?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ did they meet each other?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'Where'},
            {'type': 'choice', 'question': '_____ tall is the building?', 'options': ['Where', 'What', 'How', 'When'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ is your sister\'s name?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ are you waiting for?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'Who'},
            {'type': 'choice', 'question': '_____ did you learn to drive?', 'options': ['Where', 'What', 'How', 'When'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ is the next train?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ are you traveling to?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'Where'},
            {'type': 'choice', 'question': '_____ is your hometown?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ do you prefer coffee or tea?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ did they get married?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'When'},
            {'type': 'choice', 'question': '_____ is your mother\'s occupation?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ long does it take to get there?', 'options': ['Where', 'What', 'How', 'When'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ is the library located?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'Where'},
            {'type': 'choice', 'question': '_____ does your father work?', 'options': ['Where', 'What', 'How', 'When'], 'answer': 'Where'},
            {'type': 'choice', 'question': '_____ is your ideal vacation?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ did you buy that dress?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'Where'},
            {'type': 'choice', 'question': '_____ do you celebrate your birthday?', 'options': ['Where', 'What', 'How', 'When'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ is the concert tonight?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ did you spend your summer vacation?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'Where'},
            {'type': 'choice', 'question': '_____ is your pet\'s name?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ often do you exercise?', 'options': ['Where', 'What', 'How', 'When'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ is the nearest hospital?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'Where'},
            {'type': 'choice', 'question': '_____ did you finish your homework?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'When'},
            {'type': 'choice', 'question': '_____ is the president of the company?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'Who'},
            {'type': 'choice', 'question': '_____ far is it to the airport?', 'options': ['Where', 'What', 'How', 'When'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ is your dream job?', 'options': ['Where', 'What', 'Who', 'When'], 'answer': 'What'},
            {'type': 'fill', 'question': '_____ is your name?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ do you live?', 'answer': 'Where'},
            {'type': 'fill', 'question': '_____ is your birthday?', 'answer': 'When'},
            {'type': 'fill', 'question': '_____ is that boy?', 'answer': 'Who'},
            {'type': 'fill', 'question': '_____ do you go to school?', 'answer': 'How'},
            {'type': 'fill', 'question': '_____ many friends do you have?', 'answer': 'How'},
            {'type': 'fill', 'question': '_____ is this?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ are you from?', 'answer': 'Where'},
            {'type': 'fill', 'question': '_____ do you eat dinner?', 'answer': 'When'},
            {'type': 'fill', 'question': '_____ is your favorite subject?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ time is it now?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ does she go to work?', 'answer': 'How'},
            {'type': 'fill', 'question': '_____ are you doing?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ is your phone number?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ did you go on vacation?', 'answer': 'Where'},
            {'type': 'fill', 'question': '_____ is the capital of France?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ do you study English?', 'answer': 'How'},
            {'type': 'fill', 'question': '_____ is your favorite movie?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ are you looking for?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ did she arrive at the party?', 'answer': 'When'},
            {'type': 'fill', 'question': '_____ are those people?', 'answer': 'Who'},
            {'type': 'fill', 'question': '_____ much does this cost?', 'answer': 'How'},
            {'type': 'fill', 'question': '_____ do you want to be?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ did they meet each other?', 'answer': 'Where'},
            {'type': 'fill', 'question': '_____ tall is the building?', 'answer': 'How'},
            {'type': 'fill', 'question': '_____ is your sister\'s name?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ are you waiting for?', 'answer': 'Who'},
            {'type': 'fill', 'question': '_____ did you learn to drive?', 'answer': 'How'},
            {'type': 'fill', 'question': '_____ is the next train?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ are you traveling to?', 'answer': 'Where'},
            {'type': 'fill', 'question': '_____ is your hometown?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ do you prefer coffee or tea?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ did they get married?', 'answer': 'When'},
            {'type': 'fill', 'question': '_____ is your mother\'s occupation?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ long does it take to get there?', 'answer': 'How'},
            {'type': 'fill', 'question': '_____ is the library located?', 'answer': 'Where'},
            {'type': 'fill', 'question': '_____ does your father work?', 'answer': 'Where'},
            {'type': 'fill', 'question': '_____ is your ideal vacation?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ did you buy that dress?', 'answer': 'Where'},
            {'type': 'fill', 'question': '_____ do you celebrate your birthday?', 'answer': 'How'},
            {'type': 'fill', 'question': '_____ is the concert tonight?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ did you spend your summer vacation?', 'answer': 'Where'},
            {'type': 'fill', 'question': '_____ is your pet\'s name?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ often do you exercise?', 'answer': 'How'},
            {'type': 'fill', 'question': '_____ is the nearest hospital?', 'answer': 'Where'},
            {'type': 'fill', 'question': '_____ did you finish your homework?', 'answer': 'When'},
            {'type': 'fill', 'question': '_____ is the president of the company?', 'answer': 'Who'},
            {'type': 'fill', 'question': '_____ far is it to the airport?', 'answer': 'How'},
            {'type': 'fill', 'question': '_____ is your dream job?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ do you like to do in your free time?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ did you last visit the doctor?', 'answer': 'When'},
            {'type': 'fill', 'question': '_____ is your best friend\'s hobby?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ often does it rain here?', 'answer': 'How'},
            {'type': 'fill', 'question': '_____ are the children playing?', 'answer': 'Where'},
            {'type': 'fill', 'question': '_____ did you last see your grandparents?', 'answer': 'When'},
        ]
        
    def get_comprehensive_questions(self):
        return [
            {'type': 'choice', 'question': 'There are many _____ on the table.', 'options': ['apple', 'apples', 'appled', 'appleses'], 'answer': 'apples'},
            {'type': 'choice', 'question': 'I have three _____ in my room.', 'options': ['book', 'books', 'bookes', 'book'], 'answer': 'books'},
            {'type': 'choice', 'question': 'The _____ are playing in the garden.', 'options': ['child', 'childs', 'children', 'childrens'], 'answer': 'children'},
            {'type': 'choice', 'question': 'She bought two _____ of bread.', 'options': ['loaf', 'loafs', 'loaves', 'loafes'], 'answer': 'loaves'},
            {'type': 'choice', 'question': 'There are some _____ in the sky.', 'options': ['cloud', 'clouds', 'cloudy', 'cloudes'], 'answer': 'clouds'},
            {'type': 'choice', 'question': 'My father has two _____ at work.', 'options': ['desk', 'desks', 'deskes', 'desk'], 'answer': 'desks'},
            {'type': 'choice', 'question': 'The _____ are very beautiful in spring.', 'options': ['flower', 'flowers', 'floweres', 'flower'], 'answer': 'flowers'},
            {'type': 'choice', 'question': 'I can see many _____ in the river.', 'options': ['fish', 'fishes', 'fishs', 'fishes'], 'answer': 'fish'},
            {'type': 'choice', 'question': 'There are five _____ in my class.', 'options': ['man', 'men', 'mans', 'manes'], 'answer': 'men'},
            {'type': 'choice', 'question': 'The _____ are drinking water.', 'options': ['woman', 'womans', 'women', 'womens'], 'answer': 'women'},
            {'type': 'choice', 'question': 'I have two _____ in my bag.', 'options': ['knife', 'knifes', 'knives', 'knife'], 'answer': 'knives'},
            {'type': 'choice', 'question': 'She bought a new pair of _____', 'options': ['shoe', 'shoes', 'shooes', 'shoe'], 'answer': 'shoes'},
            {'type': 'choice', 'question': 'There are many _____ on the farm.', 'options': ['sheep', 'sheeps', 'sheepes', 'sheep'], 'answer': 'sheep'},
            {'type': 'choice', 'question': 'My grandparents have many _____ stories.', 'options': ['story', 'stories', 'storys', 'storyes'], 'answer': 'stories'},
            {'type': 'choice', 'question': 'The _____ are having a meeting.', 'options': ['policeman', 'policemans', 'policemen', 'policemers'], 'answer': 'policemen'},
            {'type': 'fill', 'question': 'There are three _____ on the plate. (tomato)', 'answer': 'tomatoes'},
            {'type': 'fill', 'question': 'I have two _____ in my hand. (watch)', 'answer': 'watches'},
            {'type': 'fill', 'question': 'The _____ are doing exercise. (baby)', 'answer': 'babies'},
            {'type': 'fill', 'question': 'She has many _____ in her room. (doll)', 'answer': 'dolls'},
            {'type': 'fill', 'question': 'There are some _____ on the tree. (leaf)', 'answer': 'leaves'},
            {'type': 'choice', 'question': '_____ is my best friend.', 'options': ['I', 'Me', 'My', 'Mine'], 'answer': 'I'},
            {'type': 'choice', 'question': 'This book is _____', 'options': ['me', 'my', 'mine', 'I'], 'answer': 'mine'},
            {'type': 'choice', 'question': 'The red bike belongs to Tom. It is _____', 'options': ['his', 'he', 'him', 'himself'], 'answer': 'his'},
            {'type': 'choice', 'question': 'The classroom is _____ (our).', 'options': ['our', 'ours', 'we', 'us'], 'answer': 'ours'},
            {'type': 'choice', 'question': 'Help _____ to some fruits, please.', 'options': ['you', 'your', 'yours', 'yourself'], 'answer': 'yourself'},
            {'type': 'choice', 'question': 'I can do it by _____.', 'options': ['me', 'my', 'myself', 'mine'], 'answer': 'myself'},
            {'type': 'choice', 'question': '_____ is sitting under the tree.', 'options': ['Someone', 'Anyone', 'No one', 'Everyone'], 'answer': 'Someone'},
            {'type': 'choice', 'question': 'Is there _____ in the room?', 'options': ['someone', 'anyone', 'no one', 'everyone'], 'answer': 'anyone'},
            {'type': 'choice', 'question': '_____ knows the answer to this question.', 'options': ['Someone', 'Anyone', 'Everyone', 'No one'], 'answer': 'Everyone'},
            {'type': 'choice', 'question': 'There is _____ in my bag.', 'options': ['something', 'anything', 'nothing', 'everything'], 'answer': 'nothing'},
            {'type': 'choice', 'question': 'I have _____ to tell you.', 'options': ['something', 'anything', 'nothing', 'everything'], 'answer': 'something'},
            {'type': 'choice', 'question': '_____ of the two books is interesting.', 'options': ['All', 'Both', 'Either', 'Neither'], 'answer': 'Either'},
            {'type': 'choice', 'question': '_____ of my friends came to my birthday party.', 'options': ['All', 'Both', 'Either', 'Neither'], 'answer': 'All'},
            {'type': 'choice', 'question': 'I have two pencils. One is red, _____ is blue.', 'options': ['other', 'the other', 'another', 'others'], 'answer': 'the other'},
            {'type': 'choice', 'question': 'Some students are singing, _____ are dancing.', 'options': ['others', 'the others', 'another', 'other'], 'answer': 'others'},
            {'type': 'fill', 'question': 'This is _____ (I) dictionary.', 'answer': 'my'},
            {'type': 'fill', 'question': 'The blue bag is _____. (she)', 'answer': 'hers'},
            {'type': 'fill', 'question': 'We did the work _____. (we)', 'answer': 'ourselves'},
            {'type': 'fill', 'question': 'Help _____ to some cake. (you)', 'answer': 'yourself'},
            {'type': 'fill', 'question': '_____ is my brother. (he)', 'answer': 'He'},
            {'type': 'choice', 'question': 'This is an _____ book.', 'options': ['interesting', 'interested', 'interest', 'interests'], 'answer': 'interesting'},
            {'type': 'choice', 'question': 'I am _____ in this movie.', 'options': ['interesting', 'interested', 'interest', 'boring'], 'answer': 'interested'},
            {'type': 'choice', 'question': 'The news makes me _____.', 'options': ['sad', 'sadly', 'sadness', 'sads'], 'answer': 'sad'},
            {'type': 'choice', 'question': 'She looks _____ in the red dress.', 'options': ['beautiful', 'beauty', 'beautifully', 'beautifuly'], 'answer': 'beautiful'},
            {'type': 'choice', 'question': 'The flower smells _____.', 'options': ['sweet', 'sweetly', 'sweetness', 'sweetes'], 'answer': 'sweet'},
            {'type': 'choice', 'question': 'The music sounds _____.', 'options': ['beautiful', 'beauty', 'beautifully', 'beautifuly'], 'answer': 'beautiful'},
            {'type': 'choice', 'question': 'The food tastes _____.', 'options': ['good', 'well', 'better', 'best'], 'answer': 'good'},
            {'type': 'choice', 'question': 'I feel _____ today.', 'options': ['happy', 'happily', 'happier', 'happyness'], 'answer': 'happy'},
            {'type': 'choice', 'question': 'This is the _____ movie I have ever seen.', 'options': ['good', 'better', 'best', 'goodest'], 'answer': 'best'},
            {'type': 'choice', 'question': 'Tom is _____ than Jack.', 'options': ['tall', 'taller', 'tallest', 'taller'], 'answer': 'taller'},
            {'type': 'choice', 'question': 'She is as _____ as her mother.', 'options': ['beautiful', 'more beautiful', 'most beautiful', 'beautifuller'], 'answer': 'beautiful'},
            {'type': 'choice', 'question': 'This book is _____ than that one.', 'options': ['thin', 'thinner', 'thinnest', 'thiner'], 'answer': 'thinner'},
            {'type': 'choice', 'question': 'He is the _____ student in our class.', 'options': ['clever', 'cleverer', 'cleverest', 'most clever'], 'answer': 'cleverest'},
            {'type': 'choice', 'question': 'My mother bought some _____ apples.', 'options': ['red', 'redder', 'reddest', 'more red'], 'answer': 'red'},
            {'type': 'choice', 'question': 'The weather is getting _____.', 'options': ['cold', 'colder', 'coldest', 'more cold'], 'answer': 'colder'},
            {'type': 'fill', 'question': 'The book is very _____. (interest)', 'answer': 'interesting'},
            {'type': 'fill', 'question': 'I am _____ with the result. (satisfy)', 'answer': 'satisfied'},
            {'type': 'fill', 'question': 'The news made her _____. (surprise)', 'answer': 'surprised'},
            {'type': 'fill', 'question': 'He is _____ than his brother. (tall)', 'answer': 'taller'},
            {'type': 'fill', 'question': 'This is the _____ movie I have seen. (good)', 'answer': 'best'},
            {'type': 'choice', 'question': 'She speaks English _____.', 'options': ['fluent', 'fluently', 'more fluent', 'most fluent'], 'answer': 'fluently'},
            {'type': 'choice', 'question': 'He runs very _____.', 'options': ['fast', 'faster', 'fastest', 'fastly'], 'answer': 'fast'},
            {'type': 'choice', 'question': 'Please speak _____.', 'options': ['slow', 'slower', 'slowest', 'slowly'], 'answer': 'slowly'},
            {'type': 'choice', 'question': 'The boy ran _____ to catch the bus.', 'options': ['quick', 'quicker', 'quickly', 'quickest'], 'answer': 'quickly'},
            {'type': 'choice', 'question': 'She always _____ comes to school early.', 'options': ['never', 'sometimes', 'often', 'usually'], 'answer': 'always'},
            {'type': 'choice', 'question': 'He _____ goes to the library on Sundays.', 'options': ['never', 'sometimes', 'often', 'ever'], 'answer': 'never'},
            {'type': 'choice', 'question': 'I have _____ been to Beijing.', 'options': ['never', 'ever', 'already', 'yet'], 'answer': 'ever'},
            {'type': 'choice', 'question': 'Have you _____ finished your homework?', 'options': ['yet', 'already', 'never', 'ever'], 'answer': 'yet'},
            {'type': 'choice', 'question': 'She has _____ finished her work.', 'options': ['yet', 'already', 'ever', 'never'], 'answer': 'already'},
            {'type': 'choice', 'question': 'He works _____ than his brother.', 'options': ['hard', 'harder', 'hardest', 'hardly'], 'answer': 'harder'},
            {'type': 'choice', 'question': 'She plays the piano _____.', 'options': ['beautiful', 'beauty', 'beautifully', 'beautifuly'], 'answer': 'beautifully'},
            {'type': 'choice', 'question': 'We should listen _____ in class.', 'options': ['careful', 'carefully', 'careless', 'care'], 'answer': 'carefully'},
            {'type': 'choice', 'question': 'The children are playing _____.', 'options': ['happy', 'happily', 'happier', 'happiest'], 'answer': 'happily'},
            {'type': 'choice', 'question': 'He arrived at school _____.', 'options': ['late', 'later', 'latest', 'lately'], 'answer': 'late'},
            {'type': 'choice', 'question': 'Please come here _____.', 'options': ['quick', 'quicker', 'quickly', 'quickest'], 'answer': 'quickly'},
            {'type': 'fill', 'question': 'She sings _____. (beautiful)', 'answer': 'beautifully'},
            {'type': 'fill', 'question': 'He runs very _____. (fast)', 'answer': 'fast'},
            {'type': 'fill', 'question': 'Please listen _____. (careful)', 'answer': 'carefully'},
            {'type': 'fill', 'question': 'She _____ goes to school late. (usual)', 'answer': 'usually'},
            {'type': 'fill', 'question': 'He works very _____. (hard)', 'answer': 'hard'},
            {'type': 'choice', 'question': 'I have _____ apple.', 'options': ['a', 'an', 'the', '/'], 'answer': 'an'},
            {'type': 'choice', 'question': 'He is _____ honest boy.', 'options': ['a', 'an', 'the', '/'], 'answer': 'an'},
            {'type': 'choice', 'question': 'I saw _____ interesting movie yesterday.', 'options': ['a', 'an', 'the', '/'], 'answer': 'an'},
            {'type': 'choice', 'question': 'She is _____ teacher.', 'options': ['a', 'an', 'the', '/'], 'answer': 'a'},
            {'type': 'choice', 'question': 'I usually go to school by _____ bus.', 'options': ['a', 'an', 'the', '/'], 'answer': '/'},
            {'type': 'choice', 'question': 'The sun rises in _____ east.', 'options': ['a', 'an', 'the', '/'], 'answer': 'the'},
            {'type': 'choice', 'question': 'I want to visit _____ Great Wall.', 'options': ['a', 'an', 'the', '/'], 'answer': 'the'},
            {'type': 'choice', 'question': 'He is playing _____ piano now.', 'options': ['a', 'an', 'the', '/'], 'answer': 'the'},
            {'type': 'choice', 'question': 'I have _____ new bike.', 'options': ['a', 'an', 'the', '/'], 'answer': 'a'},
            {'type': 'choice', 'question': 'Beijing is _____ capital of China.', 'options': ['a', 'an', 'the', '/'], 'answer': 'the'},
            {'type': 'choice', 'question': 'She is _____ tallest girl in our class.', 'options': ['a', 'an', 'the', '/'], 'answer': 'the'},
            {'type': 'choice', 'question': 'He goes to school _____ every day.', 'options': ['a', 'an', 'the', '/'], 'answer': '/'},
            {'type': 'choice', 'question': 'I need _____ hour to finish this work.', 'options': ['a', 'an', 'the', '/'], 'answer': 'an'},
            {'type': 'choice', 'question': 'She is _____ university student.', 'options': ['a', 'an', 'the', '/'], 'answer': 'a'},
            {'type': 'choice', 'question': 'We had _____ wonderful time at the party.', 'options': ['a', 'an', 'the', '/'], 'answer': 'a'},
            {'type': 'fill', 'question': 'This is _____ book. (a)', 'answer': 'a'},
            {'type': 'fill', 'question': 'He is _____ honest boy. (an)', 'answer': 'an'},
            {'type': 'fill', 'question': 'The sun rises in _____ east. (the)', 'answer': 'the'},
            # 首字母填空题
            {'type': 'first_letter', 'question': 'The cat is s_____ on the sofa.', 'answer': 'sitting'},
            {'type': 'first_letter', 'question': 'She likes to r_____ books in the evening.', 'answer': 'read'},
            {'type': 'first_letter', 'question': 'We play f_____ on the playground. ', 'answer': 'football'},
            {'type': 'first_letter', 'question': 'The dog is b_____ at the stranger.', 'answer': 'barking'},
            {'type': 'first_letter', 'question': 'I eat b_____ in the morning.', 'answer': 'breakfast'},
            {'type': 'first_letter', 'question': 'She can s_____ English very well.', 'answer': 'speak'},
            {'type': 'first_letter', 'question': 'The bird is s_____ in the tree.', 'answer': 'singing'},
            {'type': 'first_letter', 'question': 'I have a c_____ friend.', 'answer': 'close'},
            {'type': 'first_letter', 'question': 'The moon is s_____ in the sky.', 'answer': 'shining'},
            {'type': 'first_letter', 'question': 'We go to s_____ by bus.', 'answer': 'school'},
            {'type': 'first_letter', 'question': 'He l_____ in Shanghai with his family.', 'answer': 'lives'},
            {'type': 'first_letter', 'question': 'She w_____ a red dress today.', 'answer': 'wears'},
            {'type': 'first_letter', 'question': 'The water is very c_____ in summer.', 'answer': 'cool'},
            {'type': 'first_letter', 'question': 'They a_____ at the park at 3 o\'clock.', 'answer': 'arrive'},
            {'type': 'first_letter', 'question': 'I love to e_____ ice cream in hot weather.', 'answer': 'eat'},
            {'type': 'first_letter', 'question': 'The flower is very b_____.', 'answer': 'beautiful'},
            {'type': 'first_letter', 'question': 'He r_____ his bike to school every day.', 'answer': 'rides'},
            {'type': 'first_letter', 'question': 'We have m_____ at home every Sunday.', 'answer': 'meals'},
            {'type': 'first_letter', 'question': 'The rain is f_____ from the sky.', 'answer': 'falling'},
            {'type': 'first_letter', 'question': 'I f_____ happy today.', 'answer': 'feel'},
            {'type': 'first_letter', 'question': 'The car is d_____ down the street.', 'answer': 'driving'},
            {'type': 'first_letter', 'question': 'She is c_____ a letter to her friend.', 'answer': 'writing'},
            {'type': 'first_letter', 'question': 'The children are p_____ in the garden.', 'answer': 'playing'},
            {'type': 'first_letter', 'question': 'I like to d_____ music in my free time.', 'answer': 'listen'},
            {'type': 'first_letter', 'question': 'The baby is s_____ in the crib.', 'answer': 'sleeping'},
            {'type': 'first_letter', 'question': 'He is h_____ a shower right now.', 'answer': 'taking'},
            {'type': 'first_letter', 'question': 'The teacher is e_____ a book to students.', 'answer': 'reading'},
            {'type': 'first_letter', 'question': 'We are h_____ dinner together.', 'answer': 'having'},
            {'type': 'first_letter', 'question': 'The old man is w_____ with a walking stick.', 'answer': 'walking'},
            {'type': 'first_letter', 'question': 'She is s_____ her homework in her room.', 'answer': 'doing'},
            {'type': 'first_letter', 'question': 'The train is c_____ into the station.', 'answer': 'coming'},
            {'type': 'first_letter', 'question': 'I am s_____ on the bench.', 'answer': 'sitting'},
            {'type': 'first_letter', 'question': 'The chef is c_____ in the kitchen.', 'answer': 'cooking'},
            {'type': 'first_letter', 'question': 'We are w_____ for the movie to start.', 'answer': 'waiting'},
            {'type': 'first_letter', 'question': 'The artist is p_____ a beautiful painting.', 'answer': 'painting'},
            {'type': 'first_letter', 'question': 'She is l_____ her favorite song.', 'answer': 'singing'},
            {'type': 'first_letter', 'question': 'The computer is w_____ very slowly.', 'answer': 'working'},
            {'type': 'first_letter', 'question': 'I am r_____ a book in the library.', 'answer': 'reading'},
            {'type': 'first_letter', 'question': 'The waiter is s_____ food to the customers.', 'answer': 'serving'},
            {'type': 'first_letter', 'question': 'The photographer is t_____ pictures at the event.', 'answer': 'taking'},
            {'type': 'first_letter', 'question': 'She is s_____ her hair with a brush.', 'answer': 'brushing'},
            {'type': 'first_letter', 'question': 'The musician is p_____ the piano beautifully.', 'answer': 'playing'},
            {'type': 'first_letter', 'question': 'We are e_____ our vacation in Hawaii.', 'answer': 'enjoying'},
            {'type': 'first_letter', 'question': 'The gardener is w_____ the plants in the garden.', 'answer': 'watering'},
            {'type': 'first_letter', 'question': 'The student is w_____ notes in class.', 'answer': 'taking'},
            {'type': 'first_letter', 'question': 'She is h_____ a conversation with her friend.', 'answer': 'having'},
            {'type': 'first_letter', 'question': 'The doctor is e_____ the patient carefully.', 'answer': 'examining'},
            {'type': 'first_letter', 'question': 'I am c_____ my room right now.', 'answer': 'cleaning'},
            {'type': 'first_letter', 'question': 'The swimmer is s_____ in the pool.', 'answer': 'swimming'},
            {'type': 'first_letter', 'question': 'The baker is m_____ fresh bread in the bakery.', 'answer': 'making'},
            {'type': 'first_letter', 'question': 'We are p_____ games at the party.', 'answer': 'playing'},
            {'type': 'first_letter', 'question': 'The dancer is m_____ gracefully on stage.', 'answer': 'moving'},
            {'type': 'first_letter', 'question': 'She is w_____ a beautiful dress to the party.', 'answer': 'wearing'},
            {'type': 'first_letter', 'question': 'The driver is s_____ very carefully on the road.', 'answer': 'driving'},
            {'type': 'first_letter', 'question': 'I am l_____ down on the grass.', 'answer': 'lying'},
            {'type': 'first_letter', 'question': 'The fisherman is c_____ fish by the river.', 'answer': 'catching'},
            {'type': 'first_letter', 'question': 'She is s_____ cookies in the kitchen.', 'answer': 'baking'},
            {'type': 'first_letter', 'question': 'The pilot is f_____ the airplane in the sky.', 'answer': 'flying'},
            {'type': 'first_letter', 'question': 'We are e_____ a picnic in the park.', 'answer': 'having'},
            {'type': 'first_letter', 'question': 'The mechanic is r_____ the broken car.', 'answer': 'repairing'},
            {'type': 'first_letter', 'question': 'She is s_____ gifts for her family.', 'answer': 'buying'},
            {'type': 'first_letter', 'question': 'The soldier is g_____ his duty to protect the country.', 'answer': 'doing'},
            {'type': 'fill', 'question': 'I have _____ orange. (an)', 'answer': 'an'},
            {'type': 'fill', 'question': 'She is playing _____ guitar. (the)', 'answer': 'the'},
            {'type': 'choice', 'question': 'The cat is _____ the table.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'on'},
            {'type': 'choice', 'question': 'She sits _____ the park every morning.', 'options': ['in', 'on', 'at', 'by'], 'answer': 'in'},
            {'type': 'choice', 'question': 'The book is _____ my bag.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'in'},
            {'type': 'choice', 'question': 'We will meet _____ 3 o\'clock.', 'options': ['in', 'on', 'at', 'by'], 'answer': 'at'},
            {'type': 'choice', 'question': 'The ball is _____ the box.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'in'},
            {'type': 'choice', 'question': 'My school is _____ the corner.', 'options': ['on', 'in', 'at', 'around'], 'answer': 'on'},
            {'type': 'choice', 'question': 'The dog is sleeping _____ the sofa.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'on'},
            {'type': 'choice', 'question': 'I live _____ Beijing with my parents.', 'options': ['on', 'in', 'at', 'to'], 'answer': 'in'},
            {'type': 'choice', 'question': 'The flowers are _____ the vase on the table.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'in'},
            {'type': 'choice', 'question': 'The train will arrive _____ noon tomorrow.', 'options': ['in', 'on', 'at', 'by'], 'answer': 'at'},
            {'type': 'choice', 'question': 'The children are playing _____ the garden.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'in'},
            {'type': 'choice', 'question': 'There is a picture _____ the wall.', 'options': ['on', 'in', 'at', 'under'], 'answer': 'on'},
            {'type': 'choice', 'question': 'I go to school _____ foot every day.', 'options': ['by', 'on', 'in', 'with'], 'answer': 'by'},
            {'type': 'choice', 'question': 'She goes to work _____ car.', 'options': ['by', 'on', 'in', 'with'], 'answer': 'by'},
            {'type': 'choice', 'question': 'The moon is _____ the night sky.', 'options': ['on', 'in', 'at', 'in'], 'answer': 'in'},
            {'type': 'choice', 'question': 'I will meet you _____ the school gate.', 'options': ['at', 'in', 'on', 'to'], 'answer': 'at'},
            {'type': 'choice', 'question': 'The supermarket is _____ the left.', 'options': ['at', 'in', 'on', 'to'], 'answer': 'on'},
            {'type': 'choice', 'question': 'Write your name _____ the paper.', 'options': ['at', 'in', 'on', 'in'], 'answer': 'on'},
            {'type': 'choice', 'question': 'The teacher is standing _____ the blackboard.', 'options': ['at', 'in', 'on', 'in front of'], 'answer': 'in front of'},
            {'type': 'choice', 'question': 'The cat is hiding _____ the bed.', 'options': ['under', 'in', 'on', 'at'], 'answer': 'under'},
            {'type': 'fill', 'question': 'The dog is sleeping _____ the sofa.', 'answer': 'on'},
            {'type': 'fill', 'question': 'I live _____ Beijing.', 'answer': 'in'},
            {'type': 'fill', 'question': 'The flowers are _____ the vase.', 'answer': 'in'},
            {'type': 'fill', 'question': 'The train will arrive _____ noon.', 'answer': 'at'},
            {'type': 'fill', 'question': 'The children are playing _____ the garden.', 'answer': 'in'},
            {'type': 'choice', 'question': 'He _____ to school every day.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'goes'},
            {'type': 'choice', 'question': 'She _____ English very well.', 'options': ['speak', 'speaks', 'speaking', 'spoke'], 'answer': 'speaks'},
            {'type': 'choice', 'question': 'I _____ to the store yesterday.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'went'},
            {'type': 'choice', 'question': 'She is _____ a book now.', 'options': ['read', 'reads', 'reading', 'readed'], 'answer': 'reading'},
            {'type': 'choice', 'question': 'They _____ basketball every weekend.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'play'},
            {'type': 'choice', 'question': 'We _____ dinner at 6 PM.', 'options': ['have', 'has', 'having', 'had'], 'answer': 'have'},
            {'type': 'choice', 'question': 'He _____ his teeth twice a day.', 'options': ['brush', 'brushes', 'brushing', 'brushed'], 'answer': 'brushes'},
            {'type': 'choice', 'question': 'Yesterday, I _____ to the park.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'went'},
            {'type': 'choice', 'question': 'She is _____ her homework right now.', 'options': ['do', 'does', 'doing', 'did'], 'answer': 'doing'},
            {'type': 'choice', 'question': 'They usually _____ football after school.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'play'},
            {'type': 'choice', 'question': 'We _____ breakfast together every morning.', 'options': ['have', 'has', 'having', 'had'], 'answer': 'have'},
            {'type': 'choice', 'question': 'He _____ his room every Sunday.', 'options': ['clean', 'cleans', 'cleaning', 'cleaned'], 'answer': 'cleans'},
            {'type': 'choice', 'question': 'I _____ my teeth every morning.', 'options': ['brush', 'brushes', 'brushing', 'brushed'], 'answer': 'brush'},
            {'type': 'choice', 'question': 'She is _____ a letter now.', 'options': ['write', 'writes', 'writing', 'wrote'], 'answer': 'writing'},
            {'type': 'choice', 'question': 'They _____ to the library yesterday.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'went'},
            {'type': 'choice', 'question': 'We are _____ a picture in art class.', 'options': ['draw', 'draws', 'drawing', 'drew'], 'answer': 'drawing'},
            {'type': 'choice', 'question': 'He always _____ his bag to school.', 'options': ['bring', 'brings', 'bringing', 'brought'], 'answer': 'brings'},
            {'type': 'choice', 'question': 'My mother _____ cooking.', 'options': ['like', 'likes', 'liking', 'liked'], 'answer': 'likes'},
            {'type': 'choice', 'question': 'The cat _____ fish.', 'options': ['like', 'likes', 'liking', 'liked'], 'answer': 'likes'},
            {'type': 'choice', 'question': 'He _____ basketball very well.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'plays'},
            {'type': 'fill', 'question': 'Yesterday, I _____ to the park.', 'answer': 'went'},
            {'type': 'fill', 'question': 'She is _____ her homework.', 'answer': 'doing'},
            {'type': 'fill', 'question': 'They _____ football every afternoon.', 'answer': 'play'},
            {'type': 'fill', 'question': 'We _____ breakfast together.', 'answer': 'have'},
            {'type': 'fill', 'question': 'He _____ his room every Sunday.', 'answer': 'cleans'},
            {'type': 'choice', 'question': '_____ a book on the desk.', 'options': ['There is', 'There are', 'There was', 'There were'], 'answer': 'There is'},
            {'type': 'choice', 'question': '_____ some apples in the basket.', 'options': ['There is', 'There are', 'There was', 'There were'], 'answer': 'There are'},
            {'type': 'choice', 'question': '_____ a cat under the chair.', 'options': ['There is', 'There are', 'There was', 'There were'], 'answer': 'There is'},
            {'type': 'choice', 'question': '_____ many students in the classroom.', 'options': ['There is', 'There are', 'There was', 'There were'], 'answer': 'There are'},
            {'type': 'choice', 'question': '_____ a meeting yesterday.', 'options': ['There is', 'There are', 'There was', 'There were'], 'answer': 'There was'},
            {'type': 'choice', 'question': '_____ some milk in the glass.', 'options': ['There is', 'There are', 'There was', 'There were'], 'answer': 'There is'},
            {'type': 'choice', 'question': '_____ two windows in my room.', 'options': ['There is', 'There are', 'There was', 'There were'], 'answer': 'There are'},
            {'type': 'choice', 'question': '_____ a beautiful flower in the garden.', 'options': ['There is', 'There are', 'There was', 'There were'], 'answer': 'There is'},
            {'type': 'choice', 'question': '_____ many people at the party last night.', 'options': ['There is', 'There are', 'There was', 'There were'], 'answer': 'There were'},
            {'type': 'choice', 'question': '_____ some water in the bottle.', 'options': ['There is', 'There are', 'There was', 'There were'], 'answer': 'There is'},
            {'type': 'choice', 'question': '_____ a tree behind our house.', 'options': ['There is', 'There are', 'There was', 'There were'], 'answer': 'There is'},
            {'type': 'choice', 'question': '_____ many books on the shelf.', 'options': ['There is', 'There are', 'There was', 'There were'], 'answer': 'There are'},
            {'type': 'choice', 'question': '_____ an accident yesterday.', 'options': ['There is', 'There are', 'There was', 'There were'], 'answer': 'There was'},
            {'type': 'choice', 'question': '_____ some news in the newspaper.', 'options': ['There is', 'There are', 'There was', 'There were'], 'answer': 'There is'},
            {'type': 'choice', 'question': '_____ a police station near here.', 'options': ['There is', 'There are', 'There was', 'There were'], 'answer': 'There is'},
            {'type': 'fill', 'question': '_____ a book on the desk.', 'answer': 'There is'},
            {'type': 'fill', 'question': '_____ some apples in the basket.', 'answer': 'There are'},
            {'type': 'fill', 'question': '_____ a cat under the chair.', 'answer': 'There is'},
            {'type': 'fill', 'question': '_____ many students in the classroom.', 'answer': 'There are'},
            {'type': 'fill', 'question': '_____ a meeting yesterday.', 'answer': 'There was'},
            {'type': 'choice', 'question': '_____ careful!', 'options': ['Be', 'Is', 'Are', 'Do'], 'answer': 'Be'},
            {'type': 'choice', 'question': '_____ not late for school!', 'options': ['Be', 'Is', 'Are', 'Do'], 'answer': 'Be'},
            {'type': 'choice', 'question': '_____ your homework now!', 'options': ['Do', 'Does', 'Did', 'Doing'], 'answer': 'Do'},
            {'type': 'choice', 'question': '_____ come here, please!', 'options': ['Do', 'Does', 'Did', 'Please'], 'answer': 'Do'},
            {'type': 'choice', 'question': '_____ not make noise!', 'options': ['Do', 'Does', 'Did', 'Please'], 'answer': 'Do'},
            {'type': 'choice', 'question': '_____ to bed early tonight!', 'options': ['Go', 'Goes', 'Going', 'Went'], 'answer': 'Go'},
            {'type': 'choice', 'question': '_____ the window, please!', 'options': ['Open', 'Opens', 'Opening', 'Opened'], 'answer': 'Open'},
            {'type': 'choice', 'question': '_____ your hands!', 'options': ['Clap', 'Claps', 'Clapping', 'Clapped'], 'answer': 'Clap'},
            {'type': 'choice', 'question': '_____ a song for us!', 'options': ['Sing', 'Sings', 'Singing', 'Sang'], 'answer': 'Sing'},
            {'type': 'choice', 'question': '_____ quiet!', 'options': ['Be', 'Is', 'Are', 'Do'], 'answer': 'Be'},
            {'type': 'fill', 'question': '_____ careful!', 'answer': 'Be'},
            {'type': 'fill', 'question': '_____ not late!', 'answer': 'Be'},
            {'type': 'fill', 'question': '_____ your homework!', 'answer': 'Do'},
            {'type': 'fill', 'question': '_____ here!', 'answer': 'Come'},
            {'type': 'fill', 'question': '_____ the door!', 'answer': 'Open'},
            {'type': 'choice', 'question': '_____ you like apples?', 'options': ['Do', 'Does', 'Is', 'Are'], 'answer': 'Do'},
            {'type': 'choice', 'question': '_____ she a student?', 'options': ['Do', 'Does', 'Is', 'Are'], 'answer': 'Is'},
            {'type': 'choice', 'question': '_____ they playing in the garden?', 'options': ['Do', 'Does', 'Are', 'Is'], 'answer': 'Are'},
            {'type': 'choice', 'question': '_____ he go to school by bus?', 'options': ['Do', 'Does', 'Is', 'Are'], 'answer': 'Does'},
            {'type': 'choice', 'question': '_____ you tired now?', 'options': ['Do', 'Does', 'Are', 'Is'], 'answer': 'Are'},
            {'type': 'choice', 'question': '_____ there a book on the desk?', 'options': ['Do', 'Does', 'Is', 'Are'], 'answer': 'Is'},
            {'type': 'choice', 'question': '_____ she have a sister?', 'options': ['Do', 'Does', 'Is', 'Are'], 'answer': 'Does'},
            {'type': 'choice', 'question': '_____ you want some water?', 'options': ['Do', 'Does', 'Are', 'Is'], 'answer': 'Do'},
            {'type': 'choice', 'question': '_____ it raining outside?', 'options': ['Do', 'Does', 'Is', 'Are'], 'answer': 'Is'},
            {'type': 'choice', 'question': '_____ they your friends?', 'options': ['Do', 'Does', 'Are', 'Is'], 'answer': 'Are'},
            {'type': 'choice', 'question': '_____ you see the bird?', 'options': ['Can', 'Could', 'May', 'Will'], 'answer': 'Can'},
            {'type': 'choice', 'question': '_____ I help you?', 'options': ['Can', 'Could', 'May', 'Will'], 'answer': 'May'},
            {'type': 'choice', 'question': '_____ you come to my party?', 'options': ['Can', 'Could', 'May', 'Will'], 'answer': 'Will'},
            {'type': 'choice', 'question': '_____ I use your pencil?', 'options': ['Can', 'Could', 'May', 'Will'], 'answer': 'May'},
            {'type': 'choice', 'question': '_____ you please open the window?', 'options': ['Can', 'Could', 'May', 'Will'], 'answer': 'Could'},
            {'type': 'fill', 'question': '_____ you like apples? Yes, I _____.', 'answer': 'Do do'},
            {'type': 'fill', 'question': '_____ she a student? Yes, she _____.', 'answer': 'Is is'},
            {'type': 'fill', 'question': '_____ they playing? Yes, they _____.', 'answer': 'Are are'},
            {'type': 'fill', 'question': '_____ he go to school? No, he _____.', 'answer': 'Does does not'},
            {'type': 'fill', 'question': '_____ you tired? No, I _____.', 'answer': 'Am am not'},
            {'type': 'choice', 'question': '_____ is your name?', 'options': ['What', 'Where', 'When', 'Who'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ are you going?', 'options': ['What', 'Where', 'When', 'Who'], 'answer': 'Where'},
            {'type': 'choice', 'question': '_____ is your birthday?', 'options': ['What', 'Where', 'When', 'Who'], 'answer': 'When'},
            {'type': 'choice', 'question': '_____ is that woman?', 'options': ['What', 'Where', 'When', 'Who'], 'answer': 'Who'},
            {'type': 'choice', 'question': '_____ time is it now?', 'options': ['What', 'Where', 'When', 'How'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ color do you like?', 'options': ['What', 'Where', 'Which', 'Who'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ is your favorite subject?', 'options': ['What', 'Where', 'Which', 'Who'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ does your father do?', 'options': ['What', 'Where', 'When', 'Who'], 'answer': 'What'},
            {'type': 'choice', 'question': '_____ old are you?', 'options': ['What', 'How', 'When', 'Where'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ are you feeling?', 'options': ['What', 'How', 'When', 'Where'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ do you go to school?', 'options': ['What', 'How', 'When', 'Where'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ is the weather today?', 'options': ['What', 'How', 'When', 'Where'], 'answer': 'How'},
            {'type': 'choice', 'question': '_____ books are these?', 'options': ['What', 'Whose', 'Who', 'Which'], 'answer': 'Whose'},
            {'type': 'choice', 'question': '_____ one do you prefer?', 'options': ['What', 'Where', 'Which', 'Who'], 'answer': 'Which'},
            {'type': 'choice', 'question': '_____ did you do yesterday?', 'options': ['What', 'Where', 'When', 'Who'], 'answer': 'What'},
            {'type': 'fill', 'question': '_____ is your name?', 'answer': 'What'},
            {'type': 'fill', 'question': '_____ are you going?', 'answer': 'Where'},
            {'type': 'fill', 'question': '_____ is your birthday?', 'answer': 'When'},
            {'type': 'fill', 'question': '_____ is that woman?', 'answer': 'Who'},
            {'type': 'fill', 'question': '_____ time is it?', 'answer': 'What'},
            {'type': 'choice', 'question': 'There are _____ days in a week.', 'options': ['seven', 'six', 'five', 'eight'], 'answer': 'seven'},
            {'type': 'choice', 'question': 'Today is her _____ birthday.', 'options': ['twelve', 'twelfth', 'twelveth', 'twentyth'], 'answer': 'twelfth'},
            {'type': 'choice', 'question': 'I have been there _____ times.', 'options': ['two', 'three', 'four', 'five'], 'answer': 'three'},
            {'type': 'choice', 'question': 'She is in _____ grade now.', 'options': ['four', 'fourth', 'fourd', 'forthe'], 'answer': 'four'},
            {'type': 'choice', 'question': 'Today is the _____ of May.', 'options': ['five', 'fifth', 'fiveth', 'fiving'], 'answer': 'fifth'},
            {'type': 'choice', 'question': 'There are _____ months in a year.', 'options': ['eleven', 'twelve', 'thirteen', 'fourteen'], 'answer': 'twelve'},
            {'type': 'choice', 'question': 'My phone number is _____.', 'options': ['one eight six, two seven four, five six nine', 'eight six one, two seven four, five six nine', 'one eight six, seven two four, five six nine', 'one eight six, two seven four, five nine six'], 'answer': 'one eight six, two seven four, five six nine'},
            {'type': 'choice', 'question': 'He lives on the _____ floor.', 'options': ['three', 'third', 'threeth', 'threeding'], 'answer': 'third'},
            {'type': 'choice', 'question': 'I have _____ apples.', 'options': ['twenty-one', 'twenty one', 'twenty-first', 'twenty first'], 'answer': 'twenty-one'},
            {'type': 'choice', 'question': 'Tomorrow is her _____ birthday.', 'options': ['twentieth', 'twenty', 'twentyth', 'twentyth'], 'answer': 'twentieth'},
            {'type': 'fill', 'question': 'There are _____ days in a week.', 'answer': 'seven'},
            {'type': 'fill', 'question': 'Today is her _____ birthday.', 'answer': 'twelfth'},
            {'type': 'fill', 'question': 'She is in _____ grade.', 'answer': 'four'},
            {'type': 'fill', 'question': 'Today is the _____ of May.', 'answer': 'fifth'},
            {'type': 'fill', 'question': 'He lives on the _____ floor.', 'answer': 'third'},
            {'type': 'choice', 'question': 'I _____ swim very well.', 'options': ['can', 'may', 'must', 'should'], 'answer': 'can'},
            {'type': 'choice', 'question': 'You _____ finish your homework first.', 'options': ['can', 'may', 'must', 'should'], 'answer': 'must'},
            {'type': 'choice', 'question': '_____ I use your pen?', 'options': ['Can', 'May', 'Must', 'Should'], 'answer': 'May'},
            {'type': 'choice', 'question': 'You _____ help others.', 'options': ['can', 'may', 'must', 'should'], 'answer': 'should'},
            {'type': 'choice', 'question': 'It _____ rain today.', 'options': ['can', 'may', 'must', 'should'], 'answer': 'may'},
            {'type': 'choice', 'question': 'You _____ not tell anyone.', 'options': ['can', 'may', 'must', 'should'], 'answer': 'must'},
            {'type': 'choice', 'question': '_____ you like some tea?', 'options': ['Can', 'Would', 'Must', 'Should'], 'answer': 'Would'},
            {'type': 'choice', 'question': 'I _____ like to have a cup of coffee.', 'options': ['can', 'may', 'will', 'would'], 'answer': 'would'},
            {'type': 'choice', 'question': 'You _____ come to the party tomorrow.', 'options': ['can', 'must', 'may', 'will'], 'answer': 'will'},
            {'type': 'choice', 'question': 'We _____ respect our teachers.', 'options': ['can', 'may', 'must', 'should'], 'answer': 'should'},
            {'type': 'choice', 'question': '_____ I help you with your bags?', 'options': ['Can', 'May', 'Must', 'Could'], 'answer': 'Could'},
            {'type': 'choice', 'question': 'You _____ be more careful.', 'options': ['can', 'may', 'must', 'should'], 'answer': 'should'},
            {'type': 'choice', 'question': 'The child _____ walk yet.', 'options': ['can', 'cannot', 'must', 'should'], 'answer': 'cannot'},
            {'type': 'choice', 'question': '_____ you please pass me the book?', 'options': ['Can', 'May', 'Must', 'Will'], 'answer': 'Can'},
            {'type': 'choice', 'question': 'I _____ speak English when I was five.', 'options': ['can', 'could', 'may', 'might'], 'answer': 'could'},
            {'type': 'fill', 'question': 'I _____ swim very well.', 'answer': 'can'},
            {'type': 'fill', 'question': 'You _____ finish your homework first.', 'answer': 'must'},
            {'type': 'fill', 'question': '_____ I use your pen?', 'answer': 'May'},
            {'type': 'fill', 'question': 'You _____ help others.', 'answer': 'should'},
            {'type': 'fill', 'question': 'It _____ rain today.', 'answer': 'may'},
            {'type': 'choice', 'question': 'I enjoy _____ music.', 'options': ['listen', 'listens', 'listening', 'listened'], 'answer': 'listening'},
            {'type': 'choice', 'question': 'She hates _____ early.', 'options': ['wake', 'wakes', 'waking', 'waked'], 'answer': 'waking'},
            {'type': 'choice', 'question': 'They are good at _____ games.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'playing'},
            {'type': 'choice', 'question': 'He dislikes _____ vegetables.', 'options': ['eat', 'eats', 'eating', 'ate'], 'answer': 'eating'},
            {'type': 'choice', 'question': 'We are interested in _____ stories.', 'options': ['read', 'reads', 'reading', 'readed'], 'answer': 'reading'},
            {'type': 'choice', 'question': 'My brother practices _____ the piano every day.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'playing'},
            {'type': 'choice', 'question': 'She avoids _____ in the rain.', 'options': ['walk', 'walks', 'walking', 'walked'], 'answer': 'walking'},
            {'type': 'choice', 'question': 'They keep _____ English every day.', 'options': ['study', 'studies', 'studying', 'studied'], 'answer': 'studying'},
            {'type': 'choice', 'question': 'He finishes _____ his homework at 9 PM.', 'options': ['do', 'does', 'doing', 'did'], 'answer': 'doing'},
            {'type': 'choice', 'question': 'I am considering _____ a new car.', 'options': ['buy', 'buys', 'buying', 'bought'], 'answer': 'buying'},
            {'type': 'choice', 'question': 'She suggested _____ to the park.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'going'},
            {'type': 'choice', 'question': 'They stopped _____ because it started to rain.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'playing'},
            {'type': 'choice', 'question': 'I remember _____ her at the party.', 'options': ['meet', 'meets', 'meeting', 'met'], 'answer': 'meeting'},
            {'type': 'choice', 'question': 'He admitted _____ the window.', 'options': ['break', 'breaks', 'breaking', 'broke'], 'answer': 'breaking'},
            {'type': 'choice', 'question': 'We are looking forward to _____ you.', 'options': ['see', 'sees', 'seeing', 'saw'], 'answer': 'seeing'},
            {'type': 'fill', 'question': 'I like _____ in the morning.', 'answer': 'running'},
            {'type': 'fill', 'question': 'She is good at _____ pictures.', 'answer': 'drawing'},
            {'type': 'fill', 'question': 'They enjoy _____ with friends.', 'answer': 'playing'},
            {'type': 'fill', 'question': 'He dislikes _____ in the rain.', 'answer': 'walking'},
            {'type': 'fill', 'question': 'We are busy _____ our project.', 'answer': 'working on'},
            {'type': 'choice', 'question': 'This book is _____ than that one.', 'options': ['thin', 'thinner', 'thinnest', 'thiner'], 'answer': 'thinner'},
            {'type': 'choice', 'question': 'He is the _____ student in our class.', 'options': ['clever', 'cleverer', 'cleverest', 'most clever'], 'answer': 'cleverest'},
            {'type': 'choice', 'question': 'Tom is _____ than Jack.', 'options': ['tall', 'taller', 'tallest', 'taller'], 'answer': 'taller'},
            {'type': 'choice', 'question': 'She is as _____ as her mother.', 'options': ['beautiful', 'more beautiful', 'most beautiful', 'beautifuller'], 'answer': 'beautiful'},
            {'type': 'choice', 'question': 'This is the _____ movie I have ever seen.', 'options': ['good', 'better', 'best', 'goodest'], 'answer': 'best'},
            {'type': 'choice', 'question': 'The weather is getting _____.', 'options': ['cold', 'colder', 'coldest', 'more cold'], 'answer': 'colder'},
            {'type': 'choice', 'question': 'He works _____ than his brother.', 'options': ['hard', 'harder', 'hardest', 'hardly'], 'answer': 'harder'},
            {'type': 'choice', 'question': 'My sister is _____ than me.', 'options': ['young', 'younger', 'youngest', 'youngest'], 'answer': 'younger'},
            {'type': 'choice', 'question': 'This is the _____ apple on the table.', 'options': ['big', 'bigger', 'biggest', 'biggest'], 'answer': 'biggest'},
            {'type': 'choice', 'question': 'He runs _____ than I.', 'options': ['fast', 'faster', 'fastest', 'faster'], 'answer': 'faster'},
            {'type': 'choice', 'question': 'She is the _____ girl in our class.', 'options': ['pretty', 'prettier', 'prettiest', 'more pretty'], 'answer': 'prettiest'},
            {'type': 'choice', 'question': 'This problem is _____ than that one.', 'options': ['difficult', 'more difficult', 'most difficult', 'difficulter'], 'answer': 'more difficult'},
            {'type': 'choice', 'question': 'He is _____ student in our class.', 'options': ['tall', 'taller', 'tallest', 'taller'], 'answer': 'tallest'},
            {'type': 'choice', 'question': 'Today is _____ than yesterday.', 'options': ['hot', 'hotter', 'hottest', 'hoter'], 'answer': 'hotter'},
            {'type': 'choice', 'question': 'This book is _____ of the three.', 'options': ['thin', 'thinner', 'thinnest', 'thiner'], 'answer': 'thinnest'},
            {'type': 'fill', 'question': 'This book is _____ than that one.', 'answer': 'thinner'},
            {'type': 'fill', 'question': 'He is the _____ student.', 'answer': 'cleverest'},
            {'type': 'fill', 'question': 'Tom is _____ than Jack.', 'answer': 'taller'},
            {'type': 'fill', 'question': 'This is the _____ movie.', 'answer': 'best'},
            {'type': 'fill', 'question': 'The weather is getting _____.', 'answer': 'colder'},
            {'type': 'choice', 'question': 'The sky is _____.', 'options': ['blue', 'red', 'yellow', 'green'], 'answer': 'blue'},
            {'type': 'choice', 'question': 'The grass is _____.', 'options': ['blue', 'red', 'yellow', 'green'], 'answer': 'green'},
            {'type': 'choice', 'question': 'The sun is _____.', 'options': ['blue', 'red', 'yellow', 'green'], 'answer': 'yellow'},
            {'type': 'choice', 'question': 'It is _____ today.', 'options': ['sunny', 'rain', 'snow', 'windy'], 'answer': 'sunny'},
            {'type': 'choice', 'question': 'It is _____ outside. Take an umbrella.', 'options': ['sunny', 'raining', 'snowing', 'windy'], 'answer': 'raining'},
            {'type': 'choice', 'question': 'In winter, it often _____.', 'options': ['rain', 'rains', 'snow', 'snows'], 'answer': 'snows'},
            {'type': 'choice', 'question': 'It is very _____ today. The wind is strong.', 'options': ['sunny', 'rainy', 'snowy', 'windy'], 'answer': 'windy'},
            {'type': 'choice', 'question': 'I like _____ days.', 'options': ['cloud', 'cloudy', 'clouds', 'clouding'], 'answer': 'cloudy'},
            {'type': 'choice', 'question': 'The weather is _____ and hot.', 'options': ['sun', 'sunny', 'sunning', 'sunned'], 'answer': 'sunny'},
            {'type': 'choice', 'question': 'It is a _____ day for a picnic.', 'options': ['nice', 'bad', 'terrible', 'awful'], 'answer': 'nice'},
            {'type': 'fill', 'question': 'The sky is _____.', 'answer': 'blue'},
            {'type': 'fill', 'question': 'The grass is _____.', 'answer': 'green'},
            {'type': 'fill', 'question': 'It is _____ today.', 'answer': 'sunny'},
            {'type': 'fill', 'question': 'It is _____ outside.', 'answer': 'raining'},
            {'type': 'fill', 'question': 'In winter, it often _____.', 'answer': 'snows'},
            {'type': 'choice', 'question': 'He _____ to school every day.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'goes'},
            {'type': 'choice', 'question': 'She _____ English very well.', 'options': ['speak', 'speaks', 'speaking', 'spoke'], 'answer': 'speaks'},
            {'type': 'choice', 'question': 'My mother _____ cooking.', 'options': ['like', 'likes', 'liking', 'liked'], 'answer': 'likes'},
            {'type': 'choice', 'question': 'The cat _____ fish.', 'options': ['like', 'likes', 'liking', 'liked'], 'answer': 'likes'},
            {'type': 'choice', 'question': 'He _____ basketball very well.', 'options': ['play', 'plays', 'playing', 'played'], 'answer': 'plays'},
            {'type': 'choice', 'question': 'My sister _____ music.', 'options': ['like', 'likes', 'liking', 'liked'], 'answer': 'likes'},
            {'type': 'choice', 'question': 'The teacher _____ us English.', 'options': ['teach', 'teaches', 'teaching', 'taught'], 'answer': 'teaches'},
            {'type': 'choice', 'question': 'Tom _____ his homework every day.', 'options': ['do', 'does', 'doing', 'did'], 'answer': 'does'},
            {'type': 'choice', 'question': 'She always _____ early.', 'options': ['wake', 'wakes', 'waking', 'woke'], 'answer': 'wakes'},
            {'type': 'choice', 'question': 'The bird _____ in the tree.', 'options': ['sing', 'sings', 'singing', 'sang'], 'answer': 'sings'},
            {'type': 'choice', 'question': 'My father _____ to work by car.', 'options': ['go', 'goes', 'going', 'went'], 'answer': 'goes'},
            {'type': 'choice', 'question': 'The sun _____ in the east.', 'options': ['rise', 'rises', 'rising', 'rose'], 'answer': 'rises'},
            {'type': 'choice', 'question': 'She _____ a letter to her friend.', 'options': ['write', 'writes', 'writing', 'wrote'], 'answer': 'writes'},
            {'type': 'choice', 'question': 'The clock _____ six o\'clock.', 'options': ['show', 'shows', 'showing', 'showed'], 'answer': 'shows'},
            {'type': 'choice', 'question': 'He _____ his teeth every morning.', 'options': ['brush', 'brushes', 'brushing', 'brushed'], 'answer': 'brushes'},
            {'type': 'choice', 'question': 'The dog _____ bones.', 'options': ['love', 'loves', 'loving', 'loved'], 'answer': 'loves'},
            {'type': 'choice', 'question': 'She _____ a beautiful voice.', 'options': ['have', 'has', 'having', 'had'], 'answer': 'has'},
            {'type': 'choice', 'question': 'He _____ in a big house.', 'options': ['live', 'lives', 'living', 'lived'], 'answer': 'lives'},
            {'type': 'choice', 'question': 'The computer _____ fast.', 'options': ['work', 'works', 'working', 'worked'], 'answer': 'works'},
            {'type': 'choice', 'question': 'She _____ her mother very much.', 'options': ['love', 'loves', 'loving', 'loved'], 'answer': 'loves'},
            {'type': 'fill', 'question': 'My sister _____ music.', 'answer': 'likes'},
            {'type': 'fill', 'question': 'He always _____ early.', 'answer': 'gets up'},
            {'type': 'fill', 'question': 'The teacher _____ us English.', 'answer': 'teaches'},
            {'type': 'fill', 'question': 'She _____ her homework every day.', 'answer': 'does'},
            {'type': 'fill', 'question': 'My father _____ to work by car.', 'answer': 'goes'},
            {'type': 'choice', 'question': 'She is a teacher, _____ she?', 'options': ['isn\'t', 'is', 'doesn\'t', 'does'], 'answer': 'isn\'t'},
            {'type': 'choice', 'question': 'He can swim, _____ he?', 'options': ['can\'t', 'can', 'doesn\'t', 'does'], 'answer': 'can\'t'},
            {'type': 'choice', 'question': 'They are students, _____ they?', 'options': ['aren\'t', 'are', 'doesn\'t', 'does'], 'answer': 'aren\'t'},
            {'type': 'choice', 'question': 'She doesn\'t like apples, _____ she?', 'options': ['does', 'doesn\'t', 'is', 'isn\'t'], 'answer': 'does'},
            {'type': 'choice', 'question': 'He went to school yesterday, _____ he?', 'options': ['did', 'didn\'t', 'was', 'wasn\'t'], 'answer': 'didn\'t'},
            {'type': 'choice', 'question': 'You will come to my party, _____ you?', 'options': ['won\'t', 'will', 'doesn\'t', 'does'], 'answer': 'won\'t'},
            {'type': 'choice', 'question': 'She has a car, _____ she?', 'options': ['hasn\'t', 'has', 'doesn\'t', 'does'], 'answer': 'hasn\'t'},
            {'type': 'choice', 'question': 'You have finished your work, _____ you?', 'options': ['haven\'t', 'have', 'doesn\'t', 'does'], 'answer': 'haven\'t'},
            {'type': 'choice', 'question': 'It is raining, _____ it?', 'options': ['isn\'t', 'is', 'doesn\'t', 'does'], 'answer': 'isn\'t'},
            {'type': 'choice', 'question': 'There is a book on the table, _____ there?', 'options': ['isn\'t', 'is', 'doesn\'t', 'does'], 'answer': 'isn\'t'},
            {'type': 'fill', 'question': 'She is a teacher, _____ she?', 'answer': 'isn\'t'},
            {'type': 'fill', 'question': 'He can swim, _____ he?', 'answer': 'can\'t'},
            {'type': 'fill', 'question': 'They are students, _____ they?', 'answer': 'aren\'t'},
            {'type': 'fill', 'question': 'She doesn\'t like apples, _____ she?', 'answer': 'does'},
            {'type': 'fill', 'question': 'He went to school yesterday, _____ he?', 'answer': 'didn\'t'},
            {'type': 'choice', 'question': 'It is _____ past three.', 'options': ['a quarter', 'half', 'quarter', 'fifteen minutes'], 'answer': 'half'},
            {'type': 'choice', 'question': 'It is _____ to six.', 'options': ['a quarter', 'half', 'quarter', 'five minutes'], 'answer': 'a quarter'},
            {'type': 'choice', 'question': 'It is _____ for lunch.', 'options': ['time', 'o\'clock', 'half past one', 'a quarter'], 'answer': 'time'},
            {'type': 'choice', 'question': 'I wake up at _____ every morning.', 'options': ['six o\'clock', 'seven clock', 'eight o\'clock', 'morning'], 'answer': 'six o\'clock'},
            {'type': 'choice', 'question': 'The meeting starts at _____.', 'options': ['nine thirty', 'nine and half', 'nine half', 'half nine'], 'answer': 'nine thirty'},
            {'type': 'fill', 'question': 'It is _____ past three.', 'answer': 'half'},
            {'type': 'fill', 'question': 'It is _____ to six.', 'answer': 'a quarter'},
            {'type': 'fill', 'question': 'I wake up at _____ every morning.', 'answer': 'six o\'clock'},
            {'type': 'fill', 'question': 'The meeting starts at _____.', 'answer': 'nine thirty'},
            {'type': 'fill', 'question': 'It is time _____ lunch.', 'answer': 'for'},
        ]
        
    def get_first_letter_questions(self):
        # 从综合练习题库中提取所有首字母填空题目
        comprehensive_questions = self.get_comprehensive_questions()
        first_letter_questions = [q for q in comprehensive_questions if q['type'] == 'first_letter']
        
        # 从其他题库补充更多首字母填空题目
        additional_questions = [
            # 基础补充题目
            {'type': 'first_letter', 'question': 'The sun is v_____ bright today.', 'answer': 'very'},
            {'type': 'first_letter', 'question': 'I w_____ to school every day.', 'answer': 'walk'},
            {'type': 'first_letter', 'question': 'She is r_____ a book in the library.', 'answer': 'reading'},
            {'type': 'first_letter', 'question': 'The flowers s_____ very sweet.', 'answer': 'smell'},
            {'type': 'first_letter', 'question': 'We are h_____ a great time.', 'answer': 'having'},
            {'type': 'first_letter', 'question': 'The c_____ is sleeping on the chair.', 'answer': 'cat'},
            {'type': 'first_letter', 'question': 'I can s_____ the music from here.', 'answer': 'hear'},
            {'type': 'first_letter', 'question': 'The b_____ is flying in the sky.', 'answer': 'bird'},
            {'type': 'first_letter', 'question': 'She is w_____ her teeth.', 'answer': 'washing'},
            {'type': 'first_letter', 'question': 'The r_____ is falling heavily.', 'answer': 'rain'},
            {'type': 'first_letter', 'question': 'I l_____ my homework every day.', 'answer': 'do'},
            {'type': 'first_letter', 'question': 'The d_____ is barking loudly.', 'answer': 'dog'},
            {'type': 'first_letter', 'question': 'She is c_____ a beautiful picture.', 'answer': 'drawing'},
            {'type': 'first_letter', 'question': 'The clock is t_____ very loudly.', 'answer': 'ticking'},
            {'type': 'first_letter', 'question': 'We are l_____ for the bus.', 'answer': 'waiting'},
            {'type': 'first_letter', 'question': 'The f_____ is very delicious.', 'answer': 'food'},
            {'type': 'first_letter', 'question': 'I am v_____ excited about the trip.', 'answer': 'very'},
            {'type': 'first_letter', 'question': 'The b_____ is ringing at the door.', 'answer': 'bell'},
            {'type': 'first_letter', 'question': 'She is s_____ a song quietly.', 'answer': 'singing'},
            {'type': 'first_letter', 'question': 'The t_____ is playing in the park.', 'answer': 'children'},
            
            # 新增的扩展题目
            {'type': 'first_letter', 'question': 'The teacher is w_____ on the blackboard.', 'answer': 'writing'},
            {'type': 'first_letter', 'question': 'She is c_____ a delicious cake.', 'answer': 'baking'},
            {'type': 'first_letter', 'question': 'The students are l_____ in the classroom.', 'answer': 'learning'},
            {'type': 'first_letter', 'question': 'I am d_____ my best to finish the work.', 'answer': 'doing'},
            {'type': 'first_letter', 'question': 'The mailman is d_____ letters to houses.', 'answer': 'delivering'},
            {'type': 'first_letter', 'question': 'She is h_____ her hands with soap.', 'answer': 'washing'},
            {'type': 'first_letter', 'question': 'The baby is c_____ in his mother\'s arms.', 'answer': 'crying'},
            {'type': 'first_letter', 'question': 'We are p_____ for the exam tomorrow.', 'answer': 'preparing'},
            {'type': 'first_letter', 'question': 'The fisherman is s_____ on the lake.', 'answer': 'sitting'},
            {'type': 'first_letter', 'question': 'She is w_____ a beautiful scarf.', 'answer': 'wearing'},
            {'type': 'first_letter', 'question': 'The fire is b_____ brightly in the fireplace.', 'answer': 'burning'},
            {'type': 'first_letter', 'question': 'I am r_____ my teeth every morning.', 'answer': 'brushing'},
            {'type': 'first_letter', 'question': 'The shop is o_____ from 9 AM to 5 PM.', 'answer': 'open'},
            {'type': 'first_letter', 'question': 'She is t_____ a walk in the garden.', 'answer': 'taking'},
            {'type': 'first_letter', 'question': 'The phone is r_____ in the living room.', 'answer': 'ringing'},
            {'type': 'first_letter', 'question': 'We are c_____ about the new movie.', 'answer': 'talking'},
            {'type': 'first_letter', 'question': 'The cat is h_____ under the table.', 'answer': 'hiding'},
            {'type': 'first_letter', 'question': 'She is l_____ her keys on the table.', 'answer': 'leaving'},
            {'type': 'first_letter', 'question': 'The car is p_____ in the garage.', 'answer': 'parked'},
            {'type': 'first_letter', 'question': 'I am w_____ for my friend at the cafe.', 'answer': 'waiting'},
            {'type': 'first_letter', 'question': 'The dog is c_____ a bone in the yard.', 'answer': 'chewing'},
            {'type': 'first_letter', 'question': 'She is s_____ her hair in the mirror.', 'answer': 'looking'},
            {'type': 'first_letter', 'question': 'The sun is s_____ in the west.', 'answer': 'setting'},
            {'type': 'first_letter', 'question': 'We are d_____ to the movies tonight.', 'answer': 'going'},
            {'type': 'first_letter', 'question': 'The book is o_____ on page 25.', 'answer': 'open'},
            {'type': 'first_letter', 'question': 'I am f_____ very hungry right now.', 'answer': 'feeling'},
            {'type': 'first_letter', 'question': 'The bird is f_____ away quickly.', 'answer': 'flying'},
            {'type': 'first_letter', 'question': 'She is r_____ her bicycle to work.', 'answer': 'riding'},
            {'type': 'first_letter', 'question': 'The baby is s_____ soundly in his crib.', 'answer': 'sleeping'},
            {'type': 'first_letter', 'question': 'We are s_____ at the dinner table.', 'answer': 'sitting'},
            {'type': 'first_letter', 'question': 'The teacher is e_____ the students\' homework.', 'answer': 'examining'},
            {'type': 'first_letter', 'question': 'She is d_____ a letter to her grandmother.', 'answer': 'writing'},
            {'type': 'first_letter', 'question': 'The train is a_____ at the station.', 'answer': 'arriving'},
            {'type': 'first_letter', 'question': 'I am w_____ my favorite TV show.', 'answer': 'watching'},
            {'type': 'first_letter', 'question': 'The flowers are g_____ in the garden.', 'answer': 'growing'},
            {'type': 'first_letter', 'question': 'She is c_____ her room for the party.', 'answer': 'decorating'},
            {'type': 'first_letter', 'question': 'The car is w_____ down the highway.', 'answer': 'driving'},
            {'type': 'first_letter', 'question': 'We are p_____ our vacation photos.', 'answer': 'looking'},
            {'type': 'first_letter', 'question': 'The cat is s_____ on the windowsill.', 'answer': 'sitting'},
            {'type': 'first_letter', 'question': 'She is c_____ soup for dinner.', 'answer': 'cooking'},
            {'type': 'first_letter', 'question': 'The students are r_____ for their test.', 'answer': 'studying'},
            {'type': 'first_letter', 'question': 'I am s_____ my shopping list.', 'answer': 'writing'},
            {'type': 'first_letter', 'question': 'The rain is s_____ heavily outside.', 'answer': 'pouring'},
            {'type': 'first_letter', 'question': 'She is p_____ her shoes at the door.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The wind is b_____ through the trees.', 'answer': 'blowing'},
            {'type': 'first_letter', 'question': 'We are c_____ our suitcases for the trip.', 'answer': 'packing'},
            {'type': 'first_letter', 'question': 'The baby is f_____ his bottle eagerly.', 'answer': 'drinking'},
            {'type': 'first_letter', 'question': 'She is s_____ her face with a towel.', 'answer': 'wiping'},
            {'type': 'first_letter', 'question': 'The phone is b_____ loudly.', 'answer': 'ringing'},
            {'type': 'first_letter', 'question': 'I am c_____ my emails right now.', 'answer': 'checking'},
            {'type': 'first_letter', 'question': 'The dog is b_____ his tail happily.', 'answer': 'wagging'},
            {'type': 'first_letter', 'question': 'She is p_____ her makeup carefully.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The snow is f_____ outside the window.', 'answer': 'falling'},
            {'type': 'first_letter', 'question': 'We are l_____ our backpacks for school.', 'answer': 'packing'},
            {'type': 'first_letter', 'question': 'The teacher is e_____ the blackboard with chalk.', 'answer': 'erasing'},
            {'type': 'first_letter', 'question': 'She is r_____ her books from the shelf.', 'answer': 'taking'},
            {'type': 'first_letter', 'question': 'The sun is s_____ brightly today.', 'answer': 'shining'},
            {'type': 'first_letter', 'question': 'I am f_____ my keys in my bag.', 'answer': 'looking'},
            {'type': 'first_letter', 'question': 'The children are l_____ in the playground.', 'answer': 'running'},
            {'type': 'first_letter', 'question': 'She is s_____ her teeth at the dentist.', 'answer': 'getting'},
            {'type': 'first_letter', 'question': 'The train is d_____ to the next station.', 'answer': 'moving'},
            {'type': 'first_letter', 'question': 'We are p_____ our tickets for the concert.', 'answer': 'buying'},
            {'type': 'first_letter', 'question': 'The cat is s_____ a mouse in the garden.', 'answer': 'chasing'},
            {'type': 'first_letter', 'question': 'She is w_____ her hands to warm them.', 'answer': 'rubbing'},
            {'type': 'first_letter', 'question': 'The car is s_____ in the traffic.', 'answer': 'stuck'},
            {'type': 'first_letter', 'question': 'I am c_____ my teeth at the dentist.', 'answer': 'getting'},
            {'type': 'first_letter', 'question': 'The birds are s_____ in the trees.', 'answer': 'sitting'},
            {'type': 'first_letter', 'question': 'She is h_____ her baby to sleep.', 'answer': 'rocking'},
            {'type': 'first_letter', 'question': 'The students are r_____ in the library.', 'answer': 'studying'},
            {'type': 'first_letter', 'question': 'We are s_____ the beach this weekend.', 'answer': 'visiting'},
            {'type': 'first_letter', 'question': 'The coffee is t_____ very bitter.', 'answer': 'tasting'},
            {'type': 'first_letter', 'question': 'She is c_____ her hair with a comb.', 'answer': 'combing'},
            {'type': 'first_letter', 'question': 'The baby is g_____ his first steps.', 'answer': 'taking'},
            {'type': 'first_letter', 'question': 'I am s_____ my watch to the correct time.', 'answer': 'setting'},
            {'type': 'first_letter', 'question': 'The leaves are f_____ from the trees.', 'answer': 'falling'},
            {'type': 'first_letter', 'question': 'She is w_____ her hands together.', 'answer': 'clapping'},
            {'type': 'first_letter', 'question': 'The teacher is g_____ the students their grades.', 'answer': 'giving'},
            {'type': 'first_letter', 'question': 'We are s_____ for our vacation.', 'answer': 'getting'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ very fragrant.', 'answer': 'smelling'},
            {'type': 'first_letter', 'question': 'She is h_____ the phone to her ear.', 'answer': 'holding'},
            {'type': 'first_letter', 'question': 'The clock is s_____ four o\'clock.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'I am l_____ my homework on the desk.', 'answer': 'leaving'},
            {'type': 'first_letter', 'question': 'The students are s_____ in a circle.', 'answer': 'sitting'},
            {'type': 'first_letter', 'question': 'She is d_____ her baby\'s bottle.', 'answer': 'warming'},
            {'type': 'first_letter', 'question': 'The sun is s_____ behind the clouds.', 'answer': 'hiding'},
            {'type': 'first_letter', 'question': 'We are s_____ the dishes after dinner.', 'answer': 'washing'},
            {'type': 'first_letter', 'question': 'The teacher is p_____ a picture on the wall.', 'answer': 'hanging'},
            {'type': 'first_letter', 'question': 'She is r_____ her umbrella to open it.', 'answer': 'trying'},
            {'type': 'first_letter', 'question': 'The dog is c_____ his bone in the corner.', 'answer': 'burying'},
            {'type': 'first_letter', 'question': 'I am w_____ the radio for music.', 'answer': 'turning'},
            {'type': 'first_letter', 'question': 'The children are s_____ a sandcastle.', 'answer': 'building'},
            {'type': 'first_letter', 'question': 'She is b_____ her eyes to pray.', 'answer': 'closing'},
            {'type': 'first_letter', 'question': 'The car is r_____ in the parking lot.', 'answer': 'parked'},
            {'type': 'first_letter', 'question': 'We are s_____ the new house.', 'answer': 'visiting'},
            {'type': 'first_letter', 'question': 'The baby is c_____ his toy bear.', 'answer': 'cuddling'},
            {'type': 'first_letter', 'question': 'She is w_____ her hands in the sink.', 'answer': 'washing'},
            {'type': 'first_letter', 'question': 'The sun is s_____ down on the beach.', 'answer': 'shining'},
            {'type': 'first_letter', 'question': 'I am r_____ my hair with a towel.', 'answer': 'drying'},
            {'type': 'first_letter', 'question': 'The students are w_____ their attention to the teacher.', 'answer': 'paying'},
            {'type': 'first_letter', 'question': 'She is s_____ a story to her children.', 'answer': 'telling'},
            {'type': 'first_letter', 'question': 'The train is a_____ at the platform.', 'answer': 'stopping'},
            {'type': 'first_letter', 'question': 'We are p_____ for winter to come.', 'answer': 'getting'},
            {'type': 'first_letter', 'question': 'The cat is s_____ on the warm blanket.', 'answer': 'curling'},
            {'type': 'first_letter', 'question': 'She is h_____ her coat on the hanger.', 'answer': 'hanging'},
            {'type': 'first_letter', 'question': 'The phone is v_____ on the table.', 'answer': 'vibrating'},
            {'type': 'first_letter', 'question': 'I am s_____ my hands in my pockets.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The children are w_____ to the park.', 'answer': 'walking'},
            {'type': 'first_letter', 'question': 'She is c_____ her shoes at the door.', 'answer': 'changing'},
            {'type': 'first_letter', 'question': 'The snow is m_____ on the ground.', 'answer': 'melting'},
            {'type': 'first_letter', 'question': 'We are s_____ for the weekend.', 'answer': 'waiting'},
            {'type': 'first_letter', 'question': 'The bird is s_____ its nest in the tree.', 'answer': 'building'},
            {'type': 'first_letter', 'question': 'She is d_____ a piece of cake.', 'answer': 'cutting'},
            {'type': 'first_letter', 'question': 'The car is s_____ in the driveway.', 'answer': 'parked'},
            {'type': 'first_letter', 'question': 'I am f_____ my phone on the table.', 'answer': 'leaving'},
            {'type': 'first_letter', 'question': 'The students are r_____ their homework.', 'answer': 'doing'},
            {'type': 'first_letter', 'question': 'She is w_____ her baby to sleep.', 'answer': 'rocking'},
            {'type': 'first_letter', 'question': 'The sun is s_____ in the blue sky.', 'answer': 'shining'},
            {'type': 'first_letter', 'question': 'We are c_____ our vacation plans.', 'answer': 'discussing'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his bone under the tree.', 'answer': 'burying'},
            {'type': 'first_letter', 'question': 'She is t_____ her watch to check the time.', 'answer': 'looking'},
            {'type': 'first_letter', 'question': 'The rain is s_____ against the window.', 'answer': 'splashing'},
            {'type': 'first_letter', 'question': 'I am p_____ my books into my bag.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The children are s_____ their toys.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'She is w_____ her hair with a hairdryer.', 'answer': 'drying'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ in the vase.', 'answer': 'sitting'},
            {'type': 'first_letter', 'question': 'We are s_____ for the bus at the stop.', 'answer': 'waiting'},
            {'type': 'first_letter', 'question': 'The teacher is w_____ on the blackboard.', 'answer': 'writing'},
            {'type': 'first_letter', 'question': 'She is c_____ a beautiful dress.', 'answer': 'wearing'},
            {'type': 'first_letter', 'question': 'The baby is s_____ in his high chair.', 'answer': 'sitting'},
            {'type': 'first_letter', 'question': 'I am r_____ to the sound of music.', 'answer': 'dancing'},
            {'type': 'first_letter', 'question': 'The students are l_____ their lessons.', 'answer': 'learning'},
            {'type': 'first_letter', 'question': 'She is s_____ her umbrella.', 'answer': 'opening'},
            {'type': 'first_letter', 'question': 'The car is s_____ on the road.', 'answer': 'moving'},
            {'type': 'first_letter', 'question': 'We are c_____ our camping trip.', 'answer': 'planning'},
            {'type': 'first_letter', 'question': 'The cat is s_____ its fur.', 'answer': 'cleaning'},
            {'type': 'first_letter', 'question': 'She is r_____ a song on the guitar.', 'answer': 'playing'},
            {'type': 'first_letter', 'question': 'The sun is s_____ behind the mountains.', 'answer': 'hiding'},
            {'type': 'first_letter', 'question': 'I am s_____ my wallet in my pocket.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The children are s_____ their art projects.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'She is w_____ her hands to dry them.', 'answer': 'shaking'},
            {'type': 'first_letter', 'question': 'The rain is s_____ heavily on the roof.', 'answer': 'hitting'},
            {'type': 'first_letter', 'question': 'We are s_____ for the weekend to start.', 'answer': 'waiting'},
            {'type': 'first_letter', 'question': 'The bird is s_____ its wings in flight.', 'answer': 'flapping'},
            {'type': 'first_letter', 'question': 'She is c_____ her teeth at the dentist.', 'answer': 'getting'},
            {'type': 'first_letter', 'question': 'The train is a_____ at the next station.', 'answer': 'stopping'},
            {'type': 'first_letter', 'question': 'I am s_____ my hands with friends.', 'answer': 'shaking'},
            {'type': 'first_letter', 'question': 'The students are s_____ their presentations.', 'answer': 'preparing'},
            {'type': 'first_letter', 'question': 'She is w_____ her baby in the stroller.', 'answer': 'pushing'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ in the garden.', 'answer': 'blooming'},
            {'type': 'first_letter', 'question': 'We are s_____ our vacation photos.', 'answer': 'looking'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his tail at visitors.', 'answer': 'wagging'},
            {'type': 'first_letter', 'question': 'She is c_____ her makeup for the party.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The sun is s_____ over the ocean.', 'answer': 'shining'},
            {'type': 'first_letter', 'question': 'I am s_____ my hands in my coat.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The children are s_____ in the snow.', 'answer': 'playing'},
            {'type': 'first_letter', 'question': 'She is w_____ a letter to her friend.', 'answer': 'writing'},
            {'type': 'first_letter', 'question': 'The car is s_____ in the traffic jam.', 'answer': 'stuck'},
            {'type': 'first_letter', 'question': 'We are s_____ our camping gear.', 'answer': 'packing'},
            {'type': 'first_letter', 'question': 'The cat is s_____ on the sunny windowsill.', 'answer': 'sitting'},
            {'type': 'first_letter', 'question': 'She is h_____ her baby to her chest.', 'answer': 'holding'},
            {'type': 'first_letter', 'question': 'The phone is v_____ on silent mode.', 'answer': 'vibrating'},
            {'type': 'first_letter', 'question': 'I am r_____ for the weekend to come.', 'answer': 'waiting'},
            {'type': 'first_letter', 'question': 'The students are s_____ their notebooks.', 'answer': 'opening'},
            {'type': 'first_letter', 'question': 'She is s_____ her shoes to tie them.', 'answer': 'untying'},
            {'type': 'first_letter', 'question': 'The sun is s_____ over the city.', 'answer': 'shining'},
            {'type': 'first_letter', 'question': 'We are s_____ for the concert to start.', 'answer': 'waiting'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his favorite toy.', 'answer': 'playing'},
            {'type': 'first_letter', 'question': 'She is c_____ her hair with a brush.', 'answer': 'brushing'},
            {'type': 'first_letter', 'question': 'The baby is s_____ in his crib.', 'answer': 'sleeping'},
            {'type': 'first_letter', 'question': 'I am s_____ my keys on the counter.', 'answer': 'leaving'},
            {'type': 'first_letter', 'question': 'The teacher is e_____ the classroom.', 'answer': 'cleaning'},
            {'type': 'first_letter', 'question': 'She is s_____ her hands in the air.', 'answer': 'raising'},
            {'type': 'first_letter', 'question': 'The rain is s_____ on the windows.', 'answer': 'beating'},
            {'type': 'first_letter', 'question': 'We are s_____ our holiday plans.', 'answer': 'discussing'},
            {'type': 'first_letter', 'question': 'The cat is s_____ under the car.', 'answer': 'hiding'},
            {'type': 'first_letter', 'question': 'She is w_____ her hands with a tissue.', 'answer': 'wiping'},
            {'type': 'first_letter', 'question': 'The car is s_____ down the street.', 'answer': 'driving'},
            {'type': 'first_letter', 'question': 'I am s_____ my hair in the mirror.', 'answer': 'combing'},
            {'type': 'first_letter', 'question': 'The children are s_____ their bikes.', 'answer': 'riding'},
            {'type': 'first_letter', 'question': 'She is c_____ a puzzle with her daughter.', 'answer': 'doing'},
            {'type': 'first_letter', 'question': 'The sun is s_____ through the clouds.', 'answer': 'shining'},
            {'type': 'first_letter', 'question': 'We are s_____ for the train to arrive.', 'answer': 'waiting'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his bone happily.', 'answer': 'chewing'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby in the carriage.', 'answer': 'pushing'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ in the sunlight.', 'answer': 'blooming'},
            {'type': 'first_letter', 'question': 'I am s_____ my homework in the bag.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The students are s_____ their projects.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'She is w_____ her eyes from the bright light.', 'answer': 'covering'},
            {'type': 'first_letter', 'question': 'The car is s_____ in the parking garage.', 'answer': 'parked'},
            {'type': 'first_letter', 'question': 'We are s_____ our camping supplies.', 'answer': 'organizing'},
            {'type': 'first_letter', 'question': 'The cat is s_____ its whiskers.', 'answer': 'cleaning'},
            {'type': 'first_letter', 'question': 'She is s_____ her shoes at the entrance.', 'answer': 'removing'},
            {'type': 'first_letter', 'question': 'The sun is s_____ over the mountains.', 'answer': 'rising'},
            {'type': 'first_letter', 'question': 'I am s_____ my watch to the alarm.', 'answer': 'setting'},
            {'type': 'first_letter', 'question': 'The children are s_____ their sleds.', 'answer': 'pulling'},
            {'type': 'first_letter', 'question': 'She is c_____ her tea with sugar.', 'answer': 'sweetening'},
            {'type': 'first_letter', 'question': 'The phone is r_____ on the nightstand.', 'answer': 'sitting'},
            {'type': 'first_letter', 'question': 'We are s_____ our bags for the trip.', 'answer': 'packing'},
            {'type': 'first_letter', 'question': 'The bird is s_____ its nest with twigs.', 'answer': 'building'},
            {'type': 'first_letter', 'question': 'She is s_____ her coat from the closet.', 'answer': 'taking'},
            {'type': 'first_letter', 'question': 'The rain is s_____ softly on the roof.', 'answer': 'falling'},
            {'type': 'first_letter', 'question': 'I am s_____ my hands together.', 'answer': 'clapping'},
            {'type': 'first_letter', 'question': 'The students are s_____ their presentations.', 'answer': 'practicing'},
            {'type': 'first_letter', 'question': 'She is w_____ her baby\'s temperature.', 'answer': 'taking'},
            {'type': 'first_letter', 'question': 'The car is s_____ in the wrong direction.', 'answer': 'driving'},
            {'type': 'first_letter', 'question': 'We are s_____ our vacation itinerary.', 'answer': 'planning'},
            {'type': 'first_letter', 'question': 'The cat is s_____ on the warm windowsill.', 'answer': 'curling'},
            {'type': 'first_letter', 'question': 'She is s_____ her necklace in the drawer.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The snow is s_____ beautifully outside.', 'answer': 'falling'},
            {'type': 'first_letter', 'question': 'I am s_____ my teeth before bed.', 'answer': 'brushing'},
            {'type': 'first_letter', 'question': 'The children are s_____ their artwork.', 'answer': 'displaying'},
            {'type': 'first_letter', 'question': 'She is w_____ her hands in celebration.', 'answer': 'raising'},
            {'type': 'first_letter', 'question': 'The train is s_____ into the tunnel.', 'answer': 'entering'},
            {'type': 'first_letter', 'question': 'We are s_____ for our family reunion.', 'answer': 'preparing'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his water bowl.', 'answer': 'drinking'},
            {'type': 'first_letter', 'question': 'She is s_____ her dress for the party.', 'answer': 'choosing'},
            {'type': 'first_letter', 'question': 'The sun is s_____ down on the field.', 'answer': 'shining'},
            {'type': 'first_letter', 'question': 'I am s_____ my hat to block the sun.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The students are s_____ their experiment.', 'answer': 'conducting'},
            {'type': 'first_letter', 'question': 'She is s_____ her hands with sanitizer.', 'answer': 'cleaning'},
            {'type': 'first_letter', 'question': 'The car is s_____ on the shoulder.', 'answer': 'stopped'},
            {'type': 'first_letter', 'question': 'We are s_____ our picnic in the park.', 'answer': 'having'},
            {'type': 'first_letter', 'question': 'The cat is s_____ its favorite toy.', 'answer': 'playing'},
            {'type': 'first_letter', 'question': 'She is s_____ her books on the shelf.', 'answer': 'arranging'},
            {'type': 'first_letter', 'question': 'The rain is s_____ against the door.', 'answer': 'hitting'},
            {'type': 'first_letter', 'question': 'I am s_____ my hands in my pockets.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The children are s_____ their bikes in the garage.', 'answer': 'parking'},
            {'type': 'first_letter', 'question': 'She is s_____ her wedding ring.', 'answer': 'wearing'},
            {'type': 'first_letter', 'question': 'The sun is s_____ in the evening sky.', 'answer': 'setting'},
            {'type': 'first_letter', 'question': 'We are s_____ our camping tent.', 'answer': 'setting'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his favorite spot.', 'answer': 'looking'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby\'s bottle.', 'answer': 'warming'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ in the spring.', 'answer': 'blooming'},
            {'type': 'first_letter', 'question': 'I am s_____ my shoes to tie the laces.', 'answer': 'untying'},
            {'type': 'first_letter', 'question': 'The students are s_____ their classroom.', 'answer': 'cleaning'},
            {'type': 'first_letter', 'question': 'She is s_____ her hair with a ribbon.', 'answer': 'tying'},
            {'type': 'first_letter', 'question': 'The car is s_____ smoothly on the highway.', 'answer': 'moving'},
            {'type': 'first_letter', 'question': 'We are s_____ our travel documents.', 'answer': 'organizing'},
            {'type': 'first_letter', 'question': 'The cat is s_____ on the garden fence.', 'answer': 'climbing'},
            {'type': 'first_letter', 'question': 'She is s_____ her umbrella to dry.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The snow is s_____ on the mountain peak.', 'answer': 'lying'},
            {'type': 'first_letter', 'question': 'I am s_____ my alarm clock.', 'answer': 'setting'},
            {'type': 'first_letter', 'question': 'The children are s_____ in the sandbox.', 'answer': 'playing'},
            {'type': 'first_letter', 'question': 'She is s_____ her jewelry box.', 'answer': 'organizing'},
            {'type': 'first_letter', 'question': 'The sun is s_____ behind the clouds.', 'answer': 'hiding'},
            {'type': 'first_letter', 'question': 'We are s_____ our fishing rods.', 'answer': 'preparing'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his tail in circles.', 'answer': 'spinning'},
            {'type': 'first_letter', 'question': 'She is s_____ her child to bed.', 'answer': 'rocking'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ by the river.', 'answer': 'growing'},
            {'type': 'first_letter', 'question': 'I am s_____ my backpack for school.', 'answer': 'packing'},
            {'type': 'first_letter', 'question': 'The students are s_____ their questions.', 'answer': 'asking'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby\'s pacifier.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The car is s_____ in the driveway.', 'answer': 'waiting'},
            {'type': 'first_letter', 'question': 'We are s_____ our holiday greeting cards.', 'answer': 'writing'},
            {'type': 'first_letter', 'question': 'The cat is s_____ in the sunlight.', 'answer': 'sleeping'},
            {'type': 'first_letter', 'question': 'She is s_____ her hands to warm them.', 'answer': 'rubbing'},
            {'type': 'first_letter', 'question': 'The rain is s_____ through the leaves.', 'answer': 'dripping'},
            {'type': 'first_letter', 'question': 'I am s_____ my watch battery.', 'answer': 'changing'},
            {'type': 'first_letter', 'question': 'The children are s_____ their school supplies.', 'answer': 'organizing'},
            {'type': 'first_letter', 'question': 'She is s_____ her hair into a ponytail.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The sun is s_____ over the horizon.', 'answer': 'rising'},
            {'type': 'first_letter', 'question': 'We are s_____ our picnic basket.', 'answer': 'packing'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his water dish.', 'answer': 'refilling'},
            {'type': 'first_letter', 'question': 'She is s_____ her wedding dress.', 'answer': 'wearing'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ their petals.', 'answer': 'opening'},
            {'type': 'first_letter', 'question': 'I am s_____ my hands in the air.', 'answer': 'raising'},
            {'type': 'first_letter', 'question': 'The students are s_____ their graduation caps.', 'answer': 'wearing'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby\'s room.', 'answer': 'decorating'},
            {'type': 'first_letter', 'question': 'The car is s_____ down the mountain.', 'answer': 'descending'},
            {'type': 'first_letter', 'question': 'We are s_____ our hiking boots.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The cat is s_____ its tail.', 'answer': 'chasing'},
            {'type': 'first_letter', 'question': 'She is s_____ her glasses on the table.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The snow is s_____ on the pine trees.', 'answer': 'lying'},
            {'type': 'first_letter', 'question': 'I am s_____ my feet up.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The children are s_____ their sleds downhill.', 'answer': 'pulling'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby to sleep.', 'answer': 'singing'},
            {'type': 'first_letter', 'question': 'The sun is s_____ through the trees.', 'answer': 'filtering'},
            {'type': 'first_letter', 'question': 'We are s_____ our camping chairs.', 'answer': 'setting'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his favorite spot on the rug.', 'answer': 'finding'},
            {'type': 'first_letter', 'question': 'She is s_____ her necklace clasp.', 'answer': 'fastening'},
            {'type': 'first_letter', 'question': 'The rain is s_____ on the garden.', 'answer': 'watering'},
            {'type': 'first_letter', 'question': 'I am s_____ my hands together.', 'answer': 'folding'},
            {'type': 'first_letter', 'question': 'The students are s_____ their graduation photos.', 'answer': 'taking'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby\'s blanket.', 'answer': 'tucking'},
            {'type': 'first_letter', 'question': 'The car is s_____ around the corner.', 'answer': 'turning'},
            {'type': 'first_letter', 'question': 'We are s_____ our camping stove.', 'answer': 'lighting'},
            {'type': 'first_letter', 'question': 'The cat is s_____ under the sofa.', 'answer': 'hiding'},
            {'type': 'first_letter', 'question': 'She is s_____ her shoes on the mat.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The snow is s_____ on the power lines.', 'answer': 'gathering'},
            {'type': 'first_letter', 'question': 'I am s_____ my hands in my lap.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The children are s_____ their bicycles home.', 'answer': 'riding'},
            {'type': 'first_letter', 'question': 'She is s_____ her wedding ring on her finger.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The sun is s_____ on the beach.', 'answer': 'setting'},
            {'type': 'first_letter', 'question': 'We are s_____ our campfire.', 'answer': 'making'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his bone to hide it.', 'answer': 'trying'},
            {'type': 'first_letter', 'question': 'She is s_____ her hair out of her eyes.', 'answer': 'pushing'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ in the greenhouse.', 'answer': 'growing'},
            {'type': 'first_letter', 'question': 'I am s_____ my watch back on.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The students are s_____ their graduation ceremony.', 'answer': 'attending'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby\'s pacifier back.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The car is s_____ in the parking space.', 'answer': 'fitting'},
            {'type': 'first_letter', 'question': 'We are s_____ our campfire for the night.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The cat is s_____ in the cardboard box.', 'answer': 'curling'},
            {'type': 'first_letter', 'question': 'She is s_____ her shoes back on.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The snow is s_____ on the mailbox.', 'answer': 'stacking'},
            {'type': 'first_letter', 'question': 'I am s_____ my feet under the blanket.', 'answer': 'tucking'},
            {'type': 'first_letter', 'question': 'The children are s_____ their sleds back home.', 'answer': 'carrying'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby back in the crib.', 'answer': 'laying'},
            {'type': 'first_letter', 'question': 'The sun is s_____ for the night.', 'answer': 'setting'},
            {'type': 'first_letter', 'question': 'We are s_____ our camping gear away.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his bone in his mouth.', 'answer': 'holding'},
            {'type': 'first_letter', 'question': 'She is s_____ her hair in a bun.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ in the evening light.', 'answer': 'glowing'},
            {'type': 'first_letter', 'question': 'I am s_____ my hands behind my head.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The students are s_____ their graduation caps in the air.', 'answer': 'throwing'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby\'s room in order.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The car is s_____ in the garage.', 'answer': 'parked'},
            {'type': 'first_letter', 'question': 'We are s_____ our camping adventure behind us.', 'answer': 'leaving'},
            {'type': 'first_letter', 'question': 'The cat is s_____ on the kitchen counter.', 'answer': 'sitting'},
            {'type': 'first_letter', 'question': 'She is s_____ her coat back on the hook.', 'answer': 'hanging'},
            {'type': 'first_letter', 'question': 'The snow is s_____ outside the window.', 'answer': 'falling'},
            {'type': 'first_letter', 'question': 'I am s_____ my phone back in my pocket.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The children are s_____ their snowmen in the yard.', 'answer': 'building'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby back to sleep.', 'answer': 'rocking'},
            {'type': 'first_letter', 'question': 'The sun is s_____ over the mountains.', 'answer': 'shining'},
            {'type': 'first_letter', 'question': 'We are s_____ our camping memories.', 'answer': 'cherishing'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his favorite toy under the bed.', 'answer': 'hiding'},
            {'type': 'first_letter', 'question': 'She is s_____ her hair in a braid.', 'answer': 'plaiting'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ in the garden center.', 'answer': 'blooming'},
            {'type': 'first_letter', 'question': 'I am s_____ my hands behind my back.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The students are s_____ their school year.', 'answer': 'finishing'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby\'s mobile to the crib.', 'answer': 'attaching'},
            {'type': 'first_letter', 'question': 'The car is s_____ in reverse.', 'answer': 'moving'},
            {'type': 'first_letter', 'question': 'We are s_____ our camping trip in our minds.', 'answer': 'remembering'},
            {'type': 'first_letter', 'question': 'The cat is s_____ on the windowsill.', 'answer': 'perched'},
            {'type': 'first_letter', 'question': 'She is s_____ her ring back in the jewelry box.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The snow is s_____ on the windowsill.', 'answer': 'collecting'},
            {'type': 'first_letter', 'question': 'I am s_____ my feet on the footrest.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The children are s_____ their bicycles away.', 'answer': 'parking'},
            {'type': 'first_letter', 'question': 'She is s_____ her wedding dress back in the closet.', 'answer': 'hanging'},
            {'type': 'first_letter', 'question': 'The sun is s_____ through the bedroom window.', 'answer': 'streaming'},
            {'type': 'first_letter', 'question': 'We are s_____ our camping gear back in the attic.', 'answer': 'storing'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his bone in his doghouse.', 'answer': 'burying'},
            {'type': 'first_letter', 'question': 'She is s_____ her hair back from her face.', 'answer': 'pushing'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ their last bloom.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'I am s_____ my hands on the armrests.', 'answer': 'resting'},
            {'type': 'first_letter', 'question': 'The students are s_____ their caps and gowns.', 'answer': 'removing'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby\'s toys back in the box.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The car is s_____ back to the city.', 'answer': 'returning'},
            {'type': 'first_letter', 'question': 'We are s_____ our camping adventure behind us.', 'answer': 'ending'},
            {'type': 'first_letter', 'question': 'The cat is s_____ in the sunbeam.', 'answer': 'lounging'},
            {'type': 'first_letter', 'question': 'She is s_____ her necklace back on the stand.', 'answer': 'placing'},
            {'type': 'first_letter', 'question': 'The snow is s_____ softly to the ground.', 'answer': 'drifting'},
            {'type': 'first_letter', 'question': 'I am s_____ my head back.', 'answer': 'tilting'},
            {'type': 'first_letter', 'question': 'The children are s_____ their sleds back in the garage.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby back in the carriage.', 'answer': 'strapping'},
            {'type': 'first_letter', 'question': 'The sun is s_____ its final rays.', 'answer': 'sending'},
            {'type': 'first_letter', 'question': 'We are s_____ our camping fire for good.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his bone for the last time.', 'answer': 'taking'},
            {'type': 'first_letter', 'question': 'She is s_____ her hair back to its normal style.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ their final beauty.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'I am s_____ my eyes to rest.', 'answer': 'closing'},
            {'type': 'first_letter', 'question': 'The students are s_____ their graduation ceremony.', 'answer': 'completing'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby\'s room for the night.', 'answer': 'preparing'},
            {'type': 'first_letter', 'question': 'The car is s_____ for the last time.', 'answer': 'parking'},
            {'type': 'first_letter', 'question': 'We are s_____ our camping memories.', 'answer': ' treasuring'},
            {'type': 'first_letter', 'question': 'The cat is s_____ for the night.', 'answer': 'settling'},
            {'type': 'first_letter', 'question': 'She is s_____ her day.', 'answer': 'ending'},
            {'type': 'first_letter', 'question': 'The snow is s_____ for the season.', 'answer': 'ending'},
            {'type': 'first_letter', 'question': 'I am s_____ for sleep.', 'answer': 'getting'},
            {'type': 'first_letter', 'question': 'The children are s_____ for bedtime.', 'answer': 'getting'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby down.', 'answer': 'laying'},
            {'type': 'first_letter', 'question': 'The sun is s_____ for tomorrow.', 'answer': 'waiting'},
            {'type': 'first_letter', 'question': 'We are s_____ for new adventures.', 'answer': 'ready'},
            {'type': 'first_letter', 'question': 'The dog is s_____ in his bed.', 'answer': 'settling'},
            {'type': 'first_letter', 'question': 'She is s_____ in her dreams.', 'answer': 'drifting'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ for spring.', 'answer': 'waiting'},
            {'type': 'first_letter', 'question': 'I am s_____ in my dreams.', 'answer': 'sleeping'},
            {'type': 'first_letter', 'question': 'The students are s_____ their futures.', 'answer': 'planning'},
            {'type': 'first_letter', 'question': 'She is s_____ in her sleep.', 'answer': 'resting'},
            {'type': 'first_letter', 'question': 'The car is s_____ in the garage.', 'answer': 'parked'},
            {'type': 'first_letter', 'question': 'We are s_____ for tomorrow.', 'answer': 'ready'},
            {'type': 'first_letter', 'question': 'The cat is s_____ by the fire.', 'answer': 'curling'},
            {'type': 'first_letter', 'question': 'She is s_____ peacefully.', 'answer': 'sleeping'},
            {'type': 'first_letter', 'question': 'The snow is s_____ silently.', 'answer': 'falling'},
            {'type': 'first_letter', 'question': 'I am s_____ contentedly.', 'answer': 'sleeping'},
            {'type': 'first_letter', 'question': 'The children are s_____ soundly.', 'answer': 'sleeping'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby.', 'answer': 'rocking'},
            {'type': 'first_letter', 'question': 'The sun is s_____ for the new day.', 'answer': 'waiting'},
            {'type': 'first_letter', 'question': 'We are s_____ for the future.', 'answer': 'ready'},
            {'type': 'first_letter', 'question': 'The dog is s_____ by the fire.', 'answer': 'sleeping'},
            {'type': 'first_letter', 'question': 'She is s_____ her dreams.', 'answer': 'enjoying'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ for the new season.', 'answer': 'waiting'},
            {'type': 'first_letter', 'question': 'I am s_____ my dreams.', 'answer': 'living'},
            {'type': 'first_letter', 'question': 'The students are s_____ their goals.', 'answer': 'setting'},
            {'type': 'first_letter', 'question': 'She is s_____ her night.', 'answer': 'ending'},
            {'type': 'first_letter', 'question': 'The car is s_____ for the morning.', 'answer': 'ready'},
            {'type': 'first_letter', 'question': 'We are s_____ our rest.', 'answer': 'taking'},
            {'type': 'first_letter', 'question': 'The cat is s_____ in the moonlight.', 'answer': 'sleeping'},
            {'type': 'first_letter', 'question': 'She is s_____ in the night.', 'answer': 'dreaming'},
            {'type': 'first_letter', 'question': 'The snow is s_____ on the ground.', 'answer': 'lying'},
            {'type': 'first_letter', 'question': 'I am s_____ my eyes.', 'answer': 'closing'},
            {'type': 'first_letter', 'question': 'The children are s_____ their sleep.', 'answer': 'enjoying'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby close.', 'answer': 'holding'},
            {'type': 'first_letter', 'question': 'The sun is s_____ its promise.', 'answer': 'keeping'},
            {'type': 'first_letter', 'question': 'We are s_____ our dreams.', 'answer': 'chasing'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his dreams.', 'answer': 'chasing'},
            {'type': 'first_letter', 'question': 'She is s_____ her thoughts.', 'answer': 'following'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ their beauty.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'I am s_____ my rest.', 'answer': 'enjoying'},
            {'type': 'first_letter', 'question': 'The students are s_____ their futures.', 'answer': 'building'},
            {'type': 'first_letter', 'question': 'She is s_____ her night away.', 'answer': 'spending'},
            {'type': 'first_letter', 'question': 'The car is s_____ its time.', 'answer': 'waiting'},
            {'type': 'first_letter', 'question': 'We are s_____ our time.', 'answer': 'enjoying'},
            {'type': 'first_letter', 'question': 'The cat is s_____ the night away.', 'answer': 'sleeping'},
            {'type': 'first_letter', 'question': 'She is s_____ in the silence.', 'answer': 'resting'},
            {'type': 'first_letter', 'question': 'The snow is s_____ peacefully.', 'answer': 'falling'},
            {'type': 'first_letter', 'question': 'I am s_____ my peace.', 'answer': 'finding'},
            {'type': 'first_letter', 'question': 'The children are s_____ their dreams.', 'answer': 'having'},
            {'type': 'first_letter', 'question': 'She is s_____ her baby to sleep.', 'answer': 'putting'},
            {'type': 'first_letter', 'question': 'The sun is s_____ the world.', 'answer': 'warming'},
            {'type': 'first_letter', 'question': 'We are s_____ our lives.', 'answer': 'living'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his life.', 'answer': 'enjoying'},
            {'type': 'first_letter', 'question': 'She is s_____ her love.', 'answer': 'giving'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ their fragrance.', 'answer': 'sharing'},
            {'type': 'first_letter', 'question': 'I am s_____ my happiness.', 'answer': 'feeling'},
            {'type': 'first_letter', 'question': 'The students are s_____ their education.', 'answer': 'pursuing'},
            {'type': 'first_letter', 'question': 'She is s_____ her patience.', 'answer': 'practicing'},
            {'type': 'first_letter', 'question': 'The car is s_____ its purpose.', 'answer': 'serving'},
            {'type': 'first_letter', 'question': 'We are s_____ our happiness.', 'answer': 'finding'},
            {'type': 'first_letter', 'question': 'The cat is s_____ its nature.', 'answer': 'being'},
            {'type': 'first_letter', 'question': 'She is s_____ her destiny.', 'answer': 'fulfilling'},
            {'type': 'first_letter', 'question': 'The snow is s_____ its beauty.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'I am s_____ my potential.', 'answer': 'realizing'},
            {'type': 'first_letter', 'question': 'The children are s_____ their potential.', 'answer': 'discovering'},
            {'type': 'first_letter', 'question': 'She is s_____ her dreams.', 'answer': 'achieving'},
            {'type': 'first_letter', 'question': 'The sun is s_____ its purpose.', 'answer': 'fulfilling'},
            {'type': 'first_letter', 'question': 'We are s_____ our dreams.', 'answer': 'achieving'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his purpose.', 'answer': 'fulfilling'},
            {'type': 'first_letter', 'question': 'She is s_____ her life.', 'answer': 'living'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ their purpose.', 'answer': 'fulfilling'},
            {'type': 'first_letter', 'question': 'I am s_____ my life.', 'answer': 'living'},
            {'type': 'first_letter', 'question': 'The students are s_____ their purpose.', 'answer': 'fulfilling'},
            {'type': 'first_letter', 'question': 'She is s_____ her destiny.', 'answer': 'living'},
            {'type': 'first_letter', 'question': 'The car is s_____ its life.', 'answer': 'living'},
            {'type': 'first_letter', 'question': 'We are s_____ our destiny.', 'answer': 'living'},
            {'type': 'first_letter', 'question': 'The cat is s_____ its destiny.', 'answer': 'living'},
            {'type': 'first_letter', 'question': 'She is s_____ her potential.', 'answer': 'realizing'},
            {'type': 'first_letter', 'question': 'The snow is s_____ its beauty.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'I am s_____ my purpose.', 'answer': 'fulfilling'},
            {'type': 'first_letter', 'question': 'The children are s_____ their purpose.', 'answer': 'fulfilling'},
            {'type': 'first_letter', 'question': 'She is s_____ her life.', 'answer': 'loving'},
            {'type': 'first_letter', 'question': 'The sun is s_____ its light.', 'answer': 'shining'},
            {'type': 'first_letter', 'question': 'We are s_____ our love.', 'answer': 'sharing'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his love.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'She is s_____ her kindness.', 'answer': 'sharing'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ their beauty.', 'answer': 'sharing'},
            {'type': 'first_letter', 'question': 'I am s_____ my joy.', 'answer': 'sharing'},
            {'type': 'first_letter', 'question': 'The students are s_____ their knowledge.', 'answer': 'sharing'},
            {'type': 'first_letter', 'question': 'She is s_____ her wisdom.', 'answer': 'sharing'},
            {'type': 'first_letter', 'question': 'The car is s_____ its service.', 'answer': 'providing'},
            {'type': 'first_letter', 'question': 'We are s_____ our service.', 'answer': 'providing'},
            {'type': 'first_letter', 'question': 'The cat is s_____ its companionship.', 'answer': 'providing'},
            {'type': 'first_letter', 'question': 'She is s_____ her support.', 'answer': 'providing'},
            {'type': 'first_letter', 'question': 'The snow is s_____ its peace.', 'answer': 'bringing'},
            {'type': 'first_letter', 'question': 'I am s_____ my peace.', 'answer': 'bringing'},
            {'type': 'first_letter', 'question': 'The children are s_____ their laughter.', 'answer': 'bringing'},
            {'type': 'first_letter', 'question': 'She is s_____ her warmth.', 'answer': 'bringing'},
            {'type': 'first_letter', 'question': 'The sun is s_____ its warmth.', 'answer': 'bringing'},
            {'type': 'first_letter', 'question': 'We are s_____ our happiness.', 'answer': 'bringing'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his joy.', 'answer': 'bringing'},
            {'type': 'first_letter', 'question': 'She is s_____ her love.', 'answer': 'bringing'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ their fragrance.', 'answer': 'bringing'},
            {'type': 'first_letter', 'question': 'I am s_____ my gratitude.', 'answer': 'bringing'},
            {'type': 'first_letter', 'question': 'The students are s_____ their enthusiasm.', 'answer': 'bringing'},
            {'type': 'first_letter', 'question': 'She is s_____ her excitement.', 'answer': 'bringing'},
            {'type': 'first_letter', 'question': 'The car is s_____ its reliability.', 'answer': 'providing'},
            {'type': 'first_letter', 'question': 'We are s_____ our commitment.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The cat is s_____ its independence.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'She is s_____ her confidence.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The snow is s_____ its purity.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'I am s_____ my determination.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The children are s_____ their curiosity.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'She is s_____ her creativity.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The sun is s_____ its constancy.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'We are s_____ our perseverance.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his loyalty.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'She is s_____ her strength.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ their resilience.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'I am s_____ my resilience.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The students are s_____ their determination.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'She is s_____ her dedication.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The car is s_____ its durability.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'We are s_____ our reliability.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The cat is s_____ its agility.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'She is s_____ her flexibility.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The snow is s_____ its silence.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'I am s_____ my serenity.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The children are s_____ their playfulness.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'She is s_____ her spontaneity.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The sun is s_____ its energy.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'We are s_____ our vitality.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The dog is s_____ his energy.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'She is s_____ her dynamism.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The flowers are s_____ their vitality.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'I am s_____ my dynamism.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The students are s_____ their energy.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'She is s_____ her enthusiasm.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The car is s_____ its power.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'We are s_____ our strength.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The cat is s_____ its power.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'She is s_____ her capability.', 'answer': 'showing'},
            {'type': 'first_letter', 'question': 'The snow is s_____ its majesty.', 'answer': 'showing'},
        ]
        
        # 合并并去重
        all_questions = first_letter_questions + additional_questions
        seen_answers = set()
        unique_questions = []
        for q in all_questions:
            if q['answer'] not in seen_answers:
                unique_questions.append(q)
                seen_answers.add(q['answer'])
        
        first_letter_questions = unique_questions
    
        # 打乱顺序
        import random
        random.shuffle(first_letter_questions)
        return first_letter_questions[:50]  # 返回最多50题
    
        return [
            {
                'type': 'reading',
                'title': 'My Cat Mimi',
                'article': 'I have a cat named Mimi. She is white and black. Mimi likes to sleep in the sun and drink milk. Every morning, she wakes me up by meowing loudly. Mimi is very playful and loves to chase butterflies in the garden.',
                'questions': [
                    {'type': 'choice', 'question': 'What is the name of the cat?', 'options': ['Mimi', 'Fluffy', 'Snow', 'Shadow'], 'answer': 'Mimi'},
                    {'type': 'choice', 'question': 'What color is Mimi?', 'options': ['All white', 'All black', 'White and black', 'Brown and white'], 'answer': 'White and black'},
                    {'type': 'choice', 'question': 'What does Mimi like to chase?', 'options': ['Birds', 'Butterflies', 'Fish', 'Other cats'], 'answer': 'Butterflies'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Birthday Party',
                'article': 'Today is Tom\'s birthday. His friends come to his house for a party. They bring gifts and balloons. Tom\'s mom bakes a big chocolate cake. Everyone sings happy birthday and eats cake together. Tom feels very happy.',
                'questions': [
                    {'type': 'choice', 'question': 'Who has a birthday today?', 'options': ['Mike', 'Tom', 'John', 'David'], 'answer': 'Tom'},
                    {'type': 'choice', 'question': 'What kind of cake does Tom\'s mom bake?', 'options': ['Vanilla cake', 'Chocolate cake', 'Strawberry cake', 'Carrot cake'], 'answer': 'Chocolate cake'},
                    {'type': 'choice', 'question': 'How does Tom feel at the party?', 'options': ['Sad', 'Angry', 'Happy', 'Scared'], 'answer': 'Happy'}
                ]
            },
            {
                'type': 'reading',
                'title': 'At the Park',
                'article': 'The park is full of children today. Some are playing on the swings, others are sliding down the slide. Sarah and her brother are flying a red kite. The trees are green and there are colorful flowers everywhere.',
                'questions': [
                    {'type': 'choice', 'question': 'What are some children playing on?', 'options': ['Bikes', 'Swings and slides', 'Skateboards', 'Balls'], 'answer': 'Swings and slides'},
                    {'type': 'choice', 'question': 'What color is the kite?', 'options': ['Blue', 'Green', 'Red', 'Yellow'], 'answer': 'Red'},
                    {'type': 'choice', 'question': 'What color are the trees?', 'options': ['Brown', 'Yellow', 'Green', 'Red'], 'answer': 'Green'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Busy Bee',
                'article': 'A little bee flies from flower to flower all day long. It collects sweet nectar to make honey. The bee is very busy and never stops working. Flowers depend on bees to carry pollen from one flower to another.',
                'questions': [
                    {'type': 'choice', 'question': 'What does the bee collect from flowers?', 'options': ['Water', 'Nectar', 'Leaves', 'Dirt'], 'answer': 'Nectar'},
                    {'type': 'choice', 'question': 'What does the bee make from nectar?', 'options': ['Wax', 'Honey', 'Butter', 'Jam'], 'answer': 'Honey'},
                    {'type': 'choice', 'question': 'How would you describe the bee?', 'options': ['Lazy', 'Busy', 'Sleepy', 'Sad'], 'answer': 'Busy'}
                ]
            },
            {
                'type': 'reading',
                'title': 'Rainy Day',
                'article': 'It is raining outside. Raindrops fall on the windows and roofs. Tom cannot play in the garden, so he stays inside. He reads books and draws pictures. When the rain stops, Tom will go outside to jump in the puddles.',
                'questions': [
                    {'type': 'choice', 'question': 'What is the weather like?', 'options': ['Sunny', 'Cloudy', 'Rainy', 'Snowy'], 'answer': 'Rainy'},
                    {'type': 'choice', 'question': 'What does Tom do inside?', 'options': ['Sleeps', 'Reads and draws', 'Cooks', 'Cleans'], 'answer': 'Reads and draws'},
                    {'type': 'choice', 'question': 'What will Tom do when the rain stops?', 'options': ['Go to school', 'Jump in puddles', 'Take a nap', 'Call friends'], 'answer': 'Jump in puddles'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Little Fish',
                'article': 'In a clear blue pond, a little fish swims with his family. The fish is small and silver with bright blue stripes. He likes to play hide-and-seek among the water plants. When danger comes, he quickly hides behind a big rock.',
                'questions': [
                    {'type': 'choice', 'question': 'Where does the little fish live?', 'options': ['Ocean', 'River', 'Pond', 'Lake'], 'answer': 'Pond'},
                    {'type': 'choice', 'question': 'What color are the fish\'s stripes?', 'options': ['Red', 'Green', 'Blue', 'Yellow'], 'answer': 'Blue'},
                    {'type': 'choice', 'question': 'Where does the fish hide when there is danger?', 'options': ['In the plants', 'Behind a rock', 'Under a log', 'In a cave'], 'answer': 'Behind a rock'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The School Bus',
                'article': 'Every morning, Amy waits at the bus stop with her backpack. The yellow school bus arrives at 7:30 AM. Amy climbs aboard and sits by the window. The bus driver greets all the children with a smile. On the way to school, Amy looks at the passing trees and houses.',
                'questions': [
                    {'type': 'choice', 'question': 'What time does the school bus arrive?', 'options': ['7:00 AM', '7:30 AM', '8:00 AM', '8:30 AM'], 'answer': '7:30 AM'},
                    {'type': 'choice', 'question': 'What color is the school bus?', 'options': ['Blue', 'Green', 'Yellow', 'Red'], 'answer': 'Yellow'},
                    {'type': 'choice', 'question': 'Where does Amy sit on the bus?', 'options': ['In the front', 'By the window', 'In the back', 'Standing'], 'answer': 'By the window'}
                ]
            },
            {
                'type': 'reading',
                'title': 'A Day at the Beach',
                'article': 'Jenny and her family go to the beach on Saturday. The sun shines brightly and the waves are small. Jenny builds a sandcastle with her bucket and shovel. She also collects pretty shells and colorful sea glass. At lunchtime, they eat sandwiches and drink cold juice.',
                'questions': [
                    {'type': 'choice', 'question': 'When do they go to the beach?', 'options': ['Sunday', 'Friday', 'Saturday', 'Monday'], 'answer': 'Saturday'},
                    {'type': 'choice', 'question': 'What does Jenny build with her tools?', 'options': ['A boat', 'A sandcastle', 'A house', 'A flower'], 'answer': 'A sandcastle'},
                    {'type': 'choice', 'question': 'What do they drink at lunch?', 'options': ['Milk', 'Water', 'Cold juice', 'Tea'], 'answer': 'Cold juice'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Library',
                'article': 'The town library is a quiet place full of books. Mrs. Johnson works there as a librarian. Children come to borrow books about animals, space, and adventure stories. The library also has computers where kids can play educational games.',
                'questions': [
                    {'type': 'choice', 'question': 'What is a librarian?', 'options': ['A doctor', 'A teacher', 'A library worker', 'A writer'], 'answer': 'A library worker'},
                    {'type': 'choice', 'question': 'What can you find in the library?', 'options': ['Toys', 'Food', 'Books', 'Animals'], 'answer': 'Books'},
                    {'type': 'choice', 'question': 'What do children play on the library computers?', 'options': ['Shooting games', 'Racing games', 'Educational games', 'Fighting games'], 'answer': 'Educational games'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Hungry Rabbit',
                'article': 'A white rabbit lives in a burrow near the carrot field. Every morning, he hops out to look for food. Today, he is very hungry and finds a big orange carrot. He munches it happily and feels much better. The rabbit thanks the farmer for growing such delicious carrots.',
                'questions': [
                    {'type': 'choice', 'question': 'What color is the rabbit?', 'options': ['Brown', 'Gray', 'White', 'Black'], 'answer': 'White'},
                    {'type': 'choice', 'question': 'Where does the rabbit live?', 'options': ['In a tree', 'In a burrow', 'In a house', 'In a cave'], 'answer': 'In a burrow'},
                    {'type': 'choice', 'question': 'What does the rabbit eat?', 'options': ['Grass', 'Carrots', 'Leaves', 'Berries'], 'answer': 'Carrots'}
                ]
            },
            {
                'type': 'reading',
                'title': 'Moonbeam Lady',
                'article': 'When night comes, the Moonbeam Lady puts on her silver-white dress and comes out to play. She sends soft light to help children fall asleep. The little children see her gentle light and soon enter beautiful dreams. The Moonbeam Lady watches over all the children with her caring light.',
                'questions': [
                    {'type': 'choice', 'question': 'What color is the Moonbeam Lady\'s dress?', 'options': ['Red', 'Blue', 'Silver-white', 'Yellow'], 'answer': 'Silver-white'},
                    {'type': 'choice', 'question': 'How do children feel when they see the moonlight?', 'options': ['Very excited', 'Cannot sleep', 'Fall into dreams', 'Very happy'], 'answer': 'Fall into dreams'}
                ]
            },
            # 继续添加更多文章...
            {
                'type': 'reading',
                'title': 'The Rainbow Bridge',
                'article': 'After the rain stopped, a beautiful rainbow appeared in the sky. The rainbow has seven colors: red, orange, yellow, green, blue, indigo, and violet. Children pointed at the rainbow and said, "How beautiful!" An old man told the children that this is a gift from nature.',
                'questions': [
                    {'type': 'choice', 'question': 'How many colors does the rainbow have?', 'options': ['Five', 'Six', 'Seven', 'Eight'], 'answer': 'Seven'},
                    {'type': 'choice', 'question': 'When does the rainbow appear?', 'options': ['During rain', 'After rain stops', 'When sunny', 'When cloudy'], 'answer': 'After rain stops'},
                    {'type': 'choice', 'question': 'According to the old man, what is the rainbow?', 'options': ['Clouds', 'A gift', 'A bridge', 'A window'], 'answer': 'A gift'}
                ]
            },
            {
                'type': 'reading',
                'title': 'Little Tadpoles Find Their Mother',
                'article': 'Spring came, and the water plants in the pond swayed gently. Little tadpoles swam around in the water, searching for their mother. The tadpoles first met a duck mother who said, "Your mother has four legs." The tadpoles then met a fish mother who said, "Your mother has four legs and two arms." Finally, the little tadpoles found their frog mother.',
                'questions': [
                    {'type': 'choice', 'question': 'What are the little tadpoles doing?', 'options': ['Finding their mother', 'Looking for food', 'Looking for friends', 'Looking for home'], 'answer': 'Finding their mother'},
                    {'type': 'choice', 'question': 'What did the duck mother say about the tadpoles mother?', 'options': ['She has four legs', 'She has two legs', 'She has no legs', 'She has six legs'], 'answer': 'She has four legs'},
                    {'type': 'choice', 'question': 'What is the tadpoles mother?', 'options': ['A fish', 'A frog', 'A duck', 'A crab'], 'answer': 'A frog'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Brave Little Duckling',
                'article': 'The little duckling was learning to swim for the first time. He was afraid of water and dared not go into the water. Duck mother encouraged him and said, "My child, you are born to swim." The little duckling gathered courage and jumped into the water. Really, he naturally knew how to swim. The little duckling swam happily in the water.',
                'questions': [
                    {'type': 'choice', 'question': 'What was the little duckling learning for the first time?', 'options': ['Flying', 'Swimming', 'Walking', 'Singing'], 'answer': 'Swimming'},
                    {'type': 'choice', 'question': 'How did the little duckling feel at first?', 'options': ['Very excited', 'Very afraid', 'Very calm', 'Very angry'], 'answer': 'Very afraid'},
                    {'type': 'choice', 'question': 'What did duck mother tell the little duckling?', 'options': ['You were born to swim', 'You cannot swim', 'You are stupid', 'You are clever'], 'answer': 'You were born to swim'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Apple Tree Story',
                'article': 'There is an apple tree in the yard. In spring, it is covered with pink flowers. In summer, it grows green leaves. In autumn, it bears red apples. In winter, all its leaves fall off to prepare for winter. The apple tree has different beautiful scenery in each season.',
                'questions': [
                    {'type': 'choice', 'question': 'What color flowers does the apple tree have in spring?', 'options': ['Red', 'Pink', 'White', 'Yellow'], 'answer': 'Pink'},
                    {'type': 'choice', 'question': 'When does the apple tree bear apples?', 'options': ['Spring', 'Summer', 'Autumn', 'Winter'], 'answer': 'Autumn'},
                    {'type': 'choice', 'question': 'What happens to the apple tree in winter?', 'options': ['Leaves fall off', 'Continues blooming', 'Bears apples', 'Grows new leaves'], 'answer': 'Leaves fall off'}
                ]
            },
            {
                'type': 'reading',
                'title': 'Baby Bird Learns to Fly',
                'article': 'When the baby bird was born, it couldn\'t fly yet. Bird mother taught it to practice every day. The baby bird jumped from the tree branch and tried to flap its wings. The first time it fell down, and the second time it also fell down. But the baby bird didn\'t give up and kept practicing hard. Finally, the baby bird learned to fly and was happy to fly freely in the sky.',
                'questions': [
                    {'type': 'choice', 'question': 'Could the baby bird fly when it was born?', 'options': ['Yes', 'No', 'Not sure', 'Sometimes'], 'answer': 'No'},
                    {'type': 'choice', 'question': 'What did the baby bird do when it fell down while practicing?', 'options': ['Gave up', 'Kept trying', 'Cried', 'Got scared'], 'answer': 'Kept trying'},
                    {'type': 'choice', 'question': 'What happened to the baby bird in the end?', 'options': ['Still couldn\'t fly', 'Learned to fly', 'Didn\'t want to fly', 'Flew very slowly'], 'answer': 'Learned to fly'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Seed\'s Journey',
                'article': 'A tiny seed fell into the soil. The seed absorbed the moisture from the rainwater and slowly began to sprout. It first grew tender green leaves, then grew taller and taller. Spring turned into summer, and summer turned into autumn. When autumn arrived, the seed had grown into a big tree with lots of fruit on its branches.',
                'questions': [
                    {'type': 'choice', 'question': 'Where did the seed fall?', 'options': ['In water', 'In soil', 'On rocks', 'On a tree'], 'answer': 'In soil'},
                    {'type': 'choice', 'question': 'What did the seed grow first?', 'options': ['Flowers', 'Fruit', 'Small leaves', 'Tree roots'], 'answer': 'Small leaves'},
                    {'type': 'choice', 'question': 'What did the seed become in autumn?', 'options': ['A small flower', 'A big tree', 'Grass', 'A rock'], 'answer': 'A big tree'}
                ]
            },
            {
                'type': 'reading',
                'title': 'Winter Snow',
                'article': 'Winter came, and snowflakes began to fall from the sky. The snowflakes looked like white feathers, gently landing on the ground. Soon, the earth was covered with a white coat. Children built snowmen, had snowball fights, and had a wonderful time playing. Even little animals came out to play, and the little rabbit left many footprints in the snow.',
                'questions': [
                    {'type': 'choice', 'question': 'What do snowflakes look like?', 'options': ['Feathers', 'Petals', 'Leaves', 'Rocks'], 'answer': 'Feathers'},
                    {'type': 'choice', 'question': 'What do children do in the snow?', 'options': ['Build snowmen', 'Have snowball fights', 'Play', 'All of the above'], 'answer': 'All of the above'},
                    {'type': 'choice', 'question': 'How are the little rabbit\'s footprints?', 'options': ['Very big', 'Very small', 'In strings', 'No footprints'], 'answer': 'In strings'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Sea\'s Gift',
                'article': 'The sea gives people many gifts. There are fresh seafood, beautiful shells, and shining pearls. Children collect shells at the beach and find shells of various colors: white ones, pink ones, and purple ones. They make the shells into beautiful decorations.',
                'questions': [
                    {'type': 'choice', 'question': 'What gifts does the sea give people?', 'options': ['Only seafood', 'Only shells', 'Seafood, shells, pearls', 'Only pearls'], 'answer': 'Seafood, shells, pearls'},
                    {'type': 'choice', 'question': 'What do children do at the beach?', 'options': ['Swim', 'Collect shells', 'Fish', 'Build castles'], 'answer': 'Collect shells'},
                    {'type': 'choice', 'question': 'What colors are the shells?', 'options': ['Only white', 'Only pink', 'White, pink, purple', 'No color'], 'answer': 'White, pink, purple'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Busy Bee\'s Work',
                'article': 'Little bees are very diligent every day. They are busy from morning to night, flying to flower gardens to collect nectar. The collected nectar is stored in the beehive and turned into sweet honey. The little bees work together with division of labor: some collect nectar, some build the hive, and some take care of larvae. Their work makes the entire beehive full of life.',
                'questions': [
                    {'type': 'choice', 'question': 'How do the little bees work?', 'options': ['Very lazy', 'Very diligent', 'Very casual', 'Very careless'], 'answer': 'Very diligent'},
                    {'type': 'choice', 'question': 'What do the little bees do when they fly to flower gardens?', 'options': ['Play', 'Collect nectar', 'Build hives', 'Sleep'], 'answer': 'Collect nectar'},
                    {'type': 'choice', 'question': 'What do the little bees achieve through division of labor?', 'options': ['Make the hive full of life', 'Make flowers more beautiful', 'Make the sky bluer', 'Make the earth greener'], 'answer': 'Make the hive full of life'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Value of Time',
                'article': 'Time is very precious, like gold. We should use our limited time to do useful things. Children should seize the time to study, adults should seize the time to work, and elderly people should seize the time to exercise. Time never comes back once it\'s gone. We should cherish every minute and every second.',
                'questions': [
                    {'type': 'choice', 'question': 'What is time like?', 'options': ['Water', 'Gold', 'Stone', 'Wood'], 'answer': 'Gold'},
                    {'type': 'choice', 'question': 'What should children seize time to do?', 'options': ['Play', 'Study', 'Sleep', 'Eat'], 'answer': 'Study'},
                    {'type': 'choice', 'question': 'What is the characteristic of time?', 'options': ['Will come back', 'Never comes back', 'Very slow', 'Very fast'], 'answer': 'Never comes back'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Sun and the Moon',
                'article': 'The sun and the moon are two good friends in the sky. During the day, Grandfather Sun comes out to work, sending out warm light that fills the earth with life. At night, Grandmother Moon comes out to work, sending out gentle silver light to illuminate the dark night sky. They take turns working, bringing light to people.',
                'questions': [
                    {'type': 'choice', 'question': 'When does the sun come out?', 'options': ['Daytime', 'Nighttime', 'Noon', 'Early morning'], 'answer': 'Daytime'},
                    {'type': 'choice', 'question': 'What kind of light does the sun send out?', 'options': ['Cold', 'Warm', 'Strong', 'Dim'], 'answer': 'Warm'},
                    {'type': 'choice', 'question': 'When does Grandmother Moon come out?', 'options': ['Daytime', 'Nighttime', 'Noon', 'Early morning'], 'answer': 'Nighttime'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Brave Little Warrior',
                'article': 'Little warrior Xiaoming is very brave. In one mission, he encountered difficulties. But he wasn\'t afraid; instead, he calmly thought of solutions. Finally, he overcame the difficulties and completed the mission. Everyone praised him as a brave little warrior.',
                'questions': [
                    {'type': 'choice', 'question': 'What kind of person is Xiaoming?', 'options': ['Lazy', 'Brave', 'Timid', 'Careless'], 'answer': 'Brave'},
                    {'type': 'choice', 'question': 'How did Xiaoming react when he encountered difficulties?', 'options': ['Very scared', 'Calm thinking', 'Gave up', 'Cried'], 'answer': 'Calm thinking'},
                    {'type': 'choice', 'question': 'What do people think of Xiaoming?', 'options': ['Very stupid', 'Very lazy', 'Very brave', 'Very careless'], 'answer': 'Very brave'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Little Fox\'s Wisdom',
                'article': 'The little fox in the forest is very clever. Once, it saw a little rabbit fall into a trap. The little fox thought of a good idea and found a long tree branch, letting the little rabbit grab it and climb up. After being saved, the little rabbit was very grateful for the little fox\'s wisdom.',
                'questions': [
                    {'type': 'choice', 'question': 'What is the little fox\'s characteristic?', 'options': ['Very stupid', 'Very clever', 'Very lazy', 'Very fierce'], 'answer': 'Very clever'},
                    {'type': 'choice', 'question': 'What problem did the little rabbit encounter?', 'options': ['Got lost', 'Fell into a trap', 'Hungry', 'Sick'], 'answer': 'Fell into a trap'},
                    {'type': 'choice', 'question': 'How did the little fox save the little rabbit?', 'options': ['Jumped down to rescue', 'Found a long branch', 'Called other animals', 'Called for help'], 'answer': 'Found a long branch'}
                ]
            },
            {
                'type': 'reading',
                'title': 'Autumn Harvest',
                'article': 'Autumn is the season of harvest. The rice in the fields is golden like a golden carpet. The apples in the orchard are red like little red lanterns. Uncle farmers are busy harvesting grain and picking fruit. Their faces are filled with the joy of a bountiful harvest.',
                'questions': [
                    {'type': 'choice', 'question': 'What season is autumn?', 'options': ['Planting', 'Harvest', 'Blooming', 'Sprouting'], 'answer': 'Harvest'},
                    {'type': 'choice', 'question': 'What color is the rice in the fields?', 'options': ['Green', 'Red', 'Golden', 'White'], 'answer': 'Golden'},
                    {'type': 'choice', 'question': 'What do the apples in the orchard look like?', 'options': ['Little suns', 'Little red lanterns', 'Little stars', 'Little moons'], 'answer': 'Little red lanterns'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Dolphin\'s Performance',
                'article': 'The little dolphin at the aquarium was going to perform. The dolphin swam back and forth in the water, making various beautiful movements. It could jump, dive through rings, and splash water with its tail. The audience watched with great interest and occasionally exclaimed with admiration. After the performance, the dolphin received many little fish as a reward.',
                'questions': [
                    {'type': 'choice', 'question': 'Where does the dolphin perform?', 'options': ['At the beach', 'In a river', 'At the aquarium', 'In a lake'], 'answer': 'At the aquarium'},
                    {'type': 'choice', 'question': 'What movements can the dolphin do?', 'options': ['Jump', 'Dive through rings', 'Splash water', 'All of the above'], 'answer': 'All of the above'},
                    {'type': 'choice', 'question': 'What did the dolphin receive after the performance?', 'options': ['Applause', 'Little fish', 'Toys', 'Trophy'], 'answer': 'Little fish'}
                ]
            },
            {
                'type': 'reading',
                'title': 'Protecting the Environment',
                'article': 'We should protect the environment and not litter. Trash pollutes air and water, harming small animals. Planting trees can purify the air, making the sky bluer and grass greener. We should start from small things to protect our beautiful Earth home.',
                'questions': [
                    {'type': 'choice', 'question': 'What should we do for the environment?', 'options': ['Destroy', 'Protect', 'Pollute', 'Ignore'], 'answer': 'Protect'},
                    {'type': 'choice', 'question': 'What impact does trash have on the environment?', 'options': ['Makes environment more beautiful', 'Pollutes air and water', 'Makes animals happier', 'No impact'], 'answer': 'Pollutes air and water'},
                    {'type': 'choice', 'question': 'What are the benefits of planting trees?', 'options': ['Purify air', 'Make sky bluer', 'Grass greener', 'All of the above'], 'answer': 'All of the above'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Little Monkey\'s Lesson',
                'article': 'The little monkey was very greedy for food. When it saw peaches, it would pick them and eat right away. But it didn\'t wash the peaches before eating. As a result, its stomach hurt. The little monkey regretted it and understood the importance of washing food before eating. From then on, the little monkey would carefully wash food before eating.',
                'questions': [
                    {'type': 'choice', 'question': 'What is the little monkey\'s characteristic?', 'options': ['Very diligent', 'Very greedy for food', 'Very clever', 'Very lazy'], 'answer': 'Very greedy for food'},
                    {'type': 'choice', 'question': 'Why did the little monkey\'s stomach hurt?', 'options': ['Ate too much', 'Didn\'t wash peaches before eating', 'Peaches were bad', 'Peaches were too sweet'], 'answer': 'Didn\'t wash peaches before eating'},
                    {'type': 'choice', 'question': 'What lesson did the little monkey learn?', 'options': ['Peaches are sweet', 'Wash food before eating', 'Peaches are sour', 'Eat slowly'], 'answer': 'Wash food before eating'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Ants Moving House',
                'article': 'The ants discovered that it was going to rain, so they quickly moved house. They formed a long line, carrying food and eggs. Some big ants carried heavy things, and some small ants carried light things. Everyone worked together, and they finished moving quickly. Their new home was very safe and wouldn\'t be flooded by rainwater.',
                'questions': [
                    {'type': 'choice', 'question': 'Why did the ants move house?', 'options': ['It was going to rain', 'House was broken', 'Going traveling', 'Finding a new home'], 'answer': 'It was going to rain'},
                    {'type': 'choice', 'question': 'How did the ants move?', 'options': ['Formed a line', 'Walked one by one', 'Ran around randomly', 'Didn\'t move'], 'answer': 'Formed a line'},
                    {'type': 'choice', 'question': 'How did the ants behave while moving?', 'options': ['Each worked independently', 'Worked together', 'Very lazy', 'Not united'], 'answer': 'Worked together'}
                ]
            },
            {
                'type': 'reading',
                'title': 'Spring Outing',
                'article': 'Spring came, and the school organized a spring outing. Children brought backpacks and water bottles and took a bus. They went to a park in the suburbs and saw green grass, blooming flowers, and heard birds singing on tree branches. Everyone had a picnic on the grass, played, and spent a happy day.',
                'questions': [
                    {'type': 'choice', 'question': 'When does the school organize spring outings?', 'options': ['Summer', 'Autumn', 'Winter', 'Spring'], 'answer': 'Spring'},
                    {'type': 'choice', 'question': 'What did the children bring?', 'options': ['Toys', 'Backpacks and water bottles', 'Books', 'Umbrellas'], 'answer': 'Backpacks and water bottles'},
                    {'type': 'choice', 'question': 'What did children do during the spring outing?', 'options': ['Picnic', 'Play', 'Listen to birds singing', 'All of the above'], 'answer': 'All of the above'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Library\'s Secret',
                'article': 'There are many interesting books in the library. There are story books, science books, and picture albums. Children can read quietly in the library. The librarian aunt is very kind, and she will help children find books. Here, children can learn a lot of knowledge.',
                'questions': [
                    {'type': 'choice', 'question': 'What is in the library?', 'options': ['Many interesting books', 'Toys', 'Food', 'Computers'], 'answer': 'Many interesting books'},
                    {'type': 'choice', 'question': 'What kind of place is the library?', 'options': ['Noisy', 'Quiet', 'Dirty', 'Messy'], 'answer': 'Quiet'},
                    {'type': 'choice', 'question': 'What is the librarian aunt\'s characteristic?', 'options': ['Very strict', 'Very kind', 'Very lazy', 'Very fierce'], 'answer': 'Very kind'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Little Star\'s Wish',
                'article': 'The little star twinkles in the night sky, and it has a wish: hoping that all children can grow up happily. The little star works hard to shine every day, adding beauty to the night sky. When children see the little star, they all make their own wishes.',
                'questions': [
                    {'type': 'choice', 'question': 'What is the little star doing?', 'options': ['Sleeping', 'Twinkling', 'Moving', 'Getting smaller'], 'answer': 'Twinkling'},
                    {'type': 'choice', 'question': 'What is the little star\'s wish?', 'options': ['To become brighter itself', 'For all children to grow up happily', 'To become bigger', 'To become smaller'], 'answer': 'For all children to grow up happily'},
                    {'type': 'choice', 'question': 'What does the little star do for the night sky?', 'options': ['Adds beauty', 'Reduces light', 'Covers the moon', 'Makes noise'], 'answer': 'Adds beauty'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Clever Crow',
                'article': 'A crow was very thirsty and wanted to drink water. But there was too little water in the bottle, and the crow couldn\'t reach it. The clever crow thought of a good idea. It found some small stones and dropped them one by one into the bottle. The water level rose slowly, and the crow finally got to drink water.',
                'questions': [
                    {'type': 'choice', 'question': 'What did the crow want to do?', 'options': ['Eat food', 'Drink water', 'Play', 'Sleep'], 'answer': 'Drink water'},
                    {'type': 'choice', 'question': 'Why couldn\'t the crow drink the water?', 'options': ['Too little water', 'Bottle too high', 'Water too hot', 'Water too cold'], 'answer': 'Too little water'},
                    {'type': 'choice', 'question': 'How did the crow finally get to drink water?', 'options': ['Directly drink', 'Drop stones to raise water level', 'Break the bottle', 'Ask for help'], 'answer': 'Drop stones to raise water level'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Little Hedgehog\'s Gift',
                'article': 'There was going to be a party in the forest, and the little hedgehog wanted to give gifts to everyone. But its spikes might hurt its friends, and the hedgehog felt worried. Finally, the clever hedgehog had a great idea: it made a beautiful fruit cake with fruits, and everyone loved it.',
                'questions': [
                    {'type': 'choice', 'question': 'What was going to happen in the forest?', 'options': ['Sports game', 'Party', 'Performance', 'Competition'], 'answer': 'Party'},
                    {'type': 'choice', 'question': 'What worried the little hedgehog?', 'options': ['No gift', 'Its spikes might hurt friends', 'Can\'t make cake', 'Too lazy'], 'answer': 'Its spikes might hurt friends'},
                    {'type': 'choice', 'question': 'What was the little hedgehog\'s final gift?', 'options': ['Flowers', 'Fruit cake', 'Toys', 'Books'], 'answer': 'Fruit cake'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Magical Change',
                'article': 'Water is magical because it can change its form. When the weather is very cold, water turns into ice. When the weather is hot, ice melts back into water. When water meets something very hot, it turns into water vapor and flies away. Water\'s changes are truly amazing!',
                'questions': [
                    {'type': 'choice', 'question': 'What does water turn into when the weather is very cold?', 'options': ['Water vapor', 'Ice', 'Stone', 'Wood'], 'answer': 'Ice'},
                    {'type': 'choice', 'question': 'What does ice turn into when the weather is hot?', 'options': ['Stone', 'Water', 'Water vapor', 'Sand'], 'answer': 'Water'},
                    {'type': 'choice', 'question': 'What happens when water meets something very hot?', 'options': ['Turns into water vapor', 'Turns into stone', 'Turns into wood', 'Stays the same'], 'answer': 'Turns into water vapor'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Charm of Music',
                'article': 'Music is beautiful and can make people happy. Little birds love to sing, and flowers seem to dance. When music plays, people unconsciously sway to the rhythm. Music makes the world more beautiful.',
                'questions': [
                    {'type': 'choice', 'question': 'What is music like?', 'options': ['Very unpleasant', 'Very beautiful', 'Very boring', 'Very noisy'], 'answer': 'Very beautiful'},
                    {'type': 'choice', 'question': 'How do little birds react to music?', 'options': ['Afraid', 'Love to sing', 'Run away', 'Sleep'], 'answer': 'Love to sing'},
                    {'type': 'choice', 'question': 'How does music make the world?', 'options': ['More noisy', 'More beautiful', 'More quiet', 'More boring'], 'answer': 'More beautiful'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Little Mushroom\'s Growth',
                'article': 'After the rain, little mushrooms peeked out from the soil. They were first small white dots, then slowly grew into little umbrellas. Mushrooms like to grow in damp, dark places. They absorb nutrients from the soil and grow slowly.',
                'questions': [
                    {'type': 'choice', 'question': 'When do little mushrooms appear?', 'options': ['Sunny day', 'After rain', 'Winter', 'Windy day'], 'answer': 'After rain'},
                    {'type': 'choice', 'question': 'What do little mushrooms look like when they grow up?', 'options': ['Little umbrella', 'Little tree', 'Little grass', 'Little flower'], 'answer': 'Little umbrella'},
                    {'type': 'choice', 'question': 'What environment do mushrooms like?', 'options': ['Dry and bright', 'Damp and dark', 'Cold', 'Hot'], 'answer': 'Damp and dark'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Power of Friendship',
                'article': 'Little rabbit and little squirrel are good friends. When little rabbit was sick, little squirrel came to take care of it. When little squirrel met difficulties, little rabbit came to help. True friendship is like this: caring for each other and helping each other.',
                'questions': [
                    {'type': 'choice', 'question': 'What is the relationship between little rabbit and little squirrel?', 'options': ['Enemies', 'Friends', 'Strangers', 'Relatives'], 'answer': 'Friends'},
                    {'type': 'choice', 'question': 'What did little squirrel do when little rabbit was sick?', 'options': ['Ran away', 'Took care of it', 'Ignored it', 'Laughed at it'], 'answer': 'Took care of it'},
                    {'type': 'choice', 'question': 'What is true friendship like?', 'options': ['Only wants returns', 'Cares and helps each other', 'Only cares about self', 'Uses each other'], 'answer': 'Cares and helps each other'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Beautiful Starry Sky',
                'article': 'The night sky is beautiful. There are many little stars in the sky, and they twinkle and blink their eyes. The moon wears a silver-white dress, adding light to the night sky. Children look at the beautiful starry sky and make wishes.',
                'questions': [
                    {'type': 'choice', 'question': 'How is the night sky?', 'options': ['Very beautiful', 'Very scary', 'Very boring', 'Very dark'], 'answer': 'Very beautiful'},
                    {'type': 'choice', 'question': 'What are the little stars doing?', 'options': ['Staying still', 'Twinkling and blinking', 'Moving', 'Singing'], 'answer': 'Twinkling and blinking'},
                    {'type': 'choice', 'question': 'What color clothes does the moon wear?', 'options': ['Red', 'Silver-white', 'Blue', 'Yellow'], 'answer': 'Silver-white'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Little Snail\'s Journey',
                'article': 'The little snail wanted to see the outside world. Although it crawled very slowly, it didn\'t give up. It crawled step by step forward, saw beautiful flowers, and heard the songs of little birds. Finally, the little snail reached its destination. Although it took a long time, it was very happy.',
                'questions': [
                    {'type': 'choice', 'question': 'What did the little snail want to do?', 'options': ['Sleep', 'See the outside world', 'Eat food', 'Play'], 'answer': 'See the outside world'},
                    {'type': 'choice', 'question': 'How did the little snail crawl?', 'options': ['Very fast', 'Very slow', 'Normal', 'Very fast'], 'answer': 'Very slow'},
                    {'type': 'choice', 'question': 'How did the little snail feel at the end?', 'options': ['Very depressed', 'Very angry', 'Very happy', 'Very scared'], 'answer': 'Very happy'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Hardworking Bee',
                'article': 'Bees are hardworking little insects. They are busy from morning to night every day, flying to flower gardens to collect nectar. The collected nectar is stored in the beehive and made into sweet honey. The bees work together with division of labor, and none of them are lazy.',
                'questions': [
                    {'type': 'choice', 'question': 'What are bees?', 'options': ['Lazy animals', 'Hardworking little insects', 'Fierce animals', 'Lazy animals'], 'answer': 'Hardworking little insects'},
                    {'type': 'choice', 'question': 'What do bees do every day?', 'options': ['Sleep', 'Busy collecting nectar', 'Play', 'Daydream'], 'answer': 'Busy collecting nectar'},
                    {'type': 'choice', 'question': 'How do the bees behave?', 'options': ['Work together with division', 'Are lazy', 'Don\'t cooperate', 'Very lazy'], 'answer': 'Work together with division'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Magical Seed',
                'article': 'Xiaoming planted a magical seed. The seed sprouted quickly and grew green leaves. Then it grew taller and taller, and beautiful flowers bloomed. The flowers had seven colors, like a rainbow.',
                'questions': [
                    {'type': 'choice', 'question': 'What did Xiaoming plant?', 'options': ['Ordinary seed', 'Magical seed', 'Stone', 'Wood'], 'answer': 'Magical seed'},
                    {'type': 'choice', 'question': 'What did the seed grow after sprouting?', 'options': ['Flowers', 'Green leaves', 'Fruit', 'Bugs'], 'answer': 'Green leaves'},
                    {'type': 'choice', 'question': 'What is special about the flowers?', 'options': ['Only one color', 'Seven colors', 'No color', 'Can talk'], 'answer': 'Seven colors'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Magic Cloud',
                'article': 'There are magical clouds in the sky. In the morning, the clouds are white, like cotton candy. At noon, the clouds turn gray, like a gray blanket. In the evening, the clouds become colorful, like a beautiful painting.',
                'questions': [
                    {'type': 'choice', 'question': 'What do morning clouds look like?', 'options': ['Blanket', 'Cotton candy', 'Painting', 'Stone'], 'answer': 'Cotton candy'},
                    {'type': 'choice', 'question': 'What color are the clouds at noon?', 'options': ['White', 'Colorful', 'Gray', 'Red'], 'answer': 'Gray'},
                    {'type': 'choice', 'question': 'What do evening clouds look like?', 'options': ['Painting', 'Blanket', 'Stone', 'Wood'], 'answer': 'Painting'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Little Fish\'s Dream',
                'article': 'The little fish swims happily in the water, and it has a dream: to see the outside world above the water. Although the little fish can\'t live without water, it swims toward the surface every day, hoping to realize its dream one day.',
                'questions': [
                    {'type': 'choice', 'question': 'How is the little fish in the water?', 'options': ['Very painful', 'Swimming happily', 'Very bored', 'Very scared'], 'answer': 'Swimming happily'},
                    {'type': 'choice', 'question': 'What is the little fish\'s dream?', 'options': ['Sleep in water', 'See the world above water', 'Eat more food', 'Grow into a big fish'], 'answer': 'See the world above water'},
                    {'type': 'choice', 'question': 'What does the little fish do to realize its dream?', 'options': ['Give up', 'Swim hard toward the surface', 'Sleep', 'Daydream'], 'answer': 'Swim hard toward the surface'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Happy Stream',
                'article': 'The little stream sings a happy song as it flows forward. It passes through green grass and sees beautiful flowers. It passes through dense forests and hears birds singing. The stream sings all the way, bringing joy to nature.',
                'questions': [
                    {'type': 'choice', 'question': 'What is the little stream doing?', 'options': ['Sleeping', 'Singing', 'Daydreaming', 'Crying'], 'answer': 'Singing'},
                    {'type': 'choice', 'question': 'Where does the little stream pass through?', 'options': ['Grassland', 'Forest', 'Flowers', 'All of the above'], 'answer': 'All of the above'},
                    {'type': 'choice', 'question': 'What does the little stream bring to nature?', 'options': ['Joy', 'Sadness', 'Fear', 'Anger'], 'answer': 'Joy'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Little Kite\'s Flight',
                'article': 'The little kite wanted to fly into the sky. Although it had the help of wind, it needed people\'s guidance. The little kite flew hard, higher and higher, and finally reached the highest point of the sky. There, it saw beautiful clouds and the vast earth.',
                'questions': [
                    {'type': 'choice', 'question': 'What did the little kite want to do?', 'options': ['Stay on the ground', 'Fly into the sky', 'Sleep', 'Eat food'], 'answer': 'Fly into the sky'},
                    {'type': 'choice', 'question': 'What help does the little kite need?', 'options': ['Wind\'s help', 'People\'s guidance', 'All of the above', 'No help needed'], 'answer': 'All of the above'},
                    {'type': 'choice', 'question': 'What did the little kite see at the highest point of the sky?', 'options': ['Beautiful clouds', 'Vast earth', 'Beautiful scenery', 'All of the above'], 'answer': 'All of the above'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Colorful Butterfly',
                'article': 'There is a colorful butterfly in the garden. Its wings have red, yellow, blue, and green colors, as beautiful as a rainbow. The butterfly dances gracefully among the flowers, bringing infinite vitality and energy to the garden.',
                'questions': [
                    {'type': 'choice', 'question': 'What colors does the butterfly\'s wings have?', 'options': ['Only red', 'Only yellow', 'Red, yellow, blue, green', 'No color'], 'answer': 'Red, yellow, blue, green'},
                    {'type': 'choice', 'question': 'What do the butterfly\'s wings look like?', 'options': ['Stone', 'Rainbow', 'Wood', 'Water'], 'answer': 'Rainbow'},
                    {'type': 'choice', 'question': 'What does the butterfly do in the garden?', 'options': ['Sleep', 'Dance gracefully', 'Daydream', 'Eat food'], 'answer': 'Dance gracefully'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Brave Little Ant',
                'article': 'A little ant got lost and couldn\'t find his way home. He was very scared but didn\'t cry. The little ant thought calmly and finally found his way home by leaving a scent trail. This story teaches us: when facing difficulties, stay calm and think carefully.',
                'questions': [
                    {'type': 'choice', 'question': 'What problem did the little ant have?', 'options': ['Was hungry', 'Got lost', 'Was tired', 'Was sick'], 'answer': 'Got lost'},
                    {'type': 'choice', 'question': 'How did the little ant feel when he was lost?', 'options': ['Very happy', 'Very scared but didn\'t cry', 'Very angry', 'Very excited'], 'answer': 'Very scared but didn\'t cry'},
                    {'type': 'choice', 'question': 'How did the little ant find his way home?', 'options': ['Walked randomly', 'Left a scent trail', 'Asked others for help', 'Went to sleep'], 'answer': 'Left a scent trail'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Talking Flowers',
                'article': 'In a magical garden, the flowers can talk. The red rose says, "I am the most beautiful!" The yellow sunflower says, "I am the tallest!" The white jasmine says, "I am the sweetest!" Although each flower has its own special quality, they are all happy because each one is an important part of the garden.',
                'questions': [
                    {'type': 'choice', 'question': 'What can the flowers do in the magical garden?', 'options': ['Sleep', 'Talk', 'Dance', 'Fly'], 'answer': 'Talk'},
                    {'type': 'choice', 'question': 'What is the red rose known for?', 'options': ['Being the sweetest', 'Being the most beautiful', 'Being the tallest', 'Being the reddest'], 'answer': 'Being the most beautiful'},
                    {'type': 'choice', 'question': 'What is special about each flower?', 'options': ['They are all the same', 'Each has its own special quality', 'They are all ugly', 'They are all small'], 'answer': 'Each has its own special quality'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Magic Pocket',
                'article': 'Xiao Ming has a magic pocket full of wonderful things. When his friends are hungry, food appears in the pocket. When his friends are cold, clothes appear in the pocket. When his friends are sad, jokes appear in the pocket.',
                'questions': [
                    {'type': 'choice', 'question': 'What magic thing does Xiao Ming have?', 'options': ['A magic hat', 'A magic pocket', 'A magic glove', 'A magic shoe'], 'answer': 'A magic pocket'},
                    {'type': 'choice', 'question': 'What appears in the pocket when friends are hungry?', 'options': ['Water', 'Food', 'Toys', 'Books'], 'answer': 'Food'},
                    {'type': 'choice', 'question': 'What appears in the pocket when friends are sad?', 'options': ['Food', 'Clothes', 'Jokes', 'Toys'], 'answer': 'Jokes'}
                ]
            }
        ]
        
    def show_question(self):
        try:
            self.content_layout.clear_widgets()
            
            # 检查索引是否越界
            if self.current_question_index >= len(self.exercise_data):
                self.show_results()
                return
                
            # 重置状态
            self.answer_submitted = False
            self.submit_btn.disabled = False
            self.next_btn.disabled = True
            
            current_q = self.exercise_data[self.current_question_index]
            
            # 显示题目进度
            progress_text = f"题目 {self.current_question_index + 1}/{len(self.exercise_data)}"
            self.content_layout.add_widget(create_label(text=progress_text, font_size=16, bold=True))
            
            # 根据题目类型显示不同的内容
            if current_q['type'] == 'reading':
                self.show_reading_question(current_q)
            else:
                # 显示题目内容
                question_text = f"题目：{current_q['question']}"
                self.content_layout.add_widget(create_label(text=question_text, font_size=18))
                
                if current_q['type'] == 'choice':
                    self.show_choice_question(current_q)
                elif current_q['type'] == 'fill':
                    self.show_fill_question(current_q)
                elif current_q['type'] == 'first_letter':
                    self.show_first_letter_fill_question(current_q)
        except Exception as e:
            print(f"显示题目错误: {e}")
            import traceback
            traceback.print_exc()
            self.show_results()
            
    def show_choice_question(self, question_data):
        self.user_answer = None
        
        for i, option in enumerate(question_data['options']):
            # 使用默认参数捕获当前值，避免闭包问题
            option_text = option
            option_btn = create_button(
                text=f"{chr(65+i)}. {option_text}", 
                background_color=CHILD_COLORS['inactive'],
                on_press=lambda x, opt=option_text: self.select_choice_answer(opt)
            )
            self.content_layout.add_widget(option_btn)
            
    def show_fill_question(self, question_data):
        self.user_answer = ""
        
        self.answer_input = create_textinput(text="", hint_text="请输入答案", size_hint_y=None, height=50, font_size=16)
        self.content_layout.add_widget(self.answer_input)
        
        # 使用安全的回调方式
        def on_text_change(instance, value):
            try:
                self.user_answer = value.strip()
            except:
                self.user_answer = ""
            
        self.answer_input.bind(text=on_text_change)
        
    def show_reading_question(self, question_data):
        """显示阅读理解题目"""
        try:
            self.user_answer = None
            
            # 显示文章标题
            title_label = create_label(
                text=f"【{question_data['title']}】", 
                font_size=20, 
                bold=True, 
                size_hint_y=None, 
                height=50
            )
            self.content_layout.add_widget(title_label)
            
            # 显示文章内容
            article_text = question_data['article']
            # 使用文本框显示较长的文章内容
            article_label = create_label(
                text=article_text, 
                font_size=16,
                text_size=(400, None),  # 设置宽度限制，允许自动换行
                halign='left',  # 左对齐
                valign='top',   # 顶部对齐
                size_hint_y=None,
                height=300  # 增加空间给文章内容
            )
            self.content_layout.add_widget(article_label)
            
            # 添加分隔线
            separator = create_label(text="", size_hint_y=None, height=10)
            self.content_layout.add_widget(separator)
            
            # 显示子题目
            questions = question_data['questions']
            self.current_reading_questions = questions
            self.current_reading_question_index = 0
            
            # 显示当前子题目
            self.show_current_reading_question()
            
        except Exception as e:
            print(f"显示阅读理解题目错误: {e}")
            import traceback
            traceback.print_exc()
            # 如果出错，显示一个简单的错误信息
            error_label = create_label(text="题目加载失败，请查看下一题", font_size=16, color=(1, 0, 0, 1))
            self.content_layout.add_widget(error_label)
    
    def show_current_reading_question(self):
        """显示当前阅读理解的子题目"""
        try:
            if not hasattr(self, 'current_reading_questions') or self.current_reading_question_index >= len(self.current_reading_questions):
                # 所有子题目完成，隐藏下一题按钮，显示提交按钮
                if hasattr(self, 'next_btn'):
                    self.next_btn.disabled = True
                if hasattr(self, 'submit_btn'):
                    self.submit_btn.disabled = False
                return
            
            # 清理之前的子题目显示
            # 这里可能需要更精确的清理逻辑，但为了简化，我们只清理最后的部分
            
            current_sub_q = self.current_reading_questions[self.current_reading_question_index]
            
            # 显示子题目
            question_text = f"问题 {self.current_reading_question_index + 1}: {current_sub_q['question']}"
            question_label = create_label(text=question_text, font_size=16, bold=True)
            self.content_layout.add_widget(question_label)
            
            if current_sub_q['type'] == 'choice':
                self.show_reading_choice_question(current_sub_q)
            elif current_sub_q['type'] == 'fill':
                self.show_reading_fill_question(current_sub_q)
            
        except Exception as e:
            print(f"显示阅读理解子题目错误: {e}")
            import traceback
            traceback.print_exc()
    
    def show_reading_choice_question(self, question_data):
        """显示阅读理解选择题"""
        try:
            self.user_answer = None
            
            for i, option in enumerate(question_data['options']):
                option_text = option
                option_btn = create_button(
                    text=f"{chr(65+i)}. {option_text}", 
                    background_color=CHILD_COLORS['inactive'],
                    size_hint_y=None,
                    height=40,
                    on_press=lambda x, opt=option_text: self.select_reading_choice_answer(opt)
                )
                self.content_layout.add_widget(option_btn)
            
        except Exception as e:
            print(f"显示阅读理解选择题错误: {e}")
    
    def show_reading_fill_question(self, question_data):
        """显示阅读理解填空题"""
        try:
            self.answer_input = create_textinput(
                text="", 
                hint_text="请输入答案", 
                size_hint_y=None, 
                height=40, 
                font_size=16
            )
            self.content_layout.add_widget(self.answer_input)
            
            def on_text_change(instance, value):
                try:
                    self.user_answer = value.strip()
                except:
                    self.user_answer = ""
            
            self.answer_input.bind(text=on_text_change)
            
        except Exception as e:
            print(f"显示阅读理解填空题错误: {e}")
    
    def select_reading_choice_answer(self, answer):
        """选择阅读理解题目的答案"""
        try:
            self.user_answer = answer
            # 自动进入下一题
            self.next_reading_question()
        except Exception as e:
            print(f"选择阅读理解答案错误: {e}")
    
    def next_reading_question(self):
        """进入下一个阅读理解子题目"""
        try:
            # 保存当前答案
            current_sub_q = self.current_reading_questions[self.current_reading_question_index]
            if not hasattr(self, 'reading_answers'):
                self.reading_answers = []
            
            # 保存答案
            answer_data = {
                'question_index': self.current_reading_question_index,
                'question': current_sub_q,
                'user_answer': self.user_answer,
                'is_correct': self.user_answer == current_sub_q['answer']
            }
            self.reading_answers.append(answer_data)
            
            # 进入下一题
            self.current_reading_question_index += 1
            
            if self.current_reading_question_index < len(self.current_reading_questions):
                # 还有下一题
                self.show_current_reading_question()
            else:
                # 所有子题目完成
                if hasattr(self, 'next_btn'):
                    self.next_btn.disabled = True
                if hasattr(self, 'submit_btn'):
                    self.submit_btn.disabled = False
                    
                # 显示完成信息
                complete_label = create_label(
                    text="✓ 本篇文章的所有问题已完成，请点击下一题", 
                    font_size=14, 
                    color=(0, 0.6, 0, 1),
                    size_hint_y=None,
                    height=30
                )
                self.content_layout.add_widget(complete_label)
                
        except Exception as e:
            print(f"进入下一个阅读理解题目错误: {e}")

    def show_first_letter_fill_question(self, question_data):
        self.user_answer = ""
        
        # 获取答案的首字母
        first_letter = question_data['answer'][0].upper() if question_data['answer'] else ''
        
        # 显示首字母提示
        hint_layout = BoxLayout(size_hint_y=None, height=50, spacing=10, orientation='horizontal', padding=[10, 0, 10, 0])
        hint_layout.add_widget(create_label(text="首字母：", font_size=16, bold=True))
        hint_layout.add_widget(create_label(text=first_letter, font_size=24, bold=True, color=(0.8, 0.2, 0.2, 1)))
        hint_layout.add_widget(Widget(size_hint_x=None, width=20))  # 占位
        self.content_layout.add_widget(hint_layout)
        
        # 创建输入框
        self.answer_input = create_textinput(text="", hint_text="请输入剩余字母", size_hint_y=None, height=50, font_size=16)
        self.content_layout.add_widget(self.answer_input)
        
        # 使用安全的回调方式
        def on_text_change(instance, value):
            try:
                self.user_answer = first_letter.lower() + value.strip()  # 自动添加首字母
            except:
                self.user_answer = ""
            
        self.answer_input.bind(text=on_text_change)
        
    def select_choice_answer(self, answer):
        try:
            self.user_answer = answer
            
            # 更新按钮颜色
            for child in self.content_layout.children:
                if isinstance(child, Button):
                    if child.text.endswith(answer):
                        child.background_color = CHILD_COLORS['accent']
                    else:
                        child.background_color = CHILD_COLORS['inactive']
        except Exception as e:
            print(f"选择答案错误: {e}")
                    
    def submit_answer(self, instance=None):
        try:
            print(f"[DEBUG] submit_answer called, index={self.current_question_index}")
            
            # 防止重复提交
            if self.answer_submitted:
                print(f"[DEBUG] Already submitted, skipping")
                return
                
            # 检查索引是否越界
            if self.current_question_index >= len(self.exercise_data):
                print(f"[DEBUG] Index out of bounds: {self.current_question_index} >= {len(self.exercise_data)}")
                return
                
            current_q = self.exercise_data[self.current_question_index]
            
            # 处理不同类型的题目
            if current_q['type'] == 'reading':
                # 对于阅读理解题目，答案已经在过程中完成了
                # 直接保存阅读理解的答案统计
                if hasattr(self, 'reading_answers') and self.reading_answers:
                    correct_count = sum(1 for ans in self.reading_answers if ans['is_correct'])
                    total_count = len(self.reading_answers)
                    self.correct_answers += correct_count
                    
                    result_text = f"阅读理解完成！\n正确: {correct_count}/{total_count}"
                else:
                    result_text = "阅读理解完成！"
                
                # 直接添加结果标签
                result_label = Label(
                    text=result_text,
                    font_size=18,
                    bold=True,
                    size_hint_y=None,
                    height=60,
                    color=(0.1, 0.1, 0.1, 1),
                    font_name=DEFAULT_FONT,
                    text_size=(None, None),  # 允许多行显示
                    halign='center',
                    valign='middle'
                )
                
                result_label.background_color = CHILD_COLORS['success']
                self.content_layout.add_widget(result_label)
                
                # 清理阅读理解相关状态
                if hasattr(self, 'reading_answers'):
                    delattr(self, 'reading_answers')
                if hasattr(self, 'current_reading_questions'):
                    delattr(self, 'current_reading_questions')
                if hasattr(self, 'current_reading_question_index'):
                    delattr(self, 'current_reading_question_index')
                
            else:
                # 对于普通题目，检查用户答案
                if not hasattr(self, 'user_answer') or not self.user_answer:
                    print(f"[DEBUG] No user answer, user_answer={getattr(self, 'user_answer', 'NOT_SET')}")
                    return
                    
                print(f"[DEBUG] user_answer = {self.user_answer}")
                    
                correct_answer = current_q['answer'].lower().strip()
                user_answer = str(self.user_answer).lower().strip()
                
                is_correct = user_answer == correct_answer
                
                if is_correct:
                    self.correct_answers += 1
                    result_text = "正确！"
                else:
                    result_text = "错误！正确答案是：" + current_q['answer']
                    
                # 直接添加结果标签
                result_label = Label(
                    text=result_text,
                    font_size=24,
                    bold=True,
                    size_hint_y=None,
                    height=50,
                    color=(0.1, 0.1, 0.1, 1),
                    font_name=DEFAULT_FONT  # 使用中文字体
                )
                
                # 根据对错设置背景色
                if is_correct:
                    result_label.background_color = CHILD_COLORS['success']
                else:
                    result_label.background_color = CHILD_COLORS['warning']
                    
                self.content_layout.add_widget(result_label)
                
            # 更新按钮状态和提交状态
            self.submit_btn.disabled = True
            self.next_btn.disabled = False
            self.answer_submitted = True
            
            print(f"[DEBUG] Answer submitted successfully")
        except Exception as e:
            print(f"[ERROR] submit_answer错误: {e}")
            import traceback
            traceback.print_exc()
        
    def next_question(self, instance=None):
        try:
            print(f"[DEBUG] next_question called, index={self.current_question_index}")
            
            # 清理当前题目的状态
            self.user_answer = None
            self.answer_input = None
            
            self.current_question_index += 1
            self.submit_btn.disabled = False
            self.next_btn.disabled = True
            self.answer_submitted = False  # 重置提交状态
            
            print(f"[DEBUG] Moving to question {self.current_question_index}, total={len(self.exercise_data)}")
            
            if self.current_question_index < len(self.exercise_data):
                self.show_question()
            else:
                print(f"[DEBUG] All questions completed, showing results")
                self.show_results()
        except Exception as e:
            print(f"[ERROR] 下一题错误: {e}")
            import traceback
            traceback.print_exc()
            try:
                self.show_results()
            except:
                pass
            
    def show_results(self):
        try:
            self.content_layout.clear_widgets()
            
            # 计算实际题目数量
            actual_total = len(self.exercise_data)
            score_percent = (self.correct_answers / actual_total) * 100 if actual_total > 0 else 0
            
            result_title = create_label(text="练习完成！", font_size=24, bold=True)
            self.content_layout.add_widget(result_title)
            
            result_stats = create_label(text=f"总题数：{actual_total}\n正确数：{self.correct_answers}\n得分：{score_percent:.1f}分", 
                                       font_size=18)
            self.content_layout.add_widget(result_stats)
            
            # 根据得分显示鼓励话语
            if score_percent >= 90:
                encouragement = "太棒了！你的语法掌握得很好！"
            elif score_percent >= 70:
                encouragement = "不错！继续努力！"
            else:
                encouragement = "加油！多练习会更好！"
                
            encouragement_label = create_label(text=encouragement, font_size=16)
            self.content_layout.add_widget(encouragement_label)
            
            # 控制按钮
            control_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
            
            retry_btn = create_button(text="重新练习", background_color=CHILD_COLORS['accent'], 
                                     on_press=self.retry_exercise)
            back_btn = create_button(text="返回选择", background_color=CHILD_COLORS['secondary'], 
                                    on_press=self.back_to_category)
            
            control_layout.add_widget(retry_btn)
            control_layout.add_widget(back_btn)
            
            self.content_layout.add_widget(control_layout)
        except Exception as e:
            print(f"显示结果错误: {e}")
        
    def retry_exercise(self, instance=None):
        # 重新开始当前练习
        self.current_question_index = 0
        self.correct_answers = 0
        self.answer_submitted = False
        self.show_question()
        
    def back_to_category(self, instance=None):
        # 返回分类选择
        self.category_layout.opacity = 1
        self.category_layout.disabled = False
        
        self.question_layout.opacity = 0
        self.question_layout.disabled = True
        
        self.progress_label.text = "语法专项练习"


# 阅读理解屏幕
class ReadingScreen(Screen):
    def __init__(self, **kwargs):
        super(ReadingScreen, self).__init__(**kwargs)
        self.current_question_index = 0
        self.total_questions = 5
        self.correct_answers = 0
        self.exercise_data = []
        self.answer_submitted = False
        self.current_reading_questions = []
        self.current_reading_question_index = 0
        self.reading_answers = []
        self.build_ui()
    
    def build_ui(self):
        # 添加可爱背景
        self.add_cute_background()
        
        # 主布局
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 顶部导航栏
        top_bar = BoxLayout(size_hint_y=None, height=50, spacing=10)
        back_btn = create_button(text="< 返回", on_press=self.go_back)
        top_bar.add_widget(back_btn)
        
        self.progress_label = create_label(text="阅读理解", font_size=18, bold=True)
        top_bar.add_widget(self.progress_label)
        
        layout.add_widget(top_bar)
        
        # 内容区域
        self.content_layout = BoxLayout(orientation='vertical', spacing=10)
        
        # 进度信息
        self.info_label = create_label(text="", font_size=14, size_hint_y=None, height=30)
        self.content_layout.add_widget(self.info_label)
        
        layout.add_widget(self.content_layout)
        
        # 控制按钮区域
        control_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        
        self.submit_btn = create_button(text="提交答案", background_color=CHILD_COLORS['primary'], 
                                       on_press=self.submit_answer)
        self.next_btn = create_button(text="下一题", background_color=CHILD_COLORS['accent'], 
                                     on_press=self.next_question)
        
        control_layout.add_widget(self.submit_btn)
        control_layout.add_widget(self.next_btn)
        
        layout.add_widget(control_layout)
        
        self.add_widget(layout)
        
        # 初始状态
        self.next_btn.disabled = True
        self.load_questions()
        self.show_question()
    
    def add_cute_background(self):
        from random import randint
        
        bg_layout = BoxLayout()
        bg_layout.bind(pos=self.update_canvas, size=self.update_canvas)
        
        with bg_layout.canvas:
            Color(1.0, 0.95, 0.6, 1)
            Rectangle(pos=(0, 0), size=self.size)
            
            colors = [
                (1.0, 0.75, 0.3, 0.2),
                (0.3, 0.85, 0.65, 0.2),
                (0.35, 0.75, 1.0, 0.2),
                (1.0, 0.5, 0.5, 0.18),
                (0.9, 0.7, 0.95, 0.18),
                (0.4, 0.9, 0.9, 0.15),
                (1.0, 0.8, 0.6, 0.15),
            ]
            
            left_positions = [
                (50, 400, 180, 180),
                (self.width * 0.15 if self.width > 0 else 120, 100, 140, 140),
                (80, 600, 120, 120),
                (30, 200, 100, 100),
            ]
            
            for i, (x, y, w, h) in enumerate(left_positions):
                Color(*colors[i % len(colors)])
                RoundedRectangle(pos=(x, y), size=(w, h), radius=[50])
            
            right_positions = [
                (self.width - 200 if self.width > 0 else 600, 450, 200, 200),
                (self.width - 150 if self.width > 0 else 650, 200, 150, 150),
                (self.width - 280 if self.width > 0 else 520, 650, 180, 180),
                (self.width - 100 if self.width > 0 else 700, 550, 120, 120),
            ]
            
            for i, (x, y, w, h) in enumerate(right_positions):
                Color(*colors[(i + 2) % len(colors)])
                RoundedRectangle(pos=(x, y), size=(w, h), radius=[40])
    
    def update_canvas(self, instance, value):
        pass
    
    def go_back(self, instance=None):
        self.manager.current = 'main'
    
    def load_questions(self):
        """加载阅读理解题目"""
        self.exercise_data = self.get_reading_questions()
        
        # 打乱题目顺序
        import random
        random.shuffle(self.exercise_data)
        
        # 选择指定数量的题目
        self.exercise_data = self.exercise_data[:self.total_questions]
        
        print(f"加载了 {len(self.exercise_data)} 道阅读理解题目")
    
    def get_reading_questions(self):
        """获取阅读理解题库 - 50篇适合小学生的英语文章"""
        return [
            {
                'type': 'reading',
                'title': 'My Cat Mimi',
                'article': 'I have a cat named Mimi. She is white and black. Mimi likes to sleep in the sun and drink milk. Every morning, she wakes me up by meowing loudly. Mimi is very playful and loves to chase butterflies in the garden.',
                'questions': [
                    {'type': 'choice', 'question': 'What is the name of the cat?', 'options': ['Mimi', 'Fluffy', 'Snow', 'Shadow'], 'answer': 'Mimi'},
                    {'type': 'choice', 'question': 'What color is Mimi?', 'options': ['All white', 'All black', 'White and black', 'Brown and white'], 'answer': 'White and black'},
                    {'type': 'choice', 'question': 'What does Mimi like to chase?', 'options': ['Birds', 'Butterflies', 'Fish', 'Other cats'], 'answer': 'Butterflies'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Birthday Party',
                'article': 'Today is Tom\'s birthday. His friends come to his house for a party. They bring gifts and balloons. Tom\'s mom bakes a big chocolate cake. Everyone sings happy birthday and eats cake together. Tom feels very happy.',
                'questions': [
                    {'type': 'choice', 'question': 'Who has a birthday today?', 'options': ['Mike', 'Tom', 'John', 'David'], 'answer': 'Tom'},
                    {'type': 'choice', 'question': 'What kind of cake does Tom\'s mom bake?', 'options': ['Vanilla cake', 'Chocolate cake', 'Strawberry cake', 'Carrot cake'], 'answer': 'Chocolate cake'},
                    {'type': 'choice', 'question': 'How does Tom feel at the party?', 'options': ['Sad', 'Angry', 'Happy', 'Scared'], 'answer': 'Happy'}
                ]
            },
            {
                'type': 'reading',
                'title': 'At the Park',
                'article': 'The park is full of children today. Some are playing on the swings, others are sliding down the slide. Sarah and her brother are flying a red kite. The trees are green and there are colorful flowers everywhere.',
                'questions': [
                    {'type': 'choice', 'question': 'What are some children playing on?', 'options': ['Bikes', 'Swings and slides', 'Skateboards', 'Balls'], 'answer': 'Swings and slides'},
                    {'type': 'choice', 'question': 'What color is the kite?', 'options': ['Blue', 'Green', 'Red', 'Yellow'], 'answer': 'Red'},
                    {'type': 'choice', 'question': 'What color are the trees?', 'options': ['Brown', 'Yellow', 'Green', 'Red'], 'answer': 'Green'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Busy Bee',
                'article': 'A little bee flies from flower to flower all day long. It collects sweet nectar to make honey. The bee is very busy and never stops working. Flowers depend on bees to carry pollen from one flower to another.',
                'questions': [
                    {'type': 'choice', 'question': 'What does the bee collect from flowers?', 'options': ['Water', 'Nectar', 'Leaves', 'Dirt'], 'answer': 'Nectar'},
                    {'type': 'choice', 'question': 'What does the bee make from nectar?', 'options': ['Wax', 'Honey', 'Butter', 'Jam'], 'answer': 'Honey'},
                    {'type': 'choice', 'question': 'How would you describe the bee?', 'options': ['Lazy', 'Busy', 'Sleepy', 'Sad'], 'answer': 'Busy'}
                ]
            },
            {
                'type': 'reading',
                'title': 'Rainy Day',
                'article': 'It is raining outside. Raindrops fall on the windows and roofs. Tom cannot play in the garden, so he stays inside. He reads books and draws pictures. When the rain stops, Tom will go outside to jump in the puddles.',
                'questions': [
                    {'type': 'choice', 'question': 'What is the weather like?', 'options': ['Sunny', 'Cloudy', 'Rainy', 'Snowy'], 'answer': 'Rainy'},
                    {'type': 'choice', 'question': 'What does Tom do inside?', 'options': ['Sleeps', 'Reads and draws', 'Cooks', 'Cleans'], 'answer': 'Reads and draws'},
                    {'type': 'choice', 'question': 'What will Tom do when the rain stops?', 'options': ['Go to school', 'Jump in puddles', 'Take a nap', 'Call friends'], 'answer': 'Jump in puddles'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Little Fish',
                'article': 'In a clear blue pond, a little fish swims with his family. The fish is small and silver with bright blue stripes. He likes to play hide-and-seek among the water plants. When danger comes, he quickly hides behind a big rock.',
                'questions': [
                    {'type': 'choice', 'question': 'Where does the little fish live?', 'options': ['Ocean', 'River', 'Pond', 'Lake'], 'answer': 'Pond'},
                    {'type': 'choice', 'question': 'What color are the fish\'s stripes?', 'options': ['Red', 'Green', 'Blue', 'Yellow'], 'answer': 'Blue'},
                    {'type': 'choice', 'question': 'Where does the fish hide when there is danger?', 'options': ['In the plants', 'Behind a rock', 'Under a log', 'In a cave'], 'answer': 'Behind a rock'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The School Bus',
                'article': 'Every morning, Amy waits at the bus stop with her backpack. The yellow school bus arrives at 7:30 AM. Amy climbs aboard and sits by the window. The bus driver greets all the children with a smile. On the way to school, Amy looks at the passing trees and houses.',
                'questions': [
                    {'type': 'choice', 'question': 'What time does the school bus arrive?', 'options': ['7:00 AM', '7:30 AM', '8:00 AM', '8:30 AM'], 'answer': '7:30 AM'},
                    {'type': 'choice', 'question': 'What color is the school bus?', 'options': ['Blue', 'Green', 'Yellow', 'Red'], 'answer': 'Yellow'},
                    {'type': 'choice', 'question': 'Where does Amy sit on the bus?', 'options': ['In the front', 'By the window', 'In the back', 'Standing'], 'answer': 'By the window'}
                ]
            },
            {
                'type': 'reading',
                'title': 'A Day at the Beach',
                'article': 'Jenny and her family go to the beach on Saturday. The sun shines brightly and the waves are small. Jenny builds a sandcastle with her bucket and shovel. She also collects pretty shells and colorful sea glass. At lunchtime, they eat sandwiches and drink cold juice.',
                'questions': [
                    {'type': 'choice', 'question': 'When do they go to the beach?', 'options': ['Sunday', 'Friday', 'Saturday', 'Monday'], 'answer': 'Saturday'},
                    {'type': 'choice', 'question': 'What does Jenny build with her tools?', 'options': ['A boat', 'A sandcastle', 'A house', 'A flower'], 'answer': 'A sandcastle'},
                    {'type': 'choice', 'question': 'What do they drink at lunch?', 'options': ['Milk', 'Water', 'Cold juice', 'Tea'], 'answer': 'Cold juice'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Library',
                'article': 'The town library is a quiet place full of books. Mrs. Johnson works there as a librarian. Children come to borrow books about animals, space, and adventure stories. The library also has computers where kids can play educational games.',
                'questions': [
                    {'type': 'choice', 'question': 'What is a librarian?', 'options': ['A doctor', 'A teacher', 'A library worker', 'A writer'], 'answer': 'A library worker'},
                    {'type': 'choice', 'question': 'What can you find in the library?', 'options': ['Toys', 'Food', 'Books', 'Animals'], 'answer': 'Books'},
                    {'type': 'choice', 'question': 'What do children play on the library computers?', 'options': ['Shooting games', 'Racing games', 'Educational games', 'Fighting games'], 'answer': 'Educational games'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Hungry Rabbit',
                'article': 'A white rabbit lives in a burrow near the carrot field. Every morning, he hops out to look for food. Today, he is very hungry and finds a big orange carrot. He munches it happily and feels much better. The rabbit thanks the farmer for growing such delicious carrots.',
                'questions': [
                    {'type': 'choice', 'question': 'What color is the rabbit?', 'options': ['Brown', 'Gray', 'White', 'Black'], 'answer': 'White'},
                    {'type': 'choice', 'question': 'Where does the rabbit live?', 'options': ['In a tree', 'In a burrow', 'In a house', 'In a cave'], 'answer': 'In a burrow'},
                    {'type': 'choice', 'question': 'What does the rabbit eat?', 'options': ['Grass', 'Carrots', 'Leaves', 'Berries'], 'answer': 'Carrots'}
                ]
            },
            {
                'type': 'reading',
                'title': 'Little Red Riding Hood',
                'article': 'Once upon a time, there was a little girl that everyone called Little Red Riding Hood. One day, her mother asked Little Red Riding Hood to take some snacks to her grandmother. On the way, Little Red Riding Hood met a big bad wolf. The wolf pretended to be her friend and tricked her into going somewhere else.',
                'questions': [
                    {'type': 'choice', 'question': 'What do people call the little girl?', 'options': ['Little Yellow Hood', 'Little Red Riding Hood', 'Little Blue Hood', 'Little Green Hood'], 'answer': 'Little Red Riding Hood'},
                    {'type': 'choice', 'question': 'What did her mother ask Little Red Riding Hood to do?', 'options': ['Go to school', 'Take snacks to grandmother', 'Go play', 'Go shopping'], 'answer': 'Take snacks to grandmother'},
                    {'type': 'choice', 'question': 'Who did Little Red Riding Hood meet on the road?', 'options': ['Little white rabbit', 'Big bad wolf', 'Little dog', 'Little cat'], 'answer': 'Big bad wolf'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Tortoise and the Hare',
                'article': 'The rabbit and the tortoise decided to have a race. The rabbit ran very fast, while the tortoise moved very slowly. The rabbit thought he was running too fast, so he stopped to rest. Although the tortoise moved slowly, he didn\'t stop to rest and kept moving forward. In the end, the tortoise won the race.',
                'questions': [
                    {'type': 'choice', 'question': 'What were the rabbit and tortoise doing?', 'options': ['Playing a game', 'Having a race', 'Chatting', 'Eating food'], 'answer': 'Having a race'},
                    {'type': 'choice', 'question': 'Why did the rabbit stop to rest?', 'options': ['He was tired', 'He thought he was running too fast', 'He got lost', 'He wanted to see the scenery'], 'answer': 'He thought he was running too fast'},
                    {'type': 'choice', 'question': 'Who won the race?', 'options': ['Rabbit', 'Tortoise', 'It was a tie', 'No winner'], 'answer': 'Tortoise'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Three Little Pigs',
                'article': 'Three little pigs wanted to build houses. The first little pig used straw to build his house, the second little pig used wood to build his house, and the third little pig used bricks to build his house. When the big bad wolf came, the straw house and the wooden house were blown down, but the brick house was not blown down.',
                'questions': [
                    {'type': 'choice', 'question': 'How many little pigs were there?', 'options': ['One', 'Two', 'Three', 'Four'], 'answer': 'Three'},
                    {'type': 'choice', 'question': 'What did the second little pig use to build his house?', 'options': ['Straw', 'Wood', 'Bricks', 'Stone'], 'answer': 'Wood'},
                    {'type': 'choice', 'question': 'Which house was not blown down?', 'options': ['The straw house', 'The wooden house', 'The brick house', 'The grass house'], 'answer': 'The brick house'}
                ]
            },
            {
                'type': 'reading',
                'title': 'Spring Garden',
                'article': 'Spring has arrived, and the garden is full of beautiful flowers. There are red roses, yellow sunflowers, purple lavender, and pink cherry blossoms. Butterflies dance among the flowers, and bees collect honey. Children play in the garden and are very happy.',
                'questions': [
                    {'type': 'choice', 'question': 'What can be found in the garden?', 'options': ['Fruits', 'Vegetables', 'Beautiful flowers', 'Trees'], 'answer': 'Beautiful flowers'},
                    {'type': 'choice', 'question': 'What color are the sunflowers?', 'options': ['Red', 'Yellow', 'Purple', 'Pink'], 'answer': 'Yellow'},
                    {'type': 'choice', 'question': 'What are the children doing?', 'options': ['Sleeping', 'Studying', 'Playing', 'Working'], 'answer': 'Playing'}
                ]
            },
            {
                'type': 'reading',
                'title': 'Rainbow After the Rain',
                'article': 'It rained, and after the rain stopped, a beautiful rainbow appeared in the sky. The rainbow has seven colors: red, orange, yellow, green, blue, indigo, and violet. Xiao Ming and his mother looked at the rainbow together, and his mother told him how rainbows are formed. Xiao Ming thought it was magical and wanted to touch the rainbow.',
                'questions': [
                    {'type': 'choice', 'question': 'When does a rainbow appear in the sky?', 'options': ['During rain', 'After rain stops', 'When sunny', 'When cloudy'], 'answer': 'After rain stops'},
                    {'type': 'choice', 'question': 'How many colors does the rainbow have?', 'options': ['Five', 'Six', 'Seven', 'Eight'], 'answer': 'Seven'},
                    {'type': 'choice', 'question': 'What did Xiao Ming want to do?', 'options': ['Draw the rainbow', 'Touch the rainbow', 'Count the rainbow colors', 'Talk to the rainbow'], 'answer': 'Touch the rainbow'}
                ]
            },
            {
                'type': 'reading',
                'title': 'Little Squirrel Prepares for Winter',
                'article': 'Winter is coming, so the little squirrel starts preparing for winter. He collects many pine cones and hides them in tree holes. When snowflakes fall, the little squirrel eats pine cones in the warm tree hole and safely spends the cold winter.',
                'questions': [
                    {'type': 'choice', 'question': 'When does the little squirrel start preparing for winter?', 'options': ['Spring', 'Summer', 'Autumn', 'Winter'], 'answer': 'Autumn'},
                    {'type': 'choice', 'question': 'What did the little squirrel collect?', 'options': ['Fruits', 'Pine cones', 'Nuts', 'Flowers'], 'answer': 'Pine cones'},
                    {'type': 'choice', 'question': 'Where did the little squirrel hide the pine cones?', 'options': ['Underground', 'In tree holes', 'In the house', 'In the grass'], 'answer': 'In tree holes'}
                ]
            },
            {
                'type': 'reading',
                'title': 'Xiao Ming\'s Day',
                'article': 'Xiao Ming is a wonderful child. In the morning, he gets up, brushes his teeth and washes his face, then has breakfast. On the way to school, he sees an injured bird and takes it to the animal hospital. After school, Xiao Ming goes home, does homework, and then plays football with his father.',
                'questions': [
                    {'type': 'choice', 'question': 'What did Xiao Ming do in the morning?', 'options': ['Slept', 'Brushed teeth, washed face, and had breakfast', 'Watched TV', 'Played'], 'answer': 'Brushed teeth, washed face, and had breakfast'},
                    {'type': 'choice', 'question': 'What did Xiao Ming do on the way to school?', 'options': ['Bought school supplies', 'Took an injured bird to the hospital', 'Ate snacks', 'Met classmates'], 'answer': 'Took an injured bird to the hospital'},
                    {'type': 'choice', 'question': 'What did Xiao Ming do after school?', 'options': ['Went straight home', 'Did homework then played football', 'Went to the library', 'Helped mom with housework'], 'answer': 'Did homework then played football'}
                ]
            },
            {
                'type': 'reading',
                'title': 'The Cat\'s Tail',
                'article': 'Little cat Mimi has a long tail. The tail tells people about her mood. When she is happy, her tail stands up high; when she is angry, her tail droops down; when she is scared, her tail becomes fluffy. Mimi communicates with humans using her unique tail.',
                'questions': [
                    {'type': 'choice', 'question': 'What does Mimi have?', 'options': ['Long ears', 'A long tail', 'Long legs', 'A long nose'], 'answer': 'A long tail'},
                    {'type': 'choice', 'question': 'What does Mimi\'s tail do when she is happy?', 'options': ['Droops down', 'Stands up high', 'Becomes fluffy', 'Wags'], 'answer': 'Stands up high'},
                    {'type': 'choice', 'question': 'What does Mimi use to communicate with humans?', 'options': ['Meowing', 'Eyes', 'Tail', 'Paws'], 'answer': 'Tail'}
                ]
            }
        ]
    
    def show_question(self):
        """显示当前题目"""
        try:
            # 清理之前的内容
            self.content_layout.clear_widgets()
            
            if self.current_question_index >= len(self.exercise_data):
                self.show_result()
                return
            
            # 显示进度信息
            progress_text = f"题目 {self.current_question_index + 1}/{len(self.exercise_data)}"
            self.info_label.text = progress_text
            self.content_layout.add_widget(self.info_label)
            
            # 显示当前题目
            current_q = self.exercise_data[self.current_question_index]
            
            if current_q['type'] == 'reading':
                self.show_reading_question(current_q)
            else:
                # 对于其他类型（如果有的话）
                question_label = create_label(text=current_q['question'], font_size=18, size_hint_y=None, height=50)
                self.content_layout.add_widget(question_label)
            
        except Exception as e:
            print(f"显示题目错误: {e}")
            import traceback
            traceback.print_exc()
    
    def show_reading_question(self, question_data):
        """显示阅读理解题目"""
        try:
            # 显示文章标题
            title_label = create_label(
                text=f"【{question_data['title']}】", 
                font_size=20, 
                bold=True, 
                size_hint_y=None, 
                height=50
            )
            self.content_layout.add_widget(title_label)
            
            # 显示文章内容
            article_text = question_data['article']
            article_label = create_label(
                text=article_text, 
                font_size=16,
                text_size=(400, None),  # 设置宽度限制，允许自动换行
                halign='left',  # 左对齐
                valign='top',   # 顶部对齐
                size_hint_y=None,
                height=300  # 增加空间给文章内容
            )
            self.content_layout.add_widget(article_label)
            
            # 添加分隔线
            separator = create_label(text="", size_hint_y=None, height=10)
            self.content_layout.add_widget(separator)
            
            # 显示子题目
            questions = question_data['questions']
            self.current_reading_questions = questions
            self.current_reading_question_index = 0
            
            # 显示当前子题目
            self.show_current_reading_question()
            
        except Exception as e:
            print(f"显示阅读理解题目错误: {e}")
            import traceback
            traceback.print_exc()
    
    def show_current_reading_question(self):
        """显示当前阅读理解的子题目"""
        try:
            if not hasattr(self, 'current_reading_questions') or self.current_reading_question_index >= len(self.current_reading_questions):
                # 所有子题目完成，隐藏下一题按钮，显示提交按钮
                if hasattr(self, 'next_btn'):
                    self.next_btn.disabled = True
                if hasattr(self, 'submit_btn'):
                    self.submit_btn.disabled = False
                return
            
            # 清理之前的子题目显示
            # 这里可能需要更精确的清理逻辑，但为了简化，我们只清理最后的部分
            
            current_sub_q = self.current_reading_questions[self.current_reading_question_index]
            
            # 显示子题目
            question_text = f"问题 {self.current_reading_question_index + 1}: {current_sub_q['question']}"
            question_label = create_label(text=question_text, font_size=16, bold=True)
            self.content_layout.add_widget(question_label)
            
            if current_sub_q['type'] == 'choice':
                self.show_reading_choice_question(current_sub_q)
            elif current_sub_q['type'] == 'fill':
                self.show_reading_fill_question(current_sub_q)
            
        except Exception as e:
            print(f"显示阅读理解子题目错误: {e}")
            import traceback
            traceback.print_exc()
    
    def show_reading_choice_question(self, question_data):
        """显示阅读理解选择题"""
        try:
            self.user_answer = None
            
            for i, option in enumerate(question_data['options']):
                option_text = option
                option_btn = create_button(
                    text=f"{chr(65+i)}. {option_text}", 
                    background_color=CHILD_COLORS['inactive'],
                    size_hint_y=None,
                    height=40,
                    on_press=lambda x, opt=option_text: self.select_reading_choice_answer(opt)
                )
                self.content_layout.add_widget(option_btn)
            
        except Exception as e:
            print(f"显示阅读理解选择题错误: {e}")
    
    def show_reading_fill_question(self, question_data):
        """显示阅读理解填空题"""
        try:
            self.answer_input = create_textinput(
                text="", 
                hint_text="请输入答案", 
                size_hint_y=None, 
                height=40, 
                font_size=16
            )
            self.content_layout.add_widget(self.answer_input)
            
            def on_text_change(instance, value):
                try:
                    self.user_answer = value.strip()
                except:
                    self.user_answer = ""
            
            self.answer_input.bind(text=on_text_change)
            
        except Exception as e:
            print(f"显示阅读理解填空题错误: {e}")
    
    def select_reading_choice_answer(self, answer):
        """选择阅读理解题目的答案"""
        try:
            self.user_answer = answer
            # 自动进入下一题
            self.next_reading_question()
        except Exception as e:
            print(f"选择阅读理解答案错误: {e}")
    
    def next_reading_question(self):
        """进入下一个阅读理解子题目"""
        try:
            # 保存当前答案
            current_sub_q = self.current_reading_questions[self.current_reading_question_index]
            if not hasattr(self, 'reading_answers'):
                self.reading_answers = []
            
            # 保存答案
            answer_data = {
                'question_index': self.current_reading_question_index,
                'question': current_sub_q,
                'user_answer': self.user_answer,
                'is_correct': self.user_answer == current_sub_q['answer']
            }
            self.reading_answers.append(answer_data)
            
            # 进入下一题
            self.current_reading_question_index += 1
            
            if self.current_reading_question_index < len(self.current_reading_questions):
                # 清理当前子题目显示，然后显示下一个
                self.show_current_reading_question()
            else:
                # 当前文章的所有题目完成，禁用下一题按钮
                if hasattr(self, 'next_btn'):
                    self.next_btn.disabled = True
                if hasattr(self, 'submit_btn'):
                    self.submit_btn.disabled = False
            
        except Exception as e:
            print(f"下一题错误: {e}")
            import traceback
            traceback.print_exc()
    
    def submit_answer(self, instance=None):
        """提交答案"""
        try:
            # 对于阅读理解题目，答案已经在过程中完成了
            # 直接保存阅读理解的答案统计
            if hasattr(self, 'reading_answers') and self.reading_answers:
                correct_count = sum(1 for ans in self.reading_answers if ans['is_correct'])
                total_count = len(self.reading_answers)
                self.correct_answers += correct_count
                
                result_text = f"阅读理解完成！\n正确: {correct_count}/{total_count}"
            else:
                result_text = "阅读理解完成！"
            
            # 直接添加结果标签
            result_label = create_label(
                text=result_text,
                font_size=18,
                bold=True,
                size_hint_y=None,
                height=60,
                color=(0.1, 0.1, 0.1, 1)
            )
            
            result_label.background_color = CHILD_COLORS['success']
            self.content_layout.add_widget(result_label)
            
            # 清理阅读理解相关状态
            if hasattr(self, 'reading_answers'):
                delattr(self, 'reading_answers')
            if hasattr(self, 'current_reading_questions'):
                delattr(self, 'current_reading_questions')
            if hasattr(self, 'current_reading_question_index'):
                delattr(self, 'current_reading_question_index')
            
            # 更新按钮状态和提交状态
            self.submit_btn.disabled = True
            self.next_btn.disabled = False
            self.answer_submitted = True
            
        except Exception as e:
            print(f"提交答案错误: {e}")
            import traceback
            traceback.print_exc()
    
    def next_question(self, instance=None):
        """进入下一题"""
        try:
            self.current_question_index += 1
            self.answer_submitted = False
            
            # 重置按钮状态
            self.submit_btn.disabled = False
            self.next_btn.disabled = True
            
            # 显示下一题
            self.show_question()
            
        except Exception as e:
            print(f"下一题错误: {e}")
            import traceback
            traceback.print_exc()
    
    def show_result(self):
        """显示结果"""
        try:
            # 清理内容区域
            self.content_layout.clear_widgets()
            
            # 计算得分
            total_questions = len(self.exercise_data)
            if total_questions > 0:
                score_percent = (self.correct_answers / total_questions) * 100
            else:
                score_percent = 0
            
            # 显示结果
            result_title = create_label(text="测试完成！", font_size=24, bold=True, size_hint_y=None, height=50)
            self.content_layout.add_widget(result_title)
            
            # 详细统计
            result_stats = create_label(text=f"总题数：{total_questions}\n正确数：{self.correct_answers}\n得分：{score_percent:.1f}分", 
                                       font_size=18)
            self.content_layout.add_widget(result_stats)
            
            # 根据得分显示鼓励话语
            if score_percent >= 90:
                encouragement = "太棒了！你的阅读理解能力很强！"
            elif score_percent >= 70:
                encouragement = "不错！继续努力！"
            else:
                encouragement = "加油！多读多练会更好！"
                
            encouragement_label = create_label(text=encouragement, font_size=16)
            self.content_layout.add_widget(encouragement_label)
            
            # 控制按钮
            control_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
            
            retry_btn = create_button(text="重新练习", background_color=CHILD_COLORS['accent'], 
                                     on_press=self.retry_exercise)
            back_btn = create_button(text="返回选择", background_color=CHILD_COLORS['secondary'], 
                                    on_press=self.back_to_main)
            
            control_layout.add_widget(retry_btn)
            control_layout.add_widget(back_btn)
            
            self.content_layout.add_widget(control_layout)
        except Exception as e:
            print(f"显示结果错误: {e}")
        
    def retry_exercise(self, instance=None):
        """重新开始练习"""
        self.current_question_index = 0
        self.correct_answers = 0
        self.answer_submitted = False
        self.load_questions()
        self.show_question()
    
    def back_to_main(self, instance=None):
        """返回主页面"""
        self.manager.current = 'main'


# 译林版四年级英语词汇表数据
VOCABULARY_DATA = {
    'unit1': {
        'title': 'Unit 1: Subjects',
        'words': [
            {'chinese': '学科，科目', 'english': 'subject', 'phonetic': '/ˈsʌbdʒɪkt/'},
            {'chinese': '语文（课）；中国的', 'english': 'Chinese', 'phonetic': '/ˌtʃaɪˈniːz/'},
            {'chinese': '英语（课）；英语的', 'english': 'English', 'phonetic': '/ˈɪŋɡlɪʃ/'},
            {'chinese': '数学（课）', 'english': 'Maths', 'phonetic': '/mæθs/'},
            {'chinese': '体育（课）', 'english': 'PE', 'phonetic': '/ˌpiː ˈiː/'},
            {'chinese': '美术（课）', 'english': 'Art', 'phonetic': '/ɑːt/（英）/ɑːrt/（美）'},
            {'chinese': '科学（课）', 'english': 'science', 'phonetic': '/ˈsaɪəns/'},
            {'chinese': '信息科技（课）', 'english': 'IT', 'phonetic': '/ˌaɪ ˈtiː/'},
            {'chinese': '音乐（课）', 'english': 'Music', 'phonetic': '/ˈmjuːzɪk/'},
            {'chinese': '劳动（课）', 'english': 'Labour', 'phonetic': '/ˈleɪbə(r)/（英）/ˈleɪbər/（美）'},
            {'chinese': '最，最高程度地', 'english': 'best', 'phonetic': '/best/'},
            {'chinese': '也', 'english': 'also', 'phonetic': '/ˈɔːlsəʊ/（英）/ˈɔːlsoʊ/（美）'},
            {'chinese': '是......的时候了。', 'english': "It's time for ...", 'phonetic': '/ɪts taɪm fɔː(r) .../（英）/ɪts taɪm fɔːr .../（美）'},
            {'chinese': '鼠标；老鼠', 'english': 'mouse', 'phonetic': '/maʊs/'},
            {'chinese': '欢迎回到......', 'english': 'Welcome back to ...', 'phonetic': '/ˈwelkəm bæk tuː .../'},
            {'chinese': '擅长', 'english': 'be good at', 'phonetic': '/bi ɡʊd æt/'},
            {'chinese': '有趣的，有吸引力的', 'english': 'interesting', 'phonetic': '/ˈɪntrəstɪŋ/'},
            {'chinese': '学习', 'english': 'learn about', 'phonetic': '/lɜːn əˈbaʊt/（英）/lɜːrn əˈbaʊt/（美）'},
            {'chinese': '文化，文明', 'english': 'culture', 'phonetic': '/ˈkʌltʃə(r)/（英）/ˈkʌltʃər/（美）'},
            {'chinese': '阅读', 'english': 'read', 'phonetic': '/riːd/'},
            {'chinese': '故事', 'english': 'story', 'phonetic': '/ˈstɔːri/（英）/ˈstɔːri/（美）'},
            {'chinese': '全部，都', 'english': 'all', 'phonetic': '/ɔːl/'},
            {'chinese': '操场，运动场', 'english': 'sports ground', 'phonetic': '/ˈspɔːrts ɡraʊnd/（英）/ˈspɔːrts ɡraʊnd/（美）'}
        ]
    },
    'unit2': {
        'title': 'Unit 2: Daily Activities',
        'words': [
            {'chinese': '一天，一日', 'english': 'day', 'phonetic': '/deɪ/'},
            {'chinese': '起床', 'english': 'get up', 'phonetic': '/ɡet ʌp/'},
            {'chinese': '洗', 'english': 'wash', 'phonetic': '/wɒʃ/（英）/wɑːʃ/（美）'},
            {'chinese': '脸，面孔', 'english': 'face', 'phonetic': '/feɪs/'},
            {'chinese': '上课', 'english': 'have lessons', 'phonetic': '/hæv ˈlesnz/'},
            {'chinese': '吃', 'english': 'have', 'phonetic': '/hæv/'},
            {'chinese': '正餐（常指晚餐）', 'english': 'dinner', 'phonetic': '/ˈdɪnə(r)/（英）/ˈdɪnər/（美）'},
            {'chinese': '早餐，早饭', 'english': 'breakfast', 'phonetic': '/ˈbrekfəst/'},
            {'chinese': '午餐，午饭', 'english': 'lunch', 'phonetic': '/lʌntʃ/'},
            {'chinese': '上床睡觉', 'english': 'go to bed', 'phonetic': '/ɡəʊ tuː bed/（英）/ɡoʊ tuː bed/（美）'},
            {'chinese': '（表示整点）...... 点钟', 'english': "o'clock", 'phonetic': '/əˈklɒk/（英）/əˈklɑːk/（美）'},
            {'chinese': '早的，早', 'english': 'early', 'phonetic': '/ˈɜːli/（英）/ˈɜːrli/（美）'},
            {'chinese': '三十', 'english': 'thirty', 'phonetic': '/ˈθɜːti/（英）/ˈθɜːrti/（美）'},
            {'chinese': '首先，第一', 'english': 'first', 'phonetic': '/fɜːst/（英）/fɜːrst/（美）'},
            {'chinese': '快点', 'english': 'hurry up', 'phonetic': '/ˈhʌri ʌp/'},
            {'chinese': '几点了？', 'english': 'What time is it?', 'phonetic': '/wɒt taɪm ɪz ɪt/（英）/wɑːt taɪm ɪz ɪt/（美）'},
            {'chinese': '我来了', 'english': "I'm coming", 'phonetic': '/aɪm ˈkʌmɪŋ/'},
            {'chinese': '二十', 'english': 'twenty', 'phonetic': '/ˈtwenti/'},
            {'chinese': '赶快！加把劲！', 'english': 'Come on!', 'phonetic': '/kʌm ɒn/（英）/kʌm ɑːn/（美）'},
            {'chinese': '课，上课', 'english': 'class', 'phonetic': '/klɑːs/（英）/klæs/（美）'},
            {'chinese': '十一', 'english': 'eleven', 'phonetic': '/ɪˈlevn/'},
            {'chinese': '体育运动', 'english': 'sport', 'phonetic': '/spɔːt/（英）/spɔːrt/（美）'},
            {'chinese': '十五', 'english': 'fifteen', 'phonetic': '/ˌfɪfˈtiːn/'},
            {'chinese': '床', 'english': 'bed', 'phonetic': '/bed/'},
            {'chinese': '晚安', 'english': 'Good night!', 'phonetic': '/ɡʊd naɪt/'}
        ]
    },
    'unit3': {
        'title': 'Unit 3: Weekly Schedule',
        'words': [
            {'chinese': '周，星期', 'english': 'week', 'phonetic': '/wiːk/'},
            {'chinese': '星期一', 'english': 'Monday', 'phonetic': '/ˈmʌndeɪ/'},
            {'chinese': '星期二', 'english': 'Tuesday', 'phonetic': '/ˈtjuːzdeɪ/（英）/ˈtuːzdeɪ/（美）'},
            {'chinese': '星期三', 'english': 'Wednesday', 'phonetic': '/ˈwenzdeɪ/'},
            {'chinese': '星期四', 'english': 'Thursday', 'phonetic': '/ˈθɜːzdeɪ/（英）/ˈθɜːrzdeɪ/（美）'},
            {'chinese': '星期五', 'english': 'Friday', 'phonetic': '/ˈfraɪdeɪ/'},
            {'chinese': '星期六', 'english': 'Saturday', 'phonetic': '/ˈsætədeɪ/（英）/ˈsætərdeɪ/（美）'},
            {'chinese': '星期天', 'english': 'Sunday', 'phonetic': '/ˈsʌndeɪ/'},
            {'chinese': '什么时候', 'english': 'when', 'phonetic': '/wen/'},
            {'chinese': '每一个，每个', 'english': 'every', 'phonetic': '/ˈevri/'},
            {'chinese': '在（某时间）', 'english': 'at', 'phonetic': '/æt/'},
            {'chinese': '起床', 'english': 'up', 'phonetic': '/ʌp/'},
            {'chinese': '挺早，提前', 'english': 'early', 'phonetic': '/ˈɜːli/（英）/ˈɜːrli/（美）'},
            {'chinese': '在今天', 'english': 'today', 'phonetic': '/təˈdeɪ/'},
            {'chinese': '今天星期几？', 'english': 'What day is it today?', 'phonetic': '/wɒt deɪ ɪz ɪt təˈdeɪ/（英）/wɑːt deɪ ɪz ɪt təˈdeɪ/（美）'},
            {'chinese': '电影院', 'english': 'cinema', 'phonetic': '/ˈsɪnəmə/（英）/ˈsɪnəmə/（美）'},
            {'chinese': '放学后', 'english': 'after school', 'phonetic': '/ˈɑːftə skuːl/（英）/ˈæftər skuːl/（美）'},
            {'chinese': '跳舞，舞蹈', 'english': 'dancing', 'phonetic': '/ˈdɑːnsɪŋ/（英）/ˈdænsɪŋ/（美）'},
            {'chinese': '一节课，一课时', 'english': 'lesson', 'phonetic': '/ˈlesn/'},
            {'chinese': '牵着（动物）走，溜', 'english': 'walk', 'phonetic': '/wɔːk/（英）/wɔːk/（美）'},
            {'chinese': '狗', 'english': 'dog', 'phonetic': '/dɒɡ/（英）/dɔːɡ/（美）'},
            {'chinese': '明天，在明天', 'english': 'tomorrow', 'phonetic': '/təˈmɒrəʊ/（英）/təˈmɑːroʊ/（美）'},
            {'chinese': '空闲的', 'english': 'free', 'phonetic': '/friː/'},
            {'chinese': '明天见！', 'english': 'See you tomorrow!', 'phonetic': '/siː juː təˈmɒrəʊ/（英）/siː juː təˈmɑːroʊ/（美）'}
        ]
    },
    'unit4': {
        'title': 'Unit 4: Sports Activities',
        'words': [
            {'chinese': '打（球），踢（球）', 'english': 'play', 'phonetic': '/pleɪ/'},
            {'chinese': '足球运动；足球', 'english': 'football', 'phonetic': '/ˈfʊtbɔːl/（英）/ˈfʊtbɔːl/（美）'},
            {'chinese': '乒乓球运动', 'english': 'ping-pong', 'phonetic': '/ˈpɪŋ pɒŋ/（英）/ˈpɪŋ pɑːŋ/（美）'},
            {'chinese': '篮球运动；篮球', 'english': 'basketball', 'phonetic': '/ˈbɑːskɪtbɔːl/（英）/ˈbɑːskɪtbɔːl/（美）'},
            {'chinese': '非常的', 'english': 'great', 'phonetic': '/ɡreɪt/'},
            {'chinese': '游泳；游泳运动', 'english': 'swimming', 'phonetic': '/ˈswɪmɪŋ/'},
            {'chinese': '（表示程度）这么，那么', 'english': 'so', 'phonetic': '/səʊ/（英）/soʊ/（美）'},
            {'chinese': '好', 'english': 'well', 'phonetic': '/wel/'},
            {'chinese': '试一试', 'english': 'Have a go!', 'phonetic': '/hæv ə ɡəʊ/（英）/hæv ə ɡoʊ/（美）'},
            {'chinese': '难做的，不易的', 'english': 'hard', 'phonetic': '/hɑːd/（英）/hɑːrd/（美）'},
            {'chinese': '没关系', 'english': "It's OK", 'phonetic': '/ɪts əʊˈkeɪ/（英）/ɪts oʊˈkeɪ/（美）'},
            {'chinese': '试', 'english': 'try', 'phonetic': '/traɪ/'},
            {'chinese': '好球！', 'english': 'Well played!', 'phonetic': '/wel pleɪd/'}
        ]
    },
    'unit5': {
        'title': 'Unit 5: Appearance and Features',
        'words': [
            {'chinese': '不同的，有区别的', 'english': 'different', 'phonetic': '/ˈdɪfrənt/'},
            {'chinese': '相同的，同一的', 'english': 'same', 'phonetic': '/seɪm/'},
            {'chinese': '头发', 'english': 'hair', 'phonetic': '/heə(r)/（英）/her/（美）'},
            {'chinese': '眼睛', 'english': 'eye', 'phonetic': '/aɪ/'},
            {'chinese': '耳朵', 'english': 'ear', 'phonetic': '/ɪə(r)/（英）/ɪr/（美）'},
            {'chinese': '鼻子', 'english': 'nose', 'phonetic': '/nəʊz/（英）/noʊz/（美）'},
            {'chinese': '嘴，口', 'english': 'mouth', 'phonetic': '/maʊθ/'},
            {'chinese': '手臂', 'english': 'arm', 'phonetic': '/ɑːm/（英）/ɑːrm/（美）'},
            {'chinese': '机器人', 'english': 'robot', 'phonetic': '/ˈrəʊbɒt/（英）/ˈroʊbɑːt/（美）'},
            {'chinese': '他的', 'english': 'his', 'phonetic': '/hɪz/'},
            {'chinese': '高的', 'english': 'tall', 'phonetic': '/tɔːl/'},
            {'chinese': '玩具娃娃', 'english': 'doll', 'phonetic': '/dɒl/（英）/dɔːl/（美）'},
            {'chinese': '她的', 'english': 'her', 'phonetic': '/hɜː(r)/（英）/hɜːr/（美）'},
            {'chinese': '小的', 'english': 'small', 'phonetic': '/smɔːl/'},
            {'chinese': '带来', 'english': 'bring', 'phonetic': '/brɪŋ/'},
            {'chinese': '大量，许多', 'english': 'lots of', 'phonetic': '/lɒts ɒv/（英）/lɑːts əv/（美）'},
            {'chinese': '玩偶，木偶', 'english': 'puppet', 'phonetic': '/ˈpʌpɪt/'},
            {'chinese': '表演，演出', 'english': 'show', 'phonetic': '/ʃəʊ/（英）/ʃoʊ/（美）'}
        ]
    },
    'unit6': {
        'title': 'Unit 6: Weather and Conditions',
        'words': [
            {'chinese': '天气，气象', 'english': 'weather', 'phonetic': '/ˈweðə(r)/（英）/ˈweðər/（美）'},
            {'chinese': '多云的，阴天的', 'english': 'cloudy', 'phonetic': '/ˈklaʊdi/'},
            {'chinese': '晴朗的', 'english': 'sunny', 'phonetic': '/ˈsʌni/'},
            {'chinese': '凉的，凉爽的', 'english': 'cool', 'phonetic': '/kuːl/'},
            {'chinese': '阴雨的，多雨的', 'english': 'rainy', 'phonetic': '/ˈreɪni/'},
            {'chinese': '温度高的，热的', 'english': 'hot', 'phonetic': '/hɒt/（英）/hɑːt/（美）'},
            {'chinese': '多风的，风大的', 'english': 'windy', 'phonetic': '/ˈwɪndi/'},
            {'chinese': '温暖的，暖和的', 'english': 'warm', 'phonetic': '/wɔːm/（英）/wɔːrm/（美）'},
            {'chinese': '未雨绸缪', 'english': 'save ... for a rainy day', 'phonetic': '/seɪv ... fɔː(r) ə ˈreɪni deɪ/（英）/seɪv ... fɔːr ə ˈreɪni deɪ/（美）'},
            {'chinese': '钱', 'english': 'money', 'phonetic': '/ˈmʌni/'},
            {'chinese': '今天天气怎么样？', 'english': "What's the weather like today?", 'phonetic': '/wɒts ðə ˈweðə laɪk təˈdeɪ/（英）/wɑːts ðə ˈweðər laɪk təˈdeɪ/（美）'},
            {'chinese': '公园', 'english': 'park', 'phonetic': '/pɑːk/（英）/pɑːrk/（美）'},
            {'chinese': '（与）会面，集合', 'english': 'meet', 'phonetic': '/miːt/'},
            {'chinese': '放风筝', 'english': 'fly a kite', 'phonetic': '/flaɪ ə kaɪt/'},
            {'chinese': '担心，担忧', 'english': 'worry', 'phonetic': '/ˈwʌri/（英）/ˈwɜːri/（美）'},
            {'chinese': '伞，雨伞', 'english': 'umbrella', 'phonetic': '/ʌmˈbrelə/'},
            {'chinese': '到那里，在那里', 'english': 'there', 'phonetic': '/ðeə(r)/（英）/ðer/（美）'}
        ]
    },
    'unit7': {
        'title': 'Unit 7: Seasons and Activities',
        'words': [
            {'chinese': '季节', 'english': 'season', 'phonetic': '/ˈsiːzn/'},
            {'chinese': '春天，春季', 'english': 'spring', 'phonetic': '/sprɪŋ/'},
            {'chinese': '去划船', 'english': 'go boating', 'phonetic': '/ɡəʊ ˈbəʊtɪŋ/（英）/ɡoʊ ˈboʊtɪŋ/（美）'},
            {'chinese': '冬天，冬季', 'english': 'winter', 'phonetic': '/ˈwɪntə(r)/（英）/ˈwɪntər/（美）'},
            {'chinese': '去溜冰，去滑冰', 'english': 'go skating', 'phonetic': '/ɡəʊ ˈskeɪtɪŋ/（英）/ɡoʊ ˈskeɪtɪŋ/（美）'},
            {'chinese': '夏天，夏季', 'english': 'summer', 'phonetic': '/ˈsʌmə(r)/（英）/ˈsʌmər/（美）'},
            {'chinese': '冰淇淋', 'english': 'ice cream', 'phonetic': '/aɪs kriːm/'},
            {'chinese': '去游泳', 'english': 'go swimming', 'phonetic': '/ɡəʊ ˈswɪmɪŋ/（英）/ɡoʊ ˈswɪmɪŋ/（美）'},
            {'chinese': '秋天，秋季', 'english': 'autumn', 'phonetic': '/ˈɔːtəm/（英）/ˈɔːtəm/（美）'},
            {'chinese': '去爬山', 'english': 'go climbing', 'phonetic': '/ɡəʊ ˈklaɪmɪŋ/（英）/ɡoʊ ˈklaɪmɪŋ/（美）'},
            {'chinese': '寒冷的，冷的', 'english': 'cold', 'phonetic': '/kəʊld/（英）/koʊld/（美）'},
            {'chinese': '鸟', 'english': 'bird', 'phonetic': '/bɜːd/（英）/bɜːrd/（美）'},
            {'chinese': '回原处', 'english': 'back', 'phonetic': '/bæk/'},
            {'chinese': '在（某段时间）内', 'english': 'in', 'phonetic': '/ɪn/'},
            {'chinese': '年', 'english': 'year', 'phonetic': '/jɪə(r)/（英）/jɪr/（美）'},
            {'chinese': '栽种，种植', 'english': 'plant', 'phonetic': '/plɑːnt/（英）/plænt/（美）'},
            {'chinese': '采，摘', 'english': 'pick', 'phonetic': '/pɪk/'},
            {'chinese': '雪，积雪', 'english': 'snow', 'phonetic': '/snəʊ/（英）/snoʊ/（美）'}
        ]
    },
    'unit8': {
        'title': 'Unit 8: Clothing and Appearance',
        'words': [
            {'chinese': '假日，假期', 'english': 'holiday', 'phonetic': '/ˈhɒlədeɪ/（英）/ˈhɑːlədeɪ/（美）'},
            {'chinese': '衣服', 'english': 'clothes', 'phonetic': '/kləʊðz/（英）/kloʊðz/（美）'},
            {'chinese': '（尤指有帽舌的）便帽', 'english': 'cap', 'phonetic': '/kæp/'},
            {'chinese': '外套，外衣', 'english': 'coat', 'phonetic': '/kəʊt/（英）/koʊt/（美）'},
            {'chinese': '半身裙', 'english': 'skirt', 'phonetic': '/skɜːt/（英）/skɜːrt/（美）'},
            {'chinese': '裤子', 'english': 'trousers', 'phonetic': '/ˈtraʊzəz/（英）/ˈtraʊzərz/（美）'},
            {'chinese': '连衣裙', 'english': 'dress', 'phonetic': '/dres/'},
            {'chinese': '（男士衬衫）', 'english': 'shirt', 'phonetic': '/ʃɜːt/（英）/ʃɜːrt/（美）'},
            {'chinese': '谁的', 'english': 'who', 'phonetic': '/huː/'},
            {'chinese': '看来好像，显得', 'english': 'look', 'phonetic': '/lʊk/'},
            {'chinese': '穿着，戴着', 'english': 'in', 'phonetic': '/ɪn/'},
            {'chinese': '太阳镜，墨镜', 'english': 'sunglasses', 'phonetic': '/ˈsʌnɡlæsɪz/'},
            {'chinese': '为什么', 'english': 'why', 'phonetic': '/waɪ/'},
            {'chinese': '穿，戴', 'english': 'wear', 'phonetic': '/weə(r)/（英）/wer/（美）'},
            {'chinese': '因为', 'english': 'because', 'phonetic': '/bɪˈkɒz/（英）/bɪˈkɔːz/（美）'},
            {'chinese': '聪明的，明亮的', 'english': 'bright', 'phonetic': '/braɪt/'}
        ]
    }
}


# 词汇学习屏幕
class VocabularyScreen(Screen):
    def __init__(self, **kwargs):
        super(VocabularyScreen, self).__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        # 添加背景
        self.add_cute_background()
        
        # 主布局
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 顶部标题
        title_layout = BoxLayout(size_hint_y=None, height=60)
        back_btn = create_button(text="←", font_size=20, size_hint_x=None, width=50,
                          background_color=CHILD_COLORS['secondary'])
        back_btn.bind(on_press=self.go_back)
        title_layout.add_widget(back_btn)
        
        title_label = create_label(text="译林版四年级词汇", font_size=22, bold=True)
        title_layout.add_widget(title_label)
        
        layout.add_widget(title_layout)
        
        # 单元选择区域
        units_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=400)
        
        for unit_key, unit_data in VOCABULARY_DATA.items():
            unit_btn = create_button(
                text=f"{unit_data['title']}\n({len(unit_data['words'])}个单词)", 
                font_size=16,
                background_color=CHILD_COLORS['accent']
            )
            unit_btn.unit_key = unit_key
            unit_btn.bind(on_press=self.select_unit)
            units_layout.add_widget(unit_btn)
        
        layout.add_widget(units_layout)
        
        # 底部导航
        bottom_nav = BoxLayout(size_hint_y=None, height=60, spacing=5)
        home_btn = create_button(text="首页", font_size=14, on_press=_get_screen_transition('main'))
        vocab_nav_btn = create_button(text="词汇", font_size=14, background_color=CHILD_COLORS['primary'])
        
        bottom_nav.add_widget(home_btn)
        bottom_nav.add_widget(vocab_nav_btn)
        
        layout.add_widget(bottom_nav)
        
        self.add_widget(layout)
    
    def add_cute_background(self):
        if hasattr(self, 'bg_color') and self.bg_color:
            self.remove_widget(self.bg_color)
        
        self.bg_color = Widget(size=self.size)
        with self.bg_color.canvas:
            Color(1.0, 0.95, 0.6, 1)
            Rectangle(pos=(0, 0), size=self.size)
        
        self.add_widget(self.bg_color, index=0)
    
    def select_unit(self, instance):
        # 创建单元学习屏幕
        unit_screen = UnitLearningScreen(unit_key=instance.unit_key, name='unit_learning')
        self.manager.add_widget(unit_screen)
        self.manager.current = 'unit_learning'
    
    def go_back(self, instance):
        self.manager.current = 'main'


# 单元学习屏幕
class UnitLearningScreen(Screen):
    def __init__(self, unit_key=None, **kwargs):
        super(UnitLearningScreen, self).__init__(**kwargs)
        self.unit_key = unit_key
        self.current_word_index = 0
        self.show_translation = False
        self.practice_mode = False
        self.practice_questions = []
        self.current_practice_index = 0
        self.practice_score = 0
        self.practice_answers = []
        self.build_ui()
        self.load_unit_words()
    
    def build_ui(self):
        # 添加背景
        self.add_cute_background()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 顶部标题
        title_layout = BoxLayout(size_hint_y=None, height=60)
        back_btn = create_button(text="←", font_size=20, size_hint_x=None, width=50,
                          background_color=CHILD_COLORS['secondary'])
        back_btn.bind(on_press=self.go_back)
        title_layout.add_widget(back_btn)
        
        self.title_label = create_label(text="", font_size=20, bold=True)
        title_layout.add_widget(self.title_label)
        
        layout.add_widget(title_layout)
        
        # 单词显示区域
        word_layout = BoxLayout(orientation='vertical', spacing=20, size_hint_y=None, height=300)
        
        # 英文单词
        self.word_label = create_label(text="", font_size=32, bold=True, halign='center')
        word_layout.add_widget(self.word_label)
        
        # 音标
        self.phonetic_label = create_label(text="", font_size=18, halign='center')
        word_layout.add_widget(self.phonetic_label)
        
        # 中文翻译
        self.translation_label = create_label(text="", font_size=24, halign='center')
        word_layout.add_widget(self.translation_label)
        
        layout.add_widget(word_layout)
        
        # 控制按钮
        controls_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        
        self.prev_btn = create_button(text="← 上一词", font_size=14,
                               background_color=CHILD_COLORS['secondary'])
        self.prev_btn.bind(on_press=self.prev_word)
        
        self.translate_btn = create_button(text="显示翻译", font_size=14,
                                   background_color=CHILD_COLORS['accent'])
        self.translate_btn.bind(on_press=self.toggle_translation)
        
        self.next_btn = create_button(text="下一词 →", font_size=14,
                               background_color=CHILD_COLORS['success'])
        self.next_btn.bind(on_press=self.next_word)
        
        self.practice_btn = create_button(text="练习模式", font_size=14,
                                   background_color=CHILD_COLORS['warning'])
        self.practice_btn.bind(on_press=self.toggle_practice_mode)
        
        controls_layout.add_widget(self.prev_btn)
        controls_layout.add_widget(self.translate_btn)
        controls_layout.add_widget(self.next_btn)
        controls_layout.add_widget(self.practice_btn)
        
        layout.add_widget(controls_layout)
        
        # 进度条
        self.progress_label = create_label(text="", font_size=16, halign='center')
        layout.add_widget(self.progress_label)
        
        self.add_widget(layout)
    
    def add_cute_background(self):
        if hasattr(self, 'bg_color') and self.bg_color:
            self.remove_widget(self.bg_color)
        
        self.bg_color = Widget(size=self.size)
        with self.bg_color.canvas:
            Color(1.0, 0.95, 0.6, 1)
            Rectangle(pos=(0, 0), size=self.size)
        
        self.add_widget(self.bg_color, index=0)
    
    def load_unit_words(self):
        if self.unit_key in VOCABULARY_DATA:
            unit_data = VOCABULARY_DATA[self.unit_key]
            self.title_label.text = unit_data['title']
            self.words = unit_data['words']
            self.current_word_index = 0
            self.update_display()
    
    def update_display(self):
        if hasattr(self, 'words') and self.words:
            word = self.words[self.current_word_index]
            self.word_label.text = word['english']
            self.phonetic_label.text = word['phonetic']
            
            if self.show_translation:
                self.translation_label.text = word['chinese']
                self.translate_btn.text = "隐藏翻译"
            else:
                self.translation_label.text = "点击'显示翻译'查看中文意思"
                self.translate_btn.text = "显示翻译"
            
            self.progress_label.text = f"第 {self.current_word_index + 1} 个单词，共 {len(self.words)} 个"
            
            # 更新按钮状态
            self.prev_btn.disabled = self.current_word_index == 0
            self.next_btn.disabled = self.current_word_index == len(self.words) - 1
    
    def prev_word(self, instance):
        if self.current_word_index > 0:
            self.current_word_index -= 1
            self.show_translation = False
            self.update_display()
    
    def next_word(self, instance):
        if hasattr(self, 'words') and self.current_word_index < len(self.words) - 1:
            self.current_word_index += 1
            self.show_translation = False
            self.update_display()
    
    def toggle_translation(self, instance):
        self.show_translation = not self.show_translation
        self.update_display()
    
    def go_back(self, instance):
        # 移除当前屏幕，返回词汇主界面
        self.manager.remove_widget(self)
        self.manager.current = 'vocabulary'
    
    def toggle_practice_mode(self, instance):
        self.practice_mode = not self.practice_mode
        
        if self.practice_mode:
            self.start_practice()
        else:
            self.exit_practice()
    
    def start_practice(self):
        # 创建练习题目
        self.practice_questions = []
        self.current_practice_index = 0
        self.practice_score = 0
        self.practice_answers = []
        
        # 生成英译汉题目
        for word in self.words:
            question = {
                'type': 'translation',
                'question': f"请翻译：{word['english']}",
                'answer': word['chinese'],
                'options': [word['chinese']],
                'word': word
            }
            self.practice_questions.append(question)
        
        # 随机打乱题目顺序
        import random
        random.shuffle(self.practice_questions)
        
        self.update_practice_display()
    
    def exit_practice(self):
        self.practice_mode = False
        self.practice_questions = []
        self.current_practice_index = 0
        self.practice_score = 0
        self.practice_answers = []
        self.update_display()
    
    def update_practice_display(self):
        if not self.practice_questions or self.current_practice_index >= len(self.practice_questions):
            self.show_practice_results()
            return
        
        question = self.practice_questions[self.current_practice_index]
        
        # 练习模式下的显示
        self.word_label.text = question['question']
        self.phonetic_label.text = ""
        self.translation_label.text = "请输入你的答案"
        
        # 隐藏/显示按钮
        self.prev_btn.disabled = True
        self.next_btn.disabled = True
        self.translate_btn.disabled = True
        
        # 更新练习进度
        self.progress_label.text = f"练习进度: {self.current_practice_index + 1}/{len(self.practice_questions)} 题 | 得分: {self.practice_score}"
    
    def show_practice_results(self):
        # 显示练习结果
        self.word_label.text = "练习完成！"
        self.phonetic_label.text = ""
        
        if len(self.practice_questions) > 0:
            accuracy = (self.practice_score / len(self.practice_questions)) * 100
            self.translation_label.text = f"正确率: {accuracy:.1f}%\n答对: {self.practice_score}/{len(self.practice_questions)} 题"
        else:
            self.translation_label.text = "没有完成任何题目"
        
        # 重新启用按钮
        self.prev_btn.disabled = False
        self.next_btn.disabled = False
        self.translate_btn.disabled = False
        
        # 更新按钮文字
        self.practice_btn.text = "练习模式"
        
        # 进度显示
        self.progress_label.text = "练习完成！点击'学习模式'返回学习"


# 应用主类
class WordMasterApp(App):
    def build(self):
        # ===== 安卓优化：设置移动设备窗口大小 =====
        # 设置适合手机屏幕的窗口大小，使用更大的尺寸以确保所有内容可见
        Window.size = (480, 800)  # 增大窗口尺寸，确保所有内容可见
        Window.clearcolor = CHILD_COLORS['background']
        
        # 创建屏幕管理器（优化转场动画）
        sm = ScreenManager(transition=SlideTransition(duration=0.2, direction='left'))
        
        # 添加各个屏幕，并设置默认显示主屏幕
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(LearningScreen(name='learning'))
        sm.add_widget(ReviewScreen(name='review'))
        sm.add_widget(TestScreen(name='test'))
        sm.add_widget(DictionaryScreen(name='dictionary'))
        sm.add_widget(ReadingScreen(name='reading'))
        sm.add_widget(StatisticsScreen(name='statistics'))
        sm.add_widget(GrammarScreen(name='grammar'))
        sm.add_widget(VocabularyScreen(name='vocabulary'))
        
        # 设置默认显示的屏幕，避免闪屏
        sm.current = 'main'
        
        return sm
    
    def on_window_resize(self, instance, size):
        """响应窗口大小变化，更新UI布局"""
        width, height = size
        print(f"Window resized to: {width}x{height}")
        
        # 触发所有屏幕的响应式布局更新
        if hasattr(self, 'root') and self.root:
            for screen in self.root.children:
                if hasattr(screen, 'on_screen_resize'):
                    screen.on_screen_resize(width, height)

if __name__ == '__main__':
    WordMasterApp().run()
