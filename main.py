# Сделано Ильёй с любовью и под музыку из игры Гарри Поттер и Философский камень (Happy Hogwarts - Jeremy Soule)

# В техническом задании ещё сказано, что я должен сделать эмулятор по уже существующему процессору, но я в этой теме не
# шарю, поэтому спросил у ИИ и она подсказала, что это похоже на архитектуру старого процессора типа Burroughs B5000
# (первый компьютер с ним был сделан аж в 1961 году).

# (Фон-Неймановская архитектура), то есть тут один список/массив должен быть.
# Память на 512 элементов

# НЕОБХОДИМО СДЕЛАТЬ ЗАРАНЕЕ ГОТОВЫЙ НАБОР ИНСТРУКЦИЙ, КОТОРАЯ БЫ ПРОГРАММА ПОНИМАЛА, типа:
# 'PUSH 10'
# 'PUSH 20'
# ADD
# ADD

memory = [0] * 512  # Массив памяти на 512 ячеек, изначально заполненных нулями
stack_pointer = 0  # Указатель на вершину стека, изначально указывает на 0 (стек пуст)


# Функция для выполнения инструкций
def execute_instruction(instruction):
    global stack_pointer  # Используем глобальную переменную stack_pointer
    parts = instruction.split()
    mnemonic = parts[0].upper()  # Все команды привожу к верхнему регистру, типа "проверка на дебила", мало ли

    # Команда для помещения значения в память (в стек). То есть пишешь PUSH 100, затем в память добавляется соточка,
    # получается: === Текущий стек: 100 ===
    if mnemonic == "PUSH":
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

    # Команда ADD для складывания двух верхних элементов памяти (в пределах стека)
    elif mnemonic == "ADD":
        if stack_pointer < 2:  # Если в стеке меньше двух элементов, нельзя выполнить операцию сложения
            print("\nError: Not enough elements in the memory to perform the 'ADD' operation")
            return
        b = memory[stack_pointer - 1]  # Снимаем верхний элемент из памяти
        a = memory[stack_pointer - 2]  # Снимаем следующий элемент
        result = a + b  # Складываем два значения
        memory[stack_pointer - 2] = result  # Помещаем результат обратно на вершину стека
        stack_pointer -= 1  # Уменьшаем указатель стека на 1, так как удалили один элемент

    # Команда DELETE для удаления последнего элемента из памяти (стека)
    elif mnemonic == "DELETE":
        if stack_pointer == 0:  # Если стек пуст, нельзя удалить элемент
            print("Error: memory is empty, cannot remove element")
        else:
            stack_pointer -= 1  # Уменьшаем указатель стека
            removed_element = memory[stack_pointer]  # Считываем удаленный элемент
            print(f"Element deleted: {removed_element}")
            memory[stack_pointer] = 0  # Очищаем значение в памяти


    # ЭТА КОМАНДА ВООБЩЕ НЕ НУЖНА

    # # Суммирование всех элементов в памяти (в пределах стека). Если стек пуст, выдаётся предупреждение.
    # elif mnemonic == "SUM":
    #     if stack_pointer == 0:
    #         print("\nError: memory is empty, cannot execute 'SUM'")
    #     else:
    #         while stack_pointer > 1:
    #             b = memory[stack_pointer - 1]  # Снимаем верхний элемент
    #             a = memory[stack_pointer - 2]  # Снимаем предпоследний элемент
    #             result = a + b  # Складываем два верхних элемента
    #             memory[stack_pointer - 2] = result  # Помещаем результат на место предпоследнего элемента
    #             stack_pointer -= 1  # Уменьшаем указатель стека на 1
    #         # Теперь в memory[0] хранится сумма всех элементов, остальные обнулены
    #         print(f"\nSUM OF ELEMENTS: {memory[0]}")


    # Команда для очистки памяти (стека). А-ля было у нас [100, 200, 10], а потом всё стало [].
    elif mnemonic == "CLEAR":
        for i in range(stack_pointer):
            memory[i] = 0  # Очищаем все элементы в пределах стека
        stack_pointer = 0  # Сбрасываем указатель стека на 0
        print("MEMORY IS CLEARED.")

    # Команда для завершения работы программы
    elif mnemonic == "EXIT":
        print("\nEnd of program.")
        return "exit"

    # Если команда не поддерживается
    else:
        print(f"Инструкция '{mnemonic}' не поддерживается")


# Это основной цикл, в котором вводятся команды (ну тут как бы единственная переменная - command, логично же)
while True:
    # Получаем команду от пользователя
    command = input("\nCOMMAND LIST:\n\nPUSH <value_number_int>\nADD\nDELETE\n"
                    "SUM\nCLEAR\n"
                    "EXIT\n\nCommand for use: ")

    # Выполняем команду
    if execute_instruction(command) == "exit":
        break

    # Выводим текущее состояние памяти (зону, которая используется как стек) после каждой команды
    print(f"\nCurrent memory state (stack area): {memory[:stack_pointer]}")
    print(f"RAM usage: {stack_pointer} out of 512")

