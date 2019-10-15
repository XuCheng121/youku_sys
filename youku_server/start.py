
import sys,os
sys.path.append(
    os.path.dirname(__file__)
)
from tcp_server import server
if __name__ == '__main__':
    server.run()