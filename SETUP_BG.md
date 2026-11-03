# GitHub Profile — Neon Developer Edition

Профил: https://github.com/ventsislav67

## Състояние

Новият профил вече е инсталиран директно в хранилището. Не е необходимо да изтегляш ZIP, да изпълняваш PowerShell команди или да качваш файлове ръчно.

- README.md — главната страница с банер, анимации, проекти и сертификат.
- neon-banner.gif и tech-pulse.gif — локални анимирани изображения.
- developer-stats.svg — анимирана карта с реални статистики.
- developer-languages.svg — анимирана карта с езиците в хранилищата.
- contribution-signal.svg — реална седмична графика на GitHub активността.
- github-snake-dark.svg и github-snake-light.svg — анимирана змия по contribution календара.
- scripts/render_dashboard.py — създава визуализациите.
- .github/workflows/profile-visuals.yml — автоматично обновява данните приблизително на всеки 6 часа.

## Как да обновиш статистиките ръчно

1. Отвори https://github.com/ventsislav67/ventsislav67/actions/workflows/profile-visuals.yml
2. Избери Run workflow и стартирай върху main.
3. Провери, че има зелена отметка.
4. Отвори https://github.com/ventsislav67 и обнови страницата с Ctrl+F5.

## Важно за "real time"

README страниците на GitHub не изпълняват JavaScript. Анимациите се възпроизвеждат в GIF и SVG, а числата се генерират през GitHub Actions на всеки 6 часа. Кеширането на изображенията може да забави появата на новата версия.

## Ако нещо не се вижда

Провери Actions за последното изпълнение. Първо потърси дали workflow е успешен и дали файловете developer-stats.svg, developer-languages.svg и contribution-signal.svg са създадени. Не използвай старите инструкции за качване в assets — изображенията са в основната папка.
