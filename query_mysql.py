
query_for_constraint=""" select 
	ColName.column_name,
	
	TableCon.constraint_type
	
	FROM information_schema.key_column_usage ColName
	INNER JOIN information_schema.table_constraints TableCon

	ON ColName.constraint_name = TableCon.constraint_name
	
	where ColName.table_name = '%s'
	ORDER BY constraint_type;"""


query_for_datatypes= """
	select 
	Col.column_name,
	Col.data_type,
	Col.character_maximum_length,
	Col.numeric_precision
	

	FROM information_schema.columns Col

	WHERE Col.table_name = '%s'
	
	;

	"""

query_for_reference="""
				select 
				ccu.table_name , ccu.column_name
				from information_schema.constraint_column_usage ccu
				INNER JOIN information_schema.key_column_usage kcu
				ON ccu.constraint_name = kcu.constraint_name
				AND kcu.table_name='%s'
				AND kcu.column_name ='%s'
;

"""
