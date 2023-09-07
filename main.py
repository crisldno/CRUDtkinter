from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import PersonaDatos as crud
import conexion

#ventana
v = Tk()
v.title("Aplicacion con base de datos")

ancho=450
alto=400
x_v =v.winfo_screenwidth()//2 - ancho //2
y_v =v.winfo_screenheight()//2 - ancho //2
pos = str(ancho)+"x"+str(alto)+"+"+str(x_v)+"+"+str(y_v)
v.geometry(pos)
v.state("zoomed")
v.configure(bg="#fff")

######### variables #########

txt_id = StringVar()
txt_dni = StringVar()
txt_edad = StringVar()
txt_nombre = StringVar()
txt_apellido = StringVar()
txt_direccion = StringVar()
txt_correo = StringVar()

######### funciones #########
def creditos():
    messagebox.showinfo("Creditos",
                        """Creado por: Cristian Londoño
                        
                        Instagram: cristian.ldno
                        
                        Correo: c.clo1020.clo@gmail.com
                        
                        Contacto: 3113740259
                        
                        """
                        )

def salir():
    res = messagebox.askquestion("Salir","¿Desea salir de la App")
    if res == "yes":
        v.destroy()


def llenarTabla():
    tabla.delete(*tabla.get_children())
    res=crud.findAll()
    personas=res.get("personas")
    for fila in personas:
        row = list(fila)
        row.pop(0)
        row = tuple(row)
        tabla.insert("",END,text=id,values=row)

def limpiarCampos():
    txt_dni.set("")
    txt_edad.set("")
    txt_nombre.set("")
    txt_apellido.set("")
    txt_direccion.set("")
    txt_correo.set("")
    e_dni.focus()

def guardar():
    if txt_edad.get().isnumeric():
        per={"dni":txt_dni.get(),"edad":int(txt_edad.get()),"nombre":txt_nombre.get(),"apellido":txt_apellido.get(),"direccion":txt_direccion.get(),"correo":txt_correo.get()}
        res = crud.save(per)
        if res.get("respuesta"):
            llenarTabla()
            messagebox.showinfo("OK",res.get("mensaje"))
            limpiarCampos()
        else:
            messagebox.showerror("Error", res.get("mensaje"))
    else:
        txt_edad.set("")
        e_edad.focus()
        messagebox.showerror("Upps!","La edad debe ser numerica")

def consultar():
    if txt_dni.get()!="":
        res = crud.find(txt_dni.get())
        if res.get("respuesta"):
            persona = res.get("persona")
            txt_edad.set(persona.get("edad"))
            txt_nombre.set(persona.get("nombre"))
            txt_apellido.set(persona.get("apellido"))
            txt_direccion.set(persona.get("direccion"))
            txt_correo.set(persona.get("correo"))
        else:
            e_dni.focus()
            limpiarCampos()
            messagebox.showerror("Upps!", "La persona no existe")
    else:
        e_dni.focus()
        limpiarCampos()
        messagebox.showerror("Upps!", "Ingrese el DNI")

def actualizar():
    if txt_edad.get().isnumeric():
        per = {"dni":txt_dni.get(),"edad":int(txt_edad.get()),"nombre":txt_nombre.get(),"apellido":txt_apellido.get(),"direccion":txt_direccion.get(),"correo":txt_correo.get()}
        res = crud.update(per)
        if res.get("respuesta"):
            llenarTabla()
            messagebox.showinfo("OK",res.get("mensaje"))
            limpiarCampos()
        else:
            messagebox.showerror("Error", res.get("mensaje"))
    else:
        txt_edad.set("")
        e_edad.focus()
        messagebox.showerror("Upps!","La edad debe ser numerica")


def eliminar():
    if txt_dni.get()!="":
        res = crud.find(txt_dni.get())

        if res.get("respuesta"):
            per = res.get("persona")
            respuesta=messagebox.askquestion("confirmar","¿Realmente desea eliminar a {nombre} {apellido}".format(nombre=per.get("nombre"),apellido=per.get("apellido")))
            if respuesta == "yes":
                res = crud.delete(per.get("id"))
                if res.get("respuesta"):
                    llenarTabla()
                    limpiarCampos()
                    messagebox.showinfo("OK", res.get("mensaje"))
                else:
                    messagebox.showwarning("Upss!","no se logro eliminr la persona",+res.get("mensaje"))
        else:
            messagebox.showwarning("Upss!", "no existe la persona")
            limpiarCampos()
    else:
        e_dni.focus()
        messagebox.showerror("Upps!","Debe indicar el Dni")

######### fin funciones #########

######### interfaz #########

fuente = ("verdana",12)
Label(v,text="DNI:",anchor="w",justify="left",width=10,bg="lightgreen",font=fuente).grid(row=0,column=0,padx=10,pady=5)
Label(v,text="EDAD:",anchor="w",justify="left",width=10,bg="lightgreen",font=fuente).grid(row=1,column=0,padx=10,pady=5)
Label(v,text="NOMBRE:",anchor="w",justify="left",width=10,bg="lightgreen",font=fuente).grid(row=2,column=0,padx=10,pady=5)
Label(v,text="APELLIDO:",anchor="w",justify="left",width=10,bg="lightgreen",font=fuente).grid(row=3,column=0,padx=10,pady=5)
Label(v,text="DIRECCION:",anchor="w",justify="left",width=10,bg="lightgreen",font=fuente).grid(row=4,column=0,padx=10,pady=5)
Label(v,text="CORREO:",anchor="w",justify="left",width=10,bg="lightgreen",font=fuente).grid(row=5,column=0,padx=10,pady=5)

###INPUTS###

e_dni = ttk.Entry(v,font=fuente,textvariable=txt_dni)
e_edad = ttk.Entry(v,font=fuente,textvariable=txt_edad)
e_nombre = ttk.Entry(v,font=fuente,textvariable=txt_nombre)
e_apellido = ttk.Entry(v,font=fuente,textvariable=txt_apellido)
e_direcccion = ttk.Entry(v,font=fuente,textvariable=txt_direccion)
e_correo = ttk.Entry(v,font=fuente,textvariable=txt_correo)


e_dni.grid(row=0,column=1)
e_edad.grid(row=1,column=1)
e_nombre.grid(row=2,column=1)
e_apellido.grid(row=3,column=1)
e_direcccion.grid(row=4,column=1)
e_correo.grid(row=5,column=1)

iconGuardar = PhotoImage(file="guardar.png")
iconBuscar = PhotoImage(file="buscar.png")
iconActualizar = PhotoImage(file="actualizar.png")
iconEliminar = PhotoImage(file="eliminar.png")

### botones
ttk.Button(v,text="Guardar",command=guardar,image=iconGuardar,compound=LEFT).place(x=10,y=220)
ttk.Button(v,text="Consultar",command=consultar,image=iconBuscar,compound=LEFT).place(x=120,y=220)
ttk.Button(v,text="Actualizar",command=actualizar,image=iconActualizar,compound=LEFT).place(x=230,y=220)
ttk.Button(v,text="Eliminar",command=eliminar,image=iconEliminar,compound=LEFT).place(x=340,y=220)

Label(v,text="LISTA DE PERSONAS",font=("Arial",16),bg="#fff").place(x=600,y=5)

tabla = ttk.Treeview(v)
tabla.place(x=450,y=40)
tabla["columns"]=("DNI","EDAD","NOMBRE","APELLIDO","DIRECCION","CORREO")
tabla.column("#0",width=0,stretch=NO)
tabla.column("DNI",width=100,anchor=CENTER)
tabla.column("EDAD",width=100,anchor=CENTER)
tabla.column("NOMBRE",width=150,anchor=CENTER)
tabla.column("APELLIDO",width=150,anchor=CENTER)
tabla.column("DIRECCION",width=160,anchor=CENTER)
tabla.column("CORREO",width=160,anchor=CENTER)
tabla.heading("#0",text="")
tabla.heading("DNI",text="DNI")
tabla.heading("EDAD",text="EDAD")
tabla.heading("NOMBRE",text="NOMBRE")
tabla.heading("APELLIDO",text="APELLIDO")
tabla.heading("DIRECCION",text="DIRECCION")
tabla.heading("CORREO",text="CORREO")


##### MENU #####
menuTop = Menu(v)#barra de menu superior
m_archivo = Menu(menuTop,tearoff=0)
m_archivo.add_command(label="Creditos",command=creditos)
m_archivo.add_command(label="Salir",command=salir)
menuTop.add_cascade(label="Archivo",menu=m_archivo)


m_limpiar = Menu(menuTop,tearoff=0)
m_limpiar.add_command(label="limpiar campos",command=limpiarCampos)
menuTop.add_cascade(label="Limpiar",menu=m_limpiar)


m_Crud = Menu(menuTop,tearoff=0)
m_Crud.add_command(label="Guardar",command=guardar, image=iconGuardar,compound=LEFT)
m_Crud.add_command(label="Consultar",command=consultar,image=iconBuscar,compound=LEFT)
m_Crud.add_command(label="Actualizar",command=actualizar,image=iconActualizar,compound=LEFT)
m_Crud.add_command(label="Eliminar",command=eliminar,image=iconEliminar,compound=LEFT)
menuTop.add_cascade(label="CRUD",menu=m_Crud)


v.config(menu=menuTop)

e_dni.focus()

llenarTabla()
v.mainloop()