from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)

FILENAME = 'data.csv'


def read_file():
    with open(FILENAME, 'r') as file:
        rows = file.readlines()
        whole_text = ''
        for line in rows:
            whole_text += line
        lines = whole_text.split("\n\n")[:-1]
    table = [element.replace("\n\n", "").split(";") for element in lines]
    return table


def write_file(table):
    with open(FILENAME, "w") as file:
        for record in table:
            row = ';'.join(record)
            file.write(row + "\n\n")


@app.route('/')
@app.route('/list')
def index():
    try:
        table_text = read_file()
    except FileNotFoundError:
        table_text = []
    if 'table' in session:
        table_text = session['table']
    return render_template('list.html', table=table_text)


@app.route('/story')
@app.route('/story/<id>')
def story(id=None):
    try:
        table_text = read_file()
    except FileNotFoundError:
        table_text = []
    if 'table' in session:
        table_text = session['table']
    if id is None:
        new_row = [str(id), '', '', '', '', '']
        table_text += new_row
        statuses = ['new', 'good', 'bad', 'repaired', 'trash']
        return render_template('form.html', new_row=table_text[-1], id=id, statuses=statuses)
    else:
        id = int(id)
        statuses = ['new', 'good', 'bad', 'repaired', 'trash']
        return render_template('form.html', new_row=table_text[id], id=id, statuses=statuses)


@app.route('/story', methods=['POST'])
@app.route('/story/<id>', methods=['POST'])
def story_save(id=None):
    print('POST request received!')
    storage_unit = request.form['storage_unit']
    box = request.form['box']
    item_type = request.form['item_type']
    status = request.form['status']
    comment = request.form['comment']
    try:
        table_text = read_file()
    except FileNotFoundError:
        table_text = []
    if id is not None:
        id = int(id)
        new_line = [str(id), storage_unit, box, item_type, status, comment]
        table_text[id] = new_line
    else:
        try:
            new_id = int(table_text[-1][0]) + 1
        except IndexError:
            new_id = 0
        new_line = [str(new_id), storage_unit, box, item_type, status, comment]
        table_text.append(new_line)
    try:
        if storage_unit:
            if box:
                if item_type:
                    write_file(table_text)
    except ValueError:
        print(ValueError)
    return redirect('/')


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8000
    )