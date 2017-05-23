from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
# models que importamos
from final7.models import Aparcamiento
from final7.models import Comentario
from final7.models import Pag_Usuario
from django.contrib.auth.models import User  # usuarios django
from django.contrib.auth import authenticate, login
# cosas para beautufilsoup
from bs4 import BeautifulSoup
import urllib.request
import math
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from project import settings


def login_info(request):
    if request.user.is_authenticated():
        respuesta = "<p>Logged in as " + request.user.username
        respuesta += "<a href='/logout'> Logout </a></p>"
    else:
        respuesta = "<form action='/login' method='post'>"
        respuesta += "user: <input type= 'text' name='user'>"
        respuesta += "password: <input type= 'password' name='password'>"
        respuesta += "<input type= 'submit' value='enviar'>"
        respuesta += "</form>"
        respuesta += "<a href='/register/'>Register </a>"
    return respuesta


@csrf_exempt
def milogin(request):
    name_user = request.POST['user']
    password = request.POST['password']
    user = authenticate(username=name_user, password=password)
    if user is not None:
        login(request, user)
    return redirect("/")


def lista_usuarios(request):
    # Esto es para ver la nombre de lso usuarios guardados
    list_usuar = ""
    lista_pag = Pag_Usuario.objects.all()
    for i in lista_pag:
        list_usuar += "<br><a href=" + i.Propietario + ">" + i.Tit_Pagina
        list_usuar += "</a> " + i.Propietario

    return list_usuar


@csrf_exempt
def register(request):
    if request.method == "GET":
        form1 = "Crear Usuario: "
        form1 += "<form action='/register/' method='post'>"
        form1 += "User: <input type= 'text' name='user'>"
        form1 += "Email: <input type= 'text' name='email'>"
        form1 += "Password: <input type= 'password' name='password'>"
        form1 += "<input type= 'submit' value='enviar'>"
        form1 += "</form>"
    elif request.method == "POST":
        form1 = ""
        user = request.POST['user']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(user, email, password)
        user.save()
        url = "http://localhost:1234/"
        return redirect(url)

    else:
        form1 = "Method not allowed"

    template = get_template("in_business/reg.html")
    c = Context({'content': form1})
    respuesta = template.render(c)
    return HttpResponse(respuesta, content_type="text/html")


def actualizar_pag_usu(request):
    # funcion para actualizar la base de las paginas de usuario.
    lista_usuarios = User.objects.all()
    lista_pag = Pag_Usuario.objects.all()
    for usuario in lista_usuarios:
        if len(lista_pag) == 0:
            creador = usuario.get_username()
            titulo = "Pagina de " + usuario.get_username()
            Pag_usu_object = Pag_Usuario(Propietario=creador,
                                         Tit_Pagina=titulo)
            Pag_usu_object.save()
        else:
            contador = 0
            for pag in lista_pag:
                if pag.Propietario == usuario.get_username():
                    break
                elif pag.Propietario != usuario.get_username() and contador == len(lista_pag)-1:
                    creador = usuario.get_username()
                    titulo = "Pagina de " + usuario.get_username()
                    Pag_usu_object = Pag_Usuario(Propietario=creador,
                                                 Tit_Pagina=titulo)
                    Pag_usu_object.save()
                    break
                else:
                    contador = contador + 1


def parser_XML(request):
    pag = 'http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c3'
    pag += '1cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a'
    pag += '0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residen'
    pag += 'tes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full'

    Url = urllib.request.urlopen(pag).read()
    soup = BeautifulSoup(Url, "html.parser")
    datos_parking = soup.find_all('contenido')

    for element in datos_parking:
        # coger cada elemento de los datos e ir creando la base de datos
        nombre = element.find(nombre='NOMBRE').next_element
        id_entidad = element.find(nombre='ID-ENTIDAD').next_element
        if element.find(nombre='DESCRIPCION') is None:
            descripcion = "Null"
        else:
            descripcion = element.find(nombre='DESCRIPCION').next_element

        accesibilidad = element.find(nombre='ACCESIBILIDAD').next_element
        enlace = element.find(nombre='CONTENT-URL').next_element
        clase_via = element.find(nombre='CLASE-VIAL').next_element
        nombre_via = element.find(nombre='NOMBRE-VIA').next_element
        if element.find(nombre='CODIGO-POSTAL') is None:
            codig_post = "Null"
        else:
            codig_post = element.find(nombre='CODIGO-POSTAL').next_element

        if element.find(nombre='NUM') is None:
            numero_via = 0
        else:
            numero_via = element.find(nombre='NUM').next_element

        if element.find(nombre='BARRIO') is None:
            barrio = "Null"
        else:
            barrio = element.find(nombre='BARRIO').next_element

        if element.find(nombre='DISTRITO') is None:
            distrito = "Null"
        else:
            distrito = element.find(nombre='DISTRITO').next_element

        if element.find(nombre='LATITUD') is None:
            latitud = "Null"
        else:
            latitud = element.find(nombre='LATITUD').next_element

        if element.find(nombre='LONGITUD') is None:
            longitud = "Null"
        else:
            longitud = element.find(nombre='LONGITUD').next_element

        if element.find(nombre='TELEFONO') is None:
            telefono = "Null"
        else:
            telefono = element.find(nombre='TELEFONO').next_element

        if element.find(nombre='EMAIL') is None:
            email = "Null"
        else:
            email = element.find(nombre='EMAIL').next_element

        num_coment = 0
        # tengo todos los datos necesarios guardar cada elemetno en la base
        parking_objec = Aparcamiento(Nombre=nombre,
                                     Id_Entidad=id_entidad,
                                     Descripcion=descripcion,
                                     Accesibilidad=accesibilidad,
                                     Enlace=enlace,
                                     Clase_Via=clase_via,
                                     Nombre_Via=nombre_via,
                                     Numero_Via=numero_via,
                                     Codigo_Postal=codig_post,
                                     Barrio=barrio,
                                     Distrito=distrito,
                                     Latitud=latitud,
                                     Longitud=longitud,
                                     Telefono=telefono,
                                     Email=email,
                                     Num_Coment=num_coment)
        parking_objec.save()


@csrf_exempt
def pagPrincipal(request):
    actualizar_pag_usu(request)
    num_element = len(Aparcamiento.objects.all())
    if request.method == "GET":
        if num_element == 0:
            respuesta = "No hay datos disponibles en la base de datos"
            # post para cargar los datos
            form1 = "<br>¿Actualizar Datos?<br>"
            form1 += "<form action='/' method='post'>"
            form1 += "<input type= 'hidden' name='opcion' value='1'>"
            form1 += "<input type= 'submit' value='Actualizar'>"
            form1 += "</form>"
        else:
            form1 = "<br>¿Mostrar los accesibles?<br>"
            form1 += "<form action='/' method='post'>"
            form1 += "<input type= 'hidden' name='opcion' value='2'>"
            form1 += "<input type= 'submit' value='Mostrar'>"
            form1 += "</form>"

            respuesta = ""
            lista = Aparcamiento.objects.order_by('-Num_Coment')
            lista2 = lista[:5]
            for element in lista2:
                if element.Num_Coment == 0:
                    break
                else:
                    respuesta += "<br><a href=" + element.Enlace + ">"
                    respuesta += element.Nombre + "</a><br>Direccion: "
                    respuesta += element.Clase_Via + " " + element.Nombre_Via
                    respuesta += " " + element.Numero_Via + " "
                    respuesta += element.Barrio + ", " + element.Distrito + " "
                    respuesta += element.Codigo_Postal + "<br><a href=aparcamientos/"
                    respuesta += str(element.id) + ">Mas Informacion</a>"
    elif request.method == "POST":
        opcion = request.POST['opcion']
        if opcion == "1":
            # he pinchado sobre Actualizar datos
            parser_XML(request)
            return redirect("/")

        elif opcion == "2":
            respuesta = "Actualizada Base de datos"
            form1 = "<br>¿Volver?<br>"
            form1 += "<form action='/' method='get'>"
            form1 += "<input type= 'submit' value='volver'>"
            form1 += "</form>"

            respuesta = ""
            lista = Aparcamiento.objects.order_by('-Num_Coment')
            lista = lista.filter(Accesibilidad=1)
            lista2 = lista[:5]
            for element in lista2:
                if element.Num_Coment == 0:
                    break
                else:
                    respuesta += "<br><a href=" + element.Enlace + ">"
                    respuesta += element.Nombre + "</a><br>Direccion: "
                    respuesta += element.Clase_Via + " " + element.Nombre_Via
                    respuesta += " " + element.Numero_Via + " "
                    respuesta += element.Barrio + ", " + element.Distrito
                    respuesta += " " + element.Codigo_Postal
                    respuesta += "<br><a href=" + "aparcamientos/"
                    respuesta += str(element.id) + ">Mas Informacion</a>"

    template = get_template("in_business/pag_prin.html")
    c = Context({'content': respuesta, 'login_info': login_info(request),
                'lista_usu': lista_usuarios(request), 'filtro': form1})

    respuesta = template.render(c)
    return HttpResponse(respuesta)


@csrf_exempt
def todosAparca(request):
    if request.method == "GET":
        lista = Aparcamiento.objects.all()
        respuesta = ""
        for element in lista:
            respuesta += "<br>" + element.Nombre + " " + "<a href="
            respuesta += str(element.id) + ">Mas info(enlace a pagina)</a>"
        sts = 200

        list_distr = Aparcamiento.objects.order_by()
        list_distr = list_distr.values_list('Distrito', flat=True).distinct()
        # formulario para introducir en la base de datos
        form1 = "<br>¿Filtrar por distrito?<br>"
        form1 += "<form action='/aparcamientos/' method='post'>"
        form1 += "<select name='Distrito_Elegido'>"
        for element2 in list_distr:
            form1 += "<option value='" + element2 + "'>" + element2
            form1 += "</option>"
        form1 += "<input type= 'submit' value='Filtrar'>"
        form1 += "</form>"

    elif request.method == "POST":
        dist_ele = request.body.decode('utf-8').split("=")[1]
        distrito = " "
        respuesta = ""
        lista_dist = Aparcamiento.objects.filter(Distrito=dist_ele)
        # escribir aparcamientos del distrito elegido
        for element in lista_dist:
            respuesta += "<br>" + element.Nombre + " " + "<a href="
            respuesta += str(element.id) + ">Mas info(enlace a pagina)</a>"

        # formulario para filtrar por distrito
        list_distr = Aparcamiento.objects.order_by()
        list_distr = list_distr.values_list('Distrito', flat=True).distinct()

        form1 = "<br>¿Filtrar por distrito?<br>"
        form1 += "<form action='/aparcamientos/' method='post'>"
        form1 += "<select name='Distrito_Elegido'>"
        for element2 in list_distr:
            form1 += "<option value='" + element2 + "'>" + element2
            form1 += "</option>"
        form1 += "<input type= 'submit' value='Filtrar'>"
        form1 += "</form>"

        form1 += "<br>¿Lista entera?<br>"
        form1 += "<form action='/aparcamientos/' method='get'>"
        form1 += "<input type= 'submit' value='volver'>"
        form1 += "</form>"
        sts = 200
    else:
        respuesta = "Method Not Allowed"
        sts = 404

    template = get_template("in_business/tod_aparc.html")
    c = Context({'content': respuesta, 'login_info': login_info(request),
                'filtro': form1})
    respuesta = template.render(c)
    return HttpResponse(respuesta)


@csrf_exempt
def pagAparca(request, id):
    aparc = Aparcamiento.objects.get(id=id)
    respuesta = aparc.Nombre + "<br>ID:" + aparc.Id_Entidad
    respuesta += "<br>Descripcion: " + aparc.Descripcion
    respuesta += "<br>Accesibilidad: " + str(aparc.Accesibilidad)
    respuesta += "<br>Direccion: " + aparc.Clase_Via + " " + aparc.Nombre_Via
    respuesta += " " + aparc.Numero_Via + " " + aparc.Barrio + ", "
    respuesta += aparc.Distrito + "<br>Codigo Postal: " + aparc.Codigo_Postal
    respuesta += "<br>Latitud: " + aparc.Latitud + " Longitud: "
    respuesta += aparc.Longitud + "<br>Telefono: " + aparc.Telefono
    respuesta += " Email: " + aparc.Email + "<br><a href=" + aparc.Enlace
    respuesta += ">Enlace Pagina Comunidad de Madrid</a>"
    # Comentarios
    Lista_coment = Comentario.objects.filter(Aparc_Coment=aparc.Id_Entidad)
    Lista_coment = Lista_coment.order_by('-Fecha')
    respuesta += "<br>COMENTARIOS:"
    for element in Lista_coment:
        respuesta += "<br>" + str(element.Fecha) + ": " + element.Texto

    if request.method == "GET":
        form1 = ""
        form2 = ""
        if request.user.is_authenticated():
            # formulario para añadir Comentario
            form2 += "<br>¿Añadir Comentario? "
            form2 += "<form action='/aparcamientos/" + str(id) + "' method="
            form2 += "'post'>Texto: <input type= 'text' name='texto'>"
            form2 += "<input type= 'hidden' name='opcion' value='1'>"
            form2 += "<input type= 'submit' value='enviar'>"
            form2 += "</form>"
            # formulario para añadir
            form1 += "<br>¿añadir a tu pagina? "
            form1 += "<form action='/aparcamientos/" + str(id)
            form1 += "'method='post'><input type= 'hidden' name='opcion'"
            form1 += "value='2'><input type= 'submit' value='enviar'>"
            form1 += "</form>"

        sts = 200
    elif request.method == "POST":
        opcion = request.POST['opcion']
        if opcion == "1":
            # he cogido el comentario (tengo que guardarlo en la base)
            texto = request.POST['texto']
            coment_object = Comentario(Texto=texto,
                                       Aparc_Coment=aparc.Id_Entidad)
            coment_object.save()
            aparc.Num_Coment = aparc.Num_Coment + 1
            aparc.save()
            url = "http://localhost:1234/aparcamientos/" + str(id)
            return redirect(url)
        elif opcion == "2":
            # aparcamietno guardado en la variable "aparcamiento"
            pag = Pag_Usuario.objects.get(Propietario=request.user.username)
            pag.Aparc_Selec.add(aparc)
            pag.save()
            url = "http://localhost:1234/" + request.user.username
            return redirect(url)
        else:
            sts = 404
            respuesta = "No se deberia entrar aqui"
    else:
        sts = 405
        respuesta = "Method Not Allowed"
    template = get_template("in_business/aparc.html")
    c = Context({'content': respuesta, 'login_info': login_info(request),
                'filtro': form1, 'formulario': form2})
    respuesta = template.render(c)
    return HttpResponse(respuesta, status=sts)


@csrf_exempt
def pag_usu(request, nomb_usu):
    pag = Pag_Usuario.objects.get(Propietario=nomb_usu)
    titulo = pag.Tit_Pagina
    form1 = ""
    respuesta = ""
    if request.method == "GET":
        lista = pag.Aparc_Selec.all()
        tamano_lista = len(lista)
        caso = tamano_lista/5
        caso = math.ceil(caso)
        prueba = request.GET.get("ok", False)  # (para 5 en 5)
        if prueba is False:
            if caso <= 1:
                # hay menos de 5 aparcamenintos guardados
                for element in lista:
                    respuesta += "<br>" + element.Nombre + " "
                    respuesta += "<a href=aparcamientos/" + str(element.id)
                    respuesta += ">Mas info(enlace a pagina)</a>"
            else:
                # hay mas de 5 casos
                lista = lista[:5]
                for element in lista:
                    respuesta += "<br>" + element.Nombre + " "
                    respuesta += "<a href=aparcamientos/" + str(element.id)
                    respuesta += ">Mas info(enlace a pagina)</a>"
                # formularios para ir a las otras paginas
                for i in range(caso):
                    respuesta += "<form action='" + nomb_usu + "'method='get'"
                    respuesta += "><input type= 'hidden' name='ok' value='"
                    respuesta += str(i) + "'><input type= 'submit'"
                    respuesta += " value='Pagina " + str(i) + "'></form>"
        else:
            # no es false (hay mas paginas con aparcamietnos)
            num_Pag = request.GET['ok']
            num_pag = int(num_Pag)
            indice1 = num_pag * 5
            indice2 = (num_pag + 1) * 5
            pag_lista = lista[indice1:indice2]
            for element in pag_lista:
                respuesta += "<br>" + element.Nombre + " "
                respuesta += "<a href=aparcamientos/" + str(element.id)
                respuesta += ">Mas info(enlace a pagina)</a>"
            for i in range(caso):
                respuesta += "<form action='" + nomb_usu + "' method='get'>"
                respuesta += "<input type= 'hidden' name='ok' value='" + str(i)
                respuesta += "'><input type= 'submit' value='Pagina " + str(i)
                respuesta += "'></form>"

        if nomb_usu == request.user.username:
            # formulario para Cambiar titulo
            form1 = "<br>¿Cambiar Titulo? "
            form1 += "<form action='" + nomb_usu + "' method='post'>"
            form1 += "Titulo: <input type= 'text' name='titulo'>"
            form1 += "<input type= 'hidden' name='opcion' value='1'>"
            form1 += "<input type= 'submit' value='enviar'>"
            form1 += "</form>"
            # formulario cambiar color
            form1 += "<br>¿Cambiar color de Fondo? "
            form1 += "<form action='" + nomb_usu + "' method='post'>"
            form1 += "Titulo: <input type= 'text' name='color'>"
            form1 += "<input type= 'hidden' name='opcion' value='2'>"
            form1 += "<input type= 'submit' value='enviar'>"
            form1 += "</form>"
            # formulario cambiar tamaño letra
            form1 += "<br>¿Cambiar Tamaño Letra? "
            form1 += "<form action='" + nomb_usu + "' method='post'>"
            form1 += "Titulo: <input type= 'text' name='size'>"
            form1 += "<input type= 'hidden' name='opcion' value='3'>"
            form1 += "<input type= 'submit' value='enviar'>"
            form1 += "</form>"

        sts = 200
    elif request.method == "POST":
        opcion = request.POST['opcion']
        respuesta = ""
        if opcion == "1":
            new_titulo = request.POST['titulo']
            pag = Pag_Usuario.objects.get(Propietario=nomb_usu)
            pag.Tit_Pagina = new_titulo
            pag.save()
            sts = 200
        elif opcion == "2":
            new_color = request.POST['color']
            pag = Pag_Usuario.objects.get(Propietario=nomb_usu)
            pag.Color_Pagina = new_color
            pag.save()
            sts = 200
        elif opcion == "3":
            new_taman = request.POST['size']
            pag = Pag_Usuario.objects.get(Propietario=nomb_usu)
            pag.Letra_pagina = new_taman
            pag.save()
            sts = 200
        else:
            respuesta = "Method not Allowed"
            sts = 405
        url = "http://localhost:1234/" + nomb_usu
        return redirect(url)
    else:
        respuesta = "Method not Allowed"
        sts = 405

    template = get_template("in_business/pag_usu.html")
    c = Context({'title': titulo, 'content': respuesta,
                'login_info': login_info(request), 'formulario': form1})
    respuesta = template.render(c)
    return HttpResponse(respuesta, status=sts)


def about(request):
    respuesta = "<h1>Página principal \"/\":</h1>"
    respuesta += "<p>Si no hay nada en la base de datos, nos muestra un botón,"
    respuesta += " gracias al cual guardamos todos los datos de los "
    respuesta += "aparcamientos que nos proporciona un XML de la página "
    respuesta += "de la Comunidad de Madrid.</p>"
    respuesta += "<p>Si tenemos los datos guardados en la base. Se muestra un "
    respuesta += "listado de los 5 primeros aparcamientos que más comentarios"
    respuesta += " tengan. Además hay un botón que nos permite mostrar "
    respuesta += "los aparcamientos que sean accesibles.</p>"
    respuesta += "<p>También podemos ver un formulario para entrar en la "
    respuesta += "cuenta, un enlace para registrarse "
    respuesta += " y un listado de las páginas de usuario</p>"

    respuesta += "<h1>Página Aparcamientos \"/aparcamientos\"</h1>"
    respuesta += "<p>Nos muestra un listado con todos los aparcamientos "
    respuesta += "guardados en la base y un formulario con una lista para"
    respuesta += " para filtrar por distrito. Si hemos filtrado, nos saldrá"
    respuesta += " un segundo botón para volver a la lista completa</p>"

    respuesta += "<h1>Página Aparcamiento(id) \"/aparcamientos/(id)\":</h1>"
    respuesta += "<p>Si no estamos registrados nos saldrá toda la información "
    respuesta += "sobre el aparcamiento que hemos elegido y el listado de los"
    respuesta += " comentarios que se han realizado, quedando arriba "
    respuesta += "los más recientes</p><p>Si estamos registrados, además de lo"
    respuesta += " anterior, también nos mostrará 2 formularios; uno para "
    respuesta += " añadir el aparcamiento a la página de usuario y otro para "
    respuesta += "añadir un comentario</p>"

    respuesta += "<h1>Página Usuario \"/(usuario)\"</h1>"
    respuesta += "<p>Si no somos el propietario de la página nos mostrará un "
    respuesta += "listado de los primeros 5 aparcamientos que se han añadido, "
    respuesta += "además de varios botones por si el usuario tiene másde 5 "
    respuesta += "aparcamientos guardados</p>"
    respuesta += "<p>Si somos los propietarios, además de lo anterior, "
    respuesta += "nos mostrará 3 formularios: uno para cambiar el título de la"
    respuesta += " página, otro para cambiar el color del fondo y "
    respuesta += "el último para cambiar el tamaño de la letra</p>"

    respuesta += "<h1>Pagina XML \"/(usuario)/XML\"</h1><p>"
    respuesta += "Nos muestra un listado de los datos de los aparcamientos "
    respuesta += " que tiene guardado el usuario seleccionado, "
    respuesta += "en formato XML</p>"

    respuesta += "<h1>Pagina about \"/about\"</h1>"
    respuesta += "<p>Nos muestra el funcionamiento principal de la página</p>"

    respuesta += "<h1>Pagina register \"/register\"</h1>"
    respuesta += "<p>Nos muestra un formulario para crear un usuario</p>"

    template = get_template("in_business/about.html")
    c = Context({'content': respuesta, 'login_info': login_info(request)})
    respuesta = template.render(c)

    return HttpResponse(respuesta)


def xml(request, nombre_usu):
    respuesta = "<contenidos><infoDataset><nombre>Aparcamientos</nombre>"
    respuesta += "<descripcion>Informacion de los aparcamientos de madrid"
    respuesta += " que ha seleccionado el usuario: " + nombre_usu
    respuesta += "</descripcion></infoDataset>"
    pag = Pag_Usuario.objects.get(Propietario=nombre_usu)
    lista = pag.Aparc_Selec.all()
    for element in lista:
        respuesta += "<contenido>"
        respuesta += "<nombre>" + element.Nombre.replace("&", "&amp;")
        respuesta += "</nombre><Id-Entidad>" + element.Id_Entidad
        respuesta += "</Id-Entidad><Descripcion>"
        respuesta += element.Descripcion.replace("&", "&amp;")
        respuesta += "</Descripcion><Accesibilidad>"
        respuesta += str(element.Accesibilidad) + "</Accesibilidad><Enlace>"
        respuesta += element.Enlace.replace("&", "&amp;") + "</Enlace>"
        respuesta += "<Direccion><Clase_Via>" + element.Clase_Via
        respuesta += "</Clase_Via><Nombre_Via>"
        respuesta += element.Nombre_Via.replace("&", "&amp;")
        respuesta += "</Nombre_Via><Numero_Via>" + element.Numero_Via
        respuesta += "</Numero_Via><Barrio>" + element.Barrio + "</Barrio>"
        respuesta += "<Distrito>" + element.Distrito + "</Distrito>"
        respuesta += "</Direccion><Longitud>" + element.Longitud
        respuesta += "</Longitud><Latitud>" + element.Latitud
        respuesta += "</Latitud><Datos_De_Contacto><Telefono>"
        respuesta += element.Telefono + "</Telefono><Email>"
        respuesta += element.Email + "</Email></Datos_De_Contacto></contenido>"

    respuesta += "</contenidos>"
    return HttpResponse(respuesta, content_type="text/xml")


def css(request, nombre_css):
    if request.user.is_authenticated():
        pag = Pag_Usuario.objects.get(Propietario=request.user.get_username())
        color = pag.Color_Pagina
        tamano = pag.Letra_pagina
    else:
        color = "white"
        tamano = "90%"
    template = get_template("in_business/styl.css")
    c = Context({'tamano': tamano, 'color': color})
    respuesta = template.render(c)
    return HttpResponse(respuesta, content_type="text/css")
