
from django.shortcuts import render, redirect
from django.contrib import messages
from mainapp.models import usuarios as modelo_usuario
from mainapp.models import tipos_documento_identidad as modelo_tipo
from mainapp.models import establecimientos as modelo_establecimiento
from mainapp.models import objetos_gasto as modelo_objeto
from mainapp.models import presupuestos_gastos as modelo_pyg
import hashlib

# Create your views here.

def initial(request):
    return render(request,'mainapp/initial.html')

def login(request):

    if request.method=="POST":

        correo_electronico=request.POST['correo_electronico']
        nombre_usuario=request.POST['nombre_usuario']
        clave=request.POST['clave'] 

        cifrado=hashlib.sha256()
        cifrado.update(clave.encode('utf8'))
        
        # Validar que no se repita un correo electrónico.
        filtrado=modelo_usuario.objects.filter(correo_electronico=correo_electronico)
        if len(filtrado)<1:
            messages.add_message(request=request,level=messages.WARNING,message="El correo electrónico ingresado no se encuentra registrado.")
            return redirect('url_login')
        # Validar que el correo y clave sean correctos.
        filtrado=modelo_usuario.objects.filter(correo_electronico=correo_electronico,nombre_usuario=nombre_usuario,clave=cifrado.hexdigest())
        if len(filtrado)<1:
            messages.add_message(request=request,level=messages.WARNING,message="El nombre de usuario y/o clave ingresados son incorrectos.")
            return redirect('url_login')
        return redirect('url_presupuestos_gastos')

    else:

        return render(request,'mainapp/login.html',{
            'titulo':'Ingresar',
        })

def register(request):

    if request.method=="POST":

        correo_electronico=request.POST['correo_electronico']
        nombre_usuario=request.POST['nombre_usuario']
        clave=request.POST['clave']
        tipo_documento_identidad=request.POST['tipo_documento_identidad']
        documento_identidad=request.POST['documento_identidad']
        nombres=request.POST['nombres']
        apellidos=request.POST['apellidos']
        cargo=request.POST['cargo']
        dependencia=request.POST['dependencia']
        # Validar si el correo electrónico ya está siendo usado por otro usuario.
        filtrado=modelo_usuario.objects.filter(correo_electronico=correo_electronico)
        if len(filtrado)>0:
            messages.add_message(request=request,level=messages.WARNING,message="El correo electrónico ingresado ya está siendo utilizado por un usuario.")
            return redirect('url_register')
        else:
            # usuario=modelo_usuario(correo_electronico=correo_electronico,nombre_usuario=nombre_usuario,clave=clave,tipo_documento_identidad_id=tipo_documento_identidad,documento_identidad=documento_identidad,nombres=nombres,apellidos=apellidos,cargo=cargo,dependencia=dependencia)
            cifrado=hashlib.sha256()
            cifrado.update(clave.encode('utf8'))
            usuario=modelo_usuario(correo_electronico=correo_electronico,nombre_usuario=nombre_usuario,clave=cifrado.hexdigest(),tipo_documento_identidad_id=tipo_documento_identidad,documento_identidad=documento_identidad,nombres=nombres,apellidos=apellidos,cargo=cargo,dependencia=dependencia)
            # Gaurdar el registro en la BD.
            usuario.save()
            messages.add_message(request=request,level=messages.SUCCESS,message="Se ha registrado correctamente.")
            return redirect('url_initial')

    else:

        op_tipo=modelo_tipo.objects.all()

        op_cargo=modelo_usuario.getCargo()
        lista_op_cargo=[]
        for cargo in op_cargo:
            dict_cargo={'bd':cargo[0],'human':cargo[1]}
            lista_op_cargo.append(dict_cargo)
        tupla_op_cargo=tuple(lista_op_cargo)

        op_dependencia=modelo_usuario.getDependencia()
        lista_op_dependencia=[]
        for dependencia in op_dependencia:
            dict_dependencia={'bd':dependencia[0],'human':dependencia[1]}
            lista_op_dependencia.append(dict_dependencia)
        tupla_op_dependencia=tuple(lista_op_dependencia)

        return render(request,'mainapp/register.html',{
            'titulo':'Registrarse',
            'op_tipo':op_tipo,
            'op_cargo':tupla_op_cargo,
            'op_dependencia':tupla_op_dependencia
        })

def establecimientos(request):

    establecimientos=modelo_establecimiento.objects.all()

    return render(request,'mainapp/establecimientos.html',{
        'titulo':'Establecimientos',
        'establecimientos':establecimientos
    })

def ingresarEstablecimiento(request):

    if request.method=="POST":
    
        codigo=request.POST['codigo']
        nombre=request.POST['nombre']
        jefe_zona=request.POST['jefe_zona']
        ciudad=request.POST['ciudad']
        telefono=request.POST['telefono']
        direccion=request.POST['direccion']

        establecimiento=modelo_establecimiento(codigo=codigo,nombre=nombre,jefe_zona=jefe_zona,ciudad=ciudad,telefono=telefono,direccion=direccion)
        # Guardar el registro en la BD.
        establecimiento.save()
        messages.add_message(request=request,level=messages.SUCCESS,message="Se ha creado el establecimiento correctamente.")
        return redirect('url_establecimientos')

    else:

        op_jefe_zona=modelo_establecimiento.getJefeZona()
        lista_op_jefe_zona=[]
        for jefe_zona in op_jefe_zona:
            dict_jefe_zona={'bd':jefe_zona[0],'human':jefe_zona[1]}
            lista_op_jefe_zona.append(dict_jefe_zona)
        tupla_op_jefe_zona=tuple(lista_op_jefe_zona)

        op_ciudad=modelo_establecimiento.getCiudad()
        lista_op_ciudad=[]
        for ciudad in op_ciudad:
            dict_ciudad={'bd':ciudad[0],'human':ciudad[1]}
            lista_op_ciudad.append(dict_ciudad)
        tupla_op_ciudad=tuple(lista_op_ciudad)

        return render(request,'mainapp/ingresar_establecimiento.html',{
            'titulo':'Ingresar establecimiento',
            'op_jefe_zona':tupla_op_jefe_zona,
            'op_ciudad':tupla_op_ciudad
        })

def editarEstablecimiento(request,establecimiento_id):
    
    if request.method=="POST":

        id=request.POST['id']
        codigo=request.POST['codigo']
        nombre=request.POST['nombre']
        jefe_zona=request.POST['jefe_zona']
        ciudad=request.POST['ciudad']
        telefono=request.POST['telefono']
        direccion=request.POST['direccion']

        # Editar registro en la BD.
        establecimiento=modelo_establecimiento.objects.get(id=int(id))
        establecimiento.codigo=codigo
        establecimiento.nombre=nombre
        establecimiento.jefe_zona=jefe_zona
        establecimiento.ciudad=ciudad
        establecimiento.telefono=telefono
        establecimiento.direccion=direccion
        establecimiento.save()
        messages.add_message(request=request,level=messages.SUCCESS,message="Se ha actualizado el establecimiento correctamente.")

        return redirect('url_establecimientos')

    else:

        establecimiento=modelo_establecimiento.objects.get(id=int(establecimiento_id))

        op_jefe_zona=modelo_establecimiento.getJefeZona()
        lista_op_jefe_zona=[]
        jefe_seleccionado=set()
        for jefe_zona in op_jefe_zona:
            dict_jefe_zona={'bd':jefe_zona[0],'human':jefe_zona[1]}
            lista_op_jefe_zona.append(dict_jefe_zona)
        lista_op_jefe_zona_2=[]
        for el in lista_op_jefe_zona:
            if el["bd"]!=establecimiento.jefe_zona: 
                lista_op_jefe_zona_2.append(el)
            else:
                jefe_seleccionado=el            
        tupla_op_jefe_zona=tuple(lista_op_jefe_zona_2)

        op_ciudad=modelo_establecimiento.getCiudad()
        lista_op_ciudad=[]
        ciudad_seleccionada=set()
        for ciudad in op_ciudad:
            dict_ciudad={'bd':ciudad[0],'human':ciudad[1]}
            lista_op_ciudad.append(dict_ciudad)
        lista_op_ciudad_2=[]
        for el in lista_op_ciudad:
            if el["bd"]!=establecimiento.ciudad: 
                lista_op_ciudad_2.append(el)
            else:
                ciudad_seleccionada=el
        tupla_op_ciudad=tuple(lista_op_ciudad_2)

        return render(request,'mainapp/editar_establecimiento.html',{
            'titulo':'Editar establecimiento',
            'establecimiento':establecimiento,
            'op_jefe_zona':tupla_op_jefe_zona,
            'op_ciudad':tupla_op_ciudad,
            'ciudad_seleccionada':ciudad_seleccionada,
            'jefe_seleccionado':jefe_seleccionado
        })

def eliminarEstablecimiento(request,establecimiento_id):
    establecimiento=modelo_establecimiento.objects.get(id=int(establecimiento_id))
    establecimiento.delete()
    messages.add_message(request=request,level=messages.SUCCESS,message="Se ha eliminado el establecimiento correctamente.")
    return redirect('url_establecimientos')

def objetosGasto(request):

    objetos_gasto=modelo_objeto.objects.all()
        
    return render(request,'mainapp/objetos_gasto.html',{
        'titulo':'Objetos de gasto',
        'objetos_gasto':objetos_gasto
    })

def ingresarObjetoGasto(request):
    
    if request.method=="POST":
    
        nombre=request.POST['nombre']
        descripcion=request.POST['descripcion']

        objeto_gasto=modelo_objeto(nombre=nombre,descripcion=descripcion)
       # Guardar el registro en la BD.
        objeto_gasto.save()
        messages.add_message(request=request,level=messages.SUCCESS,message="Se ha creado el objeto de gasto correctamente.")
        return redirect('url_objetos_gasto')

    else:

        return render(request,'mainapp/ingresar_objeto_gasto.html',{
            'titulo':'Ingresar objeto de gasto',
        })

def editarObjetoGasto(request,objeto_id):

    if request.method=="POST":

        id=request.POST['id']
        nombre=request.POST['nombre']
        descripcion=request.POST['descripcion']

        # Editar registro en la BD.
        objeto_gasto=modelo_objeto.objects.get(id=int(id))
        objeto_gasto.nombre=nombre
        objeto_gasto.descripcion=descripcion
        objeto_gasto.save()
        messages.add_message(request=request,level=messages.SUCCESS,message="Se ha actualizado el objeto de gasto correctamente.")

        return redirect('url_objetos_gasto')

    else:
        objeto_gasto=modelo_objeto.objects.get(id=int(objeto_id))
        return render(request,'mainapp/editar_objeto_gasto.html',{
            'titulo':'Editar objeto de gasto',
            'objeto_gasto':objeto_gasto,
        })

def eliminarObjetoGasto(request,objeto_id):
    objeto_gasto=modelo_objeto.objects.get(id=int(objeto_id))
    objeto_gasto.delete()
    messages.add_message(request=request,level=messages.SUCCESS,message="Se ha eliminado el objeto de gasto correctamente.")
    return redirect('url_objetos_gasto')

def presupuestosGastos(request):

    return render(request,'mainapp/presupuestos_gastos.html',{
        'titulo':'Presupuestos y gastos',

    })

def ingresarPyG(request):
    
    if request.method=="POST":
    
        inicio=request.POST['inicio']

        if inicio=="1":
            anio=request.POST['anio']
            establecimiento_id=request.POST['establecimiento']
            filtro=modelo_establecimiento.objects.filter(id=establecimiento_id)
            establecimiento_nombre=filtro[0].nombre
            objeto_id=request.POST['objeto']
            filtro=modelo_objeto.objects.filter(id=objeto_id)
            objeto_nombre=filtro[0].nombre
            # Revisar si estos datos ya existen en la BD o si en cambio se pueden ingresar.
            registros_pyg=modelo_pyg.objects.filter(anio=int(anio),establecimiento_id=establecimiento_id,objeto_gasto_id=objeto_id)
            if registros_pyg:
                messages.add_message(request=request,level=messages.WARNING,message="Ya se ingresaron los datos correspondientes al año, establecimiento y objeto de gasto ingresados.")
                return redirect('url_presupuestos_gastos')
            else:
                return render(request,'mainapp/ingresar_pyg.html',{
                    'titulo':'Ingresar Presupuestos y gastos', 
                    'anio':anio,
                    'establecimiento_nombre':establecimiento_nombre,
                    'establecimiento_id':establecimiento_id,
                    'objeto_nombre':objeto_nombre,
                    'objeto_id':objeto_id,
                    'inicio':0,
                })
        else:
            # Se leen datos del formulario.
            anio=request.POST['anio']
            establecimiento_id=request.POST['establecimiento_id']
            objeto_id=request.POST['objeto_id']
            lista_mes=[1,2,3,4,5,6,7,8,9,10,11,12]
            pre_ene=request.POST['pre_ene']
            pre_feb=request.POST['pre_feb']
            pre_mar=request.POST['pre_mar']
            pre_abr=request.POST['pre_abr']
            pre_may=request.POST['pre_may']
            pre_jun=request.POST['pre_jun']
            pre_jul=request.POST['pre_jul']
            pre_ago=request.POST['pre_ago']
            pre_sep=request.POST['pre_sep']
            pre_oct=request.POST['pre_oct']
            pre_nov=request.POST['pre_nov']
            pre_dic=request.POST['pre_dic']
            lista_pre=[pre_ene,pre_feb,pre_mar,pre_abr,pre_may,pre_jun,pre_jul,pre_ago,pre_sep,pre_oct,pre_nov,pre_dic]
            gas_ene=request.POST['gas_ene']
            gas_feb=request.POST['gas_feb']
            gas_mar=request.POST['gas_mar']
            gas_abr=request.POST['gas_abr']
            gas_may=request.POST['gas_may']
            gas_jun=request.POST['gas_jun']
            gas_jul=request.POST['gas_jul']
            gas_ago=request.POST['gas_ago']
            gas_sep=request.POST['gas_sep']
            gas_oct=request.POST['gas_oct']
            gas_nov=request.POST['gas_nov']
            gas_dic=request.POST['gas_dic']
            lista_gas=[gas_ene,gas_feb,gas_mar,gas_abr,gas_may,gas_jun,gas_jul,gas_ago,gas_sep,gas_oct,gas_nov,gas_dic]
            pos=0
            for mes in lista_mes:
                pyg=modelo_pyg(anio=anio,mes=mes,establecimiento_id=establecimiento_id,objeto_gasto_id=objeto_id,presupuesto=lista_pre[pos],gasto=lista_gas[pos])
                # Guardar el registro en la base de datos.
                pyg.save()
                pos+=1
            messages.add_message(request=request,level=messages.SUCCESS,message="Se ha ingresado la información correctamente.")
            return redirect('url_presupuestos_gastos')
    else:

        op_establecimiento=modelo_establecimiento.objects.all()
        op_objeto=modelo_objeto.objects.all()

        return render(request,'mainapp/ingresar_pyg.html',{
            'titulo':'Ingresar Presupuestos y gastos', 
            'op_establecimiento': op_establecimiento,
            'op_objeto':op_objeto,
            'inicio':1,
        })

def formatoDecimal(decimal):
    return format( round(decimal,2) ,',.2f')

def mostrarInformes(request):
    
    if request.method=="POST":

        anio=request.POST['anio']

        establecimientos=modelo_establecimiento.objects.all()
        objetos=modelo_objeto.objects.all()
        meses=[1,2,3,4,5,6,7,8,9,10,11,12]

        # Verificar si hay registros con ese año.
        registros_anio=modelo_pyg.objects.filter(anio=int(anio))

        if registros_anio:

            # Extraer registros registros de presupuestos y gastos.

            lista_por_est=[]
            for establecimiento in establecimientos:
                registros_est=modelo_pyg.objects.filter(anio=int(anio),establecimiento=establecimiento.id)

                lista_por_objeto=[]
                if registros_est: 
                    print("\nHas registros en el establecimiento: {0}\n".format(establecimiento))
                    for objeto in objetos:
                        registros_objeto=modelo_pyg.objects.filter(anio=int(anio),establecimiento=establecimiento.id,objeto_gasto=objeto.id)

                        lista_por_mes=[]
                        if registros_objeto:
                            for mes in meses:
                                registros_mes=modelo_pyg.objects.filter(anio=int(anio),establecimiento=establecimiento.id,objeto_gasto=objeto.id,mes=mes)
                                for registro in registros_mes:
                                    registro.presupuesto=formatoDecimal(registro.presupuesto)
                                    registro.gasto=formatoDecimal(registro.gasto)
                                lista_por_mes.append(registros_mes)

                        lista_por_objeto.append(lista_por_mes)

                lista_por_est.append(lista_por_objeto)

            return render(request,'mainapp/informes.html',{
                'titulo':'Informes',
                'anio':anio,
                'establecimientos':establecimientos,
                'lista_por_est':lista_por_est,
            })

        else:

            messages.add_message(request=request,level=messages.INFO,message="No hay registros para el año ingresado.")
            return redirect('url_mostrar_informes')

    else:

        return render(request,'mainapp/mostrar_informes.html',{
            'titulo':'Mostrar Informes',
        })