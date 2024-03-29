SELECT
    t.table_name,
    c.column_name,
    c.data_type,
    CASE
        WHEN c.is_nullable = 'YES' THEN 'YES'
        ELSE 'NO'
    END AS is_nullable,
    CASE
        WHEN pk.column_name IS NOT NULL THEN 'YES'
        ELSE 'NO'
    END AS is_primary_key,
    CASE
        WHEN fk.column_name IS NOT NULL THEN 'YES'
        ELSE 'NO'
    END AS is_foreign_key,
    fk.referenced_table_name,
    fk.referenced_column_name

FROM
    information_schema.tables t

INNER JOIN
    information_schema.columns c
    ON t.table_name = c.table_name
    AND t.table_schema = c.table_schema

LEFT JOIN (
    SELECT
        kcu.table_name,
        kcu.table_schema,
        kcu.column_name,
        rel_kcu.table_name AS referenced_table_name,
        rel_kcu.column_name AS referenced_column_name
    FROM
        information_schema.referential_constraints rc

    INNER JOIN
        information_schema.key_column_usage kcu
        ON rc.constraint_schema = kcu.constraint_schema
        AND rc.constraint_name = kcu.constraint_name

    INNER JOIN
        information_schema.key_column_usage rel_kcu
        ON rc.unique_constraint_schema = rel_kcu.constraint_schema
        AND rc.unique_constraint_name = rel_kcu.constraint_name
        AND kcu.ordinal_position = rel_kcu.ordinal_position
) fk
ON t.table_name = fk.table_name
AND t.table_schema = fk.table_schema
AND c.column_name = fk.column_name

LEFT JOIN (
    SELECT
        tc.table_name,
        tc.table_schema,
        kcu.column_name
    FROM
        information_schema.table_constraints tc

    INNER JOIN
        information_schema.key_column_usage kcu
        ON tc.constraint_schema = kcu.constraint_schema
        AND tc.constraint_name = kcu.constraint_name
        AND tc.constraint_type = 'PRIMARY KEY'
) pk
ON t.table_name = pk.table_name
AND t.table_schema = pk.table_schema
AND c.column_name = pk.column_name

WHERE
    t.table_type = 'BASE TABLE'
    AND t.table_schema NOT IN ('pg_catalog', 'information_schema')

ORDER BY
    t.table_name,
    c.ordinal_position;