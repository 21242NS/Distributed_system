from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
import json
from urllib.parse import parse_qs, urlparse

import numpy as np
from PIL import Image

from mandelbrot_set import mandelbrot


class ServiceHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urlparse(self.path)

        if route.path == "/health":
            self.send_json({"service": "mandelbrot", "status": "ok"})
            return

        if route.path == "/mandelbrot.png":
            self.send_mandelbrot(parse_qs(route.query))
            return

        if route.path == "/":
            self.send_html()
            return

        self.send_error(404, "Not found")

    def send_html(self):
        body = b"""<!doctype html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <title>Mandelbrot</title>
    <style>
        body { font-family: sans-serif; max-width: 980px; margin: 2rem auto; }
        form { display: flex; flex-wrap: wrap; gap: 1rem; align-items: end; }
        label { display: grid; gap: .25rem; }
        input { width: 8rem; padding: .35rem; }
        button { padding: .45rem .8rem; cursor: pointer; }
        img { display: block; width: min(100%, 800px); margin-top: 1.5rem; image-rendering: pixelated; }
    </style>
</head>
<body>
  <h1>Ensemble de Mandelbrot</h1>
    <form id="controls">
        <label>Resolution <input name="resolution" type="number" min="100" max="1200" value="600"></label>
        <label>Zoom <input name="zoom" type="number" min="1" max="100000" step="any" value="1"></label>
        <label>Centre X <input name="center_x" type="number" step="any" value="-0.5"></label>
        <label>Centre Y <input name="center_y" type="number" step="any" value="0"></label>
        <label>Iterations <input name="iterations" type="number" min="20" max="500" value="80"></label>
        <button type="submit">Calculer</button>
    </form>
    <img id="fractal" src="/mandelbrot.png?resolution=600&zoom=1&center_x=-0.5&center_y=0&iterations=80" alt="Ensemble de Mandelbrot en noir sur fond blanc">
    <script>
        const form = document.querySelector('#controls');
        const image = document.querySelector('#fractal');
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            const params = new URLSearchParams(new FormData(form));
            params.set('cache', Date.now());
            image.src = '/mandelbrot.png?' + params;
        });
    </script>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_mandelbrot(self, query):
        resolution = self.get_int(query, "resolution", 600, 100, 1200)
        zoom = self.get_float(query, "zoom", 1.0, 1.0, 100000.0)
        center_x = self.get_float(query, "center_x", -0.5, -2.0, 2.0)
        center_y = self.get_float(query, "center_y", 0.0, -2.0, 2.0)
        iterations = self.get_int(query, "iterations", 80, 20, 500)
        half_width = 1.5 / zoom
        half_height = 1.5 / zoom
        values = mandelbrot(
            resolution=resolution,
            n_processes=2,
            n_max=iterations,
            boundries=(
                (center_x - half_width, center_x + half_width),
                (center_y - half_height, center_y + half_height),
            ),
        )
        image = self.to_image(values)
        output = BytesIO()
        image.save(output, format="PNG")
        body = output.getvalue()

        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    @staticmethod
    def get_int(query, name, default, minimum, maximum):
        try:
            value = int(query.get(name, [default])[0])
        except (TypeError, ValueError):
            value = default
        return max(minimum, min(value, maximum))

    @staticmethod
    def get_float(query, name, default, minimum, maximum):
        try:
            value = float(query.get(name, [default])[0])
        except (TypeError, ValueError):
            value = default
        return max(minimum, min(value, maximum))

    @staticmethod
    def to_image(values):
        inside = values > values.max() - 1
        pixels = np.where(inside, 0, 255).astype(np.uint8)
        return Image.fromarray(pixels, mode="L")

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}", flush=True)

if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8000), ServiceHandler)
    print("Application listening on port 8000", flush=True)
    server.serve_forever()