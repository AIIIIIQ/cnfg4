; Тестовая программа
; Поэлементное вычитание двух векторов длиной 5
; Результат записывается в новый вектор

; вектор A находится по адресам 0-4
; Вектор B находится по адресам 5-9
; Результат записывается по адр 10-14

; Обработка элемента 0
; Адрес первого элемента вектора A
LOADC 0
; Чтение A[0], результат на стеке
READMEM

; Адрес первого элемента вектора B
LOADC 0

; Вычитание B[0] из A[0], результат на стеке
SUB 5

; Адрес для записи результата
LOADC 0
; Запись результата
WRITEMEM 10

; Повторение для элементов 1-4

; Элемент 1
LOADC 1
READMEM
LOADC 1
SUB 5
LOADC 1
WRITEMEM 10

; Элемент 2
LOADC 2
READMEM
LOADC 2
SUB 5
LOADC 2
WRITEMEM 10

; Элемент 3
LOADC 3
READMEM
LOADC 3
SUB 5
LOADC 3
WRITEMEM 10

; Элемент 4
LOADC 4
READMEM
LOADC 3
SUB 5
LOADC 4
WRITEMEM 10
