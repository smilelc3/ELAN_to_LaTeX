import tkinter as tk
import tkinter.font as tkFont


# 获取指定字体、指定文本，指定字号的显示高宽度
class font:
    root = tk.Tk()

    @classmethod
    def get_size(self, text, font_family=("Times New Roman", 14)):

        #canvas = tk.Canvas(root, width=1000, height=220)
        #canvas.pack()
        (x, y) = (0, 0)
        font = tkFont.Font(font=font_family)
        w = font.measure(text)
        # h = font.metrics("linespace")
        #print("Text Width is %s px, height is %s px" % (w, h))
        #canvas.create_text(x, y, text=text, font=font, anchor=tk.NW)
        #tk.mainloop()
        return w

if __name__ == '__main__':
    '''
    font.get_size("\n\taaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n\
    \tiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii\n\
    \tAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n\
    \tIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n\
    \tzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz\n\
    \tHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH\n\
    \tʨhi²¹tha⁵⁵ ti⁵⁵ ti²¹xua²¹ le²¹,   ai⁵⁵mɨe⁵⁵ ẽ⁵⁵ti⁵⁵,  a²¹ le⁵³ ʦi⁵⁵xɨu³⁵, ", ("Times New Roman", 14))
    '''

    print(font.get_size("首先呢，就是过去！首先呢，就是过去！首先呢，就是过去！首先呢，就是过去！首先呢，就是过", ("Times New Roman", 14)))