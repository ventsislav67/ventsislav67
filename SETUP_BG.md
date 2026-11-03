# GitHub Profile Neon Edition — Инсталиране

Профил: https://github.com/ventsislav67
Хранилище на профила: https://github.com/ventsislav67/ventsislav67

## Какво се променя

- `README.md` — изцяло ново оформление (съществуващият се заменя).
- `assets/neon-banner.gif` — собствен анимиран банер; не зависи от външен сървър.
- `assets/tech-pulse.gif` — собствена анимация на технологичен панел.
- `assets/github-stats.svg`, `assets/top-languages.svg` — първоначални placeholder карти, които GitHub Actions автоматично заменя с реалните статистики.
- `assets/github-snake-dark.svg`, `assets/github-snake-light.svg` — първоначална графика; GitHub Actions я заменя с анимирана змия по реалната активност.
- `.github/workflows/profile-visuals.yml` — автоматично обновяване веднъж дневно и ръчно стартиране.

## Инсталиране (Windows)

1. Разархивирай ZIP файла. Трябва да виждаш папките `assets`, `.github` и файла `README.md`.
2. Увери се, че Git е инсталиран и че имаш достъп до GitHub през Git Credential Manager / GitHub Desktop.
3. В PowerShell от разархивираната папка изпълни: `powershell -ExecutionPolicy Bypass -File .\publish.ps1`
4. Скриптът клонира хранилището в **нова локална папка**, копира новите профилни файлове и показва кои файлове ще се променят.
5. Когато скриптът поиска потвърждение, напиши `yes`, за да публикува. Не ползва `--force` и не трие другите проекти.
6. Отвори https://github.com/ventsislav67/ventsislav67/actions и избери **Refresh profile stats and animated contributions** > **Run workflow**. При първото стартиране изчакай резултатът да е със зелена отметка. Змията и статистиките се генерират при първия успешен run.

## Ако GitHub Actions не може да commit-не

Отвори **Repository > Settings > Actions > General** и провери **Workflow permissions**. Workflow-ът изрично изисква `contents: write`. Ако политиката на хранилището е по-ограничаваща, настройката може да попречи на автоматичното публикуване.

## Ако анимацията не тръгва

- Провери Actions > съответния run > стъпката `Animate GitHub contributions`.
- Ако има `resource not accessible by integration`, провери правата на GitHub Actions.
- Ако има `API rate limit`, опитай ръчно по-късно; не е необходимо да слагаш личен GitHub токен в README.
- Ако README не показва новата версия, презареди с Ctrl+F5. Изображенията понякога се кешират.
- Анимираното змийче се вижда в README като SVG изображение. При някои среди/настройки с намалено движение може да се визуализира като статично.

## Важно

GitHub README не изпълнява JavaScript, затова интерактивни мини приложения не могат да работят директно в него. Тук анимациите са GIF/SVG файлове, а данните се подновяват през GitHub Actions.

Не променяй автоматично генерираните `github-*.svg` файлове ръчно — следващият run ще ги презапише. Не слагай GitHub token/password в README или в скрипт.
