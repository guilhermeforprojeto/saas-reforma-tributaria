# Calculadora de Tributos da Receita Federal (regime regular) em container.
# Compila o código oficial e publica a API em http://localhost:8080/api
#   docker compose -f docker/docker-compose.yml up -d --build
# Fixe a versão com RTC_REF (tag, branch ou commit do repositório oficial).

FROM eclipse-temurin:25-jdk AS build
ARG RTC_REF=main
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 --branch "${RTC_REF}" https://github.com/ReceitaFederal/calculadora-rtc-regime-regular.git . \
 || (git clone https://github.com/ReceitaFederal/calculadora-rtc-regime-regular.git . && git checkout "${RTC_REF}")
# Gera o banco SQLite com as tabelas oficiais (obrigatório) e compila sem rodar os testes
RUN mkdir -p calculadora/db \
 && ./mvnw -B -q flyway:migrate -Dflyway.configFiles=./flyway/flyway-pro.conf \
 && ./mvnw -B -q -DskipTests clean package \
 && git rev-parse --short HEAD > /src/VERSAO_OFICIAL

FROM eclipse-temurin:25-jre
WORKDIR /app
COPY --from=build /src/target/api-regime-geral.jar app.jar
COPY --from=build /src/calculadora/db calculadora/db
COPY --from=build /src/VERSAO_OFICIAL VERSAO_OFICIAL
RUN useradd --system --uid 10001 calc && chown -R calc /app
USER calc
EXPOSE 8080
ENTRYPOINT ["java", "-Dspring.profiles.active=offline", "-jar", "app.jar"]
