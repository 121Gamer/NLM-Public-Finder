from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
import pandas as pd
from searcher import search_notebooks_robust
from database import init_db, save_results, get_all_notebooks, delete_notebook, update_tags, get_stats
import io
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'nlm-finder-dev-secret-2026')

# Initialize database on startup
init_db()


@app.route('/')
def index():
    df = get_all_notebooks()
    notebooks = df.to_dict('records')
    stats = get_stats()
    return render_template('index.html', notebooks=notebooks, stats=stats)


@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', 'site:notebooklm.google.com').strip()
    if not query:
        query = 'site:notebooklm.google.com'
    try:
        num_results = max(1, min(50, int(request.form.get('num_results', 10))))
    except ValueError:
        num_results = 10

    try:
        results = search_notebooks_robust(query=query, num_results=num_results)
        if results:
            new_count = save_results(results)
            flash(
                f"Found {len(results)} links. <strong>{new_count} new</strong> notebook(s) added to the library!",
                'success'
            )
        else:
            flash("No results found for that query — try different keywords.", 'warning')
    except Exception as e:
        flash(f"Search error: {e}", 'error')

    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete():
    url = request.form.get('url', '').strip()
    if url and delete_notebook(url):
        flash("Notebook removed from library.", 'success')
    else:
        flash("Could not find that notebook to delete.", 'warning')
    return redirect(url_for('index'))


@app.route('/tag', methods=['POST'])
def tag():
    url = request.form.get('url', '').strip()
    tags = request.form.get('tags', '').strip()
    if url:
        update_tags(url, tags)
        return jsonify({"status": "ok"})
    return jsonify({"status": "error", "message": "No URL provided"}), 400


@app.route('/stats')
def stats():
    return jsonify(get_stats())


@app.route('/export')
def export():
    df = get_all_notebooks()
    if df.empty:
        flash("No data to export.", 'warning')
        return redirect(url_for('index'))

    output = io.BytesIO()
    df.to_csv(output, index=False, encoding='utf-8')
    output.seek(0)

    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='notebooklm_library.csv'
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
