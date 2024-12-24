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
    0b01010000,  # PUSH добавляет 21
    21,
    0b01010011,  # READ команда читает число перед ней (21) и добавляет в стек значение по адресу 21 (то есть 1)
    0b01010000,  # PUSH добавляет 22
    22,
    0b01010011,  # READ команда читает число перед ней (22) и добавляет в стек значение по адресу 22 (то есть 2)
    0b01000001,  # ADD
    0b01010000,  # PUSH
    23,
    0b01010011,  # READ
    0b01000001,  # ADD
    0b01010000,  # PUSH
    24,
    0b01010011,  # READ
    0b01000001,  # ADD
    0b01010000,  # PUSH
    25,
    0b01010011,  # READ
    0b01000001,  # ADD
    0b01010000,  # PUSH
    26,
    0b01010011,  # READ
    0b01000001,  # ADD
    0b01010000,  # PUSH
    27,
    0b01010011,  # READ
    0b01000001,  # ADD
    0b01010000,  # PUSH
    28,
    0b01010011,  # READ
    0b01000001,  # ADD
    0b01010000,  # PUSH
    29,
    0b01010011,  # READ
    0b01000001,  # ADD
    0b01010000,  # PUSH
    30,
    0b01010011,  # READ
    0b01000001,  # ADD
]

memory = [0] * 512
memory[:len(program)] = program
memory[len(program):len(program) + 10] = [70]
memory[len(program) + 1:] = [0] * (512 - len(program) - 1)

stack_pointer = len(program)
jump_flag = False
fallback_address = None
jump_to_fallback = False

def execute_instruction(instruction, next_val=None, prev_val=None):
    """
    Выполняет инструкцию, заданную в виде битового кода, и обновляет состояние памяти и стека.

    Параметры:
    - instruction (int): Битовая команда, которую нужно выполнить.
    - next_val (int, опционально): Значение, которое следует использовать для команды, если она требует аргумента (например, PUSH).
    - prev_val (int, опционально): Значение, которое следует использовать для команды, если она требует предыдущего аргумента (например, READ).

    Возвращает:
    - int: Возвращает адрес перехода, если команда JUMP или подобная, иначе None.

    Описание команд:
    - 0b01010000 (PUSH): Добавляет значение в стек. Если установлен флаг перехода, сохраняет значение как адрес возврата.
    - 0b01000001 (ADD): Складывает два верхних элемента стека и сохраняет результат на месте первого элемента.
    - 0b01000100 (DELETE): Удаляет верхний элемент стека.
    - 0b01000011 (CLEAR): Очищает весь стек.
    - 0b01101010 (JUMP): Выполняет цикл сложения до тех пор, пока в стеке есть элементы.
    - 0b01010011 (READ): Читает значение из памяти по указанному адресу и добавляет его в стек.

    Глобальные переменные:
    - stack_pointer (int): Указатель на текущую позицию в стеке.
    - jump_flag (bool): Флаг, указывающий на необходимость сохранения адреса возврата.
    - fallback_address (int): Адрес возврата для команды JUMP.
    - jump_to_fallback (bool): Флаг, указывающий на необходимость перехода к адресу возврата.

    Примечания:
    - Функция также выводит текущее состояние стека и использование памяти.
    - Если команда не распознана, она игнорируется.
    """    
    global stack_pointer, jump_flag, fallback_address, jump_to_fallback
    if instruction == 0b01010000:
        if next_val is None or not isinstance(next_val, int):
            print("\nError: invalid PUSH command")
            return
        if jump_flag:
            jump_flag = False
            fallback_address = next_val
            return next_val
        else:
            value = next_val
            if stack_pointer >= len(memory):
                print("\nError: memory is full, can't add new element")
                return
            memory[stack_pointer] = value
            stack_pointer += 1
    elif instruction == 0b01000001:
        if stack_pointer - len(program) < 2:
            print("\nError: Not enough elements in the memory to perform the 'ADD' operation")
            if fallback_address is not None and not jump_to_fallback:
                print(f"\nJumping to fallback address: {fallback_address}")
                jump_to_fallback = True
                return fallback_address
            return
        b = memory[stack_pointer - 1]
        a = memory[stack_pointer - 2]
        sum_result = a + b
        memory[stack_pointer - 2] = sum_result
        stack_pointer -= 1
        jump_to_fallback = False
    elif instruction == 0b01000100:
        if stack_pointer == len(program):
            print("Error: memory is empty, cannot remove element")
        else:
            stack_pointer -= 1
            removed_element = memory[stack_pointer]
            print(f"\nElement deleted: {removed_element}")
            memory[stack_pointer] = 0
        jump_to_fallback = False
    elif instruction == 0b01000011:
        for i in range(len(program), stack_pointer):
            memory[i] = 0
        stack_pointer = len(program)
        for i in range(stack_pointer, len(memory)):
            memory[i] = 0
        print("MEMORY IS CLEARED.")
        jump_to_fallback = False
    elif instruction == 0b01101010:
        while stack_pointer - len(program) > 1:
            execute_instruction(0b01000001)
    elif instruction == 0b01010011:
        if prev_val is None or not isinstance(prev_val, int):
            print("\nError: invalid READ command")
            return
        if prev_val >= len(memory):
            print("\nError: invalid memory address for READ")
            return
        value = memory[prev_val]
        if stack_pointer > len(program):
            stack_pointer -= 1
            memory[stack_pointer] = 0
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
    # print(memory)

def run_program():
    """
    Запускает выполнение программы, интерпретируя команды из памяти.

    Эта функция проходит по памяти, извлекает команды и выполняет их с помощью функции `execute_instruction`.
    Она продолжает выполнение до тех пор, пока не достигнет конца памяти или команды, которая завершает выполнение (например, команда с нулевым значением).

    Глобальные переменные:
    - instruction_pointer (int): Указатель на текущую команду в памяти.
    - memory (list): Массив, представляющий память, содержащую команды и данные.

    Примечания:
    - Функция использует глобальные переменные `instruction_pointer` и `memory`.
    - После выполнения команды функция обновляет `instruction_pointer` в зависимости от типа команды.
    - Если команда требует перехода (например, JUMP), `instruction_pointer` устанавливается на новый адрес.
    """
    global instruction_pointer
    while instruction_pointer < len(memory) and memory[instruction_pointer] != 0:
        command = memory[instruction_pointer]
        if command == 0b01010000:  # PUSH
            next_value = memory[instruction_pointer + 1]
            result = execute_instruction(command, next_value)
            if result is not None:
                instruction_pointer = result
            else:
                instruction_pointer += 2
        elif command == 0b01101010:  # JUMP
            execute_instruction(command)
            instruction_pointer += 1
        elif command == 0b01010011:  # READ
            prev_value = memory[instruction_pointer - 1]
            execute_instruction(command, prev_val=prev_value)
            instruction_pointer += 1
        else:
            result = execute_instruction(command)
            if result is not None:
                instruction_pointer = result
                if fallback_address:
                    instruction_pointer += 1
            else:
                instruction_pointer += 1

instruction_pointer = 0
run_program()
