# Comments in Dockerfiles
FROM python:2.7

# Update and install dependencies
RUN apt-get update
RUN pip install Flask
RUN pip install flask_cors
RUN pip install pymysql
RUN pip install requests
RUN pip install networkx
RUN pip install re

# Add code
ADD . /opt/spoiless/spoilessbackend

# Set the working directory
WORKDIR /opt/spoiless/spoilessbackend

# Set environment variables
ENV FLASK_APP=controller.py

# Expose the application's port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
