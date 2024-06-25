from database.DB_connect import DBConnect
from model.gene import Gene


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select * from genes g where g.Essential = 'Essential'"""
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(Gene(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_all_nodes(genes_map):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct g.GeneID from genes g where g.Essential = 'Essential'"""
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(genes_map[row['GeneID']])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_all_edges(genes_map):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select i.GeneID1 , i.GeneID2 from interactions i where i.GeneID1 != i.GeneID2 """
        cursor.execute(query)
        result = []
        for row in cursor:
            try:
                result.append((genes_map[row['GeneID1']], genes_map[row['GeneID2']]))
            except KeyError:
                pass
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_all_pesi(genes_map):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select i.GeneID1 , i.GeneID2 , i.Expression_Corr 
                    from interactions i , genes g , genes g2 
                    where i.GeneID1 != i.GeneID2 and g.GeneId = i.GeneID1 and g2.GeneID = i.GeneID2 """
        cursor.execute(query)
        result = []
        for row in cursor:
            try:
                g1 = genes_map[row['GeneID1']]
                g2 = genes_map[row['GeneID2']]
                if g1.Chromosome == g2.Chromosome:
                    peso = 2*abs(row['Expression_Corr'])
                else:
                    peso = abs(row['Expression_Corr'])
                result.append((g1, g2, peso))
            except KeyError:
                pass
        cursor.close()
        cnx.close()
        return result
