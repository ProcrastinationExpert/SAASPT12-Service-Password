FROM php:8.4-cli

# Install library sistem yang dibutuhkan dan ekstensi pdo_mysql untuk koneksi ke database
RUN apt-get update && apt-get install -y \
    unzip \
    libzip-dev \
    && docker-php-ext-install pdo_mysql zip

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /app

COPY . .

COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh

RUN chmod +x /usr/local/bin/wait-for-it.sh

RUN composer install --no-interaction --prefer-dist --optimize-autoloader

EXPOSE 8000

CMD ["/usr/local/bin/wait-for-it.sh", "mysql-db:3306", "-t", "60", "--", "sh", "-c", "php artisan migrate && php artisan serve --host=0.0.0.0 --port=8000"]