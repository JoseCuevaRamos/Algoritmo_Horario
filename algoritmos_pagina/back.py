from flask import Flask, render_template, request, redirect, url_for,session
import csv

app = Flask(__name__, template_folder='.')
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Abrir el archivo CSV y verificar las credenciales
    with open('BasedeDatos.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Comparación de cadenas eliminando espacios en blanco adicionales
            if row['ID_ALUM'].strip() == username and row['CONTRASEÑA'].strip() == password:
                nombre=row['NOMBRE_ALUM']
                ciclo=row['CICLO_ALUM']
                session['username'] = nombre
                session['ciclo'] = ciclo
                # Autenticación exitosa, redirigir a una página de éxito o dashboard
                return redirect(url_for('success'))

    # Si las credenciales son incorrectas, redirigir a la página de login nuevamente con un mensaje de error
    return render_template('index.html', message='Credenciales incorrectas. Inténtalo nuevamente.')

@app.route('/pagina_p')
def success():
    return render_template('pagina_p.html')  # Renderiza la plantilla pagina_p.html

@app.route('/h_dispo')
def h_dispo():
    
    data = []
    with open('horario_final.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)

    # Pasar los datos a la plantilla
    return render_template('h_dispo.html', data=data)


#este es donde deben cambiar todo
@app.route('/h_p', methods=['GET', 'POST'])
def h_p():
    username = session.get('username')
    ciclo = session.get('ciclo')
    ciclof=int(ciclo)
    csvf=''
    if ciclof==1:
        csvf='ciclo1.csv'
    elif ciclof==2:
        csvf='ciclo2.csv'
    elif ciclof==3:
        csvf='ciclo3.csv'         
    elif ciclof==4:
        csvf='ciclo4.csv' 
    elif ciclof==5:
        csvf='ciclo5.csv'     
    elif ciclof==6:
        csvf='ciclo6.csv'
    elif ciclof==7:
        csvf='ciclo7.csv' 
    elif ciclof==8:
        csvf='ciclo8.csv'
    elif ciclof==9:
        csvf='ciclo9.csv' 
    elif ciclof==10:
        csvf='ciclo10.csv' 
                             
    data = []
    nombres = set()
    #cambia el nombre de la base de datos
    with open(csvf , newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #pon el nombre de la columna  del codigo o nombre de los cursos
            nombres.add(row['Curso'])

    if request.method == 'POST':
        selected_names = request.form.getlist('selected_names')
        with open(csvf, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Curso'] in selected_names:
                    data.append(row)
    else:
        with open(csvf, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)

    return render_template('h_p.html', username=username, data=data, nombres=nombres)

if __name__ == '__main__':
    app.run(debug=True)
