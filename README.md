<h1> Прикладне програмування </h1>

<h2> Лабораторна робота 4 </h2>
<h3>Виконав Павлик Богдан</h3>

<h3>1. Клонування репозиторі </h3>
    Для початку потрібно втсановити Git, якщо він у вас не встановлений:
    <br> 1. Для Windows - <i>http://git-scm.com/download/win</i>
    <br> 2. Для Linux - <i>http://git-scm.com/download/linux</i>
    <br> 3. Для Mac - <i>http://git-scm.com/download/mac</i>
    <br><br> •Спочатку необхідно створити папку, куди ми будемо клонувати репозиторі
    <br> •Далі, нажимаємо правою кнопкою миші на папку та вибираємо опцію Git Bash here
    <br> •Далі необхідно ввести таку команду: <code>git clone https://github.com/BodiaPavlyk/Labs_PP.git</code>
<h3>2. Інсталяція python та віртуального середовища </h3>
(For Windows)
<br><br><b>1. Інсталюєм pyenv для встановлення python</b>
<br> •Для цього необхідно відкрити командний рядок та ввести наступну команду:
<br><code>pip install pyenv-win --target %USERPROFILE%\.pyenv</code>
<br> •Далі, відкриваємо програму PowerShell, де вводимо команди:
<br><code>[System.Environment]::SetEnvironmentVariable('PYENV',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")</code>
<br><code>[System.Environment]::SetEnvironmentVariable('path', $HOME + "\.pyenv\pyenv-win\bin;" + $HOME + "\.pyenv\pyenv-win\shims;" + $env:Path,"User")</code>
<br> Для перевірки, вводимо у командному рядку команду <code>pyenv --version</code>, яка повинна показати версію встановленого pyenv
<br> Детальніше на сайті <i>https://pypi.org/project/pyenv-win/</i>
<br><br><b>2. Встановлення python та віртуального середовища pipenv</b>
<br> •Для встановлення python вводимо наступну команду в терміналі:
<br><code>pyenv install 3.7.9</code>
<br> •Для встановлення pipenv:
<br><code>pip install pipenv</code>
<h3>3. Запуск у PyCharm</h3>
Для запуску проекту, необхідно:
<br> 1.Відкрити <b>PyCharm</b> та відкрити папку проекту
<br> 2.Підключити бібліотек gevent у терміналі за допомогою команди pipenv install gevent
<br> 3.Скомпілювати код
<br> 4.Після запуску перейшовши за адресою <i>http://localhost:5000/api/v1/hello-world-20</i>, ви побачити текст "Hello world! Варіант 20"

<h2>Дабораторна робота 5</h2>
<h3>Проектування Rest Api y Swagger Editor</h3>
(Виконав Павлик Богдан)

<h2>Дабораторна робота 6</h2>
