from threading import Timer

class RepeatTimer(Timer):
    isRunning = False

    def run(self):
        self.isRunning = True 
        while not self.finished.wait(self.interval) and self.isRunning:
            self.function(*self.args, **self.kwargs)

    def stop(self):
        self.isRunning = False

    def cancel(self) -> None:
        self.isRunning = False
        return super().cancel()