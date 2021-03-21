

# Wave Software Development Challenge

Applicants for the Full-stack Developer role at Wave must
complete the following challenge, and submit a solution prior to the onsite
interview.

The purpose of this exercise is to create something that we can work on
together during the onsite. We do this so that you get a chance to collaborate
with Wavers during the interview in a situation where you know something better
than us (it's your code, after all!)

There isn't a hard deadline for this exercise; take as long as you need to
complete it. However, in terms of total time spent actively working on the
challenge, we ask that you not spend more than a few hours, as we value your
time and are happy to leave things open to discussion in the on-site interview.

Please use whatever programming language and framework you feel the most
comfortable with.

Feel free to email [dev.careers@waveapps.com](dev.careers@waveapps.com) if you
have any questions.

## Project Description

Imagine that this is the early days of Wave's history, and that we are prototyping a new payroll system API. A front end (that hasn't been developed yet, but will likely be a single page application) is going to use our API to achieve two goals:

1. Upload a CSV file containing data on the number of hours worked per day per employee
1. Retrieve a report detailing how much each employee should be paid in each _pay period_

All employees are paid by the hour (there are no salaried employees.) Employees belong to one of two _job groups_ which determine their wages; job group A is paid $20/hr, and job group B is paid $30/hr. Each employee is identified by a string called an "employee id" that is globally unique in our system.

Hours are tracked per employee, per day in comma-separated value files (CSV).
Each individual CSV file is known as a "time report", and will contain:

1. A header, denoting the columns in the sheet (`date`, `hours worked`,
   `employee id`, `job group`)
1. 0 or more data rows

In addition, the file name should be of the format `time-report-x.csv`,
where `x` is the ID of the time report represented as an integer. For example, `time-report-42.csv` would represent a report with an ID of `42`.

You can assume that:

1. Columns will always be in that order.
1. There will always be data in each column and the number of hours worked will always be greater than 0.
1. There will always be a well-formed header line.
1. There will always be a well-formed file name.

A sample input file named `time-report-42.csv` is included in this repo.

### What your API must do:

We've agreed to build an API with the following endpoints to serve HTTP requests:

1. An endpoint for uploading a file.

   - This file will conform to the CSV specifications outlined in the previous section.
   - Upon upload, the timekeeping information within the file must be stored to a database for archival purposes.
   - If an attempt is made to upload a file with the same report ID as a previously uploaded file, this upload should fail with an error message indicating that this is not allowed.

2. An endpoint for retrieving a payroll report structured in the following way:

   _NOTE:_ It is not the responsibility of the API to return HTML, as we will delegate the visual layout and redering to the front end. The expectation is that this API will only return JSON data.

   - Return a JSON object `payrollReport`.
   - `payrollReport` will have a single field, `employeeReports`, containing a list of objects with fields `employeeId`, `payPeriod`, and `amountPaid`.
   - The `payPeriod` field is an object containing a date interval that is roughly biweekly. Each month has two pay periods; the _first half_ is from the 1st to the 15th inclusive, and the _second half_ is from the 16th to the end of the month, inclusive. `payPeriod` will have two fields to represent this interval: `startDate` and `endDate`.
   - Each employee should have a single object in `employeeReports` for each pay period that they have recorded hours worked. The `amountPaid` field should contain the sum of the hours worked in that pay period multiplied by the hourly rate for their job group.
   - If an employee was not paid in a specific pay period, there should not be an object in `employeeReports` for that employee + pay period combination.
   - The report should be sorted in some sensical order (e.g. sorted by employee id and then pay period start.)
   - The report should be based on all _of the data_ across _all of the uploaded time reports_, for all time.

As an example, given the upload of a sample file with the following data:

   | date       | hours worked | employee id | job group |
   | ---------- | ------------ | ----------- | --------- |
   | 2020-01-04 | 10           | 1           | A         |
   | 2020-01-14 | 5            | 1           | A         |
   | 2020-01-20 | 3            | 2           | B         |
   | 2020-01-20 | 4            | 1           | A         |

A request to the report endpoint should return the following JSON response:

   ```json
   {
     "payrollReport": {
       "employeeReports": [
         {
           "employeeId": "1",
           "payPeriod": {
             "startDate": "2020-01-01",
             "endDate": "2020-01-15"
           },
           "amountPaid": "$300.00"
         },
         {
           "employeeId": "1",
           "payPeriod": {
             "startDate": "2020-01-16",
             "endDate": "2020-01-31"
           },
           "amountPaid": "$80.00"
         },
         {
           "employeeId": "2",
           "payPeriod": {
             "startDate": "2020-01-16",
             "endDate": "2020-01-31"
           },
           "amountPaid": "$90.00"
         }
       ]
     }
   }
   ```

We consider ourselves to be language agnostic here at Wave, so feel free to use any combination of technologies you see fit to both meet the requirements and showcase your skills. We only ask that your submission:

- Is easy to set up
- Can run on either a Linux or Mac OS X developer machine
- Does not require any non open-source software

### Documentation:

Please commit the following to this `README.md`:

Instructions on how to build/run your application:

[Video](https://youtu.be/EZ-7mEelTsc)

This application was built using microservice architecture. There is a <b>frontend</b> and a <b>backend</b> folder that make up the app. The technologies used are:

- frontend: <b>react</b> (tested on node v12.14.0)
- backend: <b> flask </b> (tested on python3 and pip3)
- database: <b> sqlite3 </b> (python inbuilt library)

You can either test locally, or through docker (assuming python3 and pip3 are installed for local testing):

Docker (recommended)
---
```
# root folder
# you will see "You can now view frontend in the browser"
# that's when you know it is complete
docker-compose up
```

navigate to `http://localhost:3000/` for the frontend
navigate to `http://localhost:5000/` for the backend

Local Testing
---
frontend:
```
cd frontend
npm install
npm start
```
backend:
```
cd backend

##### OPTIONAL #####
python -m venv env # if venv not installed: apt-get install python3-venv
source env/bin/activate # for windows, you can use env\Scripts\activate 
##### OPTIONAL #####

pip install -r req.txt
python db/db.py init
python db/db.py migrate
python app.py
```

navigate to `http://localhost:3000/` for the frontend
navigate to `http://localhost:5000/` for the backend



Answers to the following questions:
   - How did you test that your implementation was correct?
	   - From a logic standpoint:
		   - I attempted to test many edge cases through the csv file
		   - For example, I would upload the same file twice (under a different name), and make sure all the values in amount paid would double
		   - I also tested when employees were paid twice on a single day, paid during both periods, paid during a single period, and also paid on the exact middle date of the month
		   - Other edge cases I tested was when the csv was completely empty
		   - Although the README said there would not be a malformed csv, I decided to check cases like that too, and made sure my program responded appropriately
	   - From a UX standpoint:
		   - I made sure that the table rendered matches the JSON response from the API, and made sure that no rows were being left out.

   - If this application was destined for a production environment, what would you add or change?
	   - Use an ORM to access the database
		   - The first thing I would do is change the way the server accesses the sqlite3 db
		   - I would use an ORM like SQLAlchemy as it keeps the code much neater and very simple
	   - Use session based authentication with JWT
		   - I would also look into implementing a session for the user rather than storing a JWT token in the cookies, as a session is much safer and less prone to attacks
	   - Deploy through docker only as it is much simpler
		   - Currently in my docker-compose file, I pass in the backend url to the frontend, and pass in the frontend url to the backend for cors related tasks
		   - I would modify my docker-compose file to instead pass in the name of an environment, and actually have the urls stored in a javascript file or .env file
		   - Then, all I have to do is change my code to pick off urls based off the env name, and it should work
		   - If I want to deploy to dev, I just change the docker-compose env variable to be dev, and the application should use the dev urls
	   - Use a random key generator to generate the JWT secret key
		   - Currently, it is passed in through an env variable, or set to its default value
		   - A random key generated on the fly would be much better
	   - Make sure frontend and backend are using production builds
		   - For flask backend, the DEBUG=True flag should be changed
		   - For react frontend, we should be serving the static assets of a production build
   - What compromises did you have to make as a result of the time constraints of this challenge?
	   - Did not use an ORM like SQLAlchemy
		   - I firstly decided not to use an ORM like SQLAlchemy, simply because I haven't used it in a while, and it would just be faster for me to write the queries by hand
		   - The ORM would've cleaned up the code nicely and reduced the query sizes, but I just decided to use the queries themselves for practice and time constraints
		   - The ORM would also force me to create class models that represent the database structure, and thus I just decided to quickly go with the queries themselves and skip all of that
	   - Did not use session based authentication with JWT
		   - I also decided implement very basic security, including a JWT token that authenticates the HR admin user
		   - The compromise that I had to make was that I decided to store the token in the cookies rather than creating a server side session, and storing the token in that
		   - A session would allow me to store important information on the server side, and would be easily accessible through there
		   - Even though I use the httpOnly flag on the cookie, it is still more secure to use a session due to a session id, which is the only thing visible
	   - Did not do unit testing through the flask api
		   - I don't know how to unit test through the flask api, it would have to be something that I would have to look into
		   - For a larger project, it may be better to use a more structured framework like Django 

# Tables
- ADMINS (id, username, password)
	- stores info about users who can access the application
	- password is hashed, id is a generated uuid that the JWT is based on

- EMPLOYEES (id)
	- stores info about all employees
	- the id is used as a foreign key in the EMPLOYEE_LOGS table

- EMPLOYEE_LOGS (employee_id, log_date, hours, job_name, report_num)
	- employee_id is a foreign key that references the id column in the EMPLOYEES table
	- realistically, the EMPLOYEES table should be populated before the csv file is uploaded, to make sure that we don't upload a file that has records of an employee that doesn't exist
	- log_date is stored as a unix timestamp, easier for sorting
	- report_num is there so we know which reports have already been uploaded
	- job_name is a foreign key to name in the JOBS table
	- it might be good to store report_num in its own table instead

- JOBS (name, rate)
	- stores the name of the job "A" or "B", and the rate (20 or 30)
	- the job_name in EMPLOYEE_LOGS is a foreign key to name
	- if we run into a csv row with a job name we do not recognize, we don't process the csv file

## Submission Instructions

1. Clone the repository.
1. Complete your project as described above within your local repository.
1. Ensure everything you want to commit is committed.
1. Create a git bundle: `git bundle create your_name.bundle --all`
1. Email the bundle file to [dev.careers@waveapps.com](dev.careers@waveapps.com) and CC the recruiter you have been in contact with.

## Evaluation

Evaluation of your submission will be based on the following criteria.

1. Did you follow the instructions for submission?
1. Did you complete the steps outlined in the _Documentation_ section?
1. Were models/entities and other components easily identifiable to the
   reviewer?
1. What design decisions did you make when designing your models/entities? Are
   they explained?
1. Did you separate any concerns in your application? Why or why not?
1. Does your solution use appropriate data types for the problem as described?