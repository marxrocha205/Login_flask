from flask import Flask, render_template

app = Flask(__name__)

def read_video_links(file_path):
    video_links = []
    with open(file_path, 'r') as file:
        for line in file:
            name, url = line.strip().split('|')
            video_links.append((name, url))
    return video_links

@app.route('/')
def index():
    video_links = read_video_links('links.txt')
    return render_template('index.html', video_links=video_links)

if __name__ == '__main__':
    app.run(debug=True)
