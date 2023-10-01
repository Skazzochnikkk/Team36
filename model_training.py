import keras
import tensorflow
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

datagen = ImageDataGenerator(rescale = 1.0 / 255.0)
train_dir = r"C:\Users\Admin\Desktop\Hakaton photo\pj\train"
val_dir = r"C:\Users\Admin\Desktop\Hakaton photo\pj\val"
test_dir = r"C:\Users\Admin\Desktop\Hakaton photo\pj\test"
img_width, img_height = 768, 1024
input_shape = (img_width, img_height, 3)
epochs = 6
batch_size = 30
nb_train_samples = 2436
nb_validation_samples = 503
nb_test_samples = 491

train_generator = datagen.flow_from_directory(
    train_dir,
    target_size = (img_width, img_height),
    batch_size = batch_size,
    class_mode = 'binary'
)

val_generator = datagen.flow_from_directory(
    val_dir,
    target_size = (img_width, img_height),
    batch_size = batch_size,
    class_mode = 'binary'
)

test_generator = datagen.flow_from_directory(
    test_dir,
    target_size = (img_width, img_height),
    batch_size = batch_size,
    class_mode = 'binary'
)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=val_generator,
    validation_steps=nb_validation_samples // batch_size)

model.save('PobedaEA_V2.h5')