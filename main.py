# Сделано Ильёй с любовью и под музыку из игры Гарри Поттер и Философский камень (Happy Hogwarts - Jeremy Soule)

# В техническом задании ещё сказано, что я должен сделать эмулятор по уже существующему процессору, но я в этой теме не
# шарю, поэтому спросил у ИИ и она подсказала, что это похоже на архитектуру старого процессора типа Burroughs B5000
# (первый компьютер с ним был сделан аж в 1961 году).

# Заранее готовые инструкции (то есть простой набор действий по типу добавить 10 20 30, суммировать их и тд)
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
    0b01010000,  # PUSH 100
    100,
    0b01010000,  # PUSH 100
    100,
    0b01100110,  # FLAG FOR JUMP
    0b01000001,  # ADD
    0b01101010,  # JUMP
    0b01010000,  # PUSH 1
    1,
    0b01000100,  # DELETE
    0b01000011,  # CLEAR
]

# (Фон-Неймановская архитектура), то есть тут один список/массив должен быть.
memory = [0] * 512  # Память на 512 элементов
memory[:len(program)] = program
stack_pointer = len(program)

# Глобальная переменная для отслеживания, был ли JUMP перед PUSH
jump_flag = False
# Адрес на случай ошибки в ADD
fallback_address = None
# Флаг, что произошел переход на fallback
jump_to_fallback = False
# Флаг для вывода состояния памяти
memory_state_printed = False


def execute_instruction(instruction, next_val=None):
    global stack_pointer, jump_flag, fallback_address, jump_to_fallback, memory_state_printed

    # Команда PUSH
    if instruction == 0b01010000:
        if next_val is None or not isinstance(next_val, int):
            print("\nError: invalid PUSH command")
            return
        if jump_flag:
            # Если перед PUSH был JUMP, то возвращаем значение как адрес для перехода
            jump_flag = False  # Сбрасываем флаг JUMP
            fallback_address = next_val + 1  # Запоминаем fallback адрес
            return next_val  # Возвращаем значение для перехода по JUMP
        else:
            # Обычное поведение PUSH
            value = next_val
            if stack_pointer >= len(memory):
                print("\nError: memory is full, can't add new element")
                return
            memory[stack_pointer] = value
            stack_pointer += 1
            memory_state_printed = False  # Сбрасываем флаг вывода состояния памяти

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
        result = a + b
        memory[stack_pointer - 2] = result
        stack_pointer -= 1
        jump_to_fallback = False  # Сбрасываем флаг после успешного выполнения ADD
        memory_state_printed = False  # Сбрасываем флаг вывода состояния памяти

        # Проверка, остался ли в стеке только один элемент
        if stack_pointer - len(program) == 1:
            print("\nOnly one element left in the stack after ADD. Jumping to the instruction after PUSH 1.")
            jump_address = program.index(0b01101010)
            return program.index(0b01010000, jump_address + 1) + 2

    # Команда DELETE
    elif instruction == 0b01000100:
        if stack_pointer == len(program):
            print("Error: memory is empty, cannot remove element")
        else:
            stack_pointer -= 1
            removed_element = memory[stack_pointer]
            print(f"\nElement deleted: {removed_element}")
            memory[stack_pointer] = 0
            memory_state_printed = False  # Сбрасываем флаг вывода состояния памяти

    # Команда CLEAR
    elif instruction == 0b01000011:
        for i in range(len(program), stack_pointer):
            memory[i] = 0
        stack_pointer = len(program)
        for i in range(stack_pointer, len(memory)):
            memory[i] = 0
        print("MEMORY IS CLEARED.")
        memory_state_printed = False  # Сбрасываем флаг вывода состояния памяти

    # Команда JUMP
    elif instruction == 0b01101010:
        jump_flag = True  # Устанавливаем флаг, что JUMP был вызван
        return None  # Ждем следующую команду PUSH для перехода

    # Команда FLAG FOR JUMP
    elif instruction == 0b01100110:
        # Эта команда просто устанавливает флаг для JUMP
        pass

    else:
        print(f"Инструкция '{instruction}' не поддерживается")

    return None


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
        # Если был JUMP, устанавливаем переход на нужный адрес один раз
        if not jump_flag:  # Избегаем повторного выполнения
            try:
                jump_address = memory.index(0b01100110)
                instruction_pointer = jump_address  # Переход на найденный флаг
            except ValueError:
                print("Error: FLAG FOR JUMP not found")
                break
    else:
        result = execute_instruction(command)
        if result is not None:  # Если ADD вернула fallback адрес, переход на него
            instruction_pointer = result
            # Пропускаем команду ADD, которая вызвала ошибку, и продолжаем с DELETE
            if fallback_address:
                instruction_pointer += 1  # Пропускаем резервный адрес после прыжка
        else:
            instruction_pointer += 1  # Переход к следующей инструкции

    # Условие для вывода состояния памяти только один раз после выполнения команд, которые меняют память
    if command in [0b01010000, 0b01000001, 0b01000100, 0b01000011] and not memory_state_printed:
        print(f"\nCurrent memory state (stack area): {memory[len(program):stack_pointer]}")
        print(f"MEMORY usage: {stack_pointer} out of {512 - len(program)}")
        memory_state_printed = True  # Устанавливаем флаг, чтобы состояние памяти не выводилось снова

# Тест