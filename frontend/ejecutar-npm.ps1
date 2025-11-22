# Script para ejecutar npm evitando problemas de política de ejecución
$env:Path = "C:\Program Files\nodejs;" + $env:Path
& npm $args

