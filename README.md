## Решение задачи от РБК "Предсказание тенденций в новостных статьях"

### Настройка окружения с помощью miniconda:

```
conda create -n rbc_env python=3.8.12
conda activate rbc_env
pip install -r requirements.txt

или
( pip install ipykernel ipywidgets pyarrow catboost pymorphy2 beautifulsoup4 requests
pip install -U scikit-learn
pip install --user -U nltk )

jupyter nbextension enable --py widgetsnbextension
```


### Воспроизведение решения:
  1. Создать папку data рядом с ноутбуками и файлами, в нее поместить train и test датасеты. В данном репозитории в папке data находятся промежуточные файлы. Их можно тоже скопировать по необходимости. Все промежуточные файлы с файлами моделей находятся на [яндекс диске](https://disk.yandex.ru/d/N3mbIrYna4091w)
  2. [1_parse.ipynb](1_parse.ipynb) - Запустить парсинг страниц или же взять готовый файл [data/pages_info.p](data/pages_info.p) 
  3. [2_prepro.ipynb](2_prepro.ipynb) - Предобработка и объединение данных
  4. [3_train_predict.ipynb](3_train_predict.ipynb) - Тренировка моделей и получение предсказаний.

### Результат:

```
5 место
```


### License
[MIT license](LICENSE).

