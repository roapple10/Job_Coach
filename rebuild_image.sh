# rerun+rebuild image `chmod +x rebuild_image.sh; ./rebuild_image.sh`

# Stop and remove the current running container (if it exists)
docker stop jobcoach-container
docker rm jobcoach-container


# Remove the existing image (if it exists)
# This step is optional and could be skipped to take advantage of Docker's caching mechanism
docker rmi jobcoach_image
# docker volume rm jobcoach-volume

# Build the Docker image
docker build --no-cache -t jobcoach_image .

# Run the Docker container with a bind mount from the current ./backend directory
docker run -d \
  --network=bridge \
  --name jobcoach-container \
  -p 8080:8080 \
  --env-file backend/.env \
  -v "$(pwd)":/app \
  jobcoach_image \
  streamlit run app.py --server.port 8080 --server.address 0.0.0.0

