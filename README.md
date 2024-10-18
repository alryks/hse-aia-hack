# Baseline of AI Assistant Hack: Python

По вопросам/багам писать в tg: [@werserk](https://t.me/werserk)

## Ссылки

Репозиторий: https://github.com/werserk/hse-aiahp-baseline \
Тестирующая система: https://dsworks.ru/champ/hse-2024-october \
Лендинг: https://www.hse.ru/ai-assistant-hack-python/

## Описание

### YandexGPT
В бейзлайне использована модель YandexGPT. 
Если вы хотите использовать её, то вам потребуется получить [микро-грант](https://yandex.cloud/ru/docs/billing/concepts/bonus-account), чтобы не тратить свои кровные на её инференс (там просто нужно создать новый акк и сделать его "платёжным").

**Совет:** сначала тестируйте свои гипотезы на небольшом сабсете данных (например, 15-20% от всех тестовых данных),
а уже после выбора наилучшего варианта генерируйте полный сабмит. 
Так сможете потратить квоту более эффективно.

Как получить IAM Token и Folder ID можно посмотреть в [документации](https://yandex.cloud/en-ru/docs/foundation-models/quickstart/yandexgpt#api_2) Yandex Cloud.

### GigaChat
Так же у Сберовского GigaChat API есть пробный тариф - Freemium. Он тоже даст вам достаточно ресурсов.

### Локальный модели
Ну и, конечно, пробуйте запускать модели локально с [HuggingFace](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending) или других мест.

Вы можете ознакомиться с топовыми LLM моделями здесь - [LMSYS Chatbot Arena](https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard).

В ветке "new_models" вы можете увидеть пару моделей, которые мы попробовали, но не стали включать в финальный бейзлайн. Возможно они натолкнут вас на умные мысли.

### Другие подходы
Пусть мы и сделали акцент на LLM аналогичные ChatGPT, это не значит, что вы не можете использовать другие LLM модели.

Будет круто, если вам пригодятся данные "train" не только для анализа.

## Запуск

### В контейнере (пока-что не получается)

```bash
docker compose up
```

### В локальной среде

`Poetry` является более продвинутым пакетным менеджером, чем `pip`. На с большей вероятность не возникнет ситуации, что нужные пакеты установятся неправильно.

- Если запускаете на `CUDA`, то:
  1. Проверить, установлен ли CUDA Toolkit: `nvcc -V`
  2. В `pyproject.toml` изменить следующую строку:

  ```
  url = "https://download.pytorch.org/whl/cu124"
  ```

  На соответствующую версию `CUDA`.

  3. Прописать переменныю среды:
     - Windows Powershell:
     ```
     $env:CMAKE_GENERATOR = "MinGW Makefiles"
     $env:CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_C_COMPILER=C:/msys64/mingw64/bin/gcc.exe -DCMAKE_CXX_COMPILER=C:/msys64/mingw64/bin/g++.exe"
     ```
     - Windows Command Prompt: 
     ```
     set CMAKE_GENERATOR = "MinGW Makefiles"
     set CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_C_COMPILER=C:/msys64/mingw64/bin/gcc.exe -DCMAKE_CXX_COMPILER=C:/msys64/mingw64/bin/g++.exe"
     ```
     Установив пути до компиляторов `gcc` и `g++` на Windows.
     - Linux: `CMAKE_ARGS="-DGGML_CUDA=on"`
  4. *Для Windows:*
     1. Установить `Microsoft Visual Studio Developer Tools`
     2. Добавить директорию, где располагается `cl.exe` в `Path`, например, такую:

    ```
    C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.28.29910\bin\Hostx64\x64
    ```

- Если запускаете на `Apple Metal`, то:
  1. Убрать:

  ```
  [[tool.poetry.source]]
  name = "torch"
  url = "https://download.pytorch.org/whl/cu124"
  secondary = true
  ```

  2. Изменить `torch = { version = "2.5.0", source="torch"}` на `torch = "2.5.0"`
  3. Прописать переменную среды: `CMAKE_ARGS="-DGGML_METAL=on"`

Устанавливаем зависимости:
```bash
poetry lock
poetry install
```

Запускаем:
```
poetry run python main.py
```

### Переменные окружения

Создали для вас .env.example файл в корне проекта. \
Чтобы создать .env файл, запускаем следующую команду:

```bash
cp .env.example .env
```

## Структура проекта

```
.
├── app
│   ├── __init__.py
│   ├── models   <------------------------ подключаемые модели
│   │   ├── base.py
│   │   ├── __init__.py
│   │   └── yandexgpt.py
│   └── utils    <------------------------ утилиты
│       ├── __init__.py
│       ├── metric.py <------------------------ ознакомьтесь с метрикой
│       └── submit.py <------------------------ здесь всё для генерации сабмита
├── data
│   ├── complete <------------------------ подготовленные данные, сабмиты
│   ├── processed <----------------------- промежуточный этап подготовки данных
│   └── raw <----------------------------- исходные данные
│       ├── submit_example.csv
│       ├── test
│       │   ├── solutions.xlsx
│       │   ├── tasks.xlsx
│       │   └── tests.xlsx
│       └── train
│           ├── solutions.xlsx
│           ├── tasks.xlsx
│           └── tests.xlsx
├── main.py <---------------------------- [ВАЖНО] Именно этот скрипт мы будем запускать при проверке ваших решений. Он должен генерировать финальный сабмит.
├── notebooks
│   └── yandexgpt.ipynb
├── poetry.lock
├── pyproject.toml
├── README.md
└── tests
    ├── test_correctness.py <------------------------ проверить на корректность сабмит
    └── test_embedding_generation.py <--------------- попробовать генерацию эмбеддингов и подсчёт метрики


```