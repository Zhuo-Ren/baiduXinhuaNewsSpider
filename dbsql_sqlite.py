# -*- coding: utf-8 -*-
import sqlite3  # 引入sqlite3来使用sqlite


class DbSql(object):
    dbConnect = None
    dbCursor = None

    @staticmethod
    def connectDataBase(dbName):
        """
        :function 连接数据库。存在直接连，不存在则创建后连接。
                链接句柄保存在全局变量dbConnect和dbCursor。

        :param dbName=' '。要建立的表的名字。

        :example 1 \n
                connectDataBase('testdb')
        """
        # dbName用来指明要连接到的数据库名字
        # 创建连接
        DbSql.dbConnect = sqlite3.connect(dbName)
        # 创建游标
        DbSql.dbCursor = DbSql.dbConnect.cursor()
        print('建立sqlite数据库连接')

    @staticmethod
    def disconnectDataBase():
        """
        :function 断开全局变量dbConnect和dbCursor所保存的数据库链接。
                （注意，没有判断dbConnect和dbCursor是否合理，直接短开）

        :example 1 \n
                disconnectDataBase()
        """
        if DbSql.dbCursor is not None:
            # 关闭游标
            DbSql.dbCursor.close()
            # 提交事务
            DbSql.dbConnect.commit()
            # 关闭连接
            DbSql.dbConnect.close()
            # 日志
            print('释放sqlite数据库连接')

    @staticmethod
    def executeCommand(command, args=None):
        """
        :function 在全局变量dbConnect和dbCursor所保存的数据库中，执行一个语句。
                不进行语句合理性检测，如果执行出错则打印错误。

        :param command=' '。要执行的sql语句。

        :returns 执行返回的结果dbCursor.fetchall()被以list的形式返回
        """
        # 语句处理

        # 语句执行
        try:
            # 执行SQL语句
            if args is not None:
                DbSql.dbCursor.execute(command, args)
            else:
                DbSql.dbCursor.execute(command)
            DbSql.dbConnect.commit()
            # 取得返回值
            response = DbSql.dbCursor.fetchall()
            # 返回
            return(response)
        # 如果执行出错，返回异常
        except Exception as e:
            print('如下语句执行出错：', command)
            print('错误为：', e)

    @staticmethod
    def createTable(tableName, tableStructureInDict=None, tableStructureInStr=None):
        """
        :function 在全局变量dbConnect和dbCursor所保存的数据库中，直接建表。
                直接建表，不管表是否已经存在。所以可能执行报错。
                如果tableStructureInStr不空，则基于它建表
                如果tableStructureInStr为空，则基于tableStructureInDict建表。

        :param tableName=' '。要建立的表的名字。
        :param tableStructureInDict={ }。要建立的表的结构，以字典形式给出，字典中可以有无关键值对。
        :param tableStructureInStr=" "。要建立的表的结构，以字符串形式给出。

        :example 1 \n
                tableName='peoplesTable'
                tableStructureInDict={
                    'peopleId': {'类型': '整型', '主键否': '主键', '可以有无': '关键值对'},
                    'peopleLevel': {'类型': '浮点型', '主键否': '非主键'},
                    'peopleName': {'类型': '文本', '主键否': '非主键'}
                }
        :example 2 \n
                tableName='nodesTable'
                tableStructureInDict={
                    'nodesId': {'类型': '整型', '主键否': '自增主键'},
                    'nodesLevel': {'类型': '浮点型', '主键否': '非主键', '可以有无': '关键值对'},
                    'nodesContent': {'类型': '文本', '主键否': '非主键'}
                }

        :example 3 \n
                tableName='nodesTable'
                tableStructureInStr="
                    nodesId TEXT,
                    nodesLevel REAL,
                    nodesContent TEXT
                "
                tablesStructureInDict此时不生效
        """
        # 类型转换：各"通用类型"与"sqlite数据库软件支持的类型"之间的对应关系
        typeTrans = {
            '整型': 'INTEGER',
            '浮点型': 'REAL',
            '文本': 'TEXT',
        }

        # 这个函数是establishTables函数的内部子函数。
        def tableStructure_Dict2Str(tableStructureInDict):
            """
            :function 输入一个记录表结构的字典，输出建表sql语句需要的字段描述字符串

            :param tableStructureInDict={ }。一个记录表结构的字典。同createTable函数。
            :returns tableStructureInStr=' '。建表sql语句需要的字段描述字符串。
            """
            # temp是用来生成tableStructure_Str的临时变量
            temp = ''
            # 遍历并添加tableStructure_Dict中每一行的信息
            for k in tableStructureInDict.keys():
                # 添加列名
                temp = temp + k
                # 添加数据类型
                    # tableStructure_Dict[k]['类型']返回的字段类型是一种跨数据库软件的通用描述。
                    # 每种数据库软件对数据类型的支持不同
                    # 例如小数，有的数据库软件用FLOAT类型存储，有的用REAL存储
                    # 所以需要用数据类型的通用描述去typeTrans中查当前数据库软件支持的数据类型
                temp = temp + ' ' + typeTrans[tableStructureInDict[k]['类型']]
                # 添加主键标志
                switch = {
                    '非主键': '',
                    '主键': 'PRIMARY KEY',
                    '自增主键': 'PRIMARY KEY AUTOINCREMENT',
                    '联合主键': 'PRIMARY KEY'
                }
                temp = temp + ' ' + switch[tableStructureInDict[k]['主键否']]
                # 行末加逗号回车
                temp = temp + ',\n'
            # 此时temp最后还多一个逗号回车，所以要去掉最后2个字符
            tableStructureInStr = temp[0:-2]
            # 处理完成，返回结果
            return tableStructureInStr

        # 参数tableName的可用性检测
        if type(tableName) != str or tableName == '':
            print('error：没有表名信息')
            return(0)
        # 参数tableStructureInDict和tableStructureInStr的可用性检测
        if tableStructureInStr is None and tableStructureInDict is None:
            print('error：没有表结构信息')
            return(0)
        # 对于表结构信息，如果没有提供字符串，则使用字典
        if tableStructureInStr is None and type(tableStructureInDict) == dict:
            tableStructureInStr = tableStructure_Dict2Str(tableStructureInDict)
        # 对于表结构信息，如果提供了字符串，则忽略字典
        elif type(tableStructureInStr) == str and tableStructureInStr != '':
            pass
        # 其他情况
        else:
            print('error:参数tableStructure的类型不对')
        # 生成sql语句
        sqlCmd = 'CREATE TABLE ' + tableName + '(\n' + tableStructureInStr + '\n)'
        # 执行语句
        # DbSql.dbCursor.execute(sqlCmd)
        DbSql.executeCommand(sqlCmd)

    @staticmethod
    def ensureTable(tableName, tableStructureInDict=None, tableStructureInStr=None, updateStrategy='rewrite'):
        """
        :function 在全局变量dbConnect和dbCursor所保存的数据库中，按照策略建表。
                如果要建的表不存在，则直接建表。
                如果要建得表已存在，且updateStrategy='rewrite'，则删除旧表建新表。
                如果要建得表已存在，且updateStrategy='continue'，则保留旧表，不做操作。

        :param tableName=' '。要建立的表的名字。
        :param tableStructure=' 'or{ }。要建立的表的结构。
        :param updateStrategy='rewrite'or'continue'。如果要建立的表已经存在，是删除旧表建新表，还是放弃建表操作。

        :example 1 \n
                tableName='nodesTable'
                tableStructure={
                    'nodesId': {'类型': '文本', '初始值': 'None', '主键？': '主键'},
                    'nodesLevel': {'类型': '浮点型', '初始值': 'None', '主键？': '非主键'},
                    'nodesContent': {'类型': '文本', '初始值': 'None', '主键？': '非主键'}
                }

        :example 2 \n
                tableName='nodesTable'
                tableStructure="
                    nodesId TEXT,
                    nodesLevel REAL,
                    nodesContent TEXT
                "
        """
        if DbSql.isTableExists(tableName):
            if updateStrategy == 'rewrite':
                # 删除旧表
                DbSql.deleteTables(tableName)
                # 建立新表
                DbSql.createTable(tableName, tableStructureInDict, tableStructureInStr)
                pass
            elif updateStrategy == 'continue':
                return 0
            else:
                print('updateStrategy error')
        else:
            # 建立新表
            DbSql.createTable(tableName, tableStructureInDict, tableStructureInStr)

    @staticmethod
    def deleteTables(tableName):
        """
        :function 删除一个表。\n
                在全局变量dbConnect和dbCursor所保存的数据库中，删表.

        :param tableName=' '。要删除的表的名字。
        :returns 删除成果返回1，否则0

        :example 1 \n
                deleteTables('文献表')
        """
        # 此表存在则删除之
        if DbSql.isTableExists(tableName):
            sql_delete = 'DROP TABLE %s' % tableName
            DbSql.executeCommand(sql_delete)
            return (1)
        # 不存在则打印提示
        else:
            print('%s不存在，无法删除' % tableName)
            return (0)

    @staticmethod
    def isTableExists(tableName):
        """
        :function 查询某表是否存在。\n
                在全局变量dbConnect和dbCursor所保存的数据库中，查询某表是否存在。

        :param tableName=' '。要查询的表的名字。
        :returns 存在返回True,不存在返回False
        """
        return tableName in DbSql.getAllTableName()

    @staticmethod
    def getAllTableName():
        """
        :function 获取所有表名。\n
                返回全局变量dbConnect和dbCursor所保存的数据库中的所有表的表名。
        :returns 列表形式返回所有表名。例如['sqlite_sequence', 'nodeTable', '玩家表', '文献表']。
            注意，如果存在某个表是使用自增主键的，那么会sqlite会自动构建'sqlite_sequence'表。
        """
        # 生成查询语句
        sql_search = "select name from sqlite_master where type='table' "
        # 执行查询语句
        DbSql.dbCursor.execute(sql_search)
        # 获取查询语句的返回结果
        allData = DbSql.dbCursor.fetchall()  # 格式类似于：[('nodeTable',), ('文献表',)]
        # 格式转化为：['nodeTable', '文献表']
        allData = [x[0] for x in allData]
        # 返回结果
        return allData

    @staticmethod
    def getTableStructure(tableName):
        """
        :function 查询某个表的表结构。\n
                返回全局变量dbConnect和dbCursor所保存的数据库中的所有表的表名。
                # 注意：本函数默认是从所有数据表中查询某一表信息，如若缩小范围（即从系统表或某一用户的用户表进行搜索），需更改sql_query语句
                # 一般更改from后字段即可
                # 将返回结果进行保存

        :param tableName=' '。要查询的表的名字。
        :returns =[]。 返回某表全部字段信息，用列表进行存储。例如：
            [
                (0, 'nodesId', 'INTEGER', 0, None, 1), 
                (1, 'nodesLevel', 'REAL', 0, None, 0), 
                (2, 'nodesContent', 'TEXT', 0, None, 0)
            ]
        """
        result = []
        cmd = 'PRAGMA table_info(%s)' % tableName
        allData = DbSql.executeCommand(cmd)
        for ad in allData:
            result.append(ad)
        return result

    @staticmethod
    def insertRow(tableName, infoDict):
        """
        :function 在指定表中插入一行。\n

        :param tableName=' '。要插入的表的名字。
        :param infoDict={}。要插入的信息。

        :example 1 \n
                infoDict={'peopleLevel': None, 'peopleName': '龙傲天'}
                这样插入的结果是peopleId自动设置为1，peopleLevel自动转换为NULL，其他字段照常
        如果插入的行信息中有python中的空值None，则会转换为SQL中的控制NULL。 \n
        如果插入的行信息中，缺失自增主键信息，sqlite会自动按照递增的规律填充。 \n
        如果插入的行信息中，缺失主键信息，sqlite也会自动按照递增的规律填充（这么智能啊）。
        """
        # 生成sql语句
        cmd = "INSERT INTO " + tableName
        cmd = cmd + " (" + ','.join(list(infoDict.keys())) + ") "
        cmd = cmd + " VALUES ("
        for i in range(0, len(infoDict)):
            cmd = cmd + '?,'
        cmd = cmd[0:-1] + ')'
        # 执行sql语句
        args = tuple(infoDict.values())
        DbSql.executeCommand(cmd, args)

    @staticmethod
    def selectRow(tableName, selectDict=None):
        # 生成sql语句
        '''
        cmd = "SELECT * FROM " + tableName + " WHERE "
        for k in list(selectDict.keys()):
            if type(selectDict[k]) == str:
                cmd = cmd + k + ' = ' + "'" + selectDict[k] + "'"
            else:
                cmd = cmd + k + ' = ' + str(selectDict[k])
            cmd = cmd + " AND "
        cmd = cmd[0:-5]
        # 执行sql语句
        response = DbSql.executeCommand(cmd)
        return response
        '''
        cmd = "SELECT * FROM " + tableName + " WHERE "
        selectArgs = ()
        for k in list(selectDict.keys()):
            if selectDict[k] is None:
                cmd = cmd + k + ' is NULL AND '
            else:
                cmd = cmd + k + ' = ? AND '
                selectArgs = selectArgs + (selectDict[k],)
        cmd = cmd[0:-5]
        response = DbSql.executeCommand(cmd, selectArgs)
        return response
    
    @staticmethod
    def updateRow(tableName, selectDict, setDict):
        # 生成sql语句
        cmd = "UPDATE " + tableName + " SET "

        for k in list(setDict.keys()):
            cmd = cmd + k + ' = ?, '
        args = tuple(setDict.values())
        cmd = cmd[0:-2]

        cmd = cmd + " WHERE "
        for k in list(selectDict.keys()):
            if selectDict[k] is None:
                cmd = cmd + k + ' is NULL AND '
            else:
                cmd = cmd + k + ' = ? AND '
                args = args + (selectDict[k],)
        cmd = cmd[0:-5]
        # 执行sql语句
        response = DbSql.executeCommand(cmd, args)
        return response

    @staticmethod
    def getMaxIncrementId(tableName):
        """
        :function 获取使用自增主键的表的当前最大ID。

        :param tableName=' '。要搜索的表的名字。
        :return 指定的自增主键表的当前最大ID。如果提供的表名不使用自增主键，或者还没有添加过内容，那么返回0。

        :example 1 \n
                tableName='nodesTable'
        """
        # sqlite_sequence是一个系统表，存储着各表自增主键的当前最大值
        cmd = "select * from sqlite_sequence where name = '" + tableName + "'"
        response = DbSql.executeCommand(cmd)
        # response是这样的东西：[('nodeTable', 1)]。所以还有从中取出数字1。
        return response[0][1] if response != [] else 0
