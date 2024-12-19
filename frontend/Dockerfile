# Используем Nginx для хостинга статичных файлов
FROM nginx:alpine

# Копируем HTML-файлы в директорию, где Nginx ищет файлы
COPY index.html /usr/share/nginx/html/index.html

# Открываем стандартный порт Nginx
EXPOSE 80