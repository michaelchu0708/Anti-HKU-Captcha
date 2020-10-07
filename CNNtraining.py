from keras.models import Model
from keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization
from keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard

#traincsv = open('./ground.csv', 'r', encoding = 'utf8')
import csv
import numpy as np
from PIL import Image
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())

LETTERSTR = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"
LETTERSTR = LETTERSTR.lower()


def toonehot(text):
    labellist = []
    for letter in text:
        onehot = [0 for _ in range(34)]
        num = LETTERSTR.find(letter)
        onehot[num] = 1
        labellist.append(onehot)
    return labellist
print("Creating CNN model...")
in1 = Input((50, 200, 3))
out = in1
out = Conv2D(filters=32, kernel_size=(3, 3), padding='same', activation='relu')(out)
out = Conv2D(filters=32, kernel_size=(3, 3), activation='relu')(out)
out = BatchNormalization()(out)
out = MaxPooling2D(pool_size=(2, 2))(out)
out = Dropout(0.3)(out)
out = Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu')(out)
out = Conv2D(filters=64, kernel_size=(3, 3), activation='relu')(out)
out = BatchNormalization()(out)
out = MaxPooling2D(pool_size=(2, 2))(out)
out = Dropout(0.3)(out)
out = Conv2D(filters=128, kernel_size=(3, 3), padding='same', activation='relu')(out)
out = Conv2D(filters=128, kernel_size=(3, 3), activation='relu')(out)
out = BatchNormalization()(out)
out = MaxPooling2D(pool_size=(2, 2))(out)
out = Dropout(0.3)(out)
out = Conv2D(filters=256, kernel_size=(3, 3), activation='relu')(out)
out = BatchNormalization()(out)
out = MaxPooling2D(pool_size=(2, 2))(out)
out = Flatten()(out)
out = Dropout(0.3)(out)
out = [Dense(34, name='digit1', activation='softmax')(out),\
    Dense(34, name='digit2', activation='softmax')(out),\
    Dense(34, name='digit3', activation='softmax')(out),\
    Dense(34, name='digit4', activation='softmax')(out),\
    Dense(34, name='digit5', activation='softmax')(out),\
    Dense(34, name='digit6', activation='softmax')(out)]
model = Model(inputs=in1, outputs=out)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()







print("Reading training data...")
traincsv = open('./Sample/Training/Answer.csv', 'r', encoding = 'utf8')
train_data = np.stack([np.array(Image.open("./Sample/Training/" + row[0] + ".jpg"))/255.0 for row in csv.reader(traincsv)])
traincsv = open('./Sample/Training/Answer.csv', 'r', encoding = 'utf8')
read_label = [toonehot(row[1]) for row in csv.reader(traincsv)]
train_label = [[] for _ in range(6)]
for arr in read_label:
    for index in range(6):
        train_label[index].append(arr[index])
train_label = [arr for arr in np.asarray(train_label)]
print("Shape of train data:", train_data.shape)

print("Reading validation data...")
valicsv = open('./Sample/Valid/Answer.csv', 'r', encoding = 'utf8')
vali_data = np.stack([np.array(Image.open("./Sample/Valid/" + row[0] + ".jpg"))/255.0 for row in csv.reader(valicsv)])
valicsv = open('./Sample/Valid/Answer.csv', 'r', encoding = 'utf8')
read_label = [toonehot(row[1]) for row in csv.reader(valicsv)]
vali_label = [[] for _ in range(6)]
for arr in read_label:
    for index in range(6):
        vali_label[index].append(arr[index])
vali_label = [arr for arr in np.asarray(vali_label)]
print("Shape of validation data:", vali_data.shape)


filepath="./temp.h5"
checkpoint = ModelCheckpoint(filepath, monitor='val_digit6_accuracy', verbose=1, save_best_only=True, mode='max')
earlystop = EarlyStopping(monitor='val_digit6_accuracy', patience=20, verbose=1, mode='auto')
#tensorBoard = TensorBoard(log_dir = "./logs", histogram_freq = 1)
callbacks_list = [checkpoint, earlystop]
#hist = model.fit_generator(steps_per_epoch=20, generator = 
model.fit(train_data, train_label, batch_size=400, epochs=50, verbose=2, validation_data=(vali_data, vali_label), callbacks=callbacks_list)


model.save_weights('temp_final.h5')
