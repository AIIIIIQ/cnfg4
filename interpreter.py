import sys
import argparse
import csv

class Interpreter:
    def __init__(self):
        self.memory = [0] * 1024  # Память УВМ
        self.stack = []

    def initialize_memory(self):
        """
        Инициализация памяти перед выполнением программы.
        """
        # Инициализация памяти для тестов
        self.memory[0:5] = [10, 20, 30, 40, 50]  # Вектор A
        self.memory[5:10] = [1, 2, 3, 4, 5]  # Вектор B


        self.memory[100] = 17  # Для READMEM

        self.memory[785] = 21   # Для SUB

    def run(self, binary_file, result_file, mem_start, mem_end):
        # Инициализация памяти
        self.initialize_memory()

        # Чтение бинарного файла
        with open(binary_file, 'rb') as f:
            binary_data = f.read()
        instructions = [int.from_bytes(binary_data[i:i+4], byteorder='little') for i in range(0, len(binary_data), 4)]

        pc = 0  # Счётчик команд
        while pc < len(instructions):
            instr = instructions[pc]
            opcode = instr & 0b11111  # Биты 0-4
            operand = (instr >> 5) & 0b1111111111111  # Биты 5-17


            print(f'Executed opcode: {opcode}, operand: {operand}')

            if opcode == 16:  # LOADC
                self.stack.append(operand)
            elif opcode == 30:  # READMEM
                address = self.stack.pop()
                value = self.memory[address]
                print(f'Memory[{address}]: {self.memory[address]}')

                self.stack.append(value)
            elif opcode == 19:  # WRITEMEM
                address = self.stack.pop() + operand  # Адрес записи из стека + операнд
                value = self.stack.pop()  # Значение для записи

                # Запись значения в память
                self.memory[address] = value
                print(f'Memory[{address}]: {self.memory[address]}')
            elif opcode == 26:  # SUB
                address = self.stack.pop() + operand  # Адрес с учётом смещения
                value1 = self.stack.pop()  # Первый операнд (из стека)
                value2 = self.memory[address]  # Второй операнд из памяти
                print(f'Memory[{address}]: {self.memory[address]}')
                result = value1 - value2
                self.stack.append(result)
            else:
                raise ValueError(f'Unknown opcode: {opcode}')

            # Отладочная информация
            print(f'Stack: {self.stack}')

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
