# Automatic Cover Letter Generator

## About
This projects is an application that automatically generates cover letters based on a user's uploaded CV and a job offer URL. It is powered by GPT (`text-davinci-003` and `gpt-3.5-turbo`).

## Installation
1. Clone this repository: git clone https://github.com/ceptn/cover-letter-generator.git
2. Create a virtual environment (recommanded)
3. Install the required packages using `pip install -r requirements.txt`

Then, you need to make sure that the file openai_api_key.txt is included in your project directory and that it contains your OpenAI API key. This key should be kept private and not shared publicly.

## Usage
1. Navigate to the project directory: cd your-repo
2. To use the application, simply `streamlit run app.py` and navigate to localhost:8501 in your web browser. 
3. The application will ask you to upload your CV and enter the URL of the job offer.

The application will then automatically generate a cover letter for you in a well-formatted Word document.

## Files
- app.py: the main file containing the Flask application.
- main.py: a module containing the main functions of the application.
- utils.py: a module containing utility functions used by main.py.
- prompts/: a folder containing text prompts used by the application.
- requirements.txt: a file containing the required packages to run the application.

## How it Works
The application works as follows:

- The uploaded PDF CV is checked to ensure it is a proper CV.
- The URL is checked to ensure it refers to a job offer.
- The CV is parsed to extract specific content.
- The job description is parsed to extract specific content.
- The different cover letter blocks are created.
- The cover letter is output in a well-formatted Word document.

## Warning
Note that the app is not perfect and may not work for all CV and job offer formats. Additionally, the app is not a substitute for human judgment, and it is important to thoroughly review all documents before submitting them for job applications.

## Contributing
If you would like to contribute to the project, feel free to submit a pull request or to fork the project. Feel free to provide any feedback.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.