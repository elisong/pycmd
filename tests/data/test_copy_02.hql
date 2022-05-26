CREATE TABLE IF NOT EXISTS test.test (
    string_col string COMMENT 'string_col',
    bigint_col BIGINT COMMENT 'bigint_col',
    double_col DOUBLE COMMENT 'double_col',
    map_string_string_col MAP<string,string> COMMENT 'map_string_string_col',
    map_string_bigint_col MAP<string,BIGINT> COMMENT 'map_string_bigint_col'
)
COMMENT 'table'
PARTITIONED BY (
    pt string COMMENT 'pt'
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '|'
STORED AS textfile
;