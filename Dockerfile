
#
# Use the official Python image
FROM python=3.13.3
# Create and set a non-root user
RUN useradd -m -u 1000 user
USER user

# Set environment path for locally installed Python packages
ENV PATH="/home/user/.local/bin:$PATH"

# Set working directory
WORKDIR /home/user/app

# Copy only the requirements file first
COPY --chown=user requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY --chown=user . .

# Set the name of the main Flask file (if not app.py)
ENV FLASK_APP=app.py

# Start the Flask app on Hugging Face's required port
CMD ["flask", "run", "--host=0.0.0.0", "--port=7860"]