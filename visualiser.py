import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time, json

def on_message(ws, message):
    r = json.loads(message)
    print(r['audio_plot'][-1])
    print('***')

def on_error(ws, error):
    print("** error")

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        result = ws.recv()
        r = json.loads(result)
        print(r['audio_plot'][-1])
        time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://nannycam.local:8090/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
