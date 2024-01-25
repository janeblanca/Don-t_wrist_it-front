class Break:
    def __init__(self, window):
        self.window = window

    def set_break_time(self):
        break_time_str = self.window.user_input_break.text()
        try:
            self.window.break_time = int(break_time_str) * 60
            print(f"Break time set to {self.window.break_time} seconds.")
            self.window.user_input_break.clear()
        except ValueError:
            print("Invalid input. Please enter a valid integer for break time.")

    def set_break_interval(self):
        break_interval_str = self.window.user_input_interval.text()
        try:
            self.window.break_interval = int(break_interval_str) * 60  # Convert minutes to seconds
            print(f"Break interval set to {self.window.break_interval} seconds.")
            self.window.user_input_interval.clear()
        except ValueError:
            print("Invalid input. Please enter a valid integer for break interval.")

    def format_time(self, seconds):
        minutes, sec = divmod(seconds, 60)
        return f"{minutes:02d}:{sec:02d}"

    def validate_inputs(self):
        try:
            self.window.break_time = int(self.window.user_input_break.text()) * 60  # Convert minutes to seconds
            self.window.original_break_time = self.window.break_time
            print(f"Break time set to {self.window.break_time} seconds.")

            self.window.break_interval = int(self.window.user_input_interval.text()) * 60  # Convert minutes to seconds
            self.window.original_break_interval = self.window.break_interval
            print(f"Break interval set to {self.window.break_interval} seconds.")

            self.window.user_input_break.clear()
            self.window.user_input_interval.clear()

            self.window.user_input_break.setEnabled(False)
            self.window.user_input_interval.setEnabled(False)

            # Start the timer here
            self.window.break_interval_active = True
            self.window.start_timer()

        except ValueError:
            print("Invalid input. Please enter valid integers for break time and break interval.")

    def start_timer(self):
        # Get the break time duration
        break_time_str = self.window.user_input_break.text()
        break_interval_str = self.window.user_input_interval.text()

        try:
            self.window.break_time = int(break_time_str) * 60  # Convert minutes to seconds
            self.window.original_break_time = self.window.break_time

            # Check if break interval is set, then start the timer
            if break_interval_str:
                self.window.break_interval = int(break_interval_str) * 60  # Convert minutes to seconds
                self.window.original_break_interval = self.window.break_interval

                print(f"Break time set to {self.window.break_time} seconds.")
                print(f"Break interval set to {self.window.break_interval} seconds.")

                self.window.user_input_break.clear()
                self.window.user_input_interval.clear()

                self.window.user_input_break.setEnabled(False)
                self.window.user_input_interval.setEnabled(False)

                self.window.break_interval_active = True

        except ValueError:
            print("Invalid input. Please enter a valid integer for break time and interval.")