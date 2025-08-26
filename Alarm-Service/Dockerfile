FROM gradle:9.0-jdk21-alpine AS build
WORKDIR /alarmservice
COPY ./Alarm-Service/build.gradle ./Alarm-Service/settings.gradle ./
COPY ./Alarm-Service/src ./src
RUN gradle clean build -x test

FROM eclipse-temurin:21-jre-alpine
WORKDIR /alarmservice
COPY --from=build ./alarmservice/build/libs/Alarm-Service-SNAPSHOT-all.jar alarmservice.jar
ENTRYPOINT ["sh", "-c", "java -jar alarmservice.jar"]
