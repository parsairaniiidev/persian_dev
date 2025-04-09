import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Slug:
    """
    شیء مقدار برای مدیریت slug مقالات
    شامل منطق تولید و اعتبارسنجی slug
    """
    value: str

    @classmethod
    def generate_from_title(cls, title: str) -> 'Slug':
        """
        تولید slug از عنوان مقاله
        تبدیل حروف فارسی و اعمال استانداردهای SEO
        """
        # تبدیل حروف فارسی به معادل انگلیسی
        persian_map = {
            ' ': '-', '‌': '-', '،': '', '؟': '', 'آ': 'a',
            'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's',
            'ج': 'j', 'چ': 'ch', 'ح': 'h', 'خ': 'kh', 'د': 'd',
            'ذ': 'z', 'ر': 'r', 'ز': 'z', 'ژ': 'zh', 'س': 's',
            'ش': 'sh', 'ص': 's', 'ض': 'z', 'ط': 't', 'ظ': 'z',
            'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'gh', 'ک': 'k',
            'گ': 'g', 'ل': 'l', 'م': 'm', 'ن': 'n', 'و': 'v',
            'ه': 'h', 'ی': 'y'
        }
        
        slug = title.lower().strip()
        for char, replacement in persian_map.items():
            slug = slug.replace(char, replacement)
        
        # حذف کاراکترهای غیرمجاز
        slug = re.sub(r'[^\w\-]', '', slug)
        slug = re.sub(r'\-\-+', '-', slug)
        slug = slug.strip('-')
        
        return cls(slug)