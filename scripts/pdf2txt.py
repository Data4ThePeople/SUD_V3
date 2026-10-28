"""Extract text from PDFs (untrusted input) into an output dir. Usage: pdf2txt.py OUTDIR file.pdf ..."""
import sys, os
from pypdf import PdfReader
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
for f in sys.argv[2:]:
    try:
        r = PdfReader(f)
        t = '\n'.join(f'<<p{i+1}>>\n' + (p.extract_text() or '') for i, p in enumerate(r.pages))
    except Exception as e:
        t = f'ERROR {e}'
    open(os.path.join(out, os.path.basename(f) + '.txt'), 'w').write(t)
    print(f, len(t))
