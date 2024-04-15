import psycopg2
import pathlib

from Tool.Tool_EncrytExcel import read_encrypt_excel
from Tool.TempTool.Key_Info import excel_password
def insert_excel_data(excel_path):
    """
    将excel中的数据插入到postgres数据库中
    :return:
    """
    # 1.连接数据库
    con = psycopg2.connect(database="course", user="postgres", password="81991889", host="localhost", port="5432")
    # 2.创建游标
    cur = con.cursor()
    # 3.读取excel文件
    df = read_encrypt_excel(excel_path, excel_password)
    # 4.获取需要创建的表名和字段名
    table_name = 'Course'+pathlib.Path(excel_path).stem.replace("春课表", "spring")
    # table_name = "course" + time.strftime("%Y-%m-%d", time.localtime())
    columns = df.columns.tolist()
    # 判断课表是否为空
    if len(df) > 0:
        # 判断表是否存在
        try:
            cur.execute(f"select * from {table_name};")
            # 如果表存在，则询问是否覆盖
            if len(cur.fetchall()) > 0:
                print(f"表{table_name}已经存在，是否覆盖？(y/n)")
                if input() == 'y':
                    cur.execute(f'drop table {table_name};')
                    pass
                else:
                    print("已取消插入数据")
                    # 7.提交事务
                    con.commit()
                    # 8.关闭游标
                    cur.close()
                    # 9.关闭连接
                    con.close()
                    return
        except:
            # 7.提交事务
            con.commit()
            # 8.关闭游标
            cur.close()
            # 9.关闭连接
            con.close()
            con = psycopg2.connect(database="course", user="postgres", password="81991889", host="localhost",
                                   port="5432")
            cur = con.cursor()
            pass

        # 5.创建表
        create_sql = f"create table {table_name}("
        for index, column in enumerate(columns):
            create_sql += f"col{index} text,"
        create_sql = create_sql[:-1] + ")"
        cur.execute(create_sql)
        # 6.插入数据
        for index, row in df.iterrows():
            insert_sql = f"insert into {table_name} values("
            for column in columns:
                insert_sql += f"'{row[column]}',"
            insert_sql = insert_sql[:-1] + ")"
            cur.execute(insert_sql)
    # 7.提交事务
    con.commit()
    # 8.关闭游标
    cur.close()
    # 9.关闭连接
    con.close()

def main():
    insert_excel_data("../CourseData/2020Spring.xlsx")

if __name__ == '__main__':
    main()