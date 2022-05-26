# -*- coding: utf-8 -*-
# Description:  HiveQL Keywords Formatter
# Usage: hiveql [-h] [-i] [-r RESERVE] file
import argparse
import re
from pathlib import Path
from urllib.request import urlopen

from .utils import Console


parser = argparse.ArgumentParser(prog="hiveql", description="HiveQL Keywords Formatter")
parser.add_argument("-i", "--inplace", action="store_true", help="format inplace")
parser.add_argument("-o", "--output", type=str, help="output file path")
parser.add_argument("-r", "--reserve", type=str, help="patterns reserved, comma seporated")
parser.add_argument("-u", "--upgrade", action="store_true", help="upgrade keywords, built-in func online")
parser.add_argument("file", type=str, help="source file")
args = parser.parse_args()


def get_kws():
    if not args.upgrade:
        KEYWORDS = "ABORT,ACTIVATE,ACTIVE,ADD,ADMIN,AFTER,ALL,ALLOC_FRACTION,ALTER,ANALYZE,AND,ANY,APPLICATION,ARCHIVE,ARRAY,AS,ASC,AST,AT,AUTHORIZATION,AUTOCOMMIT,BEFORE,BETWEEN,BIGINT,BINARY,BOOLEAN,BOTH,BUCKET,BUCKETS,BY,CACHE,CASCADE,CASE,CAST,CBO,CHANGE,CHAR,CHECK,CLUSTER,CLUSTERED,CLUSTERSTATUS,COLLECTION,COLUMN,COLUMNS,COMMENT,COMMIT,COMPACT,COMPACTIONS,COMPUTE,CONCATENATE,CONF,CONNECTOR,CONNECTORS,CONSTRAINT,CONTINUE,COST,CREATE,CRON,CROSS,CUBE,CURRENT,CURRENT_DATE,CURRENT_TIMESTAMP,CURSOR,DATA,DATABASE,DATABASES,DATE,DATETIME,DAY,DAYOFWEEK,DAYS,DBPROPERTIES,DCPROPERTIES,DDL,DEBUG,DEC,DECIMAL,DEFAULT,DEFERRED,DEFINED,DELETE,DELIMITED,DEPENDENCY,DESC,DESCRIBE,DETAIL,DIRECTORIES,DIRECTORY,DISABLE,DISABLED,DISTINCT,DISTRIBUTE,DISTRIBUTED,DO,DOUBLE,DROP,DUMP,ELEM,ELSE,ENABLE,ENABLED,END,ENFORCED,ESCAPED,EVERY,EXCEPT,EXCHANGE,EXCLUSIVE,EXECUTE,EXECUTED,EXISTS,EXPLAIN,EXPORT,EXPRESSION,EXTENDED,EXTERNAL,EXTRACT,FALSE,FETCH,FIELDS,FILE,FILEFORMAT,FIRST,FLOAT,FLOOR,FOLLOWING,FOR,FORCE,FOREIGN,FORMAT,FORMATTED,FROM,FULL,FUNCTION,FUNCTIONS,GRANT,GROUP,GROUPING,HAVING,HOUR,HOURS,IDXPROPERTIES,IF,IGNORE,IMPORT,IN,INDEX,INDEXES,INNER,INPATH,INPUTDRIVER,INPUTFORMAT,INSERT,INT,INTEGER,INTERSECT,INTERVAL,INTO,IS,ISOLATION,ITEMS,JAR,JOIN,JOINCOST,KEY,KEY,KEYS,KILL,LAST,LATERAL,LEADING,LEFT,LESS,LEVEL,LIKE,LIMIT,LINES,LOAD,LOCAL,LOCATION,LOCK,LOCKS,LOGICAL,LONG,MACRO,MANAGED,MANAGEDLOCATION,MANAGEMENT,MAP,MAPJOIN,MAPPING,MATCHED,MATERIALIZED,MERGE,METADATA,MINUS,MINUTE,MINUTES,MONTH,MONTHS,MORE,MOVE,MSCK,NONE,NORELY,NOSCAN,NOT,NOVALIDATE,NULL,NULLS,NUMERIC,OF,OFFSET,ON,ONLY,OPERATOR,OPTION,OR,ORDER,OUT,OUTER,OUTPUTDRIVER,OUTPUTFORMAT,OVER,OVERWRITE,OWNER,PARTITION,PARTITIONED,PARTITIONS,PATH,PERCENT,PKFK_JOIN,PLAN,PLANS,PLUS,POOL,PRECEDING,PRECISION,PREPARE,PRESERVE,PRIMARY,PRINCIPALS,PROCEDURE,PURGE,QUALIFY,QUARTER,QUERY,QUERY_PARALLELISM,RANGE,READ,READS,REAL,REBUILD,RECORDREADER,RECORDWRITER,REDUCE,REFERENCES,REGEXP,RELOAD,RELY,REMOTE,RENAME,REOPTIMIZATION,REPAIR,REPL,REPLACE,REPLICATION,RESOURCE,RESPECT,RESTRICT,REVOKE,REWRITE,RIGHT,RLIKE,ROLE,ROLES,ROLLBACK,ROLLUP,ROW,ROWS,SCHEDULED,SCHEDULING_POLICY,SCHEMA,SCHEMAS,SECOND,SECONDS,SELECT,SEMI,SERDE,SERDEPROPERTIES,SERVER,SET,SETS,SHARED,SHOW,SHOW_DATABASE,SKEWED,SMALLINT,SNAPSHOT,SOME,SORT,SORTED,SPEC,SSL,START,STATISTICS,STATUS,STORED,STREAMTABLE,STRING,STRUCT,SUMMARY,SYNC,SYSTEM_TIME,SYSTEM_VERSION,TABLE,TABLES,TABLESAMPLE,TBLPROPERTIES,TEMPORARY,TERMINATED,THEN,TIME,TIMESTAMP,TIMESTAMPLOCALTZ,TINYINT,TO,TOUCH,TRAILING,TRANSACTION,TRANSACTIONAL,TRANSACTIONS,TRANSFORM,TRIGGER,TRIM,TRUE,TRUNCATE,TYPE,UNARCHIVE,UNBOUNDED,UNDO,UNION,UNIONTYPE,UNIQUE,UNIQUEJOIN,UNKNOWN,UNLOCK,UNMANAGED,UNSET,UNSIGNED,UPDATE,URI,URL,USE,USER,USING,UTC,UTC_TMESTAMP,VALIDATE,VALUE,VALUES,VARCHAR,VECTORIZATION,VIEW,VIEWS,WAIT,WEEK,WEEKS,WHEN,WHERE,WHILE,WINDOW,WITH,WITHIN,WORK,WORKLOAD,WRITE,YEAR,YEARS,ZONE"
        return KEYWORDS.split(",")

    url = "https://raw.githubusercontent.com/apache/hive/master/parser/src/java/org/apache/hadoop/hive/ql/parse/HiveLexerParent.g"
    with urlopen(url) as f:
        code = f.read().decode("utf-8")
    result = []
    for word in re.findall(r"KW[\w\s]+:\s*\'(.*)\'", code):
        result += re.findall(r"\w+", word)
    result.sort()
    return result


def get_func():
    if not args.upgrade:
        BUILTIN_FUNCS = "ST_Aggr_ConvexHull,ST_Aggr_Union,ST_Area,ST_AsBinary,ST_AsGeoJson,ST_AsJson,ST_AsShape,ST_AsText,ST_Bin,ST_BinEnvelope,ST_Boundary,ST_Buffer,ST_Centroid,ST_Contains,ST_ConvexHull,ST_CoordDim,ST_Crosses,ST_Difference,ST_Dimension,ST_Disjoint,ST_Distance,ST_EndPoint,ST_EnvIntersects,ST_Envelope,ST_Equals,ST_ExteriorRing,ST_GeodesicLengthWGS84,ST_GeomCollection,ST_GeomFromGeoJson,ST_GeomFromJson,ST_GeomFromShape,ST_GeomFromText,ST_GeomFromWKB,ST_GeometryN,ST_GeometryProcessing,ST_InteriorRingN,ST_Intersection,ST_Intersects,ST_Is3D,ST_IsClosed,ST_IsEmpty,ST_IsMeasured,ST_IsRing,ST_IsSimple,ST_Length,ST_LineFromWKB,ST_LineString,ST_M,ST_MLineFromWKB,ST_MPointFromWKB,ST_MPolyFromWKB,ST_MaxM,ST_MaxX,ST_MaxY,ST_MaxZ,ST_MinM,ST_MinX,ST_MinY,ST_MinZ,ST_MultiLineString,ST_MultiPoint,ST_MultiPolygon,ST_NumGeometries,ST_NumInteriorRing,ST_NumPoints,ST_Overlaps,ST_Point,ST_PointFromWKB,ST_PointN,ST_PointZ,ST_PolyFromWKB,ST_Polygon,ST_Relate,ST_SRID,ST_SetSRID,ST_StartPoint,ST_SymmetricDiff,ST_Touches,ST_Union,ST_Within,ST_X,ST_Y,ST_Z,abs,acos,add_months,aes_decrypt,aes_encrypt,and,approx_distinct,array,array_contains,ascii,asin,assert_true,assert_true_oom,atan,avg,base64,between,bin,bloom_filter,bround,bucket_number,buildversion,cardinality_violation,case,cast_format,cbrt,ceil,ceiling,char_length,character_length,chr,coalesce,collect_list,collect_set,compute_bit_vector_fm,compute_bit_vector_hll,compute_stats,concat,concat_ws,context_ngrams,conv,corr,cos,count,covar_pop,covar_samp,crc32,create_union,cume_dist,current_authorizer,current_catalog,current_database,current_date,current_groups,current_schema,current_timestamp,current_user,date_add,date_format,date_sub,datediff,datetime_legacy_hybrid_calendar,day,dayofmonth,dayofweek,decode,degrees,dense_rank,deserialize,div,e,elt,encode,enforce_constraint,exception_in_vertex_udaf,exception_in_vertex_udf,exp,explode,extract_union,factorial,field,find_in_set,first_value,floor,floor_day,floor_hour,floor_minute,floor_month,floor_quarter,floor_second,floor_week,floor_year,format_number,from_unixtime,from_utc_timestamp,get_json_object,get_llap_splits,get_splits,get_sql_schema,greatest,grouping,hash,hex,histogram_numeric,hour,iceberg_bucket,if,in,in_bloom_filter,in_file,index,initcap,inline,instr,internal_interval,is_not_distinct_from,isfalse,isnotfalse,isnotnull,isnottrue,isnull,istrue,java_method,json_read,json_tuple,lag,last_day,last_value,last_value,lcase,lead,least,length,levenshtein,like,likeall,likeany,ln,locate,log,log10,log2,logged_in_user,lower,lpad,ltrim,map,map_keys,map_values,matchpath,max,md5,mid,min,minute,mod,month,months_between,murmur_hash,named_struct,ndv_compute_bit_vector,negative,next_day,ngrams,noop,noopstreaming,noopwithmap,noopwithmapstreaming,not,ntile,nullif,nvl,octet_length,or,parse_url,parse_url_tuple,percent_rank,percentile,percentile_approx,percentile_cont,percentile_disc,pi,pmod,posexplode,position,positive,pow,power,printf,quarter,quote,radians,rand,rank,reflect,reflect2,regexp,regexp_extract,regexp_replace,regr_avgx,regr_avgy,regr_count,regr_intercept,regr_r2,regr_slope,regr_sxx,regr_sxy,regr_syy,repeat,replace,replicate_rows,restrict_information_schema,reverse,rlike,round,row_number,rpad,rtrim,second,sentences,sha,sha1,sha2,shiftleft,shiftright,shiftrightunsigned,sign,sin,size,sort_array,sort_array_by,soundex,space,split,split_map_privs,sq_count_check,sqrt,stack,std,stddev,stddev_pop,stddev_samp,str_to_map,struct,substr,substring,substring_index,sum,surrogate_key,tan,to_date,to_epoch_milli,to_unix_timestamp,to_utc_timestamp,translate,trim,trunc,tumbling_window,ucase,unbase64,unhex,unix_timestamp,upper,uuid,validate_acid_sort_order,var_pop,var_samp,variance,version,weekofyear,when,width_bucket,windowingtablefunction,xpath,xpath_boolean,xpath_double,xpath_float,xpath_int,xpath_long,xpath_number,xpath_short,xpath_string,year"
        return BUILTIN_FUNCS.split(",")

    url = "https://raw.githubusercontent.com/apache/hive/master/ql/src/java/org/apache/hadoop/hive/ql/exec/FunctionRegistry.java"
    with urlopen(url) as f:
        code = f.read().decode("utf-8")
    result = (
        re.findall(r"public static[\w\s]+=\s*\"(\w+)\";", code)
        + re.findall(r"private static[\w\s]+=\s*\"(\w+)\";", code)
        + re.findall(r"system.register[\w\s]+\(\"(\w+)\"", code)
    )
    result.sort()
    return result


def substitute(content):
    keywords = get_func() + get_kws()
    if args.reserve:
        keywords += args.reserve.split(",")

    # tricks while file's first/last word is keyword.
    content = " " + content + " "
    for kw in keywords:
        # overlapping patterns
        # https://stackoverflow.com/questions/44009040/replacing-all-overlapping-patterns-in-a-string/44009095#44009095
        content = re.sub(rf"(?<=[^a-zA-Z0-9_\'\"`]){kw}(?=[^a-zA-Z0-9_\'\"`])", kw, content, flags=re.I)
    return content.strip()


def patch(content):
    # some special case
    # [1] SET xxx=yyy;
    # [2] ADD JAR hdfs:///...jar;
    # [3] #set ($VARIABLE="xxxx")
    # [4] QUERY/TIME => query/time
    content = re.sub(
        r"set ([\w\.]+)=([\w\.]+);", lambda m: f"SET {m.group(1).lower()}={m.group(2).lower()};", content, flags=re.I
    )

    content = re.sub("#set", "#set", content, flags=re.I)
    content = re.sub(r"hdfs:///([\w\.\/-]+);", lambda m: m.group(0).lower(), content, flags=re.I)
    content = re.sub("query", "query", content, flags=re.I)
    content = re.sub("time", "time", content, flags=re.I)
    return content


def main():
    path = Path(args.file)
    if path.is_file():
        with path.open("r", encoding="utf-8") as f:
            content = f.read()

        content = patch(substitute(content))
        Console.info("Format success")
        print(content)
        if not args.inplace:
            if args.output:
                path = Path(args.output)
            else:
                new_name = f"{path.stem}_copy{path.suffix}"
                path = Path(path.parent, new_name)

        with path.open("w", encoding="utf-8") as f:
            f.write(content)
        Console.info(f"Save in '{path.as_posix()}' ☕️")
    else:
        Console.error(f"File '{path.as_posix()}' not exit")


if __name__ == "__main__":
    main()
