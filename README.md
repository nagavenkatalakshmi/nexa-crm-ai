# python app
## to manually run app
```
uvicorn main:app1
```

## dockerfile
```
# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["uvicorn", "main:app1", "--host", "0.0.0.0", "--port", "80"]
```


## Explanation of Each Dependency
- **fastapi**: The FastAPI framework.
- **uvicorn**: The ASGI server to run FastAPI.
- **pandas**: For data manipulation and analysis.
- **sqlalchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for connecting to the PostgreSQL database.
- **plotly**: For creating interactive visualizations.
- **openai**: To interact with the OpenAI API.
- **psycopg2-binary**: PostgreSQL database adapter for Python.
