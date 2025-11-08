# Stock Service (Spring Boot)

Mock Java API service exposing a stock price endpoint for a Python agent.

## Requirements
- Java 17+
- Gradle 8+ (or use the Gradle Wrapper)

## Build and Run (Gradle)

Dev run:
```powershell
./gradlew bootRun
# Windows PowerShell
./gradlew.bat bootRun
```

Build jar and run:
```powershell
./gradlew clean bootJar
java -jar build/libs/stock-service-0.0.1-SNAPSHOT.jar
```

The service starts on http://localhost:8080

## API
- GET `/api/v1/stock/{symbol}`

Examples:
```powershell
# Success
curl http://localhost:8080/api/v1/stock/GOOG

 # Other available mock symbols
 curl http://localhost:8080/api/v1/stock/MSFT
 curl http://localhost:8080/api/v1/stock/APPL

# Not found
curl http://localhost:8080/api/v1/stock/TSLA
```

Sample success response:
```json
{
  "symbol": "GOOG",
  "current_price": 175.5,
  "status": "SUCCESS"
}
