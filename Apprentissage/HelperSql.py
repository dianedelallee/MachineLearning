import pypyodbc

class HelperSql(object):
    """description of class"""
    #transformation des données pour insertion dans tables sql à partir d'un
    #model python

    #recupère le nom des propriétés et les valeurs pour créer le slq
    #d'insertion
    def prepaData(dataModel,table):
        values = list(dataModel.__dict__.values())
        #transformation d'un item de type dict/list en str
        for n in range(len(values)):
            if type(values[n]) in (dict,list):
                values[n] = str(values[n])

        columns = ', '.join(dataModel.__dict__.keys())
        placeholders = ', '.join('?' * len(values))
        sql = 'INSERT INTO ' + table + '({}) VALUES ({})'.format(columns, placeholders)
        return {'sqlCmd':sql,'sqlValues':values}
                            

    #insertion dans un table sql
    def insertData(dataModel,table):
        cnxn = pypyodbc.connect('DRIVER={SQL Server};SERVER=NP6DEV60;DATABASE=gecko;Trusted_Connection=Yes')
        cursor = cnxn.cursor()
        sqlConfig = HelperSql.prepaData(dataModel,table)

        cursor.execute(sqlConfig['sqlCmd'], sqlConfig['sqlValues'])
        cursor.commit()
        cnxn.close()
    
    
