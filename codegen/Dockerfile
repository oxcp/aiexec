# Use the official Nginx image as the base
FROM nginx

# Set the working directory inside the container
WORKDIR /usr/share/nginx/html

# Copy static web files (codegen.*), YAML, and TXT files to the Nginx HTML directory
COPY index.html codegen.* ./
RUN mkdir -p /usr/share/nginx/html/output
COPY output/*  ./output/
RUN mkdir -p /usr/share/nginx/html/prompts
COPY prompts/* ./prompts/

# Expose port 80
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
