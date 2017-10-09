from flask import Flask, render_template

app = Flask(__name__)
@app.route('/', methods=('GET', 'POST'))
def index():
    ''' '''
    return render_template('index.html')

@app.route('/simulation', methods=('GET', 'POST'))
def simulation():
    ''' '''
    return render_template('simulation.html')

@app.route('/error', methods=('GET', 'POST'))
def error():
    ''' '''
    return render_template('error.html')

@app.route('/robot', methods=('GET', 'POST'))
def robot():
    ''' '''
    return render_template('robot.html')

@app.route('/stereoscopic', methods=('GET', 'POST'))
def stereoscopic():
    ''' '''
    return render_template('stereoscopic.html')

@app.route('/blender', methods=('GET', 'POST'))
def blender():
    ''' '''
    return render_template('blender.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
