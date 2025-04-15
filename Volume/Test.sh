#!/bin/bash
# ${1} — UUID
cd "/teyusu/stud/${1}"

for i in {1..50}; do
    if [ ! -f T${i}I.txt ]; then exit 0; fi
    ./a.out <T${i}I.txt >T${i}A.txt

    errcode=$?
    if [ $errcode -gt 0 ]; then
        # Ошибка исполнения: 1 e 1
        echo "${i} e ${errcode}" >>Testing.log
    fi

    cmp -s T${i}O.txt T${i}A.txt
    if [ $? -eq 1 ]; then
        # Ошибка проверки: 1 w
        echo "${i} w" >>Testing.log
    fi
done