from time import sleep
import sys,os

def main():
  while True:
    byte = os.read(0,1)
    if not byte:
      break
    os.write(1, byte)
    sys.stdout.flush()
    sleep(0.1)

if __name__ == "__main__":
    main()