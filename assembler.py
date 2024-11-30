import sys
import argparse
import csv

class Assembler:
    def __init__(self):
        self.instructions = []

    def assemble(self, input_file, output_file, log_file):
        with open(input_file, 'r') as f:
            code = f.read()
        self.assemble_code(code)

        with open(log_file, 'w', newline='') as csvfile:
            log_writer = csv.writer(csvfile)
            log_writer.writerow(['Instruction', 'Opcode', 'Operand', 'Binary'])

            for instr_info in self.instructions_info:
                log_writer.writerow([
                    instr_info['line'],
                    instr_info['opcode'],
                    instr_info['operand'],
                    instr_info['binary']
                ])

        with open(output_file, 'wb') as f:
            for instr in self.instructions:
                f.write(instr.to_bytes(4, byteorder='little'))

    def assemble_code(self, code):
        self.instructions = []
        self.instructions_info = []
        lines = code.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith(';'):
                continue  # Пропускаем пустые строки и комментарии
            parts = line.split()
            instr = parts[0].upper()
            if instr == 'LOADC':
                if len(parts) < 2:
                    raise ValueError(f"Missing operand for LOADC in line: {line}")
                value = int(parts[1])
                opcode = 16  # Код операции A=16
                operand = value  # Поле B
                operand_bits = 13  # Биты 5-17 (13 бит)
                binary = self.encode_instruction(opcode, operand, operand_bits)
                self.instructions.append(binary)
                self.instructions_info.append({
                    'line': line,
                    'opcode': opcode,
                    'operand': operand,
                    'binary': self.format_binary(binary)
                })
            elif instr == 'READMEM':
                opcode = 30  # Код операции A=30
                operand = 0  # Поле B не используется
                operand_bits = 0  # Операнд отсутствует
                binary = self.encode_instruction(opcode, operand, operand_bits)
                self.instructions.append(binary)
                self.instructions_info.append({
                    'line': line,
                    'opcode': opcode,
                    'operand': operand,
                    'binary': self.format_binary(binary)
                })
            elif instr == 'WRITEMEM':
                if len(parts) < 2:
                    raise ValueError(f"Missing operand for WRITEMEM in line: {line}")
                offset = int(parts[1])  # Поле B
                opcode = 19  # Код операции A=19
                operand_bits = 11  # Биты 5-15 (11 бит)
                binary = self.encode_instruction(opcode, offset, operand_bits)
                self.instructions.append(binary)
                self.instructions_info.append({
                    'line': line,
                    'opcode': opcode,
                    'operand': offset,
                    'binary': self.format_binary(binary)
                })
            elif instr == 'SUB':
                if len(parts) < 2:
                    raise ValueError(f"Missing operand for SUB in line: {line}")
                offset = int(parts[1])  # Поле B
                opcode = 26  # Код операции A=26
                operand_bits = 11  # Биты 5-15 (11 бит)
                binary = self.encode_instruction(opcode, offset, operand_bits)
                self.instructions.append(binary)
                self.instructions_info.append({
                    'line': line,
                    'opcode': opcode,
                    'operand': offset,
                    'binary': self.format_binary(binary)
                })
            else:
                raise ValueError(f'Unknown instruction: {instr}')

    def encode_instruction(self, opcode, operand, operand_bits):
        # opcode: биты 0-4 (5 бит)
        instruction = (opcode & 0b11111)  # 5 бит для opcode
        if operand_bits > 0:
            instruction |= (operand & ((1 << operand_bits) - 1)) << 5  # operand_bits для операнда
        # Остальные биты устанавливаются в 0
        return instruction

    def format_binary(self, value):
        return '0x' + value.to_bytes(4, byteorder='little').hex()

def main():
    parser = argparse.ArgumentParser(description='Assembler for UVM')
    parser.add_argument('-i', '--input', required=True, help='Input assembly file')
    parser.add_argument('-o', '--output', required=True, help='Output binary file')
    parser.add_argument('-l', '--log', required=True, help='Log file (CSV format)')
    args = parser.parse_args()

    assembler = Assembler()
    assembler.assemble(args.input, args.output, args.log)
    print('Assembling completed successfully.')

if __name__ == '__main__':
    main()
