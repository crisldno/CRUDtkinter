import conexion as con

def save(persona):
    persona=dict(persona)
    try:
        db = con.conectar()
        cursor = db.cursor()
        columnas = tuple(persona.keys())
        valores = tuple(persona.values())
        sql = """
        INSERT INTO personas{campos} VALUES(?,?,?,?,?,?) 
        """.format(campos=columnas)

        cursor.execute(sql,(valores))
        creada = cursor.rowcount>0
        db.commit()
        if creada:
            cursor.close()
            db.close()
            return {"respuesta":creada,"mensaje":"persona registrada"}
        else:
            cursor.close()
            db.close()
            return {"respuesta":creada,"mensaje":"persona no registrada"}
    except Exception as ex:
        if "UNIQUE" in str (ex) and "correo" in str (ex):
            mensaje = "Ya existe una persona con ese correo"
        elif "UNIQUE" in str (ex) and "dni" in str (ex):
            mensaje = "Ya existe una persona con ese dni"
        else :
            mensaje = str (ex)
            cursor.close()
            db.close()
        return {"respuesta": False, "mensaje": mensaje}


def findAll():
    try:
        db = con.conectar()
        cursor=db.cursor()
        cursor.execute("SELECT * FROM personas")
        personas=cursor.fetchall()
        if personas:
            cursor.close()
            db.close()
            return {"respuesta":True,"personas":personas,"mensaje":"Listado OK"}
        else:
            cursor.close()
            db.close()
            return {"respuesta":False,"personas":personas,"mensaje":"No Hay personas registradas"}
    except Exception as ex:
        cursor.close()
        db.close()
        return {"respuesta":False,"mensaje":str(ex)}


def find(dniPersona):
    try:
        db = con.conectar()
        cursor=db.cursor()
        cursor.execute("SELECT * FROM personas WHERE dni='{dni}'".format(dni=dniPersona))
        res=cursor.fetchall()
        if res:
            info=res[0]
            persona= {"id":info[0],"dni":info[1],"edad":info[2],"nombre":info[3],"apellido":info[4],"direccion":info[5],"correo":info[6]}

            cursor.close()
            db.close()
            return {"respuesta":True,"persona":persona,"mensaje":"Persona encontada"}
        else:
            cursor.close()
            db.close()
            return {"respuesta":False,"mensaje":"Persona no encontrada"}
    except Exception as ex:
        cursor.close()
        db.close()
        return {"respuesta":False,"mensaje":str(ex)}


def update(persona):
    try:
        db = con.conectar()
        cursor = db.cursor()
        persona = dict(persona)
        dniPersona = persona.get('dni')
        persona.pop('dni')
        valores = tuple(persona.values())
        sql = """
        UPDATE personas 
        SET edad=?,nombre=?,apellido=?,direccion=?,correo=?
        WHERE dni = ?
        """
        cursor.execute(sql, valores + (dniPersona,))
        modificada = cursor.rowcount > 0
        db.commit()
        cursor.close()
        db.close()
        if modificada:
            return {"respuesta": modificada, "mensaje": "persona actualizada"}
        else:
            return {"respuesta": modificada, "mensaje": "no existe la persona con ese dni"}
    except Exception as ex:
        if "UNIQUE" in str(ex) and "correo" in str(ex):
            mensaje = "Ya existe una persona con ese correo"
        else:
            mensaje = str(ex)
        cursor.close()
        db.close()
        return {"respuesta": False, "mensaje": mensaje}


def delete(idPersona):
    try:
        db = con.conectar()
        cursor = db.cursor()

        sql="""
        DELETE FROM personas WHERE id='{id}'""".format(id=idPersona)

        cursor.execute(sql)
        eliminada = cursor.rowcount>0
        db.commit()
        cursor.close()
        db.close()
        if eliminada:
            return {"respuesta":eliminada,"mensaje":"persona eliminada"}
        else:
            return {"respuesta": eliminada, "mensaje": "no existe la persona con ese id"}
    except Exception as ex:
        cursor.close()
        db.close()
        return {"respuesta":False,"mensaje":str(ex)}




