import psycopg2

query_for_constraint = """
	select 
	kcu.column_name,
	
	tc.constraint_type
	
	FROM information_schema.key_column_usage kcu
	INNER JOIN information_schema.table_constraints tc

	ON kcu.constraint_name = tc.constraint_name
	
	where kcu.table_name = '%s'
	ORDER BY constraint_type
	; 
"""
query_for_datatypes = """
	select 
	c.column_name,
	c.data_type,
	c.character_maximum_length,
	c.numeric_precision
	

	FROM information_schema.columns c

	WHERE c.table_name = '%s'
	
	;

	"""
query_for_reference = """
				select 
				ccu.table_name , ccu.column_name
				from information_schema.constraint_column_usage ccu
				INNER JOIN information_schema.key_column_usage kcu
				ON ccu.constraint_name = kcu.constraint_name
				AND kcu.table_name='%s'
				AND kcu.column_name ='%s'
;

"""

query_for_table_ordering = """
        select tc.table_name
        FROM information_schema.table_constraints as tc
        INNER JOIN information_schema.constraint_column_usage as ccu  
        ON tc.constraint_name = ccu.constraint_name
        WHERE tc.table_name='%s'
        AND tc.table_name = ccu.table_name
 
"""

query_for_check = """
        select
       
        cc.check_clause
       
        FROM information_schema.table_constraints tc
        INNER JOIN information_schema.check_constraints cc
 
        ON cc.constraint_name = tc.constraint_name
        INNER JOIN information_schema.constraint_column_usage ccu
        ON cc.constraint_name = ccu.constraint_name
 
        where tc.table_name = '%s'
        AND ccu.column_name = '%s'
        ;
"""
