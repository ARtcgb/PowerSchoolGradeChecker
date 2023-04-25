# PowerSchool Grade Checker

PowerSchool Grade Checker is a Python-based tool that allows users to monitor the grade updates of their courses. The
application automates the process of checking course pages for updates and logs any changes in course grades and update
times.

## Features

- Automatically log in to the course website.
- Retrieve course URLs with specified targets.
- Extract and store course grades and update times.
- Compare new data with the previously stored data.
- Log any updates and changes in course grades.

## Installation

1. Ensure you have Python 3.7 or higher installed on your machine. You can download it
   from [python.org](https://www.python.org/downloads/).

2. Clone this repository or download it as a ZIP file.

    ```
    git clone https://github.com/ARtcgb/PowerSchoolGradeChecker.git
    ```

3. Navigate to the project directory.

    ```
    cd PowerSchoolGradeChecker
    ```

4. Create a virtual environment (optional but recommended).

    ```
    python -m venv venv
    ```

5. Activate the virtual environment.

   For Windows:

    ```
    venv\Scripts\activate
    ```

   For macOS and Linux:

    ```
    source venv/bin/activate
    ```

6. Install the required dependencies using the `requirements.txt` file.

    ```
    pip install -r requirements.txt
    ```

## Usage

1. Update the `config/config.properties` file with your login credentials, course website URL, and target selection.

2. Run the `main.py` script to start the PowerSchool Grade Checker

    ```
    python main.py
    ```

3. The PowerSchool Grade Checker will log in to the course website, retrieve the course URLs, and extract the course
   grades and update times. Any updates or grade changes will be logged.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
