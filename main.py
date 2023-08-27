# Auto install dependencies
import subprocess

subprocess.run(['pip3', 'install', '-r', 'requirements.txt'])

# Run application
from website import create_app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
