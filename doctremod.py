import math
import os
import PyPDF2
from docx import Document

class MTreeNode:
    def __init__(self, data, name):
        self.data = data
        self.name = name
        self.children = []
        self.parent = None

class MTree:
    def __init__(self, max_children):
        self.root = None
        self.max_children = max_children

    def insert(self, data, name):
        if self.root is None:
            self.root = MTreeNode(data, name)
        else:
            self._insert_recursive(data, name, self.root)

    def _insert_recursive(self, data, name, node):
        if len(node.children) < self.max_children:
            # Si el nodo tiene espacio, simplemente agregamos el dato
            node.children.append(MTreeNode(data, name))
        else:
            # Si el nodo está lleno, calculamos la distancia al dato existente más cercano
            min_distance = math.inf
            closest_child = None
            for child in node.children:
                distance = self.calculate_distance(data, child.data)
                if distance < min_distance:
                    min_distance = distance
                    closest_child = child

            # Insertamos el dato en el hijo más cercano
            self._insert_recursive(data, name, closest_child)

    def search(self, query, threshold):
        if self.root is None:
            return []
        else:
            return self._search_recursive(query, threshold, self.root)

    def _search_recursive(self, query, threshold, node):
        results = []

        # Verificamos si el nodo actual coincide con el criterio de búsqueda
        distance = self.calculate_distance(query, node.data)
        if distance <= threshold:
            results.append(node.name)

        # Exploramos los hijos recursivamente
        for child in node.children:
            results.extend(self._search_recursive(query, threshold, child))

        return results

    def calculate_distance(self, data1, data2):
        # Calcula la distancia entre dos documentos basada en la longitud de sus cadenas
        return abs(len(data1) - len(data2))

    def match_criteria(self, query, data):
        # Verifica si el documento contiene todas las palabras clave de la consulta
        keywords = query.split()
        for keyword in keywords:
            if keyword.lower() not in data.lower():
                return False
        return True

def search_documents_in_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            if filename.endswith('.pdf'):
                # Leer contenido de un archivo PDF
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    content = ''
                    for page in range(len(reader.pages)):
                        content += reader.pages[page].extract_text()
                    documents.append((content, filename))
            #elif filename.endswith('.docx'):
                # Leer contenido de un archivo Word
                #doc = Document(file_path)
                #content = ' '.join([p.text for p in doc.paragraphs])
                #documents.append((content, filename))
    return documents

# Ejemplo de uso
mtree = MTree(max_children=2)

# Buscar documentos en una carpeta y agregarlos al árbol
folder_path ='D:\CV'
documents = search_documents_in_folder(folder_path)
for document in documents:
    content, filename = document
    mtree.insert(content, filename)

# Realizar una búsqueda por similitud de contenido
query = "informe"
threshold = 5  # Umbral de similitud
results = mtree.search(query, threshold)

if len(results) > 0:
    print("Documentos con similitud de contenido:")
    for document_name in results:
        print("- " + document_name)
else:
    print("No se encontraron documentos con similitud de contenido.")

# No se encontraron documentos 