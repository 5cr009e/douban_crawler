import sqlite3
import jieba
import numpy as np
from wordcloud import WordCloud
from PIL import Image
from matplotlib import pyplot as plt

con = sqlite3.connect('../database/douban_top250.db')
cur = con.cursor()
sql = 'select introduction from douban250'
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]
cur.close()
con.close()

cut = jieba.cut(text)
cut_text = ' '.join(cut)

img_array = np.array(Image.open(r'./static/assets/img/mask.jpg'))
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path="msyhl.ttc"
).generate_from_text(cut_text)

fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')
# plt.show()
plt.savefig(r'./static/assets/img/wordcloud.jpg', dpi=500)