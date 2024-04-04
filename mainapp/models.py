from django.db import models

# Create your models here.

class tipos_documento_identidad(models.Model):

    # Atributos.
    id=models.PositiveSmallIntegerField(auto_created=True,primary_key=True,verbose_name='ID')
    nomenclatura=models.CharField(max_length=150,verbose_name="Nomenclatura")
    nombre=models.CharField(max_length=350,verbose_name="Nombre")

    class Meta:
        verbose_name='Tipo de documento de identidad'
        verbose_name_plural='Tipos de documento de identidad'

    def __str__(self):
        return self.nomenclatura  

    def obtenerIdNom(self):
            return (self.id, self.nomenclatura)

opciones_cargo=[("DA", "DIRECTOR DE ARQUITECTURA"),("AA", "AUXILIAR DE ARQUITECTURA"),("DC", "DIRECTOR DE CONTABILIDAD"),("AC", "AUXILIAR DE CONTABILIDAD")]
opciones_dependencia=[("ARQ", "ARQUITECTURA"),("CONT", "CONTABILIDAD")]

class usuarios(models.Model):
    
    # Atributos.
    correo_electronico=models.EmailField(max_length=250,verbose_name="Correo electrónico",unique=True)
    nombre_usuario=models.CharField(max_length=350,verbose_name="Nombre de usuario")
    clave=models.CharField(max_length=350,verbose_name="Clave")
    tipo_documento_identidad=models.ForeignKey(tipos_documento_identidad,editable=True,verbose_name="Tipo de documento de identidad",on_delete=models.CASCADE,null=True)
    documento_identidad=models.CharField(max_length=350,verbose_name="Documento de identidad")
    nombres=models.CharField(max_length=350,verbose_name="Nombres")
    apellidos=models.CharField(max_length=350,verbose_name="Apellidos")
    cargo=models.CharField(
        max_length=3,
        choices=opciones_cargo,
        null=True,
        verbose_name="Cargo"
    )
    dependencia=models.CharField(
        max_length=10,
        choices=opciones_dependencia,
        null=True,
        verbose_name="Dependencia"
    )
    fecha_registro=models.DateField(auto_now_add=True,verbose_name="Fecha de registro")

    class Meta:
        verbose_name='Usuario'
        verbose_name_plural='Usuarios'

    def __str__(self):
        return self.nombre_usuario

    def getCargo():
        return(opciones_cargo)

    def getDependencia():
        return(opciones_dependencia)

opciones_jefe_zona=[("ALE_SAU", "ALEX SAUVET"),("MER_CHA", "MERLINA CHÁVEZ"),("JHO_CAS", "JHON CASTILLO")]
opciones_ciudad=[("MED", "MEDELLÍN"),("BEL", "BELLO"),("SAN_MAR", "SANTA MARTA"),("CAL", "CALI"),("BOG", "BOGOTÁ"),("IPI", "IPIALES")]

class establecimientos(models.Model):

    # Atributos.
    codigo=models.CharField(max_length=250,verbose_name="Código")
    nombre=models.CharField(max_length=350,verbose_name="Nombre")
    jefe_zona=models.CharField(
        max_length=10,
        choices=opciones_jefe_zona,
        null=True,
        verbose_name="Jefe de zona"
    )
    ciudad=models.CharField(
        max_length=10,
        choices=opciones_ciudad,
        null=True,
        verbose_name="Ciudad"
    )
    telefono=models.BigIntegerField(verbose_name="Teléfono")
    direccion=models.CharField(max_length=500,verbose_name="Dirección")

    class Meta:
        verbose_name='Establecimiento'
        verbose_name_plural='Establecimientos'

    def __str__(self):
        return self.nombre

    def getJefeZona():
        return(opciones_jefe_zona)

    def getCiudad():
        return(opciones_ciudad)

class objetos_gasto(models.Model):

    # Atributos.
    nombre=models.CharField(max_length=350,verbose_name="Nombre") 
    descripcion=models.CharField(max_length=500,verbose_name="Descripción")   

    class Meta:
        verbose_name='Objeto de gasto'
        verbose_name_plural='Objetos de gasto'

    def __str__(self):
        return self.nombre

class presupuestos_gastos(models.Model):
    
    # Atributos.
    anio=models.BigIntegerField(verbose_name="Año")
    mes=models.SmallIntegerField(verbose_name="Mes")
    establecimiento=models.ForeignKey(establecimientos,editable=True,verbose_name="Establecimiento",on_delete=models.CASCADE,null=True)
    objeto_gasto=models.ForeignKey(objetos_gasto,editable=True,verbose_name="Objeto de gasto",on_delete=models.CASCADE,null=True)
    presupuesto=models.DecimalField(verbose_name="Presupuesto",max_digits=60,decimal_places=30)
    gasto=models.DecimalField(verbose_name="Gasto",max_digits=60,decimal_places=30)
    fecha_creacion=models.DateField(auto_now_add=True,verbose_name="Fecha de creación")

    class Meta:
        verbose_name='Objeto de gasto'
        verbose_name_plural='Objetos de gasto'

    def __str__(self):
        return self.id