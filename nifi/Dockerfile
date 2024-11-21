# Base image for Apache NiFi
FROM apache/nifi:latest

# Switch to root user to install packages
USER root

# Update and install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openssh-server \
        sshpass \
        expect && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the ssh_expect.sh script to the container
COPY ssh_expect_process_jpg.sh /tmp/ssh_expect_process_jpg.sh
COPY ssh_expect_process_video.sh /tmp/ssh_expect_process_video.sh

# Make the script executable
RUN chmod +x /tmp/ssh_expect_process_jpg.sh
RUN chmod +x /tmp/ssh_expect_process_video.sh

# Switch back to nifi user
USER nifi

#docker build -t nifi-custom .