#!/bin/bash
# ${1} — UUID, ${2} — номер упражнения
cd "/teyusu/stud/${1}"

# Генерация файлов тестов
/teyusu/gtv2 "/teyusu/exercises/${2}.xml" &>Compilation.log
if [ $? -gt 0 ]; then exit $?; fi

# Компиляция кода
g++ Main.cpp -O2 -s -static &>>Compilation.log
exit $?