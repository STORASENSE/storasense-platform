FROM gradle:9.0-jdk21-alpine AS build
WORKDIR /app
COPY Alarm-Service/app/build.gradle Alarm-Service/settings.gradle ./
COPY Alarm-Service/app/src ./src
COPY Alarm-Service/config ./config
RUN gradle clean build -x test

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=build /app/build/libs/alarm-*.jar /app/app.jar
COPY Alarm-Service/config /app/config
ENV JAVA_OPTS=""
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app/app.jar"]
