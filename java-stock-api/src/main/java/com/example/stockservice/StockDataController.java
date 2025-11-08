package com.example.stockservice;

import java.util.HashMap;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.ResponseEntity;

/**
 * MOCK JAVA API SERVICE: StockDataController
 *
 * This file represents the backend service, built using a framework like Spring Boot,
 * that the Python agent will call.
 *
 * It simulates fetching the current price for a stock symbol.
 */
@RestController
public class StockDataController {

    // Mock data storage for demonstration purposes
    private final Map<String, Double> mockPrices = new HashMap<>();

    public StockDataController() {
        // Initialize mock prices
        mockPrices.put("GOOG", 175.50);
        mockPrices.put("MSFT", 432.10);
        mockPrices.put("APPL", 192.75);
    }

    /**
     * API Endpoint: GET /api/v1/stock/{symbol}
     *
     * Retrieves the current price for the given stock symbol.
     * @param symbol The stock ticker symbol (e.g., "GOOG").
     * @return A JSON response containing the current price.
     */
    @GetMapping("/api/v1/stock/{symbol}")
    public ResponseEntity<Map<String, Object>> getCurrentPrice(@PathVariable String symbol) {
        String upperSymbol = symbol.toUpperCase();
        Map<String, Object> response = new HashMap<>();

        if (mockPrices.containsKey(upperSymbol)) {
            double price = mockPrices.get(upperSymbol);
            response.put("symbol", upperSymbol);
            response.put("current_price", price);
            response.put("status", "SUCCESS");
            // Simulate a short delay (for real API latency)
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                // Do nothing
            }
            return ResponseEntity.ok(response);
        } else {
            response.put("symbol", upperSymbol);
            response.put("status", "NOT_FOUND");
            response.put("message", "Symbol not found in mock database.");
            return ResponseEntity.status(404).body(response);
        }
    }
}
