import sys
import argparse
import csv

class Assembler:
    def __init__(self):
        self.instructions = []

    def assemble(self, input_file, output_file, log_file):
        with open(input_file, 'r') as f:
            lines = f.readlines()

        with open(log_file, 'w', newline='') as csvfile:
            log_writer = csv.writer(csvfile)
            log_writer.writerow(['Instruction', 'Opcode', 'Operand', 'Binary'])

            for line in lines:
                line = line.strip()
                if not line or line.startswith(';'):
                    continue  # Пропускаем пустые строки и комментарии
                parts = line.split()
                instr = parts[0].upper()
                if instr == 'LOADC':
                    value = int(parts[1])
                    opcode = 16  # Код операции A=16
                    operand = value  # Поле B
                    binary = self.encode_instruction(opcode, operand)
                    self.instructions.append(binary)
                    log_writer.writerow([line, opcode, operand, self.format_binary(binary)])
                elif instr == 'READMEM':
                    opcode = 30  # Код операции A=30
                    operand = 0  # Поле B не используется
                    binary = self.encode_instruction(opcode, operand)
                    self.instructions.append(binary)
                    log_writer.writerow([line, opcode, operand, self.format_binary(binary)])
                elif instr == 'WRITEMEM':
                    if len(parts) < 2:
                        raise ValueError(f"Missing operand for WRITEMEM in line: {line}")
                    offset = int(parts[1])  # Поле B
                    opcode = 19  # Код операции A=19
                    binary = self.encode_instruction(opcode, offset)
                    self.instructions.append(binary)
                    log_writer.writerow([line, opcode, offset, self.format_binary(binary)])

                elif instr == 'SUB':
                    if len(parts) < 2:
                        raise ValueError(f"Missing operand for SUB in line: {line}")
                    offset = int(parts[1])  # Поле B
                    opcode = 26  # Код операции A=26
                    binary = self.encode_instruction(opcode, offset)
                    self.instructions.append(binary)
                    log_writer.writerow([line, opcode, offset, self.format_binary(binary)])
                else:
                    raise ValueError(f'Unknown instruction: {instr}')

        with open(output_file, 'wb') as f:
            for instr in self.instructions:
                f.write(instr.to_bytes(4, byteorder='little'))

    def encode_instruction(self, opcode, operand):
        # opcode: биты 0-4 (5 бит)
        # operand: биты 5-17 (13 бит)
        instruction = (opcode & 0b11111)  # 5 бит для opcode
        instruction |= (operand & 0b1111111111111) << 5  # 13 бит для operand
        # Остальные биты (18-31) устанавливаются в 0
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
