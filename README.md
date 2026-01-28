# Amazon UI Automation Test – LambdaTest Assignment

## Overview
This project is a **UI automation framework** built using **Python, PyTest, and Selenium WebDriver** to automate an end-to-end flow on **Amazon India**.

The framework demonstrates real-world automation practices such as:
- Page Object Model (POM)
- Data-driven testing using PyTest
- Explicit waits for stability
- Browser window/tab handling
- Structured logging

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Programming language |
| PyTest | Test execution & parametrization |
| Selenium WebDriver | Browser automation |
| Page Object Model | Maintainable framework design |
| Logging | Execution traceability |
| Virtual Environment | Dependency isolation |

---

## Project Structure




---

## Test Scenario Covered

### Amazon Product Purchase Flow
1. **Launch Amazon India website**
2. **Search for a device (data-driven)**
3. **Select a specific product model**
4. **Handle newly opened browser tab**
5. **Add product to cart**
6. **Capture and log product price**
7. **Close browser**

---

## Data-Driven Testing

Tests are executed using PyTest `@parametrize`.

### Sample Test Data Format
```python
[
    ("AMAZONTC001", "Y", "positive", "Search and add iPhone to cart", "iPhone", "iPhone 14"),
    ("AMAZONTC002", "Y", "positive", "Search and add Galaxy to cart", "Samsung", "Galaxy S23")
]
```

## How to Run Tests
1. Activate the venv
2. pip install -r requirements.txt
3. pytest -v test_cases/test_amazon_test_cases.py

# Check the logs in termianl for monitoring the tests
