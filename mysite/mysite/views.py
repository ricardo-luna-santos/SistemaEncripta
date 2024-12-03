from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Persona,Mensaje
from django.contrib.auth import authenticate
from datetime import datetime
from django.core.files.base import ContentFile
import bcrypt
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from cryptography.fernet import Fernet

def log(request):
    return render(request, "index.html")
def registro(request):
    return render(request,"registro.html")
def test(request):
    return render(request,"test.html")
def menu(request):
    return render(request,"menu.html")
def recordar(request):
    return render(request, "recordar.html")
def registrarusuario(request):
    nombre=request.POST['txtnombre']
    direccion=request.POST['txtdireccion']
    telefono=request.POST['txttelefono']
    correo=request.POST['txtcorreo']
    usuario=request.POST['txtusuario']
    contrasena=request.POST['txtcontrasena']

    persona = Persona.objects.create(nombre=nombre, direccion=direccion, telefono=telefono,correo=correo,usuario=usuario,contrasena=contrasena,created_date='2023-11-07',published_date='2023-11-07')
    return redirect('/')

def login(request):
    if request.method =="POST":
        #loginsuccess = authenticate(usuario=request.POST['usuario'],contrasena=request.POST['contrasena'])
        if (Persona.objects.filter(usuario = request.POST['usuario']).exists() and Persona.objects.filter(contrasena = request.POST['contrasena']).exists()):
            return redirect('/menu/')
        else:
            return redirect('/')
    else:
        return redirect('/')
    
def encriptar(request):
    mensajes = Mensaje.objects.all()
    return render(request,"encriptar.html", {"mensajes":mensajes})

def desencriptar(request):
    mensajes = Mensaje.objects.all()
    return render(request,"desencriptar.html",{"mensajes":mensajes})

'''def encriptarmsje(request):
    mensaje=request.POST['txtmensaje']
    now = datetime.now()
    #format = now.strftime('Día :%d, Mes: %m, Año: %Y, Hora: %H, Minutos: %M, Segundos: %S')
    fecha=now
    msjenc=mensaje.encode('utf-8')
    msjenc.bcrypt.gensalt()
    key='1234567890987654'
    cipher = bcrypt.hashpw(key, msjenc)
    mensaje = Mensaje.objects.create(Mensaje=cipher, fecha=fecha)
    return redirect('/encriptar/')'''

def encriptarmsj(request):
    mensaje=request.POST['txtmensaje']
    key = Fernet.generate_key()
    fernet = Fernet(key)

    strmensaje = str.encode(mensaje)
    encMessage = fernet.encrypt(strmensaje)
    now = datetime.now()
    fecha=now
    #key=b'{mensaje}'
    #salt = bcrypt.gensalt()
    #hashed = bcrypt.hashpw(key, salt.encode())
    mensaje = Mensaje.objects.create(Mensaje=encMessage, fecha=fecha, Key=key)
    print (key)
    print (encMessage)
    return redirect('/encriptar/')

def descargar(request, datos):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition']='attachment; filename=archivo-encriptado.txt'
    print(datos)
    lines = [datos,]
    response.writelines(lines)
    return response

def descargardes(request, mensaje, key):
    print (key)
    print (mensaje)
    fernet = Fernet(key)
    decMessage = fernet.decrypt(mensaje)

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition']='attachment; filename=archivo-desencriptado.txt'
    print(decMessage)
    lines = [decMessage,]
    response.writelines(lines)
    return response

def eliminarMensaje(request, datos):
    mensaje=Mensaje.objects.get(id=datos)
    mensaje.delete()
    return redirect('/encriptar/')

def cargar(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile=request.FILES['myfile']
        fs=FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        print(filename)
        uploaded_file_url = fs.url(filename)
        return render(request, 'desencriptar.html',{'uploades_file_url':uploaded_file_url})
    return render(request, 'desencriptar.html')