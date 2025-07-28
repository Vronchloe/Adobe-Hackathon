# Adobe-Hackathon
Team DevGuys: Arman Ranjan, Gaurav Singh, Dhruv Sahni
To run the files:
Ensure you have Python 3.9 installed on your devices.
To run the files in docker, right click on the respective folder and open in terminal.
For 1a
First run docker build --platform linux/amd64 -t pdf-processor .
Then run 
docker run --rm `
 -v "${PWD}\input:/app/input:ro" `
 -v "${PWD}\output:/app/output" `
 --network none pdf-processor
All 4 lines one after the other, and run them together. 

for 1b:
Folder main terminal open ker aur ye command run kerde

docker build -t persona-pdf-analyzer .

Docker open rkhna background main.

Build ho jayega.

Phir run kerne ke liye 

docker run --rm `
  -v "${PWD}\input_jsons:/app/input_jsons" `
  -v "${PWD}\input_pdfs:/app/input_pdfs" `
  -v "${PWD}\outputs:/app/outputs" `
  -v "${PWD}\tinyllama_model:/app/tinyllama_model" `
  persona-pdf-analyzer

Ye command
