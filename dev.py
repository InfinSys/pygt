
#   IMPORTS
import pygt
from pygt.window import AppWindow
from pygt.utility.platform import win32_get_display_names


def test_window_controller(instance: AppWindow) -> None:
    """ Test window controller. """
    instance.control.disable_native_controls()
    instance.event.schedule(func=lambda: window.control.center_on_display(), delay=3000)
    instance.event.schedule(func=lambda: window.control.enable_native_controls(), delay=4000)
    instance.event.schedule(func=lambda: window.control.maximize(), delay=5000)
    instance.event.schedule(func=lambda: window.control.minimize(), delay=6000)
    instance.event.schedule(func=lambda: window.control.restore_down(), delay=7000)
    instance.event.schedule(func=lambda: window.control.restore_down(), delay=8000)
    instance.event.schedule(func=lambda: window.control.center_on_display(), delay=9000)
    instance.event.schedule(func=lambda: window.control.set_scale(.5, (16, 9)), delay=10000)
    instance.event.schedule(func=lambda: window.control.center_on_display(), delay=11000)
    instance.event.schedule(func=lambda: window.control.set_title("Testing"), delay=12000)
    instance.event.schedule(func=lambda: window.control.set_title("TESTING"), delay=13000)
    instance.event.schedule(func=lambda: window.control.set_title("TESTING!!!!!!"), delay=14000)
    instance.event.schedule(func=lambda: window.control.set_title("tk"), delay=15000)
    instance.event.schedule(func=lambda: window.control.set_background("red"), delay=16000)
    instance.event.schedule(func=lambda: window.control.set_background("green"), delay=17000)
    instance.event.schedule(func=lambda: window.control.set_background("blue"), delay=18000)
    instance.event.schedule(func=lambda: window.control.set_background("black"), delay=19000)
    instance.event.schedule(func=lambda: window.control.set_background("#ffffff"), delay=20000)
    instance.event.schedule(func=lambda: window.control.hide(), delay=21000)
    instance.event.schedule(func=lambda: window.control.show(), delay=22000)
    instance.event.schedule(func=lambda: window.control.center_on_display(display="DISPLAY1"), delay=23000)

    try:
        instance.event.schedule(func=lambda: window.control.center_on_display(display="DISPLAY2"), delay=24000)
        instance.event.schedule(func=lambda: window.control.center_on_display(display="DISPLAY3"), delay=25000)
    except Exception as e:
        del e

    instance.event.schedule(func=lambda: window.control.set_width(500), delay=26000)
    instance.event.schedule(func=lambda: window.control.set_height(250), delay=27000)
    instance.event.schedule(func=lambda: window.control.center_on_display(), delay=28000)
    instance.event.schedule(func=lambda: print("Window controller test complete!"), delay=28500)
    instance.event.schedule(func=lambda: window.control.set_title("Test Complete!"), delay=29000)
    instance.event.schedule(func=lambda: window.control.set_title("Window Controller Tests"), delay=32000)
    instance.event.schedule(func=lambda: window.control.set_title("Test Complete!"), delay=35000)
    instance.event.schedule(func=lambda: window.control.set_title("Window Controller Tests"), delay=38000)
    instance.event.schedule(func=lambda: window.control.set_title("Test Complete!"), delay=41000)


if __name__ == "__main__":
    print("\n| Dev Script |\n")

    window: AppWindow = AppWindow(width=300, height=200)
    window.mainloop()

    print("\n| Complete |")
