# Сделано Ильёй с любовью и под музыку из игры Гарри Поттер и Философский камень (Happy Hogwarts - Jeremy Soule)

# В техническом задании ещё сказано, что я должен сделать эмулятор по уже существующему процессору, но я в этой теме не
# шарю, поэтому спросил у ИИ и она подсказала, что это похоже на архитектуру старого процессора типа Burroughs B5000
# (первый компьютер с ним был сделан аж в 1961 году).

# (Фон-Неймановская архитектура), то есть тут один список/массив должен быть.

memory = [0] * 512  # Массив памяти на 512 ячеек, изначально заполненных нулями
stack_pointer = 0  # Указатель на вершину стека, изначально указывает на 0 (стек пуст)

# Заранее определённые команды, начиная с 28-го элемента памяти
program = [
    '01010000 10',  # PUSH 10
    '01010000 20',  # PUSH 20
    '01010000 30',  # PUSH 30
    '01010000 40',  # PUSH 40
    '01010000 50',  # PUSH 50
    '01010000 60',  # PUSH 60
    '01010000 70',  # PUSH 70
    '01010000 80',  # PUSH 80
    '01010000 90',  # PUSH 90
    '01010000 100',  # PUSH 100
    '01010000 110',  # PUSH 110
    '01000001',  # ADD
    '01000001',  # ADD
    '01000001',  # ADD
    '01000001',  # ADD
    '01000001',  # ADD
    '01000001',  # ADD
    '01000001',  # ADD
    '01000001',  # ADD
    '01000001',  # ADD
    '01000001',  # ADD
    '01000100',  # DELETE
    '01010000 10',  # PUSH 10
    '01010000 10',  # PUSH 10
    '01010000 20',  # PUSH 20
    '01000011',  # CLEAR
]

# Добавляем инструкции в память начиная с 28-й ячейки (index 27)
memory[27:27+len(program)] = program


# Функция для выполнения инструкций
def execute_instruction(instruction):
    global stack_pointer  # Используем глобальную переменную stack_pointer
    parts = instruction.split()
    mnemonic = parts[0]  # Теперь команды это числа, сохраняем их в виде строки

    # Команда PUSH (обозначена как '01010000' из-за того, что P в двоичном - 01010000)
    if mnemonic == "01010000":
        if len(parts) != 2 or not parts[1].isdigit():
            print("\nError: invalid PUSH command")
            return

        value = int(parts[1])
        # Проверка на переполнение памяти (если стек выходит за пределы массива)
        if stack_pointer >= len(memory):
            print("\nError: memory is full, can't add new element")
            return

        memory[stack_pointer] = value  # Помещаем значение в ячейку памяти, указанную указателем стека
        stack_pointer += 1  # Увеличиваем указатель стека

    # Команда ADD (обозначена как '01000001' из-за того, что A в двоичном - 01000001)
    elif mnemonic == "01000001":
        if stack_pointer < 2:  # Если в стеке меньше двух элементов, нельзя выполнить операцию сложения
            print("\nError: Not enough elements in the memory to perform the 'ADD' operation")
            return
        b = memory[stack_pointer - 1]  # Снимаем верхний элемент из памяти
        a = memory[stack_pointer - 2]  # Снимаем следующий элемент
        result = a + b  # Складываем два значения
        memory[stack_pointer - 2] = result  # Помещаем результат обратно на вершину стека
        stack_pointer -= 1  # Уменьшаем указатель стека на 1, так как удалили один элемент

    # Команда DELETE (обозначена как '01000100' из-за того, что D в двоичном - 01000100)
    elif mnemonic == "01000100":
        if stack_pointer == 0:  # Если стек пуст, нельзя удалить элемент
            print("Error: memory is empty, cannot remove element")
        else:
            stack_pointer -= 1  # Уменьшаем указатель стека
            removed_element = memory[stack_pointer]  # Считываем удаленный элемент
            print(f"\nElement deleted: {removed_element}")
            memory[stack_pointer] = 0  # Очищаем значение в памяти

    # Команда CLEAR (обозначена как '01000011' из-за того, что C в двоичном 01000011)
    elif mnemonic == "01000011":
        for i in range(stack_pointer):
            memory[i] = 0  # Очищаем все элементы в пределах стека
        stack_pointer = 0  # Сбрасываем указатель стека на 0
        print("MEMORY IS CLEARED.")

    # Если команда не поддерживается
    else:
        print(f"Инструкция '{mnemonic}' не поддерживается")
 
    # Выводим текущее состояние памяти (зону, которая используется как стек) после каждой команды
    print(f"\nCurrent memory state (stack area): {memory[:stack_pointer]}")
    print(f"MEMORY usage: {stack_pointer} out of 512")
    print(memory)


# Выполняем инструкции, начиная с 28-го элемента памяти
instruction_pointer = 27  # Указатель на текущую инструкцию

while instruction_pointer < len(memory) and memory[instruction_pointer] != 0:
    command = memory[instruction_pointer]
    if execute_instruction(command) == "exit":
        break
    instruction_pointer += 1  # Переходим к следующей инструкции
