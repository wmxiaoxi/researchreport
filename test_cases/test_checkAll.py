import allure
import pytest
from common.config import *
from common.base import *
class Test_checkA():
    @allure.story("行业和子类型比对")
    def test_01(self):
        try:
            content_api= get(host1 + addr1)
            print(content_api)
            insdustry_api=list(content_api['content'].keys())
            print(insdustry_api)
            sql="select distinct industry from  public.research_report"
            content_sql = sqlcheck(sql)
            insdustry = []
            for i in range(0,len(content_sql)):
                insdustry_sql=content_sql[i][0]
                insdustry.append(insdustry_sql)
                print(insdustry_sql)
                type_api=content_api['content'][insdustry_sql]
                print('type_api'+'的值'+str(type_api))
                sql1="select distinct type from  public.research_report  where industry='"+insdustry_sql+"'"
                content_sql1=sqlcheck(sql1)
                type = []
                for j in range(0, len(content_sql1)):
                    type_sql = content_sql1[j][0]
                    type.append(type_sql)
                print(insdustry_sql+"数据库子类型"+str(type)+"接口子类型"+str(type_api))
                assert len(type) ==len(type_api)
            insdustry.append('全部')
            for n  in range(0,len(type)):
                assert type[n] in type_api

            assert len(insdustry_api)==len(insdustry)
            for m in range(0,len(insdustry_api)):
                assert  insdustry_api[0]in insdustry

        except Exception as e:
            raise e



    @allure.story('查询全部得数据')
    def test_02(self):
        data={"industry":"","page":1,"priceType":"全部","rows":10,"searchWord":"","target":"","type":"","year":0}
        content_api=post(host1+addr,data,headers)
        count=content_api['content']['count']
        sql="select count(*) from public.research_report"
        count_sql=sqlcheck(sql)
        assert count == count_sql[0][0]


    @allure.story("分页查询")
    def test_03(self):
        data={"industry":"","page":2,"priceType":"全部","rows":10,"searchWord":"","target":"","type":"","year":0}
        content_api=post(host1+addr,data,headers)
        assert content_api['code'] == 0

    @allure.story("一页显示条数")
    def test_04(self):
        data={"industry":"","page":1,"priceType":"全部","rows":20,"searchWord":"","target":"","type":"","year":0}
        content_api=post(host1+addr,data,headers)
        assert content_api['code'] == 0
        assert len(content_api['content']['value'])==20



    @allure.story("关键字查询/标题,标签,来源,摘要")
    @pytest.mark.parametrize('searchWord',['2019文化','手机游戏','iimedia艾媒网','预计2019年中国'])
    def test_05(self,searchWord):
        data={"industry":"","page":1,"priceType":"全部","rows":20,"searchWord":searchWord,"target":"","type":"","year":0}
        content_api=post(host1+addr,data,headers)
        count_api=content_api['content']['count']
        sql="select count(*) from public.research_report where title like '%"+searchWord+"%' or targets like '%"+searchWord+"%' or origin like '%"+searchWord+"%' or intro like'%"+searchWord+"%'"
        count_sql=sqlcheck(sql)
        print("按关键字查询" + searchWord + "查询数据库条数" + str(count_sql[0][0]) + "接口条数" + str(count_api))
        assert count_api==count_sql[0][0]




    @allure.story("时间查询")
    @pytest.mark.parametrize('year', ['2020','2019','2018','2017','2016'])
    def test_06(self,year):
        data={"industry":"","page":1,"priceType":"全部","rows":20,"searchWord":"","target":"","type":"","year":year}
        content_api = post(host1 + addr, data, headers)
        count_api = content_api['content']['count']
        sql = "select count(*) from public.research_report where to_char(date,'yyyy')='"+year+"'"
        count_sql = sqlcheck(sql)
        print("按时间查询" + year + "查询数据库条数" + str(count_sql[0][0]) + "接口条数" + str(count_api))
        assert count_api == count_sql[0][0]



    @allure.story("付费类型")
    @pytest.mark.parametrize('priceType', ['全部','免费','付费' ])
    def test_07(self,priceType):
        data={"industry":"","page":1,"priceType":priceType,"rows":20,"searchWord":"","target":"","type":'',"year":0}
        content_api = post(host1 + addr, data, headers)
        count_api = content_api['content']['count']
        if priceType=='全部':
            sql = "select count(*) from public.research_report"
        elif priceType=='免费':
            sql= "select count(*) from public.research_report where price_type='" + priceType + "' or price_type is null"
        else:
            sql = "select count(*) from public.research_report where price_type='" + priceType+"'"
        count_sql = sqlcheck(sql)
        print("按付费类型查询"+priceType+"查询数据库条数"+str(count_sql[0][0])+"接口条数"+str(count_api))
        assert count_api == count_sql[0][0]




    @allure.story("行业查询")
    def test_06(self ):
        content_api = get(host1 + addr1)
        insdustry_api=list(content_api['content'].keys())
        for i in range(0,len(insdustry_api)):
            insdustry= insdustry_api[i]
            if insdustry=='全部':
                sql = "select count(*) from public.research_report"
                data = {"industry": '', "page": 1, "priceType": "全部", "rows": 10, "searchWord": "", "target": "",
                        "type": "", "year": 0}
            else:
                sql = "select count(*) from public.research_report where industry ='"+insdustry+"'"
                data = {"industry":insdustry, "page": 1, "priceType": "全部", "rows": 10, "searchWord": "", "target": "",
                        "type": "", "insdustry": 0}
            content_api = post(host1 + addr, data, headers)
            count_api = content_api['content']['count']
            count_sql = sqlcheck(sql)
            print("按行业"+insdustry+"查询数据库条数"+str(count_sql[0][0])+"接口条数"+str(count_api))
            assert count_api == count_sql[0][0]


    @allure.story("按子类型查询")
    def test_07(self):
        content_api = get(host1 + addr1)
        type=content_api['content']['全部']
        if None in type:
            type.remove(None)
            print(type)
        else:
            print("列表中无None值")
        for i in range(0,len(type)):
            typenew= type[i]
            sql = "select count(*) from public.research_report where type ='"+typenew+"'"
            data = {"industry":'', "page": 1, "priceType": "全部", "rows": 10, "searchWord": "", "target": "",
                        "type": typenew, "year": 0}
            content_api = post(host1 + addr, data, headers)
            count_api = content_api['content']['count']
            count_sql = sqlcheck(sql)
            print("按子类型"+typenew+"查询数据库条数"+str(count_sql[0][0])+"接口条数"+str(count_api))
            assert count_api == count_sql[0][0]




    @allure.story("关键字+时间+付费+行业+子类型")
    @pytest.mark.parametrize("searchWord,year,priceType",[('20','2019','付费',)])
    @pytest.mark.parametrize("industry", [('影视'),])
    def test_08(self,searchWord,year,priceType,industry):
        content_api = get(host1 + addr1)
        type=content_api['content'][industry]
        if None in type:
            type.remove(None)
            print(type)
        else:
            print("列表中无None值")
        type1=type[0]
        data={"industry":industry,"page":1,"priceType":priceType,"rows":20,"searchWord":searchWord,"target":"","type":type1,"year":year}
        sql = "select count(*) from (select * from public.research_report where title like '%"+searchWord+"%' or targets like '%"+searchWord+"%' or origin like '%"+searchWord+"%' or intro like'%"+searchWord+"%')aa where aa.industry='"+industry+"'and to_char(aa.date,'yyyy')='"+year+"' and aa.type='"+type1+"'and aa.price_type='"+priceType+"'"
        content_api = post(host1 + addr, data, headers)
        count_api = content_api['content']['count']
        count_sql = sqlcheck(sql)
        print("按关键字："+searchWord+"时间："+year+"付费："+priceType+"行业："+industry+"子类型："+type1+"    查询数据库数据："+str(count_api)+"；接口数据："+str(count_sql[0][0]))
        assert count_api == count_sql[0][0]







if __name__=="__main__":
    pytest.main(["-s","test_checkAll.py"])