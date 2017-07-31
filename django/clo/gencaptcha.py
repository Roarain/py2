import random
import string
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import StringIO

lower_str = 'abcdefghjkmnpqrstuvwxy'
upper_str = lower_str.upper()
int_str = ''.join(map(str,range(2,10)))
init_str = lower_str+upper_str+int_str

class GenCaptcha(object):
    def __init__(self):
        lower_str = 'abcdefghjkmnpqrstuvwxy'
        upper_str = lower_str.upper()
        int_str = ''.join(map(str, range(2, 10)))
        self.init_str = lower_str + upper_str + int_str

        self.size = (150,80)
        self.width,self.height = self.size

        self.img_type = 'jpeg'
        self.mode = 'RGB'
        self.bg_color = (144,238,144)
        self.fg_color = (0,0,255)
        self.font_size = 24
        self.font_type = '/PycharmProjects/django/cmdb/Lato-Regular.ttf'

        self.parameters = [
            1 - float(random.randint(1,2))/100,
            0,
            0,
            0,
            1 - float(random.randint(1, 10)) / 100,
            float(random.randint(1, 2)) / 500,
            0.001,
            float(random.randint(1, 2)) / 500
        ]

        self.img = Image.new(self.mode, self.size, self.bg_color)

        self.draw = ImageDraw.Draw(self.img)

    def create_line(self):
        line_num = random.randint(1,2)
        for i in range(line_num):
            start_point = (random.randint(0,self.size[0]),random.randint(0,self.size[1]))
            end_point = (random.randint(0,self.size[0]),random.randint(0,self.size[1]))
            self.draw.line([start_point,end_point],fill=(0,0,0))
    def create_point(self):
        point_num = random.randint(5,10)
        for i in range(point_num):
            w = random.randint(0,self.width)
            h = random.randint(0,self.height)
            self.draw.point((w,h),fill=(0,0,0))
    def create_char(self):
        char_str = ' '.join(random.sample(self.init_str,4))
        # char_str = 'A\n'
        font = ImageFont.truetype(self.font_type,self.font_size)
        # font = ImageFont.truetype()
        font_width , font_height = font.getsize(char_str)
        self.draw.text(((self.width-font_width)/3 ,(self.height-font_height)/3),char_str,font=font)
        return char_str.lower()
    def create_img(self):
        img = self.img.transform(self.size,Image.PERSPECTIVE,self.parameters).filter(ImageFilter.EDGE_ENHANCE_MORE)
        return img

    def save_to_mem(self):
        buf = StringIO.StringIO()
        self.create_point()
        self.create_line()
        img_char = self.create_char()
        img_ori = self.create_img()
        img_ori.save(buf,'jpeg')
        img = buf.getvalue()
        return img,img_char



