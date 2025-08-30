# ========================
# Stage 1: Builder
# ========================
FROM python:3.12-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    git \
    sudo \
    bash-completion \
    ca-certificates \
    fonts-powerline \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user with sudo access
RUN useradd -ms /bin/bash amiche && \
    echo "amiche ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set workdir and copy requirements
WORKDIR /app
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

# Install Starship
RUN curl -sS https://starship.rs/install.sh | sh -s -- -y -b /usr/local/bin

# Add starship to bashrc
RUN echo 'eval "$(starship init bash)"' >> /home/amiche/.bashrc

# ========================
# Stage 2: Runtime
# ========================
FROM python:3.12-slim AS runtime

RUN apt-get update && apt-get install -y sudo && rm -rf /var/lib/apt/lists/*

# Copy only what's needed from builder
COPY --from=builder /usr/local/bin/starship /usr/local/bin/starship
COPY --from=builder /install /usr/local
COPY --from=builder /etc/sudoers /etc/sudoers

# Create non-root user with sudo access
RUN useradd -ms /bin/bash amiche && \
    echo "amiche ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Add starship to bashrc
RUN echo 'eval "$(starship init bash)"' >> /home/amiche/.bashrc && \
    chown -R amiche:amiche /home/amiche

# Set workdir
WORKDIR /app
USER amiche

# Default command
CMD ["tail", "-f", "/dev/null"]