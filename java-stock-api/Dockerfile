# syntax=docker/dockerfile:1

# ---- Build stage ----
FROM gradle:8-jdk17 AS build
WORKDIR /workspace

# Copy build files first for caching
COPY build.gradle settings.gradle ./
RUN gradle --version

# Copy source and build
COPY src ./src
RUN gradle --no-daemon clean bootJar

# ---- Runtime stage ----
FROM eclipse-temurin:17-jre
WORKDIR /app

# Copy the fat jar from the build stage
COPY --from=build /workspace/build/libs/*.jar app.jar

EXPOSE 8080

ENV JAVA_OPTS=""

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
