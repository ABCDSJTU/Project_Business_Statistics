import Problem_1
import Problem_2
import Problem_3
import Problem_4

def main():
    while True:
        user_input = input("请输入要执行的操作（例如：'run_problem1'），或输入'exit'退出程序：")

        if user_input == 'run_problem1':
            Problem_1.solve_problem()
        elif user_input == 'run_problem2':
            Problem_2.solve_problem()
        elif user_input == 'run_problem3':
            Problem_3.solve_problem()
        elif user_input == 'run_problem4':
            Problem_4.solve_problem()
        elif user_input == 'exit':
            print("程序已退出。")
            break
        else:
            print("没有匹配的操作，请重新输入。")
        print()

if __name__ == "__main__":
    main()
