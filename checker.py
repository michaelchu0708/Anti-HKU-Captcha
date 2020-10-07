import matplotlib.pyplot as plt
from keras.preprocessing import image
import numpy as np
import keras
import os
from PIL import Image

from keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization
from keras.models import Model
print("Creating CNN model...")
LETTERSTR = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"
LETTERSTR = LETTERSTR.lower()
print(LETTERSTR)
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
#model_json = model.to_json()
#with open("model.json", "w") as json_file:
#    json_file.write(model_json)


model.load_weights("saved_model/last_model.h5")
#model.summary()
temp = []
verify = "./verify/"
i = 0
name = []
for image_path in os.listdir(verify):
    img = image.load_img(verify+image_path ,target_size=(50,200))
    name.append(image_path)
    #print(image_path)
    #img = Image.open(verify+image_path)
    img = np.asarray(img)/255.0
    temp.append(img)
    #plt.imshow(img)
    #img = np.expand_dims(img, axis=0)


test_data = np.stack(temp)
prediction = model.predict(test_data)
print(name)
#print("output: "+str(prediction))
answer=[]
temp = ""
for i in range(20):
    for char in range(6):
        temp += LETTERSTR[np.argmax(prediction[char][i])]
    answer.append(temp)
    temp = ""

print(answer)