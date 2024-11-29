import os
import subprocess

def run_test(test_name, asm_file, bin_file, log_file, result_file, mem_start, mem_end, init_memory=None):
    print(f'Running test: {test_name}')
    # Ассемблирование
    subprocess.run(['python', 'assembler.py', '-i', asm_file, '-o', bin_file, '-l', log_file])
    # Инициализация памяти (если требуется)
    if init_memory:
        interpreter_code = f'''
import sys
import argparse
import csv

class Interpreter:
    def __init__(self):
        self.memory = [0] * 1024  # Память УВМ
        self.stack = []

    def initialize_memory(self):
        {init_memory}

    def run(self, binary_file, result_file, mem_start, mem_end):
        self.initialize_memory()
        with open(binary_file, 'rb') as f:
            binary_data = f.read()
        instructions = [int.from_bytes(binary_data[i:i+4], byteorder='little') for i in range(0, len(binary_data), 4)]

        pc = 0  # Счётчик команд
        while pc < len(instructions):
            instr = instructions[pc]
            opcode = instr & 0b11111  # Биты 0-4
            operand = (instr >> 5) & 0b1111111111111  # Биты 5-17

            if opcode == 16:  # LOADC
                self.stack.append(operand)
            elif opcode == 30:  # READMEM
                address = self.stack.pop()
                value = self.memory[address]
                self.stack.append(value)
            elif opcode == 19:  # WRITEMEM
                value = self.stack.pop()
                address = self.stack.pop() + operand
                self.memory[address] = value
            elif opcode == 26:  # SUB
                value1 = self.stack.pop()
                address = self.stack.pop() + operand
                value2 = self.memory[address]
                result = value1 - value2
                self.stack.append(result)
            else:
                raise ValueError(f'Unknown opcode: {{opcode}}')

            pc += 1  # Переход к следующей инструкции

        # Сохранение результатов из памяти
        with open(result_file, 'w', newline='') as csvfile:
            result_writer = csv.writer(csvfile)
            result_writer.writerow(['Address', 'Value'])
            for addr in range(mem_start, mem_end + 1):
                result_writer.writerow([addr, self.memory[addr]])

        print('Execution completed successfully.')

def main():
    parser = argparse.ArgumentParser(description='Interpreter for UVM')
    parser.add_argument('-i', '--input', required=True, help='Input binary file')
    parser.add_argument('-o', '--output', required=True, help='Output result file (CSV)')
    parser.add_argument('--mem-start', type=int, required=True, help='Start address of memory range')
    parser.add_argument('--mem-end', type=int, required=True, help='End address of memory range')
    args = parser.parse_args()

    interpreter = Interpreter()
    interpreter.run(args.input, args.output, args.mem_start, args.mem_end)

if __name__ == '__main__':
    main()
'''
        with open('interpreter_temp.py', 'w') as f:
            f.write(interpreter_code)
        # Запуск интерпретатора с инициализацией памяти
        subprocess.run(['python', 'interpreter_temp.py', '-i', bin_file, '-o', result_file, '--mem-start', str(mem_start), '--mem-end', str(mem_end)])
        os.remove('interpreter_temp.py')
    else:
        # Запуск интерпретатора
        subprocess.run(['python', 'interpreter.py', '-i', bin_file, '-o', result_file, '--mem-start', str(mem_start), '--mem-end', str(mem_end)])

    print(f'Test {test_name} completed.\n')

def main():
    # Тест команды LOADC
    with open('test_loadc.asm', 'w') as f:
        f.write('LOADC 48\n')
    run_test('LOADC', 'test_loadc.asm', 'test_loadc.bin', 'test_loadc_log.csv', 'test_loadc_result.csv', 0, 0)

    # Тест команды READMEM
    with open('test_readmem.asm', 'w') as f:
        f.write('LOADC 100\nREADMEM\n')
    init_memory = 'self.memory[100] = 123'
    run_test('READMEM', 'test_readmem.asm', 'test_readmem.bin', 'test_readmem_log.csv', 'test_readmem_result.csv', 100, 100, init_memory)

    # Тест команды WRITEMEM
    with open('test_writemem.asm', 'w') as f:
        f.write('LOADC 555\nLOADC 200\nWRITEMEM 25\n')
    run_test('WRITEMEM', 'test_writemem.asm', 'test_writemem.bin', 'test_writemem_log.csv', 'test_writemem_result.csv', 225, 225)

    # Тест команды SUB
    with open('test_sub.asm', 'w') as f:
        f.write('LOADC 50\nLOADC 300\nSUB 10\n')
    init_memory = 'self.memory[310] = 20'
    run_test('SUB', 'test_sub.asm', 'test_sub.bin', 'test_sub_log.csv', 'test_sub_result.csv', 0, 0, init_memory)

    # Тестовая программа: поэлементное вычитание векторов
    with open('vector_subtraction.asm', 'w') as f:
        f.write('''
; Поэлементное вычитание двух векторов длиной 5

; Обработка элемента 0
LOADC 0
READMEM
LOADC 5
READMEM
SUB 0
LOADC 10
WRITEMEM 0

; Обработка элемента 1
LOADC 1
READMEM
LOADC 6
READMEM
SUB 0
LOADC 11
WRITEMEM 0

; Обработка элемента 2
LOADC 2
READMEM
LOADC 7
READMEM
SUB 0
LOADC 12
WRITEMEM 0

; Обработка элемента 3
LOADC 3
READMEM
LOADC 8
READMEM
SUB 0
LOADC 13
WRITEMEM 0

; Обработка элемента 4
LOADC 4
READMEM
LOADC 9
READMEM
SUB 0
LOADC 14
WRITEMEM 0
''')
    init_memory = '''
# Инициализация вектора A
self.memory[0] = 10
self.memory[1] = 20
self.memory[2] = 30
self.memory[3] = 40
self.memory[4] = 50
# Инициализация вектора B
self.memory[5] = 1
self.memory[6] = 2
self.memory[7] = 3
self.memory[8] = 4
self.memory[9] = 5
'''
    run_test('Vector Subtraction', 'vector_subtraction.asm', 'vector_subtraction.bin', 'vector_subtraction_log.csv', 'vector_subtraction_result.csv', 10, 14, init_memory)

if __name__ == '__main__':
    main()
