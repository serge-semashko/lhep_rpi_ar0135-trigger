import cv2
import time
import memcache
'''
apiPreference    preferred Capture API backends to use. 
Can be used to enforce a specific reader implementation 
if multiple are available: 
e.g. cv2.CAP_MSMF or cv2.CAP_DSHOW.
'''
# open video0
def returnCameraIndexes():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr
#print(returnCameraIndexes())

def frameCheck(fr):
   #0 - low brightness, 1 - good, 2 - too high brightness
    f = 0
    (h, w) = fr.shape[:2]
    for i in range(h):
        for j in range(w):
            pix = fr[i][j]
            if pix[0] == 255 or pix[1] == 255 or pix[2] == 255:
                f = 2
                break
            elif 240 <= pix[0] <= 254 or 240 <= pix[1] <= 254 or 240 <= pix[2] <= 254:
                f = 1
        if f == 2:
            break
    return f

def brightnessSelect(cap):
    lp = 0
    rp = 255
    mp = 127
    while rp - lp > 1:
        cap1.set(cv2.CAP_PROP_BRIGHTNESS, mp)
        ret, frame = cap.read()
        check_rez = frameCheck(frame)
        if check_rez == 0:
            lp = mp
            mp = (rp + lp) / 2
        elif check_rez == 2:
            rp = mp
            mp = (lp + rp) /2
        elif check_rez == 2:
            break
    return mp

#NOT WORK
capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
if capture.isOpened():
    print("capture Work")
else:
    print("capture Don't work")
    quit()

capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
width = 1920
height = 1080
capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
ret, frame = capture.read()
# Display the resulting frame
w1 = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
h1 = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(str(ret)+' '+"%dX%d"%(w1,h1) ) #+str(frame)

capture.release()
#//NOT WORK

#work ok
cap1 = cv2.VideoCapture(0)
if cap1.isOpened():
    print("cap1 Work")
else:
    print("cap1 Don't work")
    quit()
print('cap1='+str(cap1))
client = memcache.Client([('127.0.0.1', 11211)])
#cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
#print('cap'+str(cap))
# set width and height
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
print(1)

#cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# set fps
cap1.set(cv2.CAP_PROP_FPS, 60)
br = 40;
print(2)
cap1.set(cv2.CAP_PROP_BRIGHTNESS, br)
print(3)

run_num = 1 #номер рана
frame_cup = 1
frame_inter = 0.5 #500 милисекунд
run_inter = 0.1


while(True):
    print(11)
    sendValue = client.get('Value')
    print('sendValue=',sendValue)
    if sendValue and sendValue > 0:
        br = sendValue
        flag = 1
    else:
        br = brightnessSelect(cap1)
        flag = 0
    print(flag, br)
    ss = 0
    for i in range(frame_cup):
        cap1.set(cv2.CAP_PROP_BRIGHTNESS, br)
        # Capture frame-by-frame
        ret, frame = cap1.read()
        # Display the resulting frame
        w1 = cap1.get(cv2.CAP_PROP_FRAME_WIDTH) * (2 ** (1/2))
        h1 = cap1.get(cv2.CAP_PROP_FRAME_HEIGHT) * (2 ** (1/2))
        print(str(ret)+' '+"%dX%d"%(w1,h1) ) #+str(frame)
        tm = time.gmtime()
        file_name = str(tm.tm_year) + '-' + str(tm.tm_mon) + '-' + str(tm.tm_mday) + '_' + str(tm.tm_hour) + '-' + '%.5d'%(run_num) + '-' + str(i + 1) + '_' + str(ss) + '_' + str(br)
        cv2.imwrite(file_name+'.jpg', frame)
        cv2.imwrite('last.jpg', frame)
        ss += frame_inter
#    num+=1
#    if num==10:
#        aaa()
#    cv2.imshow('frame', frame)
        if flag == 0:
            br+=10;
            print('up to', br)
        time.sleep(frame_inter)
#    cap1.set(cv2.CAP_PROP_FRAME_WIDTH, w1+200)
    run_num += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print('sleep')
    time.sleep(run_inter)
    flag = 0
    print('sleep end')
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
