# 💰 Personal Expense & Asset Manager (CLI)

> **"Stop just tracking expenses. Start tracking your Net Worth."**

A robust, Python-based Command Line Interface (CLI) tool designed to manage personal finances. Unlike standard expense trackers, this tool focuses on **Real Net Worth Calculation** by tracking not just Income and Expenses, but also **Assets (Money Lended)** and **Liabilities (Money Borrowed)**.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Active-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge)

## ⚡️ Why I Built This?

As a college student, tracking daily coffee expenses is easy, but tracking **"Who owes me money?"** and **"Who do I owe?"** is messy. Most apps don't handle casual lending/borrowing effectively.

I built this tool to solve that specific problem using **Persistent Data Storage**. It calculates your financial health by combining your liquid cash with your debts and credits.

## 📸 Demo

*(Add your terminal screenshot here)*
![Expense Manager Screenshot](Link_to_your_screenshot_image_a86529.png)

## 🚀 Key Features

* **📊 Complete Cashflow Tracking:** Log Income and Expenses with precise timestamps.
* **🤝 Lending & Borrowing Engine:**
    * Track money lent to friends (Assets).
    * Track money borrowed (Liabilities).
    * **Partial Repayment Logic:** Updates balances automatically when someone pays you back partially.
* **💾 Data Persistence:** Uses `json` module to save data locally. Your records remain safe even after closing the program.
* **💎 Real Net Worth Calculator:**
    * `Net Worth = Wallet Balance + Assets (Lended) - Liabilities (Borrowed)`
* **📈 Excel Export:** One-click export to `.csv` for detailed analysis in Excel/Google Sheets.

## 🛠️ Technical Concepts Implemented

This project demonstrates core Computer Science principles:
* **Object-Oriented Programming (OOP):** Encapsulated logic within the `ExpenseManager` class.
* **File Handling (I/O):** Reads/Writes to `expense_data.json` and `expense_report.csv`.
* **Data Structures:** Uses Dictionaries and Lists for efficient state management.
* **Error Handling:** Robust `try-except` blocks to prevent crashes on invalid inputs.

## 💻 How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/expense-manager.git](https://github.com/your-username/expense-manager.git)
    ```
2.  **Navigate to the directory:**
    ```bash
    cd expense-manager
    ```
3.  **Run the script:**
    ```bash
    python manager.py
    ```

## 📂 Project Structure

```text
├── manager.py           # Main source code (Logic + UI)
├── expense_data.json    # Database file (Auto-generated on first run)
├── expense_report.csv   # Exported report (Auto-generated)
└── README.md            # Documentation
