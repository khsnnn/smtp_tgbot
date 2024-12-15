
1. **Клонируйте репозиторий**
2. **Создайте виртуальное окружение и активируйте его:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate     # Для Windows
   ```
3. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Настройте переменные окружения:**

   Создайте файл `.env` в корне проекта (пример в .env.example)

## Запуск приложения

* Запустите бота:
  ```
  python3 main.py
  ```
* Откройте своего бота в Telegram и начните взаимодействие с командой `/start`.
