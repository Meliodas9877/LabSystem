import json
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework.views import APIView

from api.rawsql import Sqlca


class SelectStu ( APIView ):
    def get(self, request):
        page_index = int ( request.query_params['page'] )
        page_size = int ( request.query_params['results'] )
        sort = request.GET.get ( 'sortField' )
        order = request.GET.get ( 'sortOrder' )
        gender = request.GET.get ( 'gender' )
        type = request.GET.get ( 'studentType' )
        searchTerm = request.GET.get ( 'searchTerm' )
        page = (page_index - 1) * page_size

        if sort == 'schoolYear':
            if order == 'ascend':
                sen_sort = ' ORDER BY "schoolYear" ASC '
            elif order == 'descend':
                sen_sort = ' ORDER BY "schoolYear" DESC '
            else:
                sen_sort = ' '
        elif sort == 'studentId':
            if order == 'ascend':
                sen_sort = ' ORDER BY "studentId" ASC '
            elif order == 'descend':
                sen_sort = ' ORDER BY "studentId" DESC '
            else:
                sen_sort = ' '
        else:
            sen_sort = ' '

        if searchTerm != 'null' and searchTerm:
            if searchTerm.isdigit ():
                sen_search = 'and "studentId" ~ ' + '\'' + str ( searchTerm ) + '\''
                sen_searchw = ' where "studentId" ~ ' + '\'' + str ( searchTerm ) + '\''
            else:
                sen_search = ' and "studentName" ~ ' + '\'' + str ( searchTerm ) + '\''
                sen_searchw = ' where "studentName" ~ ' + '\'' + str ( searchTerm ) + '\''
        else:
            sen_search = ''
            sen_searchw = ''

            # print  ('页码=',page_index,'，','每页',page_size,'条','，','Sql 语句为：',string_sort,'，','性别：',gender,'，','种类：',type,'，','第几条开始：',page)
        try:
            if gender != None and type != None:
                sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo","avatarUrl" from student where "studentType"=%s and gender=%s' +sen_search+ sen_sort + 'limit %s offset %s'
                data = Sqlca.execute ( sql, [type, gender, page_size, page] )
                totalSql = 'select count("studentId") AS num from student where "studentType"=%s and gender=%s'
                total1 = Sqlca.execute ( totalSql, [type, gender] )
                total2 = total1[0].get ( 'num' )
            elif gender != None and type == None:
                sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo","avatarUrl" from student where gender=%s ' +sen_search+ sen_sort + 'limit %s offset %s'
                data = Sqlca.execute ( sql, [gender, page_size, page] )
                totalSql = 'select count("studentId") AS num from student where gender=%s'
                total1 = Sqlca.execute ( totalSql, [gender] )
                total2 = total1[0].get ( 'num' )
            elif gender == None and type != None:
                sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo","avatarUrl" from student where "studentType"=%s ' +sen_search+ sen_sort + 'limit %s offset %s'
                data = Sqlca.execute ( sql, [type, page_size, page] )
                totalSql = 'select count("studentId") AS num from student where "studentType"=%s'
                total1 = Sqlca.execute ( totalSql, [type] )
                total2 = total1[0].get ( 'num' )
            else:
                sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo","avatarUrl" from student ' +sen_searchw+ sen_sort + 'limit %s offset %s'
                data = Sqlca.execute ( sql, [page_size, page] )
                totalSql = 'select count("studentId") AS num from student '
                total1 = Sqlca.execute ( totalSql, [] )
                total2 = total1[0].get ( 'num' )
            rtn = {'code': 1000, 'message': '查询成功',
                   'data': {'pageIndex': page_index, 'pageSize': page_size, 'total': total2, 'data': data}}

        except Exception as errordetail:
            rtn = {'code': 1001, 'message': '查询失败，原因：' + str ( errordetail ), 'data': {}}
        return Response ( rtn )

        # if type != 'null' and type:
        #     print ( "000" )
        #     if gender != 'null' and gender:
        #         print ( "step1" )
        #         if sort == 'studentId':
        #             if order == 'ascend':
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where "studentType"= %s and gender=%s  order by "studentId" ASC limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [type, gender, page_size, page] )
        #             else:
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where "studentType"= %s and gender=%s  order by "studentId" DESC limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [type, gender, page_size, page] )
        #         elif sort == 'schoolYear':
        #             if order == 'ascend':
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where "studentType"= %s and gender=%s  order by "schoolYear" ASC limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [type, gender, page_size, page] )
        #             else:
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where "studentType"= %s and gender=%s order by "schoolYear" DESC limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [type, gender, page_size, page] )
        #         else:
        #             sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where "studentType"= %s and gender=%s limit %s offset %s'
        #             data = Sqlca.execute ( sql, [type, gender, page_size, page] )
        #         totalSql = 'select count("studentId") AS num from student  where "studentType"= %s and gender=%s '
        #         total1 = Sqlca.execute ( totalSql, [type, gender] )
        #         total2 = total1[0].get ( 'num' )
        #         print ( total2 )
        #     else:
        #         if sort == "studentId":
        #             if order == "ascend":
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where "studentType"= %s  order by "studentId" limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [type, page_size, page] )
        #             else:
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where "studentType"= %s  order by "studentId" DESC limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [type, page_size, page] )
        #         elif sort == "schoolYear":
        #             if order == "ascend":
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where "studentType"= %s  order by "schoolYear" limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [type, page_size, page] )
        #             else:
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where "studentType"= %s  order by "schoolYear" DESC limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [type, page_size, page] )
        #         else:
        #             sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where "studentType"= %s limit %s offset %s'
        #             data = Sqlca.execute ( sql, [type, page_size, page] )
        #         totalSql = 'select count("studentId") AS num from student  where "studentType"= %s '
        #         total1 = Sqlca.execute ( totalSql, [type] )
        #         total2 = total1[0].get ( 'num' )
        #         print ( total2 )
        # else:
        #     if gender != 'null' and gender:
        #         if sort == "studentId":
        #             if order == "ascend":
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where gender= %s order by "studentId" limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [gender, page_size, page] )
        #             else:
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where gender= %s order by "studentId" DESC limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [gender, page_size, page] )
        #         elif sort == "schoolYear":
        #             if order == "ascend":
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where gender= %s order by "schoolYear" limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [gender, page_size, page] )
        #             else:
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where gender= %s order by "schoolYear" DESC limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [gender, page_size, page] )
        #         else:
        #             sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo" from student where gender= %s  limit %s offset %s'
        #             data = Sqlca.execute ( sql, [gender, page_size, page] )
        #         totalSql = 'select count("studentId") AS num from student  where "gender"= %s '
        #         total1 = Sqlca.execute ( totalSql, [gender] )
        #         total2 = total1[0].get ( 'num' )
        #         print ( total2 )
        #     else:
        #         if sort == "studentId":
        #             if order == "ascend":
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo"  from student  order by "studentId" limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [page_size, page] )
        #             else:
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo"  from student  order by "studentId" desc limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [page_size, page] )
        #         elif sort == "schoolYear":
        #             if order == "ascend":
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo"  from student  order by "schoolYear" limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [page_size, page] )
        #             else:
        #                 sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo"  from student  order by "schoolYear" desc limit %s offset %s'
        #                 data = Sqlca.execute ( sql, [page_size, page] )
        #         else:
        #             sql = 'select "studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo"  from student limit %s offset %s'
        #             data = Sqlca.execute ( sql, [page_size, page] )
        #         totalSql = 'select count("studentId") AS num from student  '
        #         total1 = Sqlca.execute ( totalSql, [gender] )
        #         total2 = total1[0].get ( 'num' )
        #         print ( total2 )

    def post(self, request):
        data = request.data
        password = data['idNo'][12:]
        schoolYear = data['studentId'][:4]
        sql = 'insert into student ("studentId","studentName",gender,"schoolYear",telephone,email,"studentType","idNo",password) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            Sqlca.execute ( sql, [data['studentId'], data['studentName'], data['gender'], schoolYear, data['telephone'],
                                  data['email'], data['studentType'], data['idNo'], password] )
            rtn = {'code': 1000, 'message': '成功', 'data': data}
        except Exception as errordetail:
            rtn = {'code': 1001, 'message': '插入失败，原因：' + str ( errordetail ), 'data': {}}
        return Response ( rtn )

    def put(self, request):
        data = request.data
        password = data['idNo'][12:]
        sql = 'update student set "studentName"=%s,gender=%s,telephone=%s,email=%s,"studentType"=%s,"idNo"=%s,password=%s where "studentId"=%s'
        try:
            r = Sqlca.execute ( sql, [data['studentName'], data['gender'], data['telephone'], data['email'],
                                      data['studentType'], data['idNo'], password, data['studentId']] )
            if r == 0:
                rtn = {'code': 1002, 'message': '错误，修改了0行数据', 'data': data}
            else:
                rtn = {'code': 1000, 'message': '成功', 'data': data}
        except Exception as errordetail:
            rtn = {'code': 1001, 'message': '修改失败，原因：' + str ( errordetail ), 'data': {}}
        return Response ( rtn )

    def delete(self, request):
        data = request.query_params['studentId']
        sql = 'delete from student  where "studentId"=%s'
        try:
            Sqlca.execute ( sql, [data] )
            rtn = {'code': 1000, 'message': '删除成功', 'data': {}}
        except Exception as errordetail:
            rtn = {'code': 1001, 'message': '删除失败，原因：' + str ( errordetail ), 'data': {}}
        return Response ( rtn )

class Validate ( APIView ):
    def get(self, request):
        try:
            stuId = request.query_params['studentId']
            print ( stuId )
            sql = 'select count(gender) from student where "studentId"=%s'
            count = Sqlca.execute ( sql, [stuId] )[0]['count']
            print ( count )

            rtn = {'code': 1000, 'message': '获取成功', 'count': count}
        except Exception as errorDetail:
            rtn = {'code': 1001, 'message': '获取验证失败，失败的原因：' + str ( errorDetail )}
        return Response ( rtn )

class photo(APIView):
    def post(self,request):
        try:
            stuId=request.data['studentId']
            print(stuId)
            file=request.FILES['avatar']
            file_name=default_storage.save(file.name,file)
            avatar='http://127.0.0.1:8000/media/'+file_name
            sql = 'update student set "avatarUrl"=%s where "studentId"=%s '
            data = Sqlca.execute(sql, [avatar, stuId])
            rtn = {'code': 1000, 'message': '上传成功', 'data': data}
        except Exception as errorDetail:
            rtn = {'code': 1001, 'message': '上传失败，失败的原因：' + str(errorDetail)}
        return Response(rtn)
