create table if not exists test.test (
    string_col string comment 'string_col',
    bigint_col bigint comment 'bigint_col',
    double_col double comment 'double_col',
    map_string_string_col map<string,string> comment 'map_string_string_col',
    map_string_bigint_col map<string,bigint> comment 'map_string_bigint_col'
)
comment 'table'
partitioned by (
    pt string comment 'pt'
)
row format delimited fields terminated by '|'
stored as textfile
;
