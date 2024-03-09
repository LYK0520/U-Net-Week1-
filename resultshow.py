import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

result_path = 'data/test/'
imgs_path = os.listdir(result_path)

nrows = 6
ncols = 10

pic_index=0
fig = plt.gcf()
fig.set_size_inches(ncols*2,nrows*2)

pic_index+=10
next_pix = [os.path.join(result_path,img) for img in imgs_path[pic_index-10:pic_index]]

for i,img_path in enumerate(next_pix):
    sp = plt.subplot(nrows,ncols,i+1)
    sp.axis('Off')
    img = mpimg.imread(img_path)
    plt.imshow(img)

plt.show()