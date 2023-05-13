from flask import Flask, render_template, request, send_from_directory
import os
import PyPDF2
import math

# (Aquí va el resto del código que proporcionaste, desde "class MTreeNode" hasta "mtree = MTree(max_children=2)")
from doctremod import MTreeNode, MTree, search_documents_in_folder
mtree = MTree(max_children=2)  # Añade esta línea

# (Aquí va el resto del código que proporcionaste, desde "class MTreeNode" hasta "mtree = MTree(max_children=2)")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    folder_path ='./uploads' #URL de la carpeta
    documents = search_documents_in_folder(folder_path)

    for document in documents:
        content, filename = document
        mtree.insert(content, filename)
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        for file in request.files.getlist('file'):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                content = ''
                for page in range(len(reader.pages)):
                    content += reader.pages[page].extract_text()
            mtree.insert(content, filename)
        return 'Archivos cargados y procesados.'

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = mtree.search(query)
        print(results)
        return render_template('results.html', results=results)
    return render_template('search.html')

@app.route('/download/<filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory= uploads, path=filename)

if __name__ == '__main__':
    app.run(debug=True)
