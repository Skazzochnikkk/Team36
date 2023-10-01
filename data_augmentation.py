'''from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array

datagen= ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

img=load_img('')#указать путь к файлу
x=img_to_array(img)
x=x.reshape((1,)+x.shape)

i=0
for batch in datagen.flow(x, batch_size=1, save_to_dir='previw', save_prefix='cat',save_format='jpeg'):
    i+=1
    if i>20:
        break'''