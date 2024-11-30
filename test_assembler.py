import unittest
from assembler import Assembler

class TestAssembler(unittest.TestCase):
    def setUp(self):
        self.assembler = Assembler()

    def test_loadc(self):
        # Тестирование команды LOADC 48
        asm_code = "LOADC 48"
        expected_binary = [16, 6, 0, 0]  # 0x10, 0x06, 0x00, 0x00
        self.assembler.assemble_code(asm_code)
        result_binary = self.assembler.instructions[0].to_bytes(4, byteorder='little')
        self.assertEqual(list(result_binary), expected_binary)

    def test_readmem(self):
        # Тестирование команды READMEM
        asm_code = "READMEM"
        expected_binary = [30, 0, 0, 0]  # 0x1E, 0x00, 0x00, 0x00
        self.assembler.assemble_code(asm_code)
        result_binary = self.assembler.instructions[0].to_bytes(4, byteorder='little')
        self.assertEqual(list(result_binary), expected_binary)

    def test_writemem(self):
        # Тестирование команды WRITEMEM 425
        asm_code = "WRITEMEM 425"
        expected_binary = [51, 53, 0, 0]  # 0x33, 0x35, 0x00, 0x00
        self.assembler.assemble_code(asm_code)
        result_binary = self.assembler.instructions[0].to_bytes(4, byteorder='little')
        self.assertEqual(list(result_binary), expected_binary)

    def test_sub(self):
        # Тестирование команды SUB 784
        asm_code = "SUB 784"
        expected_binary = [26, 98, 00, 0]  # 0x1A, 0x62, 0x00, 0x00
        self.assembler.assemble_code(asm_code)
        result_binary = self.assembler.instructions[0].to_bytes(4, byteorder='little')
        self.assertEqual(list(result_binary), expected_binary)

if __name__ == '__main__':
    unittest.main()
