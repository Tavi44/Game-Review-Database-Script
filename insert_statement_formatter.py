def createInsertQuery(tableName, argsDict):
    if not argsDict:
        raise ValueError('Must insert at least one value, got {}')
    query = f'INSERT INTO {tableName} ('
    queryValues = 'VALUES ('
    for arg in argsDict:
        query += f'{arg}, '
        if argsDict[arg][0] == None:
            queryValues += 'NULL, '
            continue
        if argsDict[arg][1]:
            queryValues += f'\'{argsDict[arg][0]}\', '
        else:
            queryValues += f'{argsDict[arg][0]}, '

    return query[ : -2] + ') ' + queryValues[ : -2] + ');\n'