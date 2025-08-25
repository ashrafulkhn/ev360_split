from contactor_handler.gpio_config import GPIO_PIN
import os

class GPIOController:
    def __init__(self, gpio_map):
        self.gpio_map = gpio_map
        self._export_all()

    def _export_gpio(self, gpio_num):
        gpio_path = f"/sys/class/gpio/gpio{gpio_num}"
        if not os.path.exists(gpio_path):
            with open("/sys/class/gpio/export", "w") as f:
                f.write(str(gpio_num))
        return gpio_path

    def set_direction(self, name, direction):
        gpio_num = self.gpio_map[name]
        gpio_path = f"/sys/class/gpio/gpio{gpio_num}/direction"
        with open(gpio_path, "w") as f:
            f.write(direction)

    def _export_all(self):
        for name, gpio_num in self.gpio_map.items():
            gpio_path = self._export_gpio(gpio_num)
            self.set_direction(name, "out")

    def set_value(self, name, value):
        gpio_num = self.gpio_map[name]
        gpio_path = f"/sys/class/gpio/gpio{gpio_num}/value"
        with open(gpio_path, "w") as f:
            f.write(str(value))

    def set_all(self, value):
        for name in self.gpio_map:
            self.set_value(name, value)
            print(f"{name} set to {value}")

def interactive_loop(obj):
    while True:
        state = input("Enter GPIO state (1/0): ").strip()
        if state not in ["0", "1"]:
            print("Invalid input. Use 1 or 0.")
            continue
        obj.set_all(state)
        # obj.set_all(state)

if __name__ == "__main__":
    controller = GPIOController(GPIO_PIN.GPIO_PINS)
    interactive_loop(controller)
