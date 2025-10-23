# Usar PyMySQL como reemplazo de MySQLdb si está instalado
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
