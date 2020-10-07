from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2
from keras.utils.vis_utils import plot_model
from keras.models import model_from_json
import numpy as np
import urllib.request
from PIL import Image
from keras.preprocessing import image
import cv2
import time

LETTERSTR = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"
LETTERSTR = LETTERSTR.lower()
#https://bs.cse.hku.hk/ihpbooking/stickyImg
temp = []
def main():
    #load model
    model = load_model()
    model.summary()
    #plot_model(model, to_file='model.png')
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(('https://bs.cse.hku.hk/ihpbooking/stickyImg'))
    browser.save_screenshot('tmp.png')

    #Get Captcha image
    location = browser.find_element_by_xpath("/html/body/img").location
    #x, y = location['x'] + 5, location['y'] + 5
    img = Image.open('tmp.png')
    w, d = img.size
    captcha = img.crop((w/2-100, d/2-25, w/2+ 100, d/2 + 25))
    captcha = captcha.resize((200, 50))
    captcha.convert("RGB").save('captcha_test.jpg', 'JPEG')
    img = image.load_img('captcha_test.jpg', target_size=(50, 200))
    img = np.asarray(img)/255.0
    #cv2.imshow("test", img)
    #cv2.waitKey(0)
    temp.append(img)
    test_data = np.stack(temp)
    print(test_data.shape)
    test = prediction_and_return(model, test_data)
    #print(test)

    time.sleep(20)

def load_model():
    json_file = open('./saved_model/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.load_weights("./saved_model/last_model.h5")
    return model

def prediction_and_return(model, image):
    prediction = model.predict(image)
    temp=""
    for char in range(6):
        temp += LETTERSTR[np.argmax(prediction[char][0])]

    print("Predicted Captcha:    " + temp)
    return temp


if __name__=="__main__":
   main()
