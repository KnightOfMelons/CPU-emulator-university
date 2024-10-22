program = [
    0b01010000,  # PUSH 70
    70,
    0b01010000,  # PUSH 80
    80,
    0b01010000,  # PUSH 90
    90,
    0b01010000,  # PUSH 100
    100,
    0b01010000,  # PUSH 100
    100,
    0b01010000,  # PUSH 100
    100,
    0b01010000,  # PUSH 100
    100,
    0b01000001,  # ADD. JUMP прыгает сюда
    0b01010000,  # PUSH 18
    18,  # Адрес для JUMP
    0b01101010,  # JUMP
    0b01000100,  # DELETE
    0b01000011,  # CLEAR
    10,  # Количество следующих чисел
    1,  # READ указал на это число
    2,  # READ второй указал на это число
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    0b01010011,  # Вызывается команда READ
    21,  # Нужно прочитать значение под индексом 23 (1) и поместить в стек
    0b01010011,  # Вызывается команда READ снова
    22,  # Нужно прочитать значение под индексом 24 (2) и поместить в стек
    0b01010011,
    23,
    0b01010011,
    24,
    0b01010011,
    25,
    0b01010011,
    26,
    0b01010011,
    27,
    0b01010011,
    28,
    0b01010011,
    29,
    0b01010011,
    30,
]

memory = [0] * 512  # Память на 512 элементов

# Заполняем память в нужном порядке
memory[:len(program)] = program  # Сначала основная программа
memory[len(program):len(program) + 10] = [70]  # Следующее значение - 70
memory[len(program) + 1:] = [0] * (512 - len(program) - 1)  # Оставляем место для других данных

stack_pointer = len(program)

# Глобальная переменная для отслеживания, был ли JUMP перед PUSH
jump_flag = False
# Адрес на случай ошибки в ADD
fallback_address = None
# Флаг, что произошел переход на fallback
jump_to_fallback = False


def execute_instruction(instruction, next_val=None):
    global stack_pointer, jump_flag, fallback_address, jump_to_fallback

    # Команда PUSH
    if instruction == 0b01010000:
        if next_val is None or not isinstance(next_val, int):
            print("\nError: invalid PUSH command")
            return
        if jump_flag:
            jump_flag = False  # Сбрасываем флаг JUMP
            fallback_address = next_val  # Запоминаем адрес перед JUMP для возврата после цикла ADD
            return next_val  # Возвращаем значение для перехода по JUMP
        else:
            value = next_val
            if stack_pointer >= len(memory):
                print("\nError: memory is full, can't add new element")
                return
            memory[stack_pointer] = value
            stack_pointer += 1

    # Команда ADD
    elif instruction == 0b01000001:
        if stack_pointer - len(program) < 2:
            print("\nError: Not enough elements in the memory to perform the 'ADD' operation")
            if fallback_address is not None and not jump_to_fallback:
                print(f"\nJumping to fallback address: {fallback_address}")
                jump_to_fallback = True  # Помечаем, что перешли на fallback
                return fallback_address  # Переход к резервному адресу
            return
        b = memory[stack_pointer - 1]
        a = memory[stack_pointer - 2]
        sum_result = a + b  # Переименовали 'result' в 'sum_result'
        memory[stack_pointer - 2] = sum_result
        stack_pointer -= 1
        jump_to_fallback = False  # Сбрасываем флаг после успешного выполнения ADD

    # Команда DELETE
    elif instruction == 0b01000100:
        if stack_pointer == len(program):
            print("Error: memory is empty, cannot remove element")
        else:
            stack_pointer -= 1
            removed_element = memory[stack_pointer]
            print(f"\nElement deleted: {removed_element}")
            memory[stack_pointer] = 0
        jump_to_fallback = False  # Сбрасываем флаг после выполнения DELETE

    # Команда CLEAR
    elif instruction == 0b01000011:
        for i in range(len(program), stack_pointer):
            memory[i] = 0
        stack_pointer = len(program)
        for i in range(stack_pointer, len(memory)):
            memory[i] = 0
        print("MEMORY IS CLEARED.")
        jump_to_fallback = False  # Сбрасываем флаг после выполнения CLEAR

    # Команда JUMP
    elif instruction == 0b01101010:
        while stack_pointer - len(program) > 1:  # Пока в стеке больше одного элемента
            execute_instruction(0b01000001)  # Выполняем ADD

    # Команда READ
    elif instruction == 0b01010011:
        if next_val is None or not isinstance(next_val, int):
            print("\nError: invalid READ command")
            return
        # Получаем значение по индексу, который указан как next_val
        if next_val >= len(memory):
            print("\nError: invalid memory address for READ")
            return
        value = memory[next_val]
        # Добавляем это значение в стек
        if stack_pointer >= len(memory):
            print("\nError: memory is full, can't add new element")
            return
        memory[stack_pointer] = value
        stack_pointer += 1

    else:
        if instruction < 0b01010000 or instruction > 0b01101010:
            return

    print(f"\nCurrent memory state (stack area): {memory[len(program):stack_pointer]}")
    print(f"MEMORY usage: {stack_pointer} out of {512 - len(program)}")
    print(memory)


# Выполняем инструкции начиная с начала программы
instruction_pointer = 0  # Указатель на первую инструкцию

while instruction_pointer < len(memory) and memory[instruction_pointer] != 0:
    command = memory[instruction_pointer]

    # Если команда PUSH, передаем следующее значение
    if command == 0b01010000:
        next_value = memory[instruction_pointer + 1]
        result = execute_instruction(command, next_value)
        if result is not None:  # Если результат не None, значит PUSH работал как указатель для JUMP
            instruction_pointer = result  # Переходим к новой инструкции (значение PUSH как адрес)
        else:
            instruction_pointer += 2  # Переход через команду и значение
    elif command == 0b01101010:
        execute_instruction(command)
        instruction_pointer += 1  # Переход к следующей инструкции (после JUMP и ADD)
    elif command == 0b01010011:  # READ команда
        next_value = memory[instruction_pointer + 1]
        execute_instruction(command, next_value)
        instruction_pointer += 2  # Переход через команду и значение
    else:
        result = execute_instruction(command)
        if result is not None:  # Если ADD вернула fallback адрес, переход на него
            instruction_pointer = result
            if fallback_address:
                instruction_pointer += 1  # Пропускаем резервный адрес после прыжка
        else:
            instruction_pointer += 1  # Переход к следующей инструкции
