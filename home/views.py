from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from fastbook import load_learner
import pathlib
import os

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

learner = load_learner('./models/Mask-Predictor-Learner.pkl')

def index(request):
    if request.method == 'POST':
        files = os.listdir('./media')
        if request.FILES['imgfile'] == '':
            return render(request, 'index.html', {'mess':'Please Upload an Image!'})

        try:
            for i in files: os.remove('./media/'+i)
        except Exception as e:
            pass
        filesys = FileSystemStorage()
        fileobj = request.FILES["imgfile"]
        filepth = filesys.save(fileobj.name, fileobj)
        url = filesys.url(filepth)
        preds = learner.predict("."+url)
        pred = preds[0]
        emoj = {'WithMask':'😷', 'WithoutMask':'😐 (Please wear one!)'}[pred]
        context = {'fileurl':url, 'pred':pred, 'emoj':emoj}
        return render(request, 'index.html', context)
    return render(request, 'index.html', {})