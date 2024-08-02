import os
import signal
import subprocess
import time

pid_file = "./script.pid"


def get_pid():
    try:
        with open(pid_file, 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return None
    except Exception:
        return None


def save_pid(pid):
    print("Я пытаюсь сохранить пид")
    with open(pid_file, 'w') as f:
        f.write(str(pid))


def kill_script():
    pid = get_pid()
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            time.sleep(10)  # Даем время процессу завершиться
            print("Процесс уничтожен")
        except ProcessLookupError:
            print(f"Процесс с PID {pid} не найден.")
    else:
        print("PID файл не найден или пуст.")


def restart():
    while True:
        try:
            kill_script()

            # Запускаем скрипт снова с использованием Python из виртуального окружения
            process = subprocess.Popen(["python", "main.py"])
            save_pid(process.pid)
            print("Я сохрнанил пид")
            #stdout, stderr = process.communicate()
            #print(f"Script output: {stdout.decode()}")
            #print(f"Script errors: {stderr.decode()}")

        except FileNotFoundError as e:
            print(f"FileNotFoundError: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(900)


if __name__ == "__main__":
    restart()
