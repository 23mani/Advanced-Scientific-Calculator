# 🧮 Advanced Scientific Calculator

A feature-rich desktop calculator built using **Python**, **Tkinter**, **SQLite**, and **Object-Oriented Programming (OOP)** principles. This project combines scientific calculations, database integration, file handling, and modern GUI design into a single application.

## 🚀 Features

### Basic Operations

* Addition, Subtraction, Multiplication, Division
* Percentage Calculations
* Decimal Support

### Scientific Functions

* Trigonometric Functions (`sin`, `cos`, `tan`)
* Logarithmic Functions (`log`, `ln`)
* Square Root (`√`)
* Power Operations (`x²`, `xʸ`)
* Factorial (`n!`)
* Mathematical Constants (`π`, `e`)

### Additional Features

* Memory Functions (M+, M−, MR, MC)
* Calculation History Management
* SQLite Database Integration
* Export History to CSV
* Dark Mode / Light Mode Toggle
* Error Handling for Invalid Inputs

---

## 🛠️ Technologies Used

* **Python**
* **Tkinter**
* **SQLite3**
* **CSV Module**
* **Math Module**
* **Object-Oriented Programming (OOP)**

---

## 📂 Project Structure

```text
AdvancedScientificCalculator/
│
├── main.py
├── calculator.py
├── database.py
├── themes.py
├── export.py
├── history.db
└── README.md
```

---

## ⚙️ Installation & Execution

### Clone the Repository

```bash
git clone https://github.com/your-username/AdvancedScientificCalculator.git
cd AdvancedScientificCalculator
```

### Run the Application

```bash
python main.py
```

The SQLite database file (`history.db`) will be created automatically on first execution.

---

## 🗄️ Database Schema

```sql
CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expression TEXT NOT NULL,
    result TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🧩 OOP Design

The project follows the **Single Responsibility Principle (SRP)** by dividing functionality into separate classes:

* **Calculator** → GUI, calculations, event handling
* **DatabaseManager** → SQLite operations
* **ThemeManager** → Theme switching
* **ExportManager** → CSV export functionality

---

## 📸 Screenshots
### Main Calculator Window
<img width="422" height="728" alt="image" src="https://github.com/user-attachments/assets/93db1d0f-8ce0-4750-b117-506d524028c2" />

<img width="426" height="732" alt="image" src="https://github.com/user-attachments/assets/2312b30e-fa70-4fec-bc54-0aabd3aaa798" />

### History Window
<img width="442" height="523" alt="image" src="https://github.com/user-attachments/assets/48c7d662-6e84-499c-b77d-b07e4a1b7acd" />

### Export as CSV File
<img width="732" height="480" alt="image" src="https://github.com/user-attachments/assets/25566448-10c7-4883-b04e-d1ee45ed0a9b" />


---

## 🧪 Sample Test Cases

| Expression | Output |
| ---------- | ------ |
| 10 + 20    | 30     |
| 5 × 5      | 25     |
| √25        | 5      |
| 2³         | 8      |
| sin(30)    | 0.5    |
| log(100)   | 2      |
| 5!         | 120    |

---

## 📚 Concepts Demonstrated

* Object-Oriented Programming
* GUI Development with Tkinter
* SQLite Database Management
* File Handling and CSV Export
* Exception Handling




