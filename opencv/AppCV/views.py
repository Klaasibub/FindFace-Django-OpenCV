from django.shortcuts import render
from django.http import JsonResponse
import cv2

rect = []
img_path = "media/file.png"


def get_image():
    face_cascade = cv2.CascadeClassifier('static/haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    ret, image = cam.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(10, 10))
    rect.clear()
    for (x, y, w, h) in faces:
        rect.append({"x": str(x), "y": str(y), "width": str(w), "height": str(h)})
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 0), 2)
    cv2.imwrite(img_path, image)
    cam.release()


def home(request):
    category = request.GET.get("type", "")
    if category == 'json' or category == 'image':
        get_image()
        if category == 'json':
            return JsonResponse({"Faces": rect})
        else:
            return render(request, f'AppCV/{category}.html', context={"img_path": img_path})
    return render(request, 'AppCV/home.html')
