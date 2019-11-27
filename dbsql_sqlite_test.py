# -*- coding: utf-8 -*-
from dbsql_sqlite import DbSql

try:
    DbSql.connectDataBase('../dbsql_sqlite_test.sqlite')

    print('==============表级操作===========================================')

    # 自增主键表
    DbSql.ensureTable(
        tableName='nodeTable',
        tableStructureInDict={
            'nodesId': {'类型': '整型', '主键否': '自增主键'},
            'nodesLevel': {'类型': '浮点型', '无关值': None, '主键否': '非主键'},
            'nodesContent': {'类型': '文本', '主键否': '非主键'}
        },
        updateStrategy='rewrite'
    )

    # 一般主键表
    DbSql.ensureTable(
        tableName='玩家表',
        tableStructureInDict={
            'peopleId': {'类型': '整型', '主键否': '主键'},
            'peopleLevel': {'类型': '浮点型', '无关值': None, '主键否': '非主键'},
            'peopleName': {'类型': '文本', '主键否': '非主键'}
        },
        updateStrategy='rewrite'
    )

    # 联合主键表
    DbSql.ensureTable(
        tableName='文献表',
        tableStructureInStr='''
            文献英文标题      TEXT  ,
            文献中文标题      TEXT  ,
            文献发表时间     INT   ,
            他引数量          INT    ,
            他引页面URL       TEXT   ,
            PRIMARY KEY (文献中文标题,文献英文标题)
        ''',
        updateStrategy='rewrite'
    )

    response = DbSql.getTableStructure('nodeTable')
    truth = [
        (0, 'nodesId', 'INTEGER', 0, None, 1), 
        (1, 'nodesLevel', 'REAL', 0, None, 0), 
        (2, 'nodesContent', 'TEXT', 0, None, 0)]
    print('成功:' if response == truth else '失败:', '测试ensureTable和getTableStructure')

    response = DbSql.getAllTableName()
    truth = ['sqlite_sequence', 'nodeTable', '玩家表', '文献表']
    print('成功:' if response == truth else '失败:', '测试ensureTable和getAllTableName')

    response = DbSql.isTableExists('文献表')
    truth = True
    print('成功:' if response == truth else '失败:', '测试isTableExists判断存在的表')

    response = DbSql.isTableExists('未知表')
    truth = False
    print('成功:' if response == truth else '失败:', '测试isTableExists判断不存在的表')

    response = DbSql.deleteTables('文献表')
    truth = 1
    print('成功:' if response == truth else '失败:', '测试deleteTables删除存在的表')

    response = DbSql.deleteTables('一个没建过的表')
    truth = 0
    print('成功:' if response == truth else '失败:', '测试deleteTables删除不存在的表')

    print('==============数据级操作===========================================')

    DbSql.insertRow('玩家表', {'peopleId': 5, 'peopleLevel': None, 'peopleName': '龙傲天'})
    response = DbSql.selectRow('玩家表', {'peopleName': '龙傲天'})
    truth = [(5, None, '龙傲天')]
    print('成功:' if response == truth else '失败:', '测试insertRow(一般情况)')

    DbSql.insertRow('玩家表', {'peopleLevel': 2.0, 'peopleName': '小虾米'})
    response = DbSql.selectRow('玩家表', {'peopleName': '小虾米'})
    truth = [(6, 2.0, '小虾米')]
    print('成功:' if response == truth else '失败:', '测试insertRow(一般主键缺失，自动自增)')

    response = DbSql.getMaxIncrementId('玩家表')
    truth = 0
    print('成功:' if response == truth else '失败:', '测试getMaxIncrementId（非自增表)')

    response = DbSql.getMaxIncrementId('nodeTable')
    truth = 0
    print('成功:' if response == truth else '失败:', '测试getMaxIncrementId（空自增表)')

    DbSql.insertRow('nodeTable', {'nodesLevel': 2.0, 'nodesContent': '节点B'})
    response = DbSql.getMaxIncrementId('nodeTable')
    truth = 1
    print('成功:' if response == truth else '失败:', '测试insertRow(自增主键-不提供主键)')

    DbSql.insertRow('nodeTable', {'nodesId': 7, 'nodesLevel': 4.0, 'nodesContent': '节点E'})
    response = DbSql.getMaxIncrementId('nodeTable')
    truth = 7
    print('成功:' if response == truth else '失败:', '测试insertRow(自增主键-提供不连续的主键)')

    DbSql.insertRow('nodeTable', {'nodesLevel': 5.0, 'nodesContent': '节点Q'})
    response = DbSql.getMaxIncrementId('nodeTable')
    truth = 8
    print('成功:' if response == truth else '失败:', '测试insertRow(自增主键-不提供主键之后插入新行)')

    DbSql.insertRow('nodeTable', {'nodesLevel': 15.0, 'nodesContent': None})
    response = DbSql.executeCommand("SELECT nodesContent FROM nodeTable WHERE nodesLevel=15")
    truth = [(None,)]
    print('成功:' if response == truth else '失败:', '测试insertRow(None→NULL)')

    DbSql.insertRow('nodeTable', {'nodesLevel': 16.0, 'nodesContent': 'a"a"aa\'a\'aa'})
    response = DbSql.executeCommand("SELECT nodesContent FROM nodeTable WHERE nodesLevel=16")
    truth = [('a"a"aa\'a\'aa',)]
    print('成功:' if response == truth else '失败:', '测试insertRow(转意-引号)')

    DbSql.insertRow('nodeTable', {'nodesLevel': 17.0, 'nodesContent': 'a\na'})
    response = DbSql.executeCommand("SELECT nodesContent FROM nodeTable WHERE nodesLevel=17")
    truth = [('a\na',)]
    print('成功:' if response == truth else '失败:', '测试insertRow(转意-回车)')

    response = DbSql.selectRow('nodeTable', {'nodesId': 1, 'nodesLevel': 2.0})
    truth = [(1, 2.0, '节点B')]
    print('成功:' if response == truth else '失败:', '测试selectRow(一般情况)')

    response = DbSql.selectRow('nodeTable', {'nodesId': 1, 'nodesLevel': 3.0})
    truth = []
    print('成功:' if response == truth else '失败:', '测试selectRow(搜不到的情况)')

    DbSql.insertRow('nodeTable', {'nodesLevel': 21.0, 'nodesContent': None})
    response = DbSql.selectRow('nodeTable', {'nodesContent': None})
    truth = [(9, 15.0, None), (12, 21.0, None)]
    print('成功:' if response == truth else '失败:', '测试selectRow(NULL→None)')

    DbSql.updateRow(
        tableName='nodeTable',
        selectDict={'nodesContent': '节点Q'},
        setDict={'nodesLevel': None, 'nodesContent': '节点W'}
    )
    response = DbSql.selectRow('nodeTable', {'nodesContent': '节点W'})
    truth = [(8, None, '节点W')]
    print('成功:' if response == truth else '失败:', '测试updateRow')

finally:
    DbSql.disconnectDataBase()
