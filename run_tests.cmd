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
