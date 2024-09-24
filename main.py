# Сделано Ильёй с любовью и под музыку из игры Гарри Поттер и Философский камень (Happy Hogwarts - Jeremy Soule)

# В техническом задании ещё сказано, что я должен сделать эмулятор по уже существующему процессору, но я в этой теме не
# шарю, поэтому спросил у ИИ и она подсказала, что это похоже на архитектуру старого процессора типа Burroughs B5000
# (первый компьютер с ним был сделан аж в 1961 году).

# Заранее готовые инструкции (то есть простой набор действий по типу добавить 10 20 30, суммировать их и тд)
program = [
    0b01010000,  # PUSH 10
    10,
    0b01010000,  # PUSH 20
    20,
    0b01010000,  # PUSH 30
    30,
    0b01010000,  # PUSH 40
    40,
    0b01010000,  # PUSH 50
    50,
    0b01010000,  # PUSH 60
    60,
    0b01010000,  # PUSH 70
    70,
    0b01010000,  # PUSH 80
    80,
    0b01010000,  # PUSH 90
    90,
    0b01010000,  # PUSH 100
    100,
    0b01110011,  # SUM
    0b01010000,  # PUSH 110
    110,
    0b01010000,  # PUSH 110
    110,
    0b01010000,  # PUSH 110
    110,
    0b01010000,  # PUSH 110
    110,
    0b01000001,  # ADD
    0b01000001,  # ADD
    0b01000001,  # ADD
    0b01000100,  # DELETE
    0b01010000,  # PUSH 10
    10,
    0b01010000,  # PUSH 10
    10,
    0b01010000,  # PUSH 20
    20,
    0b01000011,  # CLEAR
]

# (Фон-Неймановская архитектура), то есть тут один список/массив должен быть.
memory = [0] * 512  # Память на 512 элементов
memory[:len(program)] = program
stack_pointer = len(program)


# Функция для выполнения инструкций
def execute_instruction(instruction, next_val=None):
    global stack_pointer

    # Команда PUSH (обозначена как 0b01010000)
    if instruction == 0b01010000:
        if next_val is None or not isinstance(next_val, int):
            print("\nError: invalid PUSH command")
            return

        value = next_val
        # Проверка на переполнение памяти
        if stack_pointer >= len(memory):
            print("\nError: memory is full, can't add new element")
            return

        memory[stack_pointer] = value
        stack_pointer += 1

    # Команда ADD (обозначена как 0b01000001)
    elif instruction == 0b01000001:
        if stack_pointer - len(program) < 2:  # Если в стеке меньше двух элементов после программы
            print("\nError: Not enough elements in the memory to perform the 'ADD' operation")
            return
        b = memory[stack_pointer - 1]
        a = memory[stack_pointer - 2]
        result = a + b
        memory[stack_pointer - 2] = result
        stack_pointer -= 1

    # Команда DELETE (обозначена как 0b01000100)
    elif instruction == 0b01000100:
        if stack_pointer == len(program):
            print("Error: memory is empty, cannot remove element")
        else:
            stack_pointer -= 1
            removed_element = memory[stack_pointer]
            print(f"\nElement deleted: {removed_element}")
            memory[stack_pointer] = 0

    # Команда CLEAR (обозначена как 0b01000011)
    elif instruction == 0b01000011:
        # Очищаем стек
        for i in range(len(program), stack_pointer):
            memory[i] = 0  # Очищаем память
        stack_pointer = len(program)  # Сбрасываем указатель стека на конец программы

        # Очищаем всю память после программы
        for i in range(stack_pointer, len(memory)):
            memory[i] = 0

        print("MEMORY IS CLEARED.")

    # Команда SUM (обозначена как 0b01110011)
    elif instruction == 0b01110011:
        if stack_pointer <= len(program):
            print("\nError: Not enough elements in the memory to perform the 'SUM' operation")
            return
        total_sum = sum(memory[len(program):stack_pointer])
        memory[len(program)] = total_sum  # Записываем сумму в первый элемент стека
        for i in range(len(program) + 1, stack_pointer):  # Обнуляем остальные элементы стека
            memory[i] = 0
        stack_pointer = len(program) + 1  # Обновляем указатель стека, чтобы указывать на следующий элемент после суммы
        print(f"Total sum of stack values: {total_sum}")

    # Проверка на дебила или если пользователь написал неверную команду
    else:
        print(f"Инструкция '{instruction}' не поддерживается")

    # Вывод текущего состояния памяти
    print(f"\nCurrent memory state (stack area): {memory[len(program):stack_pointer]}")
    print(f"MEMORY usage: {stack_pointer} out of {512 - len(program)}")
    print(memory)

# Выполняем инструкции начиная с конца программы
instruction_pointer = 0  # Указатель на первую инструкцию программы

while instruction_pointer < len(memory) and memory[instruction_pointer] != 0:
    command = memory[instruction_pointer]

    # Если команда PUSH, передаем следующее значение
    if command == 0b01010000:
        next_value = memory[instruction_pointer + 1]
        execute_instruction(command, next_value)
        instruction_pointer += 2  # Переход через команду и значение
    else:
        execute_instruction(command)
        instruction_pointer += 1  # Переход к следующей инструкции