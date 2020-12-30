import pyodbc

def pyodbcLinuxUnicodeFetch(encoding):
    """\
    Used on Linux when the ``unicode_results=True`` setting doesn't work.
    """
    def pyodbcLinuxUnicodeFetch_converter(conversion, state=None):
        """\

        Convert the results of a cursor fetch to the correct format.
    
        The ``conversion.value.cursor.description`` argument contains
        information about each value returned in the form of a 7-item tuple:
        ``(name, type_code, display_size, internal_size, precision, scale,
        null_ok)``. The ``.description`` attribute will be ``None`` for
        operations which do not return rows.
    
        The ``type_code`` will be different for each driver.

        """
        cursor = conversion.value.cursor
        rows = conversion.value.result
    
        if cursor.description is None:
            conversion.result = result
        else:
            new_rows = []
            for row in rows:
                new_row = []
                for i, value in enumerate(row):
                    if value is not None and cursor.description[i][1] is type(''):
                        new_row.append(value.decode(encoding))
                    else:
                        new_row.append(value)
                new_rows.append(tuple(new_row))
            conversion.result = tuple(new_rows)
    return pyodbcLinuxUnicodeFetch_converter

pyodbc_linux_latin1_fetch = pyodbcLinuxUnicodeFetch('latin1')

def insert_record(
    connection, 
    table_name, 
    data_dict, 
    primary_key_column_name=None,
    database=None,
):
    """\
    Implementation of ``insert_record()`` for SQLServer 2000. See 
    ``insert_record()`` for details.
    """
    cursor = connection.cursor()
    columns = []
    values = []
    for k, v in data_dict.items():
        values.append(v)
        columns.append(k)
    values_str = ""
    for value in values:
        values_str += "?, "
    values_str = values_str[:-2]

    if primary_key_column_name and data_dict.has_key(primary_key_column_name):
        raise Exception(
            "You shouldn't specify the primary key in the data_dict, "
            "the new value will be returned automatically if you specify "
            "primary_key_column_name"
        )
    sql = """
        INSERT INTO %s (%s) VALUES (%s);
    """ % (
        table_name,
        ', '.join(['"%s"'%col for col in columns]),
        values_str
    )
    cursor.execute(sql, tuple(values))

    if primary_key_column_name is not None:
        cursor.execute(
            """
            SELECT @@IDENTITY
            """
        )
        uid = cursor.fetchall()[0][0]
    cursor.close()
    if primary_key_column_name is not None:
        return int(uid)
    return None


def connect(**p):
    if p.get('autocommit', False):
        raise Exception('You cannot set autocommit to True')
    if not p.has_key('dsn'):
        raise Exception('You must specify a DSN')
    p['autocommit'] = False
    dsn = p['dsn']
    del p['dsn']
    return pyodbc.connect(dsn, **p)

def update_config(bag, name, config):
    from configconvert import handle_option_error, handle_section_error
    if not bag.app.option.has_key(name):
        raise handle_section_error(
            bag, 
            name, 
            (
                "'%s.plugin' (the name of the database plugin to use"%(name)
            )
        )
    from stringconvert import unicodeToUnicode, unicodeToInteger,\
       unicodeToBoolean
    from recordconvert import toRecord
    from configconvert import stringToObject
    from conversionkit import Conversion, chainConverters

    # Re-use the converters   
    unicode_to_integer = unicodeToInteger()
    null = unicodeToUnicode()

    database_config = toRecord(
        missing_defaults=dict(
            creator=connect,
            fetch_converter=None,
            execute_converter=None,
            on_connect_sql=None,
        ),
        missing_or_empty_errors = dict(
            dsn="The required option '%s.dsn' is missing"%(name,),
            unicode_results="The required option '%s.uniocde_results' is missing"%(name,),
        ),
        converters=dict(
            dsn = null,
            unicode_results = unicodeToBoolean(),
            on_connect_sql = unicodeToUnicode(),
            creator = stringToObject(),
            fetch_converter = stringToObject(),
            execute_converter = stringToObject(),
        ),
    ) 
    import base64
    if config.has_key('odsn'):
        odsn = config['odsn']
        parts = odsn.split('|')
        s = str(parts[1])
        p = base64.urlsafe_b64decode((s[:-4] + '=' * (4 - (len(s[4:])-4) % 4))[4:])
        config['dsn'] = parts[0] + p + parts[2]
        del config['odsn']
    conversion = Conversion(config).perform(database_config)
    if not conversion.successful:
        handle_option_error(conversion, name)
    else:
        config = conversion.result
    return config



