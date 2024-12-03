; Тестовая программа
; Поэлементное вычитание двух векторов длиной 5
; Результат записывается в новый вектор

; вектор A находится по адресам 0-4
; Вектор B находится по адресам 5-9
; Результат записывается по адр 10-14



LOADC 10
LOADC 0
WRITEMEM 0
LOADC 20
LOADC 1
WRITEMEM 0
LOADC 30
LOADC 2
WRITEMEM 0
LOADC 40
LOADC 3
WRITEMEM 0
LOADC 50
LOADC 4
WRITEMEM 0

LOADC 1
LOADC 0
WRITEMEM 5
LOADC 2
LOADC 1
WRITEMEM 5
LOADC 3
LOADC 2
WRITEMEM 5
LOADC 4
LOADC 3
WRITEMEM 5
LOADC 5
LOADC 4
WRITEMEM 5



; Обработка элемента 0


; Адрес первого элемента вектора A
; Чтение A[0], результат на стеке
; Адрес первого элемента вектора B
; Вычитание B[0] из A[0], результат на стеке
; Адрес для записи результата
; Запись результата

LOADC 0
READMEM

LOADC 0

SUB 5

LOADC 0
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
LOADC 4
SUB 5
LOADC 4
WRITEMEM 10
