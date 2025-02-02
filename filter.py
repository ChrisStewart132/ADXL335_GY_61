from collections import deque

# Base Filter Class (Interface for all filters)
class Filter:
    def process(self, buffer):
        """
        Process the buffer and return the filtered value.
        :param buffer: Input buffer (deque) of values.
        :return: Filtered value.
        """
        raise NotImplementedError("Filter classes must implement this method.")

# Median Filter Implementation
class MedianFilter(Filter):
    def process(self, buffer):
        """
        Compute the median of the values in the buffer.
        :param buffer: Input buffer (deque) of values.
        :return: Median value of the buffer.
        """
        if not buffer:
            return 0  # Return 0 if the buffer is empty
        sorted_buffer = sorted(buffer)
        mid = len(sorted_buffer) // 2
        if len(sorted_buffer) % 2 == 0:
            return (sorted_buffer[mid - 1] + sorted_buffer[mid]) / 2
        else:
            return sorted_buffer[mid]

# EMA Filter Implementation
class EMAFilter(Filter):
    def __init__(self, alpha=0.3):
        """
        Initialize the EMA filter.
        :param alpha: Smoothing factor (0 < alpha < 1).
        """
        self.alpha = alpha
        self.filtered_value = None  # Initialize as None to handle the first value correctly

    def process(self, value):
        """
        Compute the Exponential Moving Average.
        :param value: The latest filtered value (not a buffer).
        :return: EMA-filtered value.
        """
        if self.filtered_value is None:
            self.filtered_value = value  # Initialize with the first value
        else:
            self.filtered_value = self.alpha * value + (1 - self.alpha) * self.filtered_value
        return self.filtered_value

# Filter Pipeline Class
class FilterPipeline:
    def __init__(self, buffer_size, filters):
        """
        Initialize the filter pipeline.
        :param buffer_size: Maximum size of the buffer (queue).
        :param filters: List of filter objects to apply in sequence.
        """
        self.buffer_size = buffer_size
        self.buffer = deque([], buffer_size)  # MicroPython-compatible way to set max size
        self.filters = filters

    def add_value(self, value):
        """
        Add a new value to the buffer.
        :param value: Input value to be added to the buffer.
        """
        if len(self.buffer) >= self.buffer_size:
            self.buffer.popleft()  # Manually enforce buffer limit in MicroPython
        self.buffer.append(value)

    def get_filtered_value(self):
        """
        Process the buffer through the pipeline of filters.
        :return: Final filtered value.
        """
        if not self.buffer:
            return 0  # Return 0 if the buffer is empty

        filtered_value = self.buffer  # Start with the full buffer for the first filter

        for i, filter_obj in enumerate(self.filters):
            # MedianFilter receives the full buffer, but EMAFilter receives a single number
            if i == 0:
                filtered_value = filter_obj.process(filtered_value)
            else:
                filtered_value = filter_obj.process(filtered_value)

        return filtered_value

# Example usage
if __name__ == "__main__":
    # Create filter objects
    median_filter = MedianFilter()
    ema_filter = EMAFilter(alpha=0.3)

    # Create a FilterPipeline with a buffer size of 5 and a list of filters
    filter_pipeline = FilterPipeline(buffer_size=5, filters=[median_filter, ema_filter])

    # Simulate input values
    input_values = [10, 12, 11, 13, 14, 15, 16, 17, 18, 19]

    # Process values through the pipeline
    print("Filter Pipeline Results:")
    for value in input_values:
        filter_pipeline.add_value(value)
        print(f"Input: {value}, Filtered: {filter_pipeline.get_filtered_value()}")
