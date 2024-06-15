FROM ros:noetic-ros-base-focal

ENV DEBIAN_FRONTEND=noninteractive

# The base image already has ROS installed with its dependencies, 
# but you might still need to install specific utilities.
RUN apt-get update && apt-get install -y \
    lsb-release \
    wget \
    curl \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# This step may not be necessary as the setup should already be in the bashrc of the base image
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

# Copy the ROS workspace into the container's /root directory
COPY catkin_ws /root/catkin_ws

# Using bash to ensure the ROS environment is properly sourced
RUN /bin/bash -c 'source /opt/ros/noetic/setup.bash && \
    apt-get update && \
    rosdep install --from-paths /root/catkin_ws/src --ignore-src --rosdistro=noetic -y && \
    rm -rf /var/lib/apt/lists/*'

# Build the ROS workspace using bash
RUN /bin/bash -c 'source /opt/ros/noetic/setup.bash && \
    cd /root/catkin_ws && \
    catkin_make'

CMD ["bash"]
