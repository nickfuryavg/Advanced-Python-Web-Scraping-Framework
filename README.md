
# Project Title: Advanced Python Web Scraping Framework

# Description:

This repository houses a sophisticated Python-based web scraping solution designed for handling large-scale data extraction tasks from websites. Utilizing multithreading, the script efficiently crawls web pages using libraries such as requests, BeautifulSoup, Scrapy, and Pandas. Data is stored in an SQLite database, ensuring data integrity and facilitating resumable crawling through checkpoint mechanisms. The solution automates extraction, handling interruptions gracefully, and generates detailed reports from clean datasets. Scheduled execution is supported via cronjobs for seamless, automated scraping operations.

# Key Features:

1. Multithreaded architecture for concurrent scraping.

2. Integration of requests, BeautifulSoup, Scrapy, and Pandas for data extraction.

3. SQLite database for persistent storage and data integrity.

4. Checkpoints for resumable crawling and handling interruptions.

5. Automated extraction and report generation using cronjobs.

# Installation

#To run this project, follow these steps:

# Step-1:

`cd /Users/sandipanray/Soket_Labs`

1. By using `cd /Users/sandipanray/Soket_Labs`, we are     navigating to the Soket_Labs directory. This allows us to work within that specific project directory, where we can perform tasks like setting up a virtual environment, running scripts, or managing project files.

# Step 2: Create and activate a virtual environment (if not  already done):

`python3 -m venv venv`

`source venv/bin/activate`

1. The `python3 -m venv venv` command creates a virtual environment named venv in the  project directory.

2. `source venv/bin/activate` activates the virtual environment. We should see (venv) indicating that it's active.

# Step 3: Install dependencies:

`pip install -r requirements.txt`

1. Installs Python dependencies listed in requirements.txt into our activated virtual environment (venv).

# Step 4:  Set environment variables (optional):

`echo $VISUAL`

`echo $EDITOR`

1. `echo $VISUAL`: the terminal will display the value stored in the VISUAL environment variable, which is usually set to the name of a text editor like nano, vim, or emacs.

2. `echo $EDITOR`: Another environment variable that also stores the name of a default text editor for terminal-based applications.

`export VISUAL=nano`

`export EDITOR=nano`

3. Sets environment variables VISUAL and EDITOR to use the Nano text editor (optional, adjust to  preferred editor).


# Step 5:  Running the Script Using Cron
"To schedule and run the script using cron:

1. Edit the crontab file:

`crontab -e`

Opens the crontab file for editing. This file manages scheduled tasks (cron jobs) on the system.

2. Add the following lines to the crontab file (replace paths and script names as necessary):

# Example cron job to run the script daily at 10:56 AM and kill it at 11:00 AM

`56 10 * * * source /Users/sandipanray/Soket_Labs/venv/bin/activate && python3 /Users/sandipanray/Soket_Labs/Modular_Advance_scrapping.py >> /Users/sandipanray/Soket_Labs/log1.log 2>&1`

`56 10 * * *`: Specifies the schedule for running the command at 10:56 AM daily.

`source /Users/sandipanray/Soket_Labs/venv/bin/activate && python3 /Users/sandipanray/Soket_Labs/Modular_Advance_scrapping.py` : Activates the virtual environment (venv) and executes the Python script (Modular_Advance_scrapping.py).

>> /Users/sandipanray/Soket_Labs/log1.log 2>&1: Redirects both standard output and standard error to log1.log for logging purposes.

`00 11 * * * pkill -f  /Users/sandipanray/Soket_Labs/Modular_Advance_scrapping.py > /path/to/your/project/log1.log 2>&1`

`00 11 * * *`: Specifies the schedule for stopping the command at 11:00 AM daily.

` /Users/sandipanray/Soket_Labs/Modular_Advance_scrapping.py`: Searches for and kills any running instance of the script specified (Modular_Advance_scrapping.py).

>> /path/to/your/project/log1.log 2>&1: Redirects both standard output and standard error to log1.log for logging purposes.

save the cronjob and exit 

# Step 6: Managing Permissions and Monitoring Processes

1. Make Scripts Executable

`chmod +x /Users/sandipanray/Soket_Labs/start_crawler.sh`

This command makes start_crawler.sh executable, allowing it to be run as a script.

2. Make `Modular_Advance_scrapping.py` Executable

`chmod +x /Users/sandipanray/Soket_Labs/Modular_Advance_scrapping.py`

Similar to the first command, this makes Modular_Advance_scrapping.py executable, enabling it to be executed as a script.

3. Grant Write Access to `start_crawler.log`

`chmod u+w /Users/sandipanray/Soket_Labs/start_crawler.log`

This command grants the owner of start_crawler.log the permission to write to the file, enabling the script or processes to append or modify the log.

4. Grant Write Access to `log1.log`

`chmod u+w /Users/sandipanray/Soket_Labs/log1.log`

Similarly, this grants the owner of log1.log write permission, allowing processes to append or modify the log as needed.

5. Check for Running Processes

`pgrep -f /Users/sandipanray/Soket_Labs/Modular_Advance_scrapping.py`

This command searches for any running processes that match the pattern Modular_Advance_scrapping.py and returns their PIDs if found.


## Conclusions:




This advanced Python web scraping framework represents a culmination of efficient data extraction techniques and robust automation capabilities. By harnessing the power of multithreading and integrating versatile libraries like requests, BeautifulSoup, Scrapy, and Pandas, the framework excels in handling diverse web scraping tasks. 

Key features such as the SQLite database integration ensure secure and scalable data storage, while checkpoint mechanisms enable seamless resumption of interrupted crawls, enhancing reliability. The framework's ability to manage large datasets and generate clear, actionable reports underscores its utility for both exploratory data analysis and large-scale information gathering projects.

Moreover, the integration with cronjobs facilitates scheduled execution, making it ideal for automated data collection and monitoring tasks. Whether extracting structured data from websites or performing complex data transformations, this framework provides a flexible and powerful solution for leveraging web resources effectively.













    
