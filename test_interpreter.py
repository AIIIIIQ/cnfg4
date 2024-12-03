import unittest
from assembler import Assembler
from interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.assembler = Assembler()
        self.interpreter = Interpreter()

    def test_loadc_execution(self):
        # Тестирование выполнения команды LOADC 48
        asm_code = "LOADC 48"
        self.assembler.assemble_code(asm_code)
        self.interpreter.initialize_memory()
        self.interpreter.run_instructions(self.assembler.instructions)
        # После выполнения LOADC 48 на стеке должно быть 48
        self.assertEqual(self.interpreter.stack[-1], 48)

    def test_readmem_execution(self):
        # Тестирование выполнения команды READMEM
        asm_code = """
        LOADC 100
        READMEM
        """
        self.assembler.assemble_code(asm_code)
        self.interpreter.initialize_memory()
        # Устанавливаем значение в памяти по адресу 100
        self.interpreter.memory[100] = 555
        self.interpreter.run_instructions(self.assembler.instructions)
        # На стеке должно быть значение 555
        self.assertEqual(self.interpreter.stack[-1], 555)

    def test_writemem_execution(self):
        # Тестирование выполнения команды WRITEMEM 25
        asm_code = """
        LOADC 555
        LOADC 200
        WRITEMEM 25
        """
        self.assembler.assemble_code(asm_code)
        self.interpreter.initialize_memory()
        self.interpreter.run_instructions(self.assembler.instructions)
        # Значение 555 должно быть записано по адресу 225 (200 + 25)
        self.assertEqual(self.interpreter.memory[225], 555)

    def test_sub_execution(self):
        # Тестирование выполнения команды SUB 10
        asm_code = """
        LOADC 50
        LOADC 300
        SUB 10
        """
        self.assembler.assemble_code(asm_code)
        self.interpreter.initialize_memory()
        self.interpreter.memory[310] = 20  # Устанавливаем значение в памяти по адресу 300 + 10
        self.interpreter.run_instructions(self.assembler.instructions)
        # На стеке должен быть результат 50 - 20 = 30
        self.assertEqual(self.interpreter.stack[-1], 30)

    def test_vector_subtraction_execution(self):
        # Тестирование выполнения программы vector_subtraction.asm
        with open('vector_subtraction.asm', 'r') as f:
            asm_code = f.read()
        self.assembler.assemble_code(asm_code)
        self.interpreter.initialize_memory()

        # Инициализируем вектор A в памяти по адресам 0-4
        #self.interpreter.memory[0:5] = [10, 20, 30, 40, 50]
        # Инициализируем вектор B в памяти по адресам 5-9
        #self.interpreter.memory[5:10] = [1, 2, 3, 4, 5]

        self.interpreter.run_instructions(self.assembler.instructions)
        # Проверяем результат вычитания в памяти
        # Результаты должны быть записаны по адресам 10-14
        expected_values = [9, 18, 27, 36, 45]
        for i in range(5):
            result = self.interpreter.memory[10 + i]
            expected = self.interpreter.memory[i] - self.interpreter.memory[5 + i]
            expected = expected_values[i]
            self.assertEqual(result, expected)
            # Можно вывести результаты для наглядности
            print(f"Memory[{10 + i}] = {result}")

if __name__ == '__main__':
    unittest.main()
