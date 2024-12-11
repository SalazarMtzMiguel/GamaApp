#!/bin/bash

headless_path=/opt/gama-platform/headless
java="java"

if [ -d "${headless_path}/../jdk" ]; then
  java="${headless_path}"/../jdk/bin/java
else
  javaVersion=$(java -version 2>&1 | head -n 1 | cut -d "\"" -f 2)
  if [[ ${javaVersion:2} == 17 ]]; then
    echo "You should use Java 17 to run GAMA"
    echo "Found you using version : $javaVersion"
    exit 1
  fi
fi

memory="0"
for arg do
  shift
  case $arg in
    -m) 
    memory="${1}" 
    shift 
    ;;
    *) 
    set -- "$@" "$arg" 
    ;;
  esac
done

if [[ $memory == "0" ]]; then
  memory=$(grep Xmx "${headless_path}"/../Gama.ini || echo "-Xmx4096m")
else
  memory=-Xmx$memory
fi

workspaceCreate=0
case "$@" in 
  *-help*|*-version*|*-validate*|*-test*|*-xml*|*-batch*|*-write-xmi*|*-socket*)
    workspaceCreate=1
    ;;
esac

function read_from_ini {
  start_line=$(grep -n -- '-server' "${headless_path}"/../Gama.ini | cut -d ':' -f 1)
  tail -n +$start_line "${headless_path}"/../Gama.ini | tr '\n' ' '
}

echo "******************************************************************"
echo "* GAMA version 1.9.3                                             *"
echo "* http://gama-platform.org                                       *"
echo "* (c) 2007-2023 UMI 209 UMMISCO IRD/SU & Partners                *"
echo "******************************************************************"
passWork=.workspace

# Crear el espacio de trabajo con WebSocket
if [ $workspaceCreate -eq 0 ]; then
  if [ ! -d "${@: -1}" ]; then
    mkdir ${@: -1}
  fi
  passWork=${@: -1}/.workspace$(find ${@: -1} -name ".workspace*" | wc -l)
  mkdir -p $passWork
else
  passWork=.workspace$(find ./ -maxdepth 1 -name ".workspace*" | wc -l)
fi

ini_arguments=$(read_from_ini)

# Ejecutar GAMA en modo WebSocket
if ! $java -cp /opt/gama-platform/plugins/org.eclipse.equinox.launcher*.jar -Xms512m $memory ${ini_arguments[@]} org.eclipse.core.launcher.Main -configuration "${headless_path}"/configuration -application msi.gama.headless.product -data $passWork "$@" -socket; then
    echo "Error in your command, here's the log:"
    cat $passWork/.metadata/.log
    exit 1
fi
