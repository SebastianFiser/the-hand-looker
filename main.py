import cv2
myimg = '/home/sebastian/Downloads/Untitled.jpeg' #change depending on your img location
foto = cv2.imread(myimg)
cv2.imshow('Foto', foto)
cv2.waitKey()
cv2.destroyAllWindows()