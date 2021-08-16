from django.db import connection
from django.db import transaction


class Sqlca:
    """
    执行原生SQL
    """
    @staticmethod
    def execute_without_parms(sql):
        with connection.cursor() as cursor:
            cursor.execute(sql)
            # print(cursor.rowcount)
            if cursor.description!=None:
                columns = [col[0] for col in cursor.description]
                data=[dict(zip(columns, row))  for row in cursor.fetchall() ]

                return data
            else:
                return cursor.rowcount

    @staticmethod
    def execute(sql, params):
        # print(transaction.get_autocommit(using=None))
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            # print(cursor.rowcount)
            # rows = cursor.fetchall()
            # print(cursor.description)
            # print(rows)
            if cursor.description != None:
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                return data
            else:
                return cursor.rowcount


    #手工commit的函数
    def autocommit(if_autocommit):
        transaction.set_autocommit(if_autocommit, using=None)

    def commit(self):
        transaction.commit(using=None)

    def rollback(self):
        transaction.rollback(using=None)