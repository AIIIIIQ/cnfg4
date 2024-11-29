# Разработка ассемблера и интерпретатора для учебной виртуальной машины (УВМ)

## План работы

1. **Понимание системы команд УВМ:**
   - Разобрать структуру каждой команды.
   - Понять, как закодированы команды в бинарном файле.
2. **Разработка ассемблера:**
   - Определить читаемое представление команд.
   - Реализовать парсер исходного текста программы.
   - Реализовать генерацию бинарного файла.
   - Создать лог-файл с ассемблированными инструкциями в формате `ключ=значение`.
3. **Разработка интерпретатора:**
   - Реализовать загрузку бинарного файла.
   - Реализовать выполнение команд УВМ.
   - Реализовать вывод значений из диапазона памяти в файл-результат в формате CSV.
4. **Тестирование:**
   - Реализовать тесты для каждой команды, используя предоставленные тестовые данные.
   - Написать и отладить тестовую программу для выполнения поэлементного вычитания над двумя векторами длины 5.

## 1. Понимание системы команд УВМ

### Структура команды

Каждая команда УВМ имеет размер 4 байта (32 бита). Биты команды распределены следующим образом:

- **Биты 0–4 (5 бит):** Код операции (A).
- **Биты 5–17 (13 бит):** Операнд или дополнительные данные (B).
- **Биты 18–31 (14 бит):** Зарезервированы или не используются (устанавливаются в ноль).

**Примечание:** Нумерация битов начинается с младшего бита (самого правого).

### Команды и их описание

1. **Загрузка константы**

   - **Код операции (A):** 16
   - **Операнд (B):** 16-битное значение, которое будет помещено на стек.
   - **Описание:** Помещает значение B на вершину стека.
   - **Тестовый пример:** A=16, B=48
     - Бинарная команда: `0x10, 0x06, 0x00, 0x00`

2. **Чтение значения из памяти**

   - **Код операции (A):** 30
   - **Описание:** Снимает адрес с вершины стека, читает значение из памяти по этому адресу, помещает его на стек.
   - **Тестовый пример:** A=30
     - Бинарная команда: `0x1E, 0x00, 0x00, 0x00`

3. **Запись значения в память**

   - **Код операции (A):** 19
   - **Операнд (B):** Смещение
   - **Описание:** Снимает значение и адрес с вершины стека, записывает значение в память по адресу `адрес + смещение`.
   - **Тестовый пример:** A=19, B=425
     - Бинарная команда: `0x33, 0x35, 0x00, 0x00`

4. **Бинарная операция: вычитание**

   - **Код операции (A):** 26
   - **Операнд (B):** Смещение
   - **Описание:** Снимает значение и адрес с вершины стека, читает второе значение из памяти по адресу `адрес + смещение`, вычитает второе значение из первого, результат помещает на стек.
   - **Тестовый пример:** A=26, B=784
     - Бинарная команда: `0x1A, 0x62, 0x00, 0x00`

## 2. Разработка ассемблера

### 2.1. Читаемое представление команд

Определим простой синтаксис для каждой команды:

- **LOADC value**
  - Загрузка константы на стек.
- **READMEM**
  - Чтение значения из памяти по адресу с вершины стека.
- **WRITEMEM offset**
  - Запись значения в память по адресу `адрес + смещение`.
- **SUB offset**
  - Вычитание значения из памяти по адресу `адрес + смещение` из значения на вершине стека.

### 2.2. Реализация ассемблера

Ассемблер будет состоять из следующих шагов:

1. **Парсинг исходного файла:**
   - Чтение исходного файла построчно.
   - Разбор каждой строки на команду и операнды.
2. **Генерация бинарного кода:**
   - Кодирование каждой команды в соответствии с заданной структурой.
   - Запись бинарных данных в выходной файл.
3. **Создание лог-файла:**
   - Запись ассемблированных инструкций в формате `ключ=значение` в лог-файл.

- **Класс `Assembler`:**
  - Метод `assemble` читает входной файл, разбирает команды и записывает бинарный код и лог.
  - Метод `encode_instruction` кодирует команду в 4-байтовое бинарное представление.
- **Используется модуль `struct`** для упаковки чисел в бинарный формат.

**Запуск ассемблера:**

```bash
assembler.py -i <input_program.asm> -o <output_program.bin> -l <program_log.csv>
```

## 3. Разработка интерпретатора

### 3.1. Реализация интерпретатора

Интерпретатор будет выполнять следующие действия:

1. **Загрузка бинарного файла:**
   - Чтение бинарного файла и разбор инструкций.
2. **Инициализация памяти и стека:**
   - Создание памяти заданного размера.
   - Инициализация стека.
3. **Выполнение инструкций:**
   - Последовательное выполнение инструкций из бинарного файла.
4. **Сохранение результатов:**
   - Запись значений из указанного диапазона памяти в CSV-файл.

- **Класс `Interpreter`:**
  - Инициализирует память и стек.
  - Метод `run` выполняет инструкции из бинарного файла.
  - Обрабатывает каждый код операции в соответствии с его функциональностью.
  - Записывает содержимое памяти в указанный диапазон в CSV-файл.

### 3.2. Запуск интерпретатора

```bash
interpreter.py -i <output_program.bin> -o <result_output.csv> --mem-start <start_address> --mem-end <end_address>
```

## 4. Тестирование

### 4.1. Сценарий для запуска тестов

- **Файл `run_tests.cmd`:**
```
@echo off

echo ==========================================
echo Running test_loadc.asm...
assembler.py -i test_loadc.asm -o test_loadc.bin -l test_loadc_log.csv
interpreter.py -i test_loadc.bin -o test_loadc_result.csv --mem-start 0 --mem-end 0
echo Completed test_loadc.asm
echo.

echo ==========================================
echo Running test_readmem.asm...
assembler.py -i test_readmem.asm -o test_readmem.bin -l test_readmem_log.csv
interpreter.py -i test_readmem.bin -o test_readmem_result.csv --mem-start 0 --mem-end 0
echo Completed test_readmem.asm
echo.

echo ==========================================
echo Running test_writemem.asm...
assembler.py -i test_writemem.asm -o test_writemem.bin -l test_writemem_log.csv
interpreter.py -i test_writemem.bin -o test_writemem_result.csv --mem-start 225 --mem-end 225
echo Completed test_writemem.asm
echo.

echo ==========================================
echo Running test_sub.asm...
assembler.py -i test_sub.asm -o test_sub.bin -l test_sub_log.csv
interpreter.py -i test_sub.bin -o test_sub_result.csv --mem-start 0 --mem-end 0
echo Completed test_sub.asm
echo.

echo ==========================================
echo Running vector_subtraction.asm...
assembler.py -i vector_subtraction.asm -o vector_subtraction.bin -l vector_subtraction_log.csv
interpreter.py -i vector_subtraction.bin -o vector_subtraction_result.csv --mem-start 10 --mem-end 14
echo Completed vector_subtraction.asm
echo.

echo ==========================================
echo All tests have been executed.
pause
```


### 4.2. Результат выполнения тестов

```
==========================================
Running test_loadc.asm...
Assembling completed successfully.
Executed opcode: 16, operand: 48
Stack: [48]
Execution completed successfully.
Completed test_loadc.asm

==========================================
Running test_readmem.asm...
Assembling completed successfully.
Executed opcode: 16, operand: 100
Stack: [100]
Executed opcode: 30, operand: 0
Memory[100]: 17
Stack: [17]
Execution completed successfully.
Completed test_readmem.asm

==========================================
Running test_writemem.asm...
Assembling completed successfully.
Executed opcode: 16, operand: 555
Stack: [555]
Executed opcode: 16, operand: 0
Stack: [555, 0]
Executed opcode: 19, operand: 425
Memory[425]: 555
Stack: []
Execution completed successfully.
Completed test_writemem.asm

==========================================
Running test_sub.asm...
Assembling completed successfully.
Executed opcode: 16, operand: 49
Stack: [49]
Executed opcode: 16, operand: 1
Stack: [49, 1]
Executed opcode: 26, operand: 784
Memory[785]: 21
Stack: [28]
Execution completed successfully.
Completed test_sub.asm

==========================================
Running vector_subtraction.asm...
Assembling completed successfully.
Executed opcode: 16, operand: 0
Stack: [0]
Executed opcode: 30, operand: 0
Memory[0]: 10
Stack: [10]
Executed opcode: 16, operand: 0
Stack: [10, 0]
Executed opcode: 26, operand: 5
Memory[5]: 1
Stack: [9]
Executed opcode: 16, operand: 0
Stack: [9, 0]
Executed opcode: 19, operand: 10
Memory[10]: 9
Stack: []
Executed opcode: 16, operand: 1
Stack: [1]
Executed opcode: 30, operand: 0
Memory[1]: 20
Stack: [20]
Executed opcode: 16, operand: 1
Stack: [20, 1]
Executed opcode: 26, operand: 5
Memory[6]: 2
Stack: [18]
Executed opcode: 16, operand: 1
Stack: [18, 1]
Executed opcode: 19, operand: 10
Memory[11]: 18
Stack: []
Executed opcode: 16, operand: 2
Stack: [2]
Executed opcode: 30, operand: 0
Memory[2]: 30
Stack: [30]
Executed opcode: 16, operand: 2
Stack: [30, 2]
Executed opcode: 26, operand: 5
Memory[7]: 3
Stack: [27]
Executed opcode: 16, operand: 2
Stack: [27, 2]
Executed opcode: 19, operand: 10
Memory[12]: 27
Stack: []
Executed opcode: 16, operand: 3
Stack: [3]
Executed opcode: 30, operand: 0
Memory[3]: 40
Stack: [40]
Executed opcode: 16, operand: 3
Stack: [40, 3]
Executed opcode: 26, operand: 5
Memory[8]: 4
Stack: [36]
Executed opcode: 16, operand: 3
Stack: [36, 3]
Executed opcode: 19, operand: 10
Memory[13]: 36
Stack: []
Executed opcode: 16, operand: 4
Stack: [4]
Executed opcode: 30, operand: 0
Memory[4]: 50
Stack: [50]
Executed opcode: 16, operand: 3
Stack: [50, 3]
Executed opcode: 26, operand: 5
Memory[8]: 4
Stack: [46]
Executed opcode: 16, operand: 4
Stack: [46, 4]
Executed opcode: 19, operand: 10
Memory[14]: 46
Stack: []
Execution completed successfully.
Completed vector_subtraction.asm

==========================================
All tests have been executed.
Для продолжения нажмите любую клавишу . . .
  ```
