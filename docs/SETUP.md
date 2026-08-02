# Setup checklist

This is the short version to share with a professor or reviewer.

## 1. Install dependencies

```bash
make setup
```

## 2. Start the API

```bash
make api
```

Expected address: `http://127.0.0.1:8000`.

Check it in a browser at `/docs` or with:

```bash
curl http://127.0.0.1:8000/api/health
```

## 3. Start the web app

In another terminal:

```bash
make web
```

Expected address: `http://127.0.0.1:5173`.

## 4. Test the prototype

1. Keep `OpenCV Haar` selected for the first run.
2. Upload a consented JPG or PNG.
3. Choose blur, pixelation, or solid mask.
4. Run analysis.
5. Use `Run all available` for a runtime comparison.
6. Open Reports and export the media-free JSON summary.

## Common setup mistakes

- White screen: the app was opened with Live Server or as a file. Use Vite.
- Upload button disabled: the browser has no selected file.
- Optional detector disabled: install its package and provide its local model as described in `models/README.md`.
- API toast in the UI: start `make api` and reload the page.
