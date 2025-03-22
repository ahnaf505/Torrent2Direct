CC = gcc
CFLAGS = -Wall -Wextra -I./src

SRC_DIR = src
BUILD_DIR = build

SRCS = $(wildcard $(SRC_DIR)/*.c)
OBJS = $(SRCS:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)
TARGET = $(BUILD_DIR)/project_binary

all: $(TARGET)

$(TARGET): $(OBJS)
	@echo "Linking..."
	$(CC) $(OBJS) -o $@

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(BUILD_DIR)
	@echo "Compiling $<..."
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	@echo "Cleaning up..."
	rm -rf $(BUILD_DIR)

debug: CFLAGS += -g
debug: clean all