#!/usr/bin/python3
# -*-coding:utf-8 -*


from entity.caption import Caption
from repo.db_connection import serverConnect


class CaptionDAO:
    """
    """
    @staticmethod
    def create(caption):
        """
        :param caption: Caption
        error : 'pymysql.err.IntegrityError: (1062, "Duplicata du champ 'mac1' pour la clef 'PRIMARY'")
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = "INSERT INTO `caption` (`mac_address`, `name`, `active`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (caption.macAddress, caption.name, caption.active))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def getAll(**kwargs):
        """
        option keywords is active : type Boolean
        :return: Array of Caption
        """
        result = []
        con = serverConnect()
        with con:
            cur = con.cursor()
            sql = "SELECT `mac_address`, `name`, `active` FROM `caption`"
            if 'active' in kwargs:
                sql = sql + " where active = " + str(1 if kwargs['active'] else 0)
                sql = sql + " order by name"
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                result.append(Caption(row["mac_address"], row["name"], row["active"]))
            cur.close()
        con.close()
        return result

    @staticmethod
    def getByMacAddress(macAddress):
        """
        :param macAddress: String
        :return: Caption
        """
        con = serverConnect()
        result = None
        with con:
            cur = con.cursor()
            cur.execute("SELECT `mac_address`, `name`, `active` FROM `caption` WHERE `mac_address` = %s",macAddress)
            row = cur.fetchone()
            if row is not None:
                result = Caption(row["mac_address"], row["name"], row["active"])
            cur.close()
        con.close()
        return result

    @staticmethod
    def update(caption):
        """
        :param caption: Caption
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = "UPDATE `caption` SET `name` =%s, `active` =%s WHERE `mac_address` = %s"
            cursor.execute(sql, (caption.name, caption.active, caption.macAddress))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def delete(caption):
        """
        :param caption: Caption
        """
        connection = serverConnect()
        with connection.cursor() as cursor:
            sql = "DELETE FROM `caption` WHERE `mac_address` = %s"
            cursor.execute(sql, (caption.macAddress))
        connection.commit()
        cursor.close()
        connection.close()

if __name__ == '__main__':
    aCaption = Caption("macAdress", "name", False)
    CaptionDAO.create(aCaption)
    aCaption = CaptionDAO.getByMacAddress("macAdress")
    print("Adresse Mac:{0} Nom:{1} active:{2}".format(aCaption.macAddress, aCaption.name, aCaption.active))
    if aCaption.active:
        print("actif")
    else:
        print("inactif")
    aCaption.active = True
    if aCaption.active:
        print("actif")
    else:
        print("inactif")
    CaptionDAO.update(aCaption)
    print("----            All            ----")
    for caption in CaptionDAO.getAll():
        print("Adresse Mac:{0} Nom:{1} active:{2}".format(caption.macAddress, caption.name, caption.active))
    print("----           Active          ----")
    for caption in CaptionDAO.getAll(active=True):
        print("Adresse Mac:{0} Nom:{1} active:{2}".format(caption.macAddress, caption.name, caption.active))
    print("----          Inactive         ----")
    for caption in CaptionDAO.getAll(active=False):
        print("Adresse Mac:{0} Nom:{1} active:{2}".format(caption.macAddress, caption.name, caption.active))
    print("-----------------------------------")
    CaptionDAO.delete(aCaption)
    """aCaption.name = "new Name2"
    aCaption = CaptionDAO.getByMacAddress("mac2")
    CaptionDAO.update(aCaption)
    for caption in CaptionDAO.getAll():
        print("Adresse Mac:{0} Nom:{1}".format(caption.macAddress, caption.name))
    CaptionDAO.delete(aCaption)
    for caption in CaptionDAO.getAll():
        print("Adresse Mac:{0} Nom:{1}".format(caption.macAddress, caption.name))"""
