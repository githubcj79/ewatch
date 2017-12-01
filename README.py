Proyecto:	ewatch
			(~/Projects/ewatch)

-------------------------------------------------------------------

Para efectos de este proyecto se creará un ambiente virtual
del mismo nombre.
	
$ virtualenv --python=/usr/bin/python2.7 ~/.myvirtualenv/ewatch			

~/Projects/ewatch$ workon
dproject
ewatch
livestatus3
sanidad

-------------------------------------------------------------------

Se inicializa git

(ewatch) ~/Projects/ewatch$ git init

(ewatch) ~/Projects/ewatch$ touch .gitignore

-------------------------------------------------------------------

Instalación de Django 1.11 LTS

(ewatch) ~/Projects/ewatch$ python -m django --version
1.11
-------------------------------------------------------------------
Django:

https://docs.djangoproject.com/es/1.11/intro/tutorial01/

(ewatch) ~/Projects/ewatch$ django-admin startproject ewatch

(ewatch) ~/Projects/ewatch/ewatch$ t
.
├── ewatch
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py

(ewatch) ~/Projects/ewatch/ewatch$ python manage.py runserver 8001

'''
CommandError: 'ewatch' conflicts with the name of an existing Python module and cannot be used as an app name. Please try another name.
'''

python manage.py startapp early

--->
	El proyecto es ewatch
	La app es early

(ewatch) ~/Projects/ewatch/ewatch/early$ touch urls.py

http://localhost:8001/early/ --> Hello, world. You're at the early index.

git commit -m "Estado inicial --> Hello, world. You're at the early index."

-------------------------------------------------------------------

(ewatch) ~/Projects/ewatch/ewatch$ python manage.py migrate

(ewatch) ~/Projects/ewatch/ewatch$ python manage.py makemigrations early
Migrations for 'early':
  early/migrations/0001_initial.py
    - Create model Country
    - Create model View

python manage.py migrate

'''
Las migraciones son muy potentes y le permiten modificar sus modelos con el tiempo, a medida que desarrolla su proyecto, sin necesidad de eliminar su base de datos o las tablas y hacer otras nuevas. Este se especializa en la actualización de su base de datos en vivo, sin perder datos. Vamos a hablar de ellas en mayor profundidad más tarde en el tutorial, pero por ahora, recuerde la guía de tres pasos para hacer cambios de modelo:

    Cambie sus modelos (en models.py).
    Ejecute el comando python manage.py makemigrations para crear migraciones para esos cambios
    Ejecute el comando python manage.py migrate para aplicar esos cambios a la base de datos.
'''

(ewatch) ~/Projects/ewatch/ewatch$ python manage.py shell
>>> from early.models import Country, View
>>> from django.utils import timezone
>>> c = Country(country_text="CHILE")
c.save()
>>> Country.objects.all()


(ewatch) ~/Projects/ewatch/ewatch$ python manage.py shell
Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from early.models import Country, View
>>> from django.utils import timezone
>>> Country.objects.all()
<QuerySet [<Country: CHILE>]>
>>> Country.objects.filter(id=1)
<QuerySet [<Country: CHILE>]>
>>> Country.objects.filter(country_text__startswith='CH')
<QuerySet [<Country: CHILE>]>
>>> c = Country.objects.get(pk=1)
>>> c.view_set.all()
<QuerySet []>
>>> c.view_set.create(view_text='CL_POS_REGIONAL', pub_date=timezone.now())
<View: CL_POS_REGIONAL>

-------------------------------------------------------------------

(ewatch) ~/Projects/ewatch/ewatch$ python manage.py createsuperuser
Username (leave blank to use 'carlos'): 
Email address: carlosjmnz79@gmail.com
Password: --> ewatch79

'''
Estamos utilizando dos vistas genéricas aquí: ListView y DetailView. Respectivamente, esas dos vistas abstraen los conceptos de «mostrar una lista de objetos» y «mostrar una página de detalles para un tipo específico de objeto.»

    Cada vista genérica tiene que saber cuál es el modelo sobre el que estará actuando. Esto se proporciona utilizando el atributo model.
    La vista genérica DetailView espera que el valor de la clave primaria capturado desde la URL sea denominado "pk", por lo que hemos cambiado``question_id`` a pk para las vistas genéricas.

Por defecto, la vista genérica DetailView utiliza una plantilla llamada <app name>/<model name>_detail.html. En nuestro caso, utilizaría la plantilla "polls/question_detail.html". El atributo template_name se utiliza para indicarle a Django que utilice un nombre de plantilla específico en vez del nombre de plantilla generado de forma automática. También especificamos el atributo template_name para la vista de lista results, esto garantiza que la vista de resultados y la vista detalle tengan un aspecto diferente cuando sean creadas, a pesar de que las dos son una vista genérica DetailView en segundo plano.

Del mismo modo, la vista genérica ListView utiliza una plantilla predeterminada llamada <app name>/<model name>_list.html; utilizamos el atributo template_name para indicarle a ListView que utilice nuestra plantilla "polls/index.html" existente.

En partes anteriores del tutorial, las plantillas se han dotado de un contexto que contiene las variables contextuales question y latest_question_list. Para DetailView se suministra la variable question de forma automática, ya que estamos utilizando un modelo (Question) de Django, Django puede determinar un nombre adecuado para la variable contextual. Sin embargo, para ListView, la variable contextual generada de forma automática es question_list. Para anular esto, proporcionamos el atributo``context_object_name`` especificando que queremos utilizar en cambio latest_question_list. Como un método alternativo, usted puede modificar sus plantillas para que coincidan con las nuevas variables contextuales predeterminadas, pero es mucho más sencillo solo indicarle a Django que utilice la variable que usted quiere.

Ejecute el servidor y utilice su nueva aplicación encuesta basada en las vistas genéricas.

Para más detalles sobre las vistas genéricas, consulte la documentación de las vistas genéricas.	
'''

Intento Cambiar vista index para que muestre la lista de paises ...

~/Projects/ewatch/ewatch$ workon ewatch
(ewatch) ~/Projects/ewatch/ewatch$ python manage.py runserver 8001

My IP : $ ifconfig

-- Agrego BRASIL, para probar paises sin vistas

(ewatch) ~/Projects/ewatch/ewatch$ python manage.py shell
Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from early.models import Country, View
>>> from django.utils import timezone
>>> c = Country(country_text="BRASIL")
>>> c.save()
>>> Country.objects.all()
<QuerySet [<Country: CHILE>, <Country: BRASIL>]>
>>>

20171110

git reset --hard c62c196e964

(ewatch) ~/Projects/ewatch/ewatch$ pip install kitchen

20171113

python manage.py runserver 10.95.3.178:8001

sudo netstat -tulpn | grep LISTEN
~$ sudo netstat -tulpn | grep LISTEN
~$ sudo iptables -A INPUT -p tcp -d 0/0 -s 0/0 --dport 8001 -j ACCEPT
nmap localhost
nmap 10.95.3.178

settings.py
    # ALLOWED_HOSTS = [ u'10.95.3.178',]
    ALLOWED_HOSTS = [ u'*',]

20171120

Las ideas:

- llevar un indicador de color a .html y dinámicamente cambiarle el color al host
- refactoring ... creando objeto host

Done :)

# -----------------------------------------------------------------------------

20171121

Idea:

- darle color al grupo en la web page.

Done.

# -----------------------------------------------------------------------------

20171121

Conversación con Juan Carlos

    - Idea, que la aplicación que desarrollé vaya a buscar en alguna parte de Chech_MK,
        los grupos a monitorear.

Idea:

- estudiar el paso a producción

# -----------------------------------------------------------------------------

20171121

(ewatch) ~/Projects/ewatch/ewatch/early$ python -c "import  setuptools"
(ewatch) ~/Projects/ewatch/ewatch/early$ echo $?
0 <-- instalado
1 <-- no instalado

# -----------------------------------------------------------------------------

20171123

César solicita semáforo variable, según estado del grupo.
Indica basarse en semáforos que tiene la presentación.

# -----------------------------------------------------------------------------

20171128

César solicita detectar todos los grupos, "por pais".

Mostrar lista de grupos por "pais"

    Seleccionar grupo --> y mostrar lo de siempre ....
                            (uso cpu, disk, memory & alerts)

    Estoy viendo si puedo detectar grupos en /home/carlos/Labs/mk-livestatus-20171128

César envió la siguiente lista a incorporar:

Por Peru:
 
PE-BANCO PERU SIEBEL                    --> PE_BANCO_PERU_SIEBEL
PE-PANGUI                                   PE_PANGUI
PE-PORTAL PROVEEDORES                       PE_PORTAL_PROVEEDORES
PE-SERVIDORES BANCO                         PE_SERVIDORES_BANCO
PE-SWITCH DE TRANSACCIONES                  PE_SWITCH_DE_TRANSACCIONES
PE-SISTEMAS CENTRO DE DISTRIBUCION          PE_SISTEMAS_CENTRO_DE_DISTRIBUCION
 
Por Argentina:
 
AR-BIZTALK                              --> AR_BIZTALK
AR-APLICACIONES RRHH                        AR_APLICACIONES_RRHH
AR-BUXIS                                    AR_BUXIS
AR-ENGAGE                                   AR_ENGAGE
AR-PANGUI                                   AR_PANGUI
 
Por Colombia:
 
CO-FLEJES                               --> CO_FLEJES
CO-GENESIX                                  CO_GENESIX
CO-MICROSTRATEGY                            CO_MICROSTRATEGY
CO-TERMINAL_SERVER                          CO_TERMINAL_SERVER
 
 
Por Brasil:
 
BR-BRETAS                               --> BR_BRETAS
BR-CARTAO                                   BR_CARTAO
BR-EMPORIUM                                 BR_EMPORIUM
BR-NOTA_FISCAL                              BR_NOTA_FISCAL
BR-SITEF                                    BR_SITEF

# -----------------------------------------------------------------------------

20171130

Estoy en ~/Projects/ewatch/ewatch/early/views.py ...

Idea:

    en template detail.html, mostrar set de grupos asociados a pais, con <a rel > asociado a
    algo como ../group, de forma de en urlconfig detectar el grupo, vía expresion regular
    y capturarlo para luego, mostrar info habitual de hosts constituyentes

Amazing: It works !!!!

Temas abiertos:

- BRASIL, ahora se va de espaldas al no tener grupos ...    FIXED
- Agregar los paises restantes a la b.d FIXED

- Cambiar despliegue por lista ...  FIXED

# -----------------------------------------------------------------------------

20171130

César:

    - agregar, ícono o color a alertas
        Idea: template tag color = f(alert)     FIXED
        
    - según lo q hallé el otro día
        --> pais --> ip para consulta
                    (en el caso de chile hay que ir a 2 ip, "sumar" grupos y recordar ip asociado al grupo)
    - mirar maqueta ... para allá va la cosa
