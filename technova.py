# # ORIGINAL CODE

# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import re
# import base64
# import ast

# # =============================
# # 🌌 Canvas Star Background + Neon Text
# # =============================
# def set_canvas_stars():
#     canvas_html = """
#     <canvas id="star-canvas" style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1000;"></canvas>
#     <script>
#     const canvas = document.getElementById('star-canvas');
#     const ctx = canvas.getContext('2d');
#     function resize() {
#         canvas.width = window.innerWidth;
#         canvas.height = window.innerHeight;
#     }
#     window.addEventListener('resize', resize);
#     resize();
#     const numStars = 80;
#     const stars = [];
#     for(let i=0;i<numStars;i++){
#         stars.push({
#             x: Math.random()*canvas.width,
#             y: Math.random()*canvas.height,
#             r: Math.random()*2+1,
#             dx: (Math.random()-0.5)*0.3,
#             dy: (Math.random()-0.5)*0.3,
#             alpha: Math.random()
#         });
#     }
#     function draw() {
#         ctx.fillStyle = '#0a0b1c';
#         ctx.fillRect(0,0,canvas.width,canvas.height);
#         for(let s of stars){
#             ctx.beginPath();
#             ctx.arc(s.x, s.y, s.r, 0, Math.PI*2);
#             ctx.fillStyle = "rgba(0,255,255,"+s.alpha+")";
#             ctx.fill();
#             s.x += s.dx;
#             s.y += s.dy;
#             s.alpha += (Math.random()-0.5)*0.02;
#             if(s.alpha<0)s.alpha=0;
#             if(s.alpha>1)s.alpha=1;
#             if(s.x<0)s.x=canvas.width;
#             if(s.x>canvas.width)s.x=0;
#             if(s.y<0)s.y=canvas.height;
#             if(s.y>canvas.height)s.y=0;
#         }
#         requestAnimationFrame(draw);
#     }
#     draw();
#     </script>
#     <style>
#     body, [data-testid="stAppViewContainer"] {
#         background-color: #0a0b1c;
#         color: #00f9ff;
#         font-family: 'Orbitron', 'Trebuchet MS', monospace;
#         text-shadow: 0 0 6px #00f9ff, 0 0 12px #00cfff;
#         overflow-x:hidden;
#     }
#     h1,h2,h3,h4,h5,h6 { color:#00f9ff !important; text-shadow:0 0 6px #00f9ff,0 0 12px #00cfff,0 0 24px #00aaff; }
#     p,div,span,label { color:#a0f0ff !important; text-shadow:0 0 4px #00f9ff; }
#     .stButton>button, .stDownloadButton>button {
#         background: linear-gradient(90deg, #00f0ff, #0066ff);
#         color:#02121b;
#         border-radius:10px;padding:8px 14px;
#         font-weight:700;font-family:'Orbitron', monospace;
#         box-shadow:0 8px 24px rgba(0,120,255,0.12);
#         transition: transform .15s ease, box-shadow .15s ease;
#     }
#     .stButton>button:hover, .stDownloadButton>button:hover { transform: translateY(-3px); box-shadow: 0 16px 36px rgba(0,120,255,0.2); }
#     [data-testid="stSidebar"] { background: linear-gradient(180deg, rgba(4,6,20,0.95), rgba(8,12,35,0.95)); color:#EAF9FF; }
#     pre, code { background: rgba(0,20,40,0.4); color: #00f9ff; text-shadow:0 0 4px #00f9ff; }
#     </style>
#     """
#     st.markdown(canvas_html, unsafe_allow_html=True)

# # =============================
# def safe_sentence_split(text: str):
#     pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
#     return pattern.split(text)

# def paragraph_summary(text: str, max_sentences: int = 5):
#     paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
#     summary_lines = []
#     for para in paragraphs:
#         sentences = safe_sentence_split(para)
#         if sentences:
#             summary_lines.append(sentences[0].strip())
#         if len(summary_lines) >= max_sentences:
#             break
#     return " ".join(summary_lines) if summary_lines else text

# # =============================
# def analyze_python(code: str, summary_length: int = 5):
#     report = {
#         "functions": [],
#         "classes": [],
#         "imports": [],
#         "purpose_summary": "",
#         "errors": [],
#         "warnings": [],
#         "suggestions": []
#     }

#     # Extract imports, functions, classes
#     for line in code.splitlines():
#         l = line.strip()
#         if l.startswith("def "):
#             report["functions"].append(l.split("(")[0][4:].strip())
#         elif l.startswith("class "):
#             report["classes"].append(l.split("(")[0][6:].strip())
#         elif l.startswith("import ") or l.startswith("from "):
#             report["imports"].append(l)

#     report["purpose_summary"] = paragraph_summary(" ".join(safe_sentence_split(code)), max_sentences=summary_length)

#     # Syntax checking
#     try:
#         tree = ast.parse(code)
#     except SyntaxError as e:
#         report["errors"].append(f"SyntaxError: {e.msg} at line {e.lineno}")
#         report["suggestions"].append("Check indentation, missing colons, parentheses, or quotes.")
#         return report

#     # Static runtime checks
#     defined_vars = set()
#     called_funcs = set()
#     class FuncVisitor(ast.NodeVisitor):
#         def visit_FunctionDef(self, node):
#             defined_vars.add(node.name)
#             self.generic_visit(node)
#         def visit_Call(self, node):
#             if isinstance(node.func, ast.Name):
#                 called_funcs.add(node.func.id)
#             self.generic_visit(node)
#         def visit_Assign(self, node):
#             for target in node.targets:
#                 if isinstance(target, ast.Name):
#                     defined_vars.add(target.id)
#             self.generic_visit(node)
#         def visit_BinOp(self, node):
#             if isinstance(node.op, (ast.Div, ast.Mod)):
#                 if isinstance(node.right, ast.Constant) and node.right.value == 0:
#                     report["warnings"].append(f"Possible division by zero at line {node.lineno}")
#             self.generic_visit(node)
#     FuncVisitor().visit(tree)

#     # Undefined function calls
#     for func in called_funcs:
#         if func not in defined_vars and func not in dir(__builtins__):
#             report["warnings"].append(f"Call to undefined function '{func}' detected")

#     # General suggestions
#     if not report["errors"]:
#         if report["warnings"]:
#             report["suggestions"].append("Review the warnings above and fix variable or function usage.")
#         else:
#             report["suggestions"].append("No obvious syntax or runtime issues detected. Test your logic.")

#     return report

# # =============================
# def fetch_from_url(url: str) -> str:
#     try:
#         resp = requests.get(url, timeout=12)
#         resp.raise_for_status()
#         ct = resp.headers.get("Content-Type", "")
#         if "text/plain" in ct or url.lower().endswith((".py", ".txt", ".md")):
#             return resp.text
#         if "text/html" in ct:
#             soup = BeautifulSoup(resp.text, "html.parser")
#             for s in soup(["script", "style", "noscript"]):
#                 s.extract()
#             return soup.get_text(separator="\n")
#         return resp.text
#     except Exception as e:
#         return f"❌ Error fetching URL: {str(e)}"

# # =============================
# def copy_button(label: str, text: str, key: str):
#     if text is None: text = ""
#     b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
#     html_button = f"""
#         <button onclick="navigator.clipboard.writeText(atob('{b64}'))"
#                 style="background:transparent;border:1px solid rgba(255,255,255,0.06);
#                        color: #EAF9FF;padding:8px 12px;border-radius:8px;cursor:pointer;
#                        font-weight:700;box-shadow:0 6px 18px rgba(0,120,255,0.06);">
#             📋 {label}
#         </button>
#     """
#     st.markdown(html_button, unsafe_allow_html=True)

# # =============================
# def main():
#     set_canvas_stars()
#     st.title("🌌 TechNova — Study & Code Assistant")
#     st.caption("Summarize documents, analyze Python code with smart debugging, fetch & explain URLs — neon starry UI")

#     tab1, tab2, tab3 = st.tabs(["📄 Document Summarizer", "💻 Code Analyzer", "🌐 URL Fetch & Explain"])

#     # ----------------------------
#     with tab1:
#         st.subheader("Summarize Documents")
#         text_input = st.text_area("Paste text here:", height=200)
#         uploaded_file = st.file_uploader("Or upload a document (.txt, .md)", type=["txt", "md"])
#         length = st.slider("Summary length (paragraphs)", 1, 10, 3)

#         if st.button("Summarize Document"):
#             content = ""
#             if uploaded_file:
#                 try: content = uploaded_file.read().decode("utf-8")
#                 except: content = uploaded_file.read().decode("latin-1")
#             elif text_input.strip(): content = text_input
#             if not content: st.warning("Paste text or upload a file.")
#             else:
#                 summary = paragraph_summary(content, max_sentences=length)
#                 st.markdown("### 📌 Summary")
#                 st.write(summary)
#                 copy_button("Copy Summary", summary, key="doc_copy")
#                 st.download_button("⬇️ Download Summary", summary, "document_summary.txt", mime="text/plain")

#     # ----------------------------
#     with tab2:
#         st.subheader("Analyze Python Code with Smart Debugging")
#         code_input = st.text_area("Paste Python code here:", height=220)
#         uploaded_code = st.file_uploader("Or upload a Python file (.py)", type=["py"])
#         length_code = st.slider("Summary length (sentences)", 1, 8, 3, key="code_len")

#         if st.button("Analyze Code"):
#             code_str = ""
#             if uploaded_code:
#                 try: code_str = uploaded_code.read().decode("utf-8")
#                 except: code_str = uploaded_code.read().decode("latin-1")
#             elif code_input.strip(): code_str = code_input
#             if not code_str: st.warning("Paste code or upload a Python file.")
#             else:
#                 report = analyze_python(code_str, summary_length=length_code)
#                 st.markdown("### 📊 Code Analysis Report")
#                 st.markdown("**Functions:**")
#                 st.write(", ".join(report["functions"]) if report["functions"] else "_none_")
#                 st.markdown("**Classes:**")
#                 st.write(", ".join(report["classes"]) if report["classes"] else "_none_")
#                 st.markdown("**Imports:**")
#                 if report["imports"]: 
#                     for imp in report["imports"]: st.code(imp)
#                 else: st.write("_none_")
#                 st.markdown("**Purpose summary:**"); st.write(report["purpose_summary"] or "_No summary available_")
#                 st.markdown("**Errors Detected:**")
#                 if report["errors"]: 
#                     for err in report["errors"]: st.error(err)
#                 else: st.write("_No syntax errors detected_")
#                 st.markdown("**Warnings / Runtime Issues:**")
#                 if report["warnings"]:
#                     for w in report["warnings"]: st.warning(w)
#                 else: st.write("_No obvious runtime issues detected_")
#                 st.markdown("**Debugging Suggestions:**")
#                 if report["suggestions"]:
#                     for sug in report["suggestions"]: st.info(sug)

#                 copy_button("Copy Report", str(report), key="code_copy")
#                 st.download_button("⬇️ Download Code Report", str(report), "code_analysis.txt", mime="text/plain")

#     # ----------------------------
#     with tab3:
#         st.subheader("Fetch, Summarize & Explain from URL")
#         url_input = st.text_input("Enter a URL:")

#         if st.button("Fetch & Analyze URL"):
#             if not url_input.strip(): st.warning("Please enter a valid URL.")
#             else:
#                 data = fetch_from_url(url_input.strip())
#                 if data.startswith("❌ Error"): st.error(data)
#                 else:
#                     st.markdown("### 📄 Content Preview")
#                     st.code(data[:1200] + ("..." if len(data) > 1200 else ""), language="text")
#                     is_code = url_input.strip().lower().endswith(".py") or ("def " in data or "class " in data)
#                     if is_code:
#                         st.markdown("### 💻 Code Analysis with Smart Debugging")
#                         report = analyze_python(data, summary_length=5)
#                         st.json(report)
#                         copy_button("Copy Report", str(report), key="url_code_copy")
#                         st.download_button("⬇️ Download Code Report", str(report), "url_code_analysis.txt")
#                     else:
#                         st.markdown("### 📌 Document Summary")
#                         summary = paragraph_summary(data, max_sentences=5)
#                         st.write(summary)
#                         copy_button("Copy Summary", summary, key="url_summary_copy")
#                         st.download_button("⬇️ Download Summary", summary, "url_summary.txt")

# # =============================
# if __name__ == "__main__":
#     main()















































# # technova_app.py
# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import re
# import base64
# import ast
# from collections import Counter
# import io

# # PDF extraction (PyPDF2)
# try:
#     import PyPDF2
# except Exception:
#     PyPDF2 = None

# # Page config
# st.set_page_config(page_title="Technova AI Toolkit", layout="wide")

# # ----------------------------
# # Utility: Copy button (real clipboard via JS)
# # ----------------------------
# def copy_button(text: str, label: str = "Copy", key: str = None):
#     """
#     Renders a button that copies `text` to the user's clipboard using JS.
#     key - unique identifier for the button element.
#     """
#     if text is None:
#         text = ""
#     safe_b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
#     el_id = f"copy-btn-{key}" if key else f"copy-btn-{abs(hash(text))}"
#     html = f"""
#     <button id="{el_id}" onclick="navigator.clipboard.writeText(atob('{safe_b64}'))"
#         style="background:transparent;border:1px solid rgba(255,255,255,0.06);
#                color:#EAF9FF;padding:8px 12px;border-radius:8px;cursor:pointer;
#                font-weight:700;margin-right:8px;">
#       📋 {label}
#     </button>
#     <script>
#     const btn_{el_id} = document.getElementById('{el_id}');
#     btn_{el_id}.addEventListener('click', () => {{
#       const old = btn_{el_id}.innerText;
#       btn_{el_id}.innerText = '✅ Copied';
#       setTimeout(()=>{{ btn_{el_id}.innerText = old; }}, 1400);
#     }});
#     </script>
#     """
#     st.markdown(html, unsafe_allow_html=True)

# # ----------------------------
# # Neon star background & basic styles
# # ----------------------------
# def set_canvas_stars():
#     canvas_html = """
#     <canvas id="star-canvas" style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1000;"></canvas>
#     <script>
#     const canvas = document.getElementById('star-canvas');
#     const ctx = canvas.getContext('2d');
#     function resize(){ canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
#     window.addEventListener('resize', resize);
#     resize();
#     const numStars = 80;
#     const stars = [];
#     for(let i=0;i<numStars;i++){
#       stars.push({x:Math.random()*canvas.width,y:Math.random()*canvas.height,r:Math.random()*2+1,dx:(Math.random()-0.5)*0.3,dy:(Math.random()-0.5)*0.3,alpha:Math.random()});
#     }
#     function draw(){
#       ctx.fillStyle='#0a0b1c'; ctx.fillRect(0,0,canvas.width,canvas.height);
#       for(let s of stars){
#         ctx.beginPath(); ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
#         ctx.fillStyle='rgba(0,255,255,'+s.alpha+')'; ctx.fill();
#         s.x+=s.dx; s.y+=s.dy; s.alpha+=(Math.random()-0.5)*0.02;
#         if(s.alpha<0)s.alpha=0; if(s.alpha>1)s.alpha=1;
#         if(s.x<0)s.x=canvas.width; if(s.x>canvas.width)s.x=0;
#         if(s.y<0)s.y=canvas.height; if(s.y>canvas.height)s.y=0;
#       }
#       requestAnimationFrame(draw);
#     }
#     draw();
#     </script>
#     <style>
#     body, [data-testid="stAppViewContainer"] {
#       background-color:#0a0b1c; color:#00f9ff;
#       font-family: 'Orbitron', 'Trebuchet MS', monospace;
#       text-shadow:0 0 6px #00f9ff,0 0 12px #00cfff; overflow-x:hidden;
#     }
#     .stButton>button, .stDownloadButton>button { background: linear-gradient(90deg,#00f0ff,#0066ff); color:#02121b; border-radius:10px; padding:8px 14px; font-weight:700; }
#     </style>
#     """
#     st.markdown(canvas_html, unsafe_allow_html=True)

# set_canvas_stars()
# st.title("🌌 Technova AI Toolkit")
# st.caption("Document summarizer • Code analyzer • AI vs Human scanner • URL fetcher — neon UI")

# # ----------------------------
# # Summarization helpers
# # ----------------------------
# STOPWORDS = set(
#     "a an and are as at be but by for if in into is it no not of on or such that the their then there these they this to was will with you your from our we he she his her its were been being than also can could should would may might have has had do does did done just over under more most other some any each many few those them which who whom whose where when why how".split()
# )

# def safe_sentence_split(text: str):
#     pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
#     return [s.strip() for s in pattern.split(text) if s.strip()]

# def summarize_text_advanced(text: str, max_sentences: int = 5, as_bullets: bool = False) -> str:
#     paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
#     sentences = []
#     for para in paragraphs:
#         sentences.extend(safe_sentence_split(para))
#     if not sentences:
#         return text

#     word_freq = Counter()
#     for s in sentences:
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         for w in words:
#             if w not in STOPWORDS and len(w) > 2:
#                 word_freq[w] += 1
#     if not word_freq:
#         return " ".join(sentences[:max_sentences])

#     max_freq = max(word_freq.values())
#     for w in list(word_freq.keys()):
#         word_freq[w] /= max_freq

#     scored = []
#     for idx, s in enumerate(sentences):
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         score = sum(word_freq.get(w, 0.0) for w in words)
#         length_penalty = 1.0 + 0.2 * max(0, (len(words) - 20) / 20)
#         position_boost = 1.1 if idx < 3 else 1.0
#         scored.append((score / length_penalty * position_boost, idx, s))

#     scored.sort(key=lambda x: (-x[0], x[1]))
#     top = sorted(scored[:max_sentences], key=lambda x: x[1])
#     if as_bullets:
#         return "\n".join([f"- {s}" for _, _, s in top])
#     return " ".join([s for _, _, s in top])

# # ----------------------------
# # Code analyzer (AST) with fixes
# # ----------------------------
# def analyze_python(code: str):
#     report = {"functions": [], "classes": [], "imports": [], "purpose_summary": "", "errors": [], "warnings": [], "fixes": []}

#     for line in code.splitlines():
#         l = line.strip()
#         if l.startswith("def "):
#             report["functions"].append(l.split("(")[0][4:].strip())
#         elif l.startswith("class "):
#             report["classes"].append(l.split("(")[0][6:].strip().rstrip(":"))
#         elif l.startswith("import ") or l.startswith("from "):
#             report["imports"].append(l)

#     report["purpose_summary"] = summarize_text_advanced(code, max_sentences=5)

#     try:
#         tree = ast.parse(code)
#     except SyntaxError as e:
#         report["errors"].append(f"SyntaxError: {e.msg} at line {e.lineno}")
#         report["fixes"].append("Check indentation, missing colons, parentheses, or quotes.")
#         return report

#     imported_names = set()
#     used_names = set()
#     assigned_names = set()
#     function_defs = []
#     class_defs = []

#     class Analyzer(ast.NodeVisitor):
#         def visit_Import(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name.split(".")[0])
#             self.generic_visit(node)

#         def visit_ImportFrom(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name)
#             self.generic_visit(node)

#         def visit_FunctionDef(self, node):
#             function_defs.append(node)
#             assigned_names.add(node.name)
#             for default in node.args.defaults:
#                 if isinstance(default, (ast.List, ast.Dict, ast.Set)):
#                     report["warnings"].append(f"Mutable default argument in function '{node.name}' at line {node.lineno}")
#                     report["fixes"].append(f"Use None as default for mutable types in '{node.name}' and create new objects inside the function.")
#             self.generic_visit(node)

#         def visit_ClassDef(self, node):
#             class_defs.append(node)
#             assigned_names.add(node.name)
#             self.generic_visit(node)

#         def visit_Name(self, node):
#             if isinstance(node.ctx, ast.Load):
#                 used_names.add(node.id)
#             if isinstance(node.ctx, ast.Store):
#                 assigned_names.add(node.id)
#             self.generic_visit(node)

#         def visit_Call(self, node):
#             if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
#                 report["warnings"].append(f"Use of {node.func.id} detected at line {node.lineno}")
#                 report["fixes"].append(f"Avoid {node.func.id}; consider safer alternatives or explicit parsing.")
#             self.generic_visit(node)

#         def visit_ExceptHandler(self, node):
#             if node.type is None:
#                 report["warnings"].append(f"Bare except detected at line {node.lineno}")
#                 report["fixes"].append("Catch specific exception classes instead of a bare except.")
#             elif isinstance(node.type, ast.Name) and node.type.id in {"Exception", "BaseException"}:
#                 report["warnings"].append(f"Overly broad exception handler '{node.type.id}' at line {node.lineno}")
#                 report["fixes"].append("Catch the narrowest relevant exception type.")
#             if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
#                 report["warnings"].append(f"Exception swallowed with pass at line {node.lineno}")
#                 report["fixes"].append("Handle the exception or log it; avoid silent failures.")
#             self.generic_visit(node)

#     Analyzer().visit(tree)

#     for name in sorted(imported_names):
#         if name not in used_names and name not in {"__future__"}:
#             report["warnings"].append(f"Possibly unused import '{name}'")
#             report["fixes"].append(f"Remove the unused import '{name}'.")

#     for name in assigned_names:
#         if name in dir(__builtins__):
#             report["warnings"].append(f"Variable or function '{name}' shadows built-in")
#             report["fixes"].append(f"Rename '{name}' to avoid shadowing built-ins.")

#     # Simple unreachable code detection
#     for fn in function_defs:
#         seen_terminator = False
#         for node in fn.body:
#             if seen_terminator:
#                 report["warnings"].append(f"Unreachable code in function '{fn.name}' after a return/raise at line {getattr(node, 'lineno', '?')}")
#                 report["fixes"].append(f"Remove or refactor unreachable code in '{fn.name}'.")
#                 break
#             if isinstance(node, (ast.Return, ast.Raise)):
#                 seen_terminator = True

#     # Docstrings
#     if ast.get_docstring(tree) is None:
#         report["warnings"].append("Module is missing a top-level docstring")
#         report["fixes"].append("Add a brief module docstring describing purpose and usage.")
#     for fn in function_defs:
#         if ast.get_docstring(fn) is None:
#             report["warnings"].append(f"Function '{fn.name}' missing a docstring")
#             report["fixes"].append(f"Add a concise docstring for '{fn.name}'.")
#     for cl in class_defs:
#         if ast.get_docstring(cl) is None:
#             report["warnings"].append(f"Class '{cl.name}' missing a docstring")
#             report["fixes"].append(f"Add a concise docstring for class '{cl.name}'.")

#     # Undefined function calls (simple)
#     defined = {fn.name for fn in function_defs} | {cl.name for cl in class_defs}
#     called = set()
#     class CallVisitor(ast.NodeVisitor):
#         def visit_Call(self, node):
#             if isinstance(node.func, ast.Name):
#                 called.add(node.func.id)
#             self.generic_visit(node)
#     CallVisitor().visit(tree)
#     for func in sorted(called):
#         if func not in defined and func not in dir(__builtins__):
#             report["warnings"].append(f"Call to undefined function '{func}' detected")
#             report["fixes"].append(f"Define '{func}' or import it before use.")

#     if not report["errors"]:
#         if report["warnings"]:
#             report["fixes"].append("Review warnings and apply the proposed fixes.")
#         else:
#             report["fixes"].append("No obvious issues; add tests and run linters for confidence.")

#     return report

# # ----------------------------
# # Heuristic AI detector (works for text/code)
# # ----------------------------
# def detect_ai_generated_code(code: str) -> dict:
#     lines = [ln for ln in code.splitlines()]
#     code_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
#     comment_lines = [ln for ln in lines if ln.strip().startswith("#")]
#     features = {}
#     total = max(1, len(lines))
#     features["comment_density"] = len(comment_lines) / total
#     normalized = [re.sub(r"\s+", " ", ln.strip()) for ln in code_lines]
#     counts = Counter(normalized)
#     repeated = sum(c for c in counts.values() if c > 1)
#     features["repeated_line_ratio"] = repeated / max(1, len(code_lines))
#     docstring_like = re.findall(r'\"\"\"(.*?)\"\"\"|\'\'\'(.*?)\'\'\'', code, flags=re.S)
#     docstrings = [d[0] or d[1] for d in docstring_like]
#     templated_docs = sum(1 for d in docstrings if re.match(r"(?i)\s*(this function|returns|parameters)\b", d.strip()))
#     features["templated_doc_ratio"] = (templated_docs / max(1, len(docstrings))) if docstrings else 0.0
#     generic_names = {"data", "result", "results", "temp", "value", "values", "item", "items", "input", "output", "res"}
#     tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code)
#     generic_count = sum(1 for t in tokens if t in generic_names)
#     features["generic_name_density"] = generic_count / max(1, len(tokens)) if tokens else 0.0
#     words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", code)]
#     trigrams = [tuple(words[i:i+3]) for i in range(len(words) - 2)]
#     trigram_counts = Counter(trigrams)
#     repeating_trigram_ratio = sum(1 for c in trigram_counts.values() if c > 1) / max(1, len(trigram_counts)) if trigram_counts else 0.0
#     features["repeating_trigram_ratio"] = repeating_trigram_ratio
#     score = (
#         35 * features["repeating_trigram_ratio"]
#         + 20 * min(1.0, abs(features["comment_density"] - 0.15) / 0.15)
#         + 20 * features["repeated_line_ratio"]
#         + 15 * features["templated_doc_ratio"]
#         + 10 * min(1.0, features["generic_name_density"] * 20)
#     )
#     score = max(0.0, min(100.0, score))
#     if score >= 65:
#         label = "Likely AI-generated"
#     elif score >= 45:
#         label = "Unclear / Mixed"
#     else:
#         label = "Likely human-written"
#     reasons = []
#     if features["repeating_trigram_ratio"] > 0.08:
#         reasons.append("High repeated phrasing patterns.")
#     if features["repeated_line_ratio"] > 0.06:
#         reasons.append("Notable repetition of similar lines.")
#     if features["templated_doc_ratio"] > 0.4:
#         reasons.append("Docstrings appear templated.")
#     if features["comment_density"] < 0.03 or features["comment_density"] > 0.4:
#         reasons.append("Atypical comment density.")
#     if features["generic_name_density"] > 0.02:
#         reasons.append("Frequent use of generic variable names.")
#     return {"score": round(score, 1), "label": label, "reasons": reasons, "features": features}

# # ----------------------------
# # Fetch from URL
# # ----------------------------
# def fetch_from_url(url: str) -> str:
#     try:
#         resp = requests.get(url, timeout=12)
#         resp.raise_for_status()
#         ct = resp.headers.get("Content-Type", "")
#         if "text/html" in ct:
#             soup = BeautifulSoup(resp.text, "html.parser")
#             for s in soup(["script", "style", "noscript"]):
#                 s.extract()
#             return soup.get_text(separator="\n")
#         return resp.text
#     except Exception as e:
#         return f"❌ Error fetching URL: {str(e)}"

# # ----------------------------
# # Tabs (unique keys for all widgets)
# # ----------------------------
# tabs = st.tabs(["Document Summarizer", "Code Analyzer", "AI vs Human Scanner", "URL Fetch & Explain"])

# # Document Summarizer tab
# with tabs[0]:
#     st.header("📄 Document Summarizer")
#     doc_text = st.text_area("Paste text", key="doc_text_input")
#     doc_file = st.file_uploader("Upload a file (.txt, .md, .pdf)", type=["txt", "md", "pdf"], key="doc_file_upload")
#     doc_url = st.text_input("Or enter URL to fetch content", key="doc_url_input")
#     doc_len = st.slider("Summary length (sentences)", 1, 12, 5, key="doc_summary_len")
#     doc_bullets = st.checkbox("Return bullets", value=False, key="doc_as_bullets")

#     if st.button("Summarize Document", key="doc_summarize_btn"):
#         content = ""
#         if doc_file:
#             fn = getattr(doc_file, "name", "")
#             if fn.lower().endswith(".pdf"):
#                 if PyPDF2 is None:
#                     st.error("PDF support requires PyPDF2. Install it with 'pip install PyPDF2'.")
#                 else:
#                     try:
#                         reader = PyPDF2.PdfReader(io.BytesIO(doc_file.read()))
#                         pages_text = []
#                         for p in reader.pages:
#                             pages_text.append(p.extract_text() or "")
#                         content = "\n".join(pages_text)
#                     except Exception as e:
#                         st.error(f"Failed to extract PDF text: {e}")
#                         content = ""
#             else:
#                 try:
#                     content = doc_file.read().decode("utf-8", errors="ignore")
#                 except Exception:
#                     content = doc_file.read().decode("latin-1", errors="ignore")
#         elif doc_url.strip():
#             content = fetch_from_url(doc_url.strip())
#         elif doc_text.strip():
#             content = doc_text

#         if not content:
#             st.warning("Please paste text, upload a file, or enter a URL.")
#         else:
#             summary = summarize_text_advanced(content, max_sentences=doc_len, as_bullets=doc_bullets)
#             with st.expander("📂 Summary (click to expand)", expanded=True):
#                 if doc_bullets:
#                     st.markdown(summary)
#                 else:
#                     st.write(summary)
#                 # copy + download
#                 copy_button(summary, label="Copy Summary", key="doc_summary_copy")
#                 st.download_button("⬇ Download Summary", summary.encode("utf-8"), "document_summary.txt", key="doc_summary_download")

# # Code Analyzer tab
# with tabs[1]:
#     st.header("💻 Code Analyzer")
#     code_text = st.text_area("Paste Python code", key="code_text_input")
#     code_file = st.file_uploader("Upload Python file (.py)", type=["py"], key="code_file_upload")
#     code_url = st.text_input("Or enter URL to fetch code", key="code_url_input")
#     code_len = st.slider("Purpose summary length (items)", 1, 8, 4, key="code_summary_len")

#     if st.button("Analyze Code", key="code_analyze_btn"):
#         code_str = ""
#         if code_file:
#             try:
#                 code_str = code_file.read().decode("utf-8", errors="ignore")
#             except Exception:
#                 code_str = code_file.read().decode("latin-1", errors="ignore")
#         elif code_url.strip():
#             code_str = fetch_from_url(code_url.strip())
#         elif code_text.strip():
#             code_str = code_text

#         if not code_str:
#             st.warning("Please paste code, upload a file, or enter a URL.")
#         else:
#             # show syntax highlighted preview
#             with st.expander("💻 Code Preview (syntax-highlighted)", expanded=False):
#                 st.code(code_str, language="python")

#             report = analyze_python(code_str)

#             with st.expander("📂 Code Purpose Summary", expanded=True):
#                 st.write(report["purpose_summary"])
#                 copy_button(report["purpose_summary"], label="Copy Summary", key="code_purpose_copy")
#                 st.download_button("⬇ Download Purpose Summary", report["purpose_summary"].encode("utf-8"), "code_purpose.txt", key="code_purpose_download")

#             with st.expander("❌ Errors"):
#                 if report["errors"]:
#                     for e in report["errors"]:
#                         st.error(e)
#                 else:
#                     st.write("_No syntax errors detected_")

#             with st.expander("⚠️ Warnings"):
#                 if report["warnings"]:
#                     for w in report["warnings"]:
#                         st.warning(w)
#                 else:
#                     st.write("_No warnings detected_")

#             with st.expander("💡 Fixes & Recommendations"):
#                 if report["fixes"]:
#                     for f in report["fixes"]:
#                         st.info(f)
#                 else:
#                     st.write("_No fixes suggested_")

#             copy_button(str(report), label="Copy Full Report", key="code_full_report_copy")
#             st.download_button("⬇ Download Full Report", str(report).encode("utf-8"), "code_analysis_report.txt", key="code_full_report_download")

# # AI vs Human Scanner tab
# with tabs[2]:
#     st.header("🤖 AI vs Human Scanner")
#     ai_text = st.text_area("Paste text or code", key="ai_text_input")
#     ai_file = st.file_uploader("Upload file (.txt, .md, .py, .pdf)", type=["txt", "md", "py", "pdf"], key="ai_file_upload")
#     ai_url = st.text_input("Or enter URL to fetch content", key="ai_url_input")
#     ai_mode = st.radio("Content type", ["Auto-detect", "Treat as Text", "Treat as Code"], index=0, key="ai_mode_radio")

#     if st.button("Detect AI / Human Likelihood", key="ai_detect_btn"):
#         content = ""
#         if ai_file:
#             fn = getattr(ai_file, "name", "")
#             if fn.lower().endswith(".pdf"):
#                 if PyPDF2 is None:
#                     st.error("PDF support requires PyPDF2. Install it with 'pip install PyPDF2'.")
#                 else:
#                     try:
#                         reader = PyPDF2.PdfReader(io.BytesIO(ai_file.read()))
#                         pages_text = []
#                         for p in reader.pages:
#                             pages_text.append(p.extract_text() or "")
#                         content = "\n".join(pages_text)
#                     except Exception as e:
#                         st.error(f"Failed to extract PDF text: {e}")
#                         content = ""
#             else:
#                 try:
#                     content = ai_file.read().decode("utf-8", errors="ignore")
#                 except Exception:
#                     content = ai_file.read().decode("latin-1", errors="ignore")
#         elif ai_url.strip():
#             content = fetch_from_url(ai_url.strip())
#         elif ai_text.strip():
#             content = ai_text

#         if not content:
#             st.warning("Please paste content, upload a file, or enter a URL.")
#         else:
#             result = detect_ai_generated_code(content)
#             header = f"📊 Likelihood: {result['label']} (Score: {result['score']}%)"
#             with st.expander(header, expanded=True):
#                 st.markdown("**Reasons / Indicators:**")
#                 if result["reasons"]:
#                     for r in result["reasons"]:
#                         st.markdown(f"- {r}")
#                 else:
#                     st.markdown("- _No strong heuristics triggered_")
#                 st.markdown("**Detailed Features:**")
#                 for k, v in result["features"].items():
#                     st.markdown(f"- {k}: {v}")

#                 copy_button(str(result), label="Copy AI Result", key="ai_result_copy")
#                 st.download_button("⬇ Download AI Result", str(result).encode("utf-8"), "ai_result.txt", key="ai_result_download")

# # URL Fetch & Explain tab
# with tabs[3]:
#     st.header("🌐 URL Fetch & Explain")
#     url_input = st.text_input("Enter any URL to fetch content", key="url_fetch_input")
#     url_len = st.slider("Summary length (sentences)", 1, 12, 6, key="url_summary_len")
#     url_bullets = st.checkbox("Return bullets", value=True, key="url_as_bullets")

#     if st.button("Fetch & Explain", key="url_fetch_btn"):
#         if not url_input.strip():
#             st.warning("Enter a valid URL.")
#         else:
#             content = fetch_from_url(url_input.strip())
#             if content.startswith("❌ Error"):
#                 st.error(content)
#             else:
#                 with st.expander("📄 Content Preview", expanded=False):
#                     st.code(content[:4000] + ("..." if len(content) > 4000 else ""), language="text")
#                 summary = summarize_text_advanced(content, max_sentences=url_len, as_bullets=url_bullets)
#                 with st.expander("📂 Summary", expanded=True):
#                     if url_bullets:
#                         st.markdown(summary)
#                     else:
#                         st.write(summary)
#                     copy_button(summary, label="Copy Summary", key="url_summary_copy")
#                     st.download_button("⬇ Download Summary", summary.encode("utf-8"), "url_summary.txt", key="url_summary_download")




































# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import re
# import base64
# import ast
# from collections import Counter
# import io

# # PDF extraction (optional)
# try:
#     import PyPDF2
#     PDF_AVAILABLE = True
# except ImportError:
#     PDF_AVAILABLE = False

# # Page config
# st.set_page_config(
#     page_title="Technova AI Nexus", 
#     layout="wide", 
#     initial_sidebar_state="collapsed"
# )

# # Enhanced copy button
# def copy_button(text: str, label: str = "Copy", key: str = None):
#     """Enhanced copy button with styling"""
#     if text is None:
#         text = ""
#     safe_b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
#     el_id = f"copy-btn-{key}" if key else f"copy-btn-{abs(hash(text))}"
    
#     html = f"""
#     <button id="{el_id}" onclick="navigator.clipboard.writeText(atob('{safe_b64}'))"
#         style="
#             background: linear-gradient(135deg, rgba(0, 249, 255, 0.1), rgba(0, 153, 204, 0.2));
#             border: 1px solid rgba(0, 249, 255, 0.4);
#             color: #00f9ff;
#             padding: 8px 16px;
#             border-radius: 8px;
#             font-family: monospace;
#             font-weight: bold;
#             cursor: pointer;
#             margin: 5px;
#             transition: all 0.3s ease;
#         "
#         onmouseover="this.style.background='linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3))'"
#         onmouseout="this.style.background='linear-gradient(135deg, rgba(0, 249, 255, 0.1), rgba(0, 153, 204, 0.2))'">
#         ⚡ {label}
#     </button>
#     <script>
#     document.getElementById('{el_id}').addEventListener('click', function() {{
#         const btn = this;
#         const oldText = btn.innerHTML;
#         btn.innerHTML = '✅ Copied!';
#         btn.style.background = 'linear-gradient(135deg, rgba(0, 255, 0, 0.2), rgba(0, 200, 0, 0.3))';
#         setTimeout(() => {{
#             btn.innerHTML = oldText;
#             btn.style.background = 'linear-gradient(135deg, rgba(0, 249, 255, 0.1), rgba(0, 153, 204, 0.2))';
#         }}, 1500);
#     }});
#     </script>
#     """
#     st.markdown(html, unsafe_allow_html=True)

# # Simplified styling
# def set_tech_styling():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;500&display=swap');
    
#     .stApp {
#         background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
#         color: #00f9ff;
#         font-family: 'Rajdhani', sans-serif;
#     }
    
#     h1, h2, h3, h4, h5, h6 {
#         font-family: 'Orbitron', monospace !important;
#         color: #00f9ff !important;
#         text-shadow: 0 0 10px rgba(0, 249, 255, 0.5);
#     }
    
#     .main-title {
#         font-size: 3rem;
#         text-align: center;
#         background: linear-gradient(45deg, #00f9ff, #0099cc, #66ccff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         margin: 2rem 0;
#     }
    
#     .subtitle {
#         text-align: center;
#         color: rgba(0, 249, 255, 0.8);
#         font-style: italic;
#         margin-bottom: 2rem;
#     }
    
#     .stTextArea textarea, .stTextInput input {
#         background: rgba(0, 20, 40, 0.8) !important;
#         border: 1px solid rgba(0, 249, 255, 0.3) !important;
#         color: #00f9ff !important;
#     }
    
#     .stButton > button {
#         background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3)) !important;
#         border: 1px solid rgba(0, 249, 255, 0.5) !important;
#         color: #00f9ff !important;
#         font-weight: bold !important;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         color: #00f9ff !important;
#         font-family: 'Orbitron', monospace !important;
#     }
    
#     .stExpander {
#         border: 1px solid rgba(0, 249, 255, 0.3);
#         border-radius: 10px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Initialize styling
# set_tech_styling()

# # Main title
# st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
# st.markdown('<p class="subtitle">Advanced AI-Powered Analysis Suite</p>', unsafe_allow_html=True)

# # Stopwords for summarization
# STOPWORDS = set([
#     "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", 
#     "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", 
#     "there", "these", "they", "this", "to", "was", "will", "with", "you", "your", "from", 
#     "our", "we", "he", "she", "his", "her", "its", "were", "been", "being", "than", 
#     "also", "can", "could", "should", "would", "may", "might", "have", "has", "had", 
#     "do", "does", "did", "done", "just", "over", "under", "more", "most", "other", 
#     "some", "any", "each", "many", "few", "those", "them", "which", "who", "whom", 
#     "whose", "where", "when", "why", "how"
# ])

# def safe_sentence_split(text: str):
#     """Split text into sentences safely"""
#     pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
#     return [s.strip() for s in pattern.split(text) if s.strip()]

# def summarize_text_advanced(text: str, max_sentences: int = 5, as_bullets: bool = False) -> str:
#     """Advanced text summarization using frequency analysis"""
#     if not text or not text.strip():
#         return "No content to summarize."
    
#     paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
#     sentences = []
#     for para in paragraphs:
#         sentences.extend(safe_sentence_split(para))
    
#     if not sentences:
#         return text

#     # Word frequency analysis
#     word_freq = Counter()
#     for s in sentences:
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         for w in words:
#             if w not in STOPWORDS and len(w) > 2:
#                 word_freq[w] += 1
    
#     if not word_freq:
#         return " ".join(sentences[:max_sentences])

#     # Normalize frequencies
#     max_freq = max(word_freq.values())
#     for w in list(word_freq.keys()):
#         word_freq[w] /= max_freq

#     # Score sentences
#     scored = []
#     for idx, s in enumerate(sentences):
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         score = sum(word_freq.get(w, 0.0) for w in words)
#         length_penalty = 1.0 + 0.2 * max(0, (len(words) - 20) / 20)
#         position_boost = 1.1 if idx < 3 else 1.0
#         scored.append((score / length_penalty * position_boost, idx, s))

#     # Select top sentences
#     scored.sort(key=lambda x: (-x[0], x[1]))
#     top = sorted(scored[:max_sentences], key=lambda x: x[1])
    
#     if as_bullets:
#         return "\n".join([f"• {s}" for _, _, s in top])
#     return " ".join([s for _, _, s in top])

# def analyze_python(code: str):
#     """Comprehensive Python code analysis"""
#     report = {
#         "functions": [], 
#         "classes": [], 
#         "imports": [], 
#         "purpose_summary": "", 
#         "errors": [], 
#         "warnings": [], 
#         "fixes": []
#     }

#     # Basic parsing
#     for line in code.splitlines():
#         l = line.strip()
#         if l.startswith("def "):
#             func_name = l.split("(")[0][4:].strip()
#             report["functions"].append(func_name)
#         elif l.startswith("class "):
#             class_name = l.split("(")[0][6:].strip().rstrip(":")
#             report["classes"].append(class_name)
#         elif l.startswith("import ") or l.startswith("from "):
#             report["imports"].append(l)

#     # Generate purpose summary
#     report["purpose_summary"] = summarize_text_advanced(code, max_sentences=3)

#     # AST analysis for deeper insights
#     try:
#         tree = ast.parse(code)
#     except SyntaxError as e:
#         report["errors"].append(f"SyntaxError: {e.msg} at line {e.lineno}")
#         report["fixes"].append("Check syntax: indentation, colons, parentheses, quotes.")
#         return report

#     # Analyze AST
#     imported_names = set()
#     used_names = set()
#     assigned_names = set()

#     class CodeAnalyzer(ast.NodeVisitor):
#         def visit_Import(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name.split(".")[0])
#             self.generic_visit(node)

#         def visit_ImportFrom(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name)
#             self.generic_visit(node)

#         def visit_FunctionDef(self, node):
#             assigned_names.add(node.name)
#             # Check for mutable default arguments
#             for default in node.args.defaults:
#                 if isinstance(default, (ast.List, ast.Dict, ast.Set)):
#                     report["warnings"].append(f"Mutable default argument in '{node.name}'")
#                     report["fixes"].append(f"Use None as default in '{node.name}' and create objects inside function")
#             self.generic_visit(node)

#         def visit_ClassDef(self, node):
#             assigned_names.add(node.name)
#             self.generic_visit(node)

#         def visit_Name(self, node):
#             if isinstance(node.ctx, ast.Load):
#                 used_names.add(node.id)
#             elif isinstance(node.ctx, ast.Store):
#                 assigned_names.add(node.id)
#             self.generic_visit(node)

#         def visit_Call(self, node):
#             if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
#                 report["warnings"].append(f"Dangerous {node.func.id} usage detected")
#                 report["fixes"].append(f"Avoid {node.func.id}; use safer alternatives")
#             self.generic_visit(node)

#     CodeAnalyzer().visit(tree)

#     # Check for unused imports
#     for name in sorted(imported_names):
#         if name not in used_names and name not in {"__future__"}:
#             report["warnings"].append(f"Possibly unused import: '{name}'")
#             report["fixes"].append(f"Remove unused import '{name}'")

#     # Check for builtin shadowing
#     builtins_list = [
#         'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir', 'enumerate', 
#         'filter', 'float', 'format', 'frozenset', 'hash', 'hex', 'id', 'input', 
#         'int', 'isinstance', 'len', 'list', 'map', 'max', 'min', 'next', 'oct', 
#         'open', 'ord', 'pow', 'print', 'range', 'repr', 'reversed', 'round', 
#         'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
#     ]
    
#     for name in assigned_names:
#         if name in builtins_list:
#             report["warnings"].append(f"Variable '{name}' shadows builtin")
#             report["fixes"].append(f"Rename '{name}' to avoid shadowing builtins")

#     # Add general recommendations
#     if not report["errors"]:
#         if not report["warnings"]:
#             report["fixes"].append("Code looks good! Consider adding tests and documentation.")
#         else:
#             report["fixes"].append("Review warnings above and apply suggested fixes.")

#     return report

# def detect_ai_generated_code(code: str) -> dict:
#     """Detect if code might be AI-generated based on patterns"""
#     if not code or not code.strip():
#         return {"score": 0, "label": "❓ No content", "reasons": [], "features": {}}
    
#     lines = code.splitlines()
#     code_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
#     comment_lines = [ln for ln in lines if ln.strip().startswith("#")]
    
#     features = {}
#     total_lines = max(1, len(lines))
    
#     # Comment density
#     features["comment_density"] = len(comment_lines) / total_lines
    
#     # Repeated lines
#     normalized = [re.sub(r"\s+", " ", ln.strip()) for ln in code_lines]
#     counts = Counter(normalized)
#     repeated = sum(c for c in counts.values() if c > 1)
#     features["repeated_line_ratio"] = repeated / max(1, len(code_lines))
    
#     # Generic variable names
#     generic_names = {"data", "result", "temp", "value", "item", "input", "output", "res"}
#     tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code)
#     generic_count = sum(1 for t in tokens if t in generic_names)
#     features["generic_name_density"] = generic_count / max(1, len(tokens))
    
#     # Calculate score
#     score = (
#         25 * min(1.0, abs(features["comment_density"] - 0.15) / 0.15) +
#         35 * features["repeated_line_ratio"] +
#         20 * min(1.0, features["generic_name_density"] * 20) +
#         20 * (1.0 if len(code_lines) > 50 and features["comment_density"] < 0.05 else 0.0)
#     )
    
#     score = max(0.0, min(100.0, score))
    
#     # Determine label
#     if score >= 70:
#         label = "🚨 Likely AI-generated"
#     elif score >= 45:
#         label = "🤔 Unclear/Mixed"
#     else:
#         label = "✅ Likely human-written"
    
#     # Generate reasons
#     reasons = []
#     if features["repeated_line_ratio"] > 0.1:
#         reasons.append("High repetition of similar code patterns")
#     if features["comment_density"] < 0.02 or features["comment_density"] > 0.4:
#         reasons.append("Unusual comment density")
#     if features["generic_name_density"] > 0.03:
#         reasons.append("Frequent generic variable names")
    
#     return {
#         "score": round(score, 1), 
#         "label": label, 
#         "reasons": reasons, 
#         "features": features
#     }

# def fetch_from_url(url: str) -> str:
#     """Fetch and extract text content from URL"""
#     try:
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
#         }
#         resp = requests.get(url, timeout=10, headers=headers)
#         resp.raise_for_status()
        
#         content_type = resp.headers.get("Content-Type", "")
#         if "text/html" in content_type:
#             soup = BeautifulSoup(resp.text, "html.parser")
#             # Remove unwanted elements
#             for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
#                 element.extract()
#             return soup.get_text(separator="\n", strip=True)
#         else:
#             return resp.text
            
#     except requests.exceptions.RequestException as e:
#         return f"❌ Error fetching URL: {str(e)}"
#     except Exception as e:
#         return f"❌ Error processing content: {str(e)}"

# # Create tabs
# tabs = st.tabs([
#     "📄 Document Processor", 
#     "🧠 Code Analyzer", 
#     "🤖 AI Detection", 
#     "🌐 URL Extractor"
# ])

# # Tab 1: Document Processor
# with tabs[0]:
#     st.header("📄 Neural Document Processor")
#     st.write("*Advanced text analysis and summarization*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         doc_text = st.text_area(
#             "Input Text", 
#             height=200, 
#             placeholder="Paste your document content here...",
#             key="doc_text_input"
#         )
    
#     with col2:
#         doc_file = st.file_uploader("Upload Document", type=["txt", "md", "pdf"], key="doc_file_upload")
#         doc_url = st.text_input("Document URL", placeholder="https://...", key="doc_url_input")
#         doc_length = st.slider("Summary Length", 1, 10, 5, key="doc_summary_length")
#         doc_bullets = st.checkbox("Use Bullets", value=False, key="doc_use_bullets")

#     if st.button("🚀 Analyze Document", type="primary", key="doc_analyze_btn"):
#         content = ""
        
#         # Get content from various sources
#         if doc_file:
#             if doc_file.name.lower().endswith(".pdf"):
#                 if not PDF_AVAILABLE:
#                     st.error("PDF processing requires PyPDF2. Install with: pip install PyPDF2")
#                 else:
#                     try:
#                         reader = PyPDF2.PdfReader(io.BytesIO(doc_file.read()))
#                         pages_text = []
#                         for page in reader.pages:
#                             pages_text.append(page.extract_text() or "")
#                         content = "\n".join(pages_text)
#                     except Exception as e:
#                         st.error(f"PDF error: {e}")
#             else:
#                 content = doc_file.read().decode("utf-8", errors="ignore")
#         elif doc_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(doc_url.strip())
#         elif doc_text.strip():
#             content = doc_text

#         if not content:
#             st.warning("Please provide content via text, file, or URL.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Processing..."):
#                 summary = summarize_text_advanced(content, doc_length, doc_bullets)
            
#             st.success("Analysis Complete!")
            
#             with st.expander("📊 Results", expanded=True):
#                 st.subheader("Summary")
#                 if doc_bullets:
#                     st.markdown(summary)
#                 else:
#                     st.write(summary)
                
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     copy_button(summary, "Copy Summary", key="doc_copy_btn")
#                 with col2:
#                     st.download_button(
#                         "💾 Download", 
#                         summary, 
#                         "summary.txt",
#                         mime="text/plain",
#                         key="doc_download_btn"
#                     )

# # Tab 2: Code Analyzer
# with tabs[1]:
#     st.header("🧠 Quantum Code Analyzer")
#     st.write("*Deep code analysis and optimization recommendations*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         code_text = st.text_area(
#             "Python Code", 
#             height=250, 
#             placeholder="Paste your Python code here...",
#             key="code_text_input"
#         )
    
#     with col2:
#         code_file = st.file_uploader("Upload Python File", type=["py"], key="code_file_upload")
#         code_url = st.text_input("Code URL", placeholder="https://...", key="code_url_input")

#     if st.button("🔍 Analyze Code", type="primary", key="code_analyze_btn"):
#         code_content = ""
        
#         if code_file:
#             code_content = code_file.read().decode("utf-8", errors="ignore")
#         elif code_url.strip():
#             with st.spinner("Fetching code..."):
#                 code_content = fetch_from_url(code_url.strip())
#         elif code_text.strip():
#             code_content = code_text

#         if not code_content:
#             st.warning("Please provide code via input, file, or URL.")
#         elif code_content.startswith("❌"):
#             st.error(code_content)
#         else:
#             with st.expander("Code Preview", expanded=False):
#                 st.code(code_content, language="python")

#             with st.spinner("Analyzing..."):
#                 report = analyze_python(code_content)

#             st.success("Analysis Complete!")

#             col1, col2 = st.columns(2)
            
#             with col1:
#                 st.subheader("📋 Summary")
#                 st.write(report["purpose_summary"])
                
#                 st.subheader("❌ Errors")
#                 if report["errors"]:
#                     for error in report["errors"]:
#                         st.error(error)
#                 else:
#                     st.success("No syntax errors found!")
            
#             with col2:
#                 st.subheader("⚠️ Warnings")
#                 if report["warnings"]:
#                     for warning in report["warnings"]:
#                         st.warning(warning)
#                 else:
#                     st.success("No warnings!")
                
#                 st.subheader("💡 Recommendations")
#                 for fix in report["fixes"]:
#                     st.info(fix)
            
#             # Copy and download options
#             col3, col4 = st.columns(2)
#             with col3:
#                 copy_button(str(report), "Copy Report", key="code_copy_btn")
#             with col4:
#                 st.download_button(
#                     "💾 Download Report", 
#                     str(report), 
#                     "code_analysis.txt",
#                     mime="text/plain",
#                     key="code_download_btn"
#                 )

# # Tab 3: AI Detection
# with tabs[2]:
#     st.header("🤖 AI Detection Matrix")
#     st.write("*Pattern recognition for AI-generated content*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         ai_text = st.text_area(
#             "Content for Analysis", 
#             height=200, 
#             placeholder="Paste text or code to analyze...",
#             key="ai_text_input"
#         )
    
#     with col2:
#         ai_file = st.file_uploader("Upload File", type=["txt", "py", "md"], key="ai_file_upload")
#         ai_url = st.text_input("Content URL", placeholder="https://...", key="ai_url_input")

#     if st.button("🔬 Scan for AI Patterns", type="primary", key="ai_analyze_btn"):
#         content = ""
        
#         if ai_file:
#             content = ai_file.read().decode("utf-8", errors="ignore")
#         elif ai_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(ai_url.strip())
#         elif ai_text.strip():
#             content = ai_text

#         if not content:
#             st.warning("Please provide content for analysis.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Analyzing patterns..."):
#                 result = detect_ai_generated_code(content)
            
#             st.success("Analysis Complete!")
            
#             # Display results
#             score_color = "🟢" if result['score'] < 45 else "🟡" if result['score'] < 65 else "🔴"
            
#             with st.expander(f"{score_color} Detection Results", expanded=True):
#                 col1, col2, col3 = st.columns(3)
                
#                 with col2:
#                     st.metric(
#                         "AI Likelihood Score", 
#                         f"{result['score']}%",
#                         delta=f"{result['score'] - 50}% vs baseline"
#                     )
                
#                 st.markdown(f"**Assessment:** {result['label']}")
                
#                 if result["reasons"]:
#                     st.subheader("🔍 Key Indicators")
#                     for reason in result["reasons"]:
#                         st.write(f"• {reason}")
#                 else:
#                     st.success("No significant AI patterns detected")
                
#                 st.subheader("📊 Feature Analysis")
#                 for feature, value in result["features"].items():
#                     feature_name = feature.replace("_", " ").title()
#                     st.write(f"• {feature_name}: `{value:.3f}`")
                
#                 # Copy and download
#                 col4, col5 = st.columns(2)
#                 with col4:
#                     copy_button(str(result), "Copy Results", key="ai_copy_btn")
#                 with col5:
#                     st.download_button(
#                         "💾 Download Analysis", 
#                         str(result), 
#                         "ai_detection.txt",
#                         mime="text/plain",
#                         key="ai_download_btn"
#                     )

# # Tab 4: URL Extractor
# with tabs[3]:
#     st.header("🌐 URL Data Extraction Engine")
#     st.write("*Advanced web content extraction and analysis*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         url_input = st.text_input(
#             "Target URL", 
#             placeholder="Enter any URL for content extraction...",
#             key="url_input_field"
#         )
    
#     with col2:
#         url_length = st.slider("Summary Length", 1, 10, 5, key="url_summary_length")
#         url_bullets = st.checkbox("Use Bullets", value=True, key="url_use_bullets")

#     if st.button("🚀 Extract & Analyze", type="primary", key="url_analyze_btn"):
#         if not url_input.strip():
#             st.warning("Please enter a valid URL.")
#         else:
#             with st.spinner("Extracting content..."):
#                 content = fetch_from_url(url_input.strip())
            
#             if content.startswith("❌"):
#                 st.error(content)
#             else:
#                 st.success("Content extracted successfully!")
                
#                 # Show metrics
#                 col1, col2, col3 = st.columns(3)
#                 with col1:
#                     st.metric("Characters", f"{len(content):,}")
#                 with col2:
#                     st.metric("Words", f"{len(content.split()):,}")
#                 with col3:
#                     st.metric("Lines", f"{len(content.splitlines()):,}")
                
#                 # Show preview
#                 with st.expander("📄 Content Preview", expanded=False):
#                     preview = content[:2000] + "..." if len(content) > 2000 else content
#                     st.text(preview)
                
#                 # Generate summary
#                 with st.spinner("Generating summary..."):
#                     summary = summarize_text_advanced(content, url_length, url_bullets)
                
#                 st.subheader("📊 Content Summary")
#                 if url_bullets:
#                     st.markdown(summary)
#                 else:
#                     st.write(summary)
                
#                 # Copy and download
#                 col4, col5 = st.columns(2)
#                 with col4:
#                     copy_button(summary, "Copy Summary", key="url_copy_btn")
#                 with col5:
#                     st.download_button(
#                         "💾 Download Summary", 
#                         summary.encode("utf-8"), 
#                         "url_summary.txt",
#                         key="url_download_btn"
#                     )

# # Footer
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; padding: 20px; color: rgba(0, 249, 255, 0.6); font-family: monospace;">
#     🌌 TECHNOVA AI NEXUS v2.0 • Advanced Neural Processing Suite
# </div>
# """, unsafe_allow_html=True)























# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import re
# import base64
# import ast
# from collections import Counter
# import io

# # PDF extraction (optional)
# try:
#     import PyPDF2
#     PDF_AVAILABLE = True
# except ImportError:
#     PDF_AVAILABLE = False

# # Page config
# st.set_page_config(
#     page_title="Technova AI Nexus", 
#     layout="wide", 
#     initial_sidebar_state="collapsed"
# )

# # Enhanced copy button
# def copy_button(text: str, label: str = "Copy", key: str = None):
#     """Enhanced copy button with styling"""
#     if text is None:
#         text = ""
#     safe_b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
#     el_id = f"copy-btn-{key}" if key else f"copy-btn-{abs(hash(text[:100]))}"
    
#     html = f"""
#     <button id="{el_id}" onclick="navigator.clipboard.writeText(atob('{safe_b64}'))"
#         style="
#             background: linear-gradient(135deg, rgba(0, 249, 255, 0.1), rgba(0, 153, 204, 0.2));
#             border: 1px solid rgba(0, 249, 255, 0.4);
#             color: #00f9ff;
#             padding: 8px 16px;
#             border-radius: 8px;
#             font-family: monospace;
#             font-weight: bold;
#             cursor: pointer;
#             margin: 5px;
#             transition: all 0.3s ease;
#         "
#         onmouseover="this.style.background='linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3))'"
#         onmouseout="this.style.background='linear-gradient(135deg, rgba(0, 249, 255, 0.1), rgba(0, 153, 204, 0.2))'">
#         ⚡ {label}
#     </button>
#     <script>
#     document.getElementById('{el_id}').addEventListener('click', function() {{
#         const btn = this;
#         const oldText = btn.innerHTML;
#         btn.innerHTML = '✅ Copied!';
#         btn.style.background = 'linear-gradient(135deg, rgba(0, 255, 0, 0.2), rgba(0, 200, 0, 0.3))';
#         setTimeout(() => {{
#             btn.innerHTML = oldText;
#             btn.style.background = 'linear-gradient(135deg, rgba(0, 249, 255, 0.1), rgba(0, 153, 204, 0.2))';
#         }}, 1500);
#     }});
#     </script>
#     """
#     st.markdown(html, unsafe_allow_html=True)

# # Simplified styling
# def set_tech_styling():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;500&display=swap');
    
#     .stApp {
#         background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
#         color: #00f9ff;
#         font-family: 'Rajdhani', sans-serif;
#     }
    
#     h1, h2, h3, h4, h5, h6 {
#         font-family: 'Orbitron', monospace !important;
#         color: #00f9ff !important;
#         text-shadow: 0 0 10px rgba(0, 249, 255, 0.5);
#     }
    
#     .main-title {
#         font-size: 3rem;
#         text-align: center;
#         background: linear-gradient(45deg, #00f9ff, #0099cc, #66ccff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         margin: 2rem 0;
#     }
    
#     .subtitle {
#         text-align: center;
#         color: rgba(0, 249, 255, 0.8);
#         font-style: italic;
#         margin-bottom: 2rem;
#     }
    
#     .stTextArea textarea, .stTextInput input {
#         background: rgba(0, 20, 40, 0.8) !important;
#         border: 1px solid rgba(0, 249, 255, 0.3) !important;
#         color: #00f9ff !important;
#     }
    
#     .stButton > button {
#         background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3)) !important;
#         border: 1px solid rgba(0, 249, 255, 0.5) !important;
#         color: #00f9ff !important;
#         font-weight: bold !important;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         color: #00f9ff !important;
#         font-family: 'Orbitron', monospace !important;
#     }
    
#     .stExpander {
#         border: 1px solid rgba(0, 249, 255, 0.3);
#         border-radius: 10px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Initialize styling
# set_tech_styling()

# # Main title
# st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
# st.markdown('<p class="subtitle">Advanced AI-Powered Analysis Suite</p>', unsafe_allow_html=True)

# # Stopwords for summarization
# STOPWORDS = set([
#     "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", 
#     "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", 
#     "there", "these", "they", "this", "to", "was", "will", "with", "you", "your", "from", 
#     "our", "we", "he", "she", "his", "her", "its", "were", "been", "being", "than", 
#     "also", "can", "could", "should", "would", "may", "might", "have", "has", "had", 
#     "do", "does", "did", "done", "just", "over", "under", "more", "most", "other", 
#     "some", "any", "each", "many", "few", "those", "them", "which", "who", "whom", 
#     "whose", "where", "when", "why", "how"
# ])

# def safe_sentence_split(text: str):
#     """Split text into sentences safely"""
#     pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
#     return [s.strip() for s in pattern.split(text) if s.strip()]

# def summarize_text_advanced(text: str, max_sentences: int = 5, as_bullets: bool = False) -> str:
#     """Advanced text summarization using frequency analysis"""
#     if not text or not text.strip():
#         return "No content to summarize."
    
#     paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
#     sentences = []
#     for para in paragraphs:
#         sentences.extend(safe_sentence_split(para))
    
#     if not sentences:
#         return text

#     # Word frequency analysis
#     word_freq = Counter()
#     for s in sentences:
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         for w in words:
#             if w not in STOPWORDS and len(w) > 2:
#                 word_freq[w] += 1
    
#     if not word_freq:
#         return " ".join(sentences[:max_sentences])

#     # Normalize frequencies
#     max_freq = max(word_freq.values())
#     for w in list(word_freq.keys()):
#         word_freq[w] /= max_freq

#     # Score sentences
#     scored = []
#     for idx, s in enumerate(sentences):
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         score = sum(word_freq.get(w, 0.0) for w in words)
#         length_penalty = 1.0 + 0.2 * max(0, (len(words) - 20) / 20)
#         position_boost = 1.1 if idx < 3 else 1.0
#         scored.append((score / length_penalty * position_boost, idx, s))

#     # Select top sentences
#     scored.sort(key=lambda x: (-x[0], x[1]))
#     top = sorted(scored[:max_sentences], key=lambda x: x[1])
    
#     if as_bullets:
#         return "\n".join([f"• {s}" for _, _, s in top])
#     return " ".join([s for _, _, s in top])

# def analyze_python(code: str):
#     """Comprehensive Python code analysis"""
#     report = {
#         "functions": [], 
#         "classes": [], 
#         "imports": [], 
#         "purpose_summary": "", 
#         "errors": [], 
#         "warnings": [], 
#         "fixes": []
#     }

#     # Basic parsing
#     for line in code.splitlines():
#         l = line.strip()
#         if l.startswith("def "):
#             func_name = l.split("(")[0][4:].strip()
#             report["functions"].append(func_name)
#         elif l.startswith("class "):
#             class_name = l.split("(")[0][6:].strip().rstrip(":")
#             report["classes"].append(class_name)
#         elif l.startswith("import ") or l.startswith("from "):
#             report["imports"].append(l)

#     # Generate purpose summary
#     report["purpose_summary"] = summarize_text_advanced(code, max_sentences=3)

#     # AST analysis for deeper insights
#     try:
#         tree = ast.parse(code)
#     except SyntaxError as e:
#         report["errors"].append(f"SyntaxError: {e.msg} at line {e.lineno}")
#         report["fixes"].append("Check syntax: indentation, colons, parentheses, quotes.")
#         return report

#     # Analyze AST
#     imported_names = set()
#     used_names = set()
#     assigned_names = set()

#     class CodeAnalyzer(ast.NodeVisitor):
#         def visit_Import(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name.split(".")[0])
#             self.generic_visit(node)

#         def visit_ImportFrom(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name)
#             self.generic_visit(node)

#         def visit_FunctionDef(self, node):
#             assigned_names.add(node.name)
#             # Check for mutable default arguments
#             for default in node.args.defaults:
#                 if isinstance(default, (ast.List, ast.Dict, ast.Set)):
#                     report["warnings"].append(f"Mutable default argument in '{node.name}'")
#                     report["fixes"].append(f"Use None as default in '{node.name}' and create objects inside function")
#             self.generic_visit(node)

#         def visit_ClassDef(self, node):
#             assigned_names.add(node.name)
#             self.generic_visit(node)

#         def visit_Name(self, node):
#             if isinstance(node.ctx, ast.Load):
#                 used_names.add(node.id)
#             elif isinstance(node.ctx, ast.Store):
#                 assigned_names.add(node.id)
#             self.generic_visit(node)

#         def visit_Call(self, node):
#             if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
#                 report["warnings"].append(f"Dangerous {node.func.id} usage detected")
#                 report["fixes"].append(f"Avoid {node.func.id}; use safer alternatives")
#             self.generic_visit(node)

#     CodeAnalyzer().visit(tree)

#     # Check for unused imports
#     for name in sorted(imported_names):
#         if name not in used_names and name not in {"__future__"}:
#             report["warnings"].append(f"Possibly unused import: '{name}'")
#             report["fixes"].append(f"Remove unused import '{name}'")

#     # Check for builtin shadowing
#     builtins_list = [
#         'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir', 'enumerate', 
#         'filter', 'float', 'format', 'frozenset', 'hash', 'hex', 'id', 'input', 
#         'int', 'isinstance', 'len', 'list', 'map', 'max', 'min', 'next', 'oct', 
#         'open', 'ord', 'pow', 'print', 'range', 'repr', 'reversed', 'round', 
#         'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
#     ]
    
#     for name in assigned_names:
#         if name in builtins_list:
#             report["warnings"].append(f"Variable '{name}' shadows builtin")
#             report["fixes"].append(f"Rename '{name}' to avoid shadowing builtins")

#     # Add general recommendations
#     if not report["errors"]:
#         if not report["warnings"]:
#             report["fixes"].append("Code looks good! Consider adding tests and documentation.")
#         else:
#             report["fixes"].append("Review warnings above and apply suggested fixes.")

#     return report

# def detect_ai_generated_code(code: str) -> dict:
#     """Detect if code might be AI-generated based on patterns"""
#     if not code or not code.strip():
#         return {"score": 0, "label": "❓ No content", "reasons": [], "features": {}}
    
#     lines = code.splitlines()
#     code_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
#     comment_lines = [ln for ln in lines if ln.strip().startswith("#")]
    
#     features = {}
#     total_lines = max(1, len(lines))
    
#     # Comment density
#     features["comment_density"] = len(comment_lines) / total_lines
    
#     # Repeated lines
#     normalized = [re.sub(r"\s+", " ", ln.strip()) for ln in code_lines]
#     counts = Counter(normalized)
#     repeated = sum(c for c in counts.values() if c > 1)
#     features["repeated_line_ratio"] = repeated / max(1, len(code_lines))
    
#     # Generic variable names
#     generic_names = {"data", "result", "temp", "value", "item", "input", "output", "res"}
#     tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code)
#     generic_count = sum(1 for t in tokens if t in generic_names)
#     features["generic_name_density"] = generic_count / max(1, len(tokens))
    
#     # Calculate score
#     score = (
#         25 * min(1.0, abs(features["comment_density"] - 0.15) / 0.15) +
#         35 * features["repeated_line_ratio"] +
#         20 * min(1.0, features["generic_name_density"] * 20) +
#         20 * (1.0 if len(code_lines) > 50 and features["comment_density"] < 0.05 else 0.0)
#     )
    
#     score = max(0.0, min(100.0, score))
    
#     # Determine label
#     if score >= 70:
#         label = "🚨 Likely AI-generated"
#     elif score >= 45:
#         label = "🤔 Unclear/Mixed"
#     else:
#         label = "✅ Likely human-written"
    
#     # Generate reasons
#     reasons = []
#     if features["repeated_line_ratio"] > 0.1:
#         reasons.append("High repetition of similar code patterns")
#     if features["comment_density"] < 0.02 or features["comment_density"] > 0.4:
#         reasons.append("Unusual comment density")
#     if features["generic_name_density"] > 0.03:
#         reasons.append("Frequent generic variable names")
    
#     return {
#         "score": round(score, 1), 
#         "label": label, 
#         "reasons": reasons, 
#         "features": features
#     }

# def fetch_from_url(url: str) -> str:
#     """Fetch and extract text content from URL"""
#     try:
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
#         }
#         resp = requests.get(url, timeout=10, headers=headers)
#         resp.raise_for_status()
        
#         content_type = resp.headers.get("Content-Type", "")
#         if "text/html" in content_type:
#             soup = BeautifulSoup(resp.text, "html.parser")
#             # Remove unwanted elements
#             for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
#                 element.extract()
#             return soup.get_text(separator="\n", strip=True)
#         else:
#             return resp.text
            
#     except requests.exceptions.RequestException as e:
#         return f"❌ Error fetching URL: {str(e)}"
#     except Exception as e:
#         return f"❌ Error processing content: {str(e)}"

# # Create tabs
# tabs = st.tabs([
#     "📄 Document Processor", 
#     "🧠 Code Analyzer", 
#     "🤖 AI Detection", 
#     "🌐 URL Extractor"
# ])

# # Tab 1: Document Processor
# with tabs[0]:
#     st.header("📄 Neural Document Processor")
#     st.write("*Advanced text analysis and summarization*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         doc_text = st.text_area(
#             "Input Text", 
#             height=200, 
#             placeholder="Paste your document content here...",
#             key="doc_text_input"
#         )
    
#     with col2:
#         doc_file = st.file_uploader("Upload Document", type=["txt", "md", "pdf"], key="doc_file_upload")
#         doc_url = st.text_input("Document URL", placeholder="https://...", key="doc_url_input")
#         doc_length = st.slider("Summary Length", 1, 10, 5, key="doc_summary_length")
#         doc_bullets = st.checkbox("Use Bullets", value=False, key="doc_use_bullets")

#     if st.button("🚀 Analyze Document", type="primary", key="doc_analyze_btn"):
#         content = ""
        
#         # Get content from various sources
#         if doc_file:
#             if doc_file.name.lower().endswith(".pdf"):
#                 if not PDF_AVAILABLE:
#                     st.error("PDF processing requires PyPDF2. Install with: pip install PyPDF2")
#                 else:
#                     try:
#                         reader = PyPDF2.PdfReader(io.BytesIO(doc_file.read()))
#                         pages_text = []
#                         for page in reader.pages:
#                             pages_text.append(page.extract_text() or "")
#                         content = "\n".join(pages_text)
#                     except Exception as e:
#                         st.error(f"PDF error: {e}")
#             else:
#                 content = doc_file.read().decode("utf-8", errors="ignore")
#         elif doc_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(doc_url.strip())
#         elif doc_text.strip():
#             content = doc_text

#         if not content:
#             st.warning("Please provide content via text, file, or URL.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Processing..."):
#                 summary = summarize_text_advanced(content, doc_length, doc_bullets)
            
#             st.success("Analysis Complete!")
            
#             with st.expander("📊 Results", expanded=True):
#                 st.subheader("Summary")
#                 if doc_bullets:
#                     st.markdown(summary)
#                 else:
#                     st.write(summary)
                
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     copy_button(summary, "Copy Summary", key="doc_copy_btn")
#                 with col2:
#                     st.download_button(
#                         "💾 Download", 
#                         summary, 
#                         "summary.txt",
#                         mime="text/plain",
#                         key="doc_download_btn"
#                     )

# # Tab 2: Code Analyzer
# with tabs[1]:
#     st.header("🧠 Quantum Code Analyzer")
#     st.write("*Deep code analysis and optimization recommendations*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         code_text = st.text_area(
#             "Python Code", 
#             height=250, 
#             placeholder="Paste your Python code here...",
#             key="code_text_input"
#         )
    
#     with col2:
#         code_file = st.file_uploader("Upload Python File", type=["py"], key="code_file_upload")
#         code_url = st.text_input("Code URL", placeholder="https://...", key="code_url_input")

#     if st.button("🔍 Analyze Code", type="primary", key="code_analyze_btn"):
#         code_content = ""
        
#         if code_file:
#             code_content = code_file.read().decode("utf-8", errors="ignore")
#         elif code_url.strip():
#             with st.spinner("Fetching code..."):
#                 code_content = fetch_from_url(code_url.strip())
#         elif code_text.strip():
#             code_content = code_text

#         if not code_content:
#             st.warning("Please provide code via input, file, or URL.")
#         elif code_content.startswith("❌"):
#             st.error(code_content)
#         else:
#             with st.expander("Code Preview", expanded=False):
#                 st.code(code_content, language="python")

#             with st.spinner("Analyzing..."):
#                 report = analyze_python(code_content)

#             st.success("Analysis Complete!")

#             col1, col2 = st.columns(2)
            
#             with col1:
#                 st.subheader("📋 Summary")
#                 st.write(report["purpose_summary"])
                
#                 st.subheader("❌ Errors")
#                 if report["errors"]:
#                     for error in report["errors"]:
#                         st.error(error)
#                 else:
#                     st.success("No syntax errors found!")
            
#             with col2:
#                 st.subheader("⚠️ Warnings")
#                 if report["warnings"]:
#                     for warning in report["warnings"]:
#                         st.warning(warning)
#                 else:
#                     st.success("No warnings!")
                
#                 st.subheader("💡 Recommendations")
#                 for fix in report["fixes"]:
#                     st.info(fix)
            
#             # Copy and download options
#             col3, col4 = st.columns(2)
#             with col3:
#                 copy_button(str(report), "Copy Report", key="code_copy_btn")
#             with col4:
#                 st.download_button(
#                     "💾 Download Report", 
#                     str(report), 
#                     "code_analysis.txt",
#                     mime="text/plain",
#                     key="code_download_btn"
#                 )

# # Tab 3: AI Detection
# with tabs[2]:
#     st.header("🤖 AI Detection Matrix")
#     st.write("*Pattern recognition for AI-generated content*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         ai_text = st.text_area(
#             "Content for Analysis", 
#             height=200, 
#             placeholder="Paste text or code to analyze...",
#             key="ai_text_input"
#         )
    
#     with col2:
#         ai_file = st.file_uploader("Upload File", type=["txt", "py", "md"], key="ai_file_upload")
#         ai_url = st.text_input("Content URL", placeholder="https://...", key="ai_url_input")

#     if st.button("🔬 Scan for AI Patterns", type="primary", key="ai_analyze_btn"):
#         content = ""
        
#         if ai_file:
#             content = ai_file.read().decode("utf-8", errors="ignore")
#         elif ai_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(ai_url.strip())
#         elif ai_text.strip():
#             content = ai_text

#         if not content:
#             st.warning("Please provide content for analysis.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Analyzing patterns..."):
#                 result = detect_ai_generated_code(content)
            
#             st.success("Analysis Complete!")
            
#             # Display results
#             score_color = "🟢" if result['score'] < 45 else "🟡" if result['score'] < 65 else "🔴"
            
#             with st.expander(f"{score_color} Detection Results", expanded=True):
#                 col1, col2, col3 = st.columns(3)
                
#                 with col2:
#                     st.metric(
#                         "AI Likelihood Score", 
#                         f"{result['score']}%",
#                         delta=f"{result['score'] - 50}% vs baseline"
#                     )
                
#                 st.markdown(f"**Assessment:** {result['label']}")
                
#                 if result["reasons"]:
#                     st.subheader("🔍 Key Indicators")
#                     for reason in result["reasons"]:
#                         st.write(f"• {reason}")
#                 else:
#                     st.success("No significant AI patterns detected")
                
#                 st.subheader("📊 Feature Analysis")
#                 for feature, value in result["features"].items():
#                     feature_name = feature.replace("_", " ").title()
#                     st.write(f"• {feature_name}: `{value:.3f}`")
                
#                 # Copy and download
#                 col4, col5 = st.columns(2)
#                 with col4:
#                     copy_button(str(result), "Copy Results", key="ai_copy_btn")
#                 with col5:
#                     st.download_button(
#                         "💾 Download Analysis", 
#                         str(result), 
#                         "ai_detection.txt",
#                         mime="text/plain",
#                         key="ai_download_btn"
#                     )

# # Tab 4: URL Extractor
# with tabs[3]:
#     st.header("🌐 URL Data Extraction Engine")
#     st.write("*Advanced web content extraction and analysis*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         url_input = st.text_input(
#             "Target URL", 
#             placeholder="Enter any URL for content extraction...",
#             key="url_input_field"
#         )
    
#     with col2:
#         url_length = st.slider("Summary Length", 1, 10, 5, key="url_summary_length")
#         url_bullets = st.checkbox("Use Bullets", value=True, key="url_use_bullets")

#     if st.button("🚀 Extract & Analyze", type="primary", key="url_analyze_btn"):
#         if not url_input.strip():
#             st.warning("Please enter a valid URL.")
#         else:
#             with st.spinner("Extracting content..."):
#                 content = fetch_from_url(url_input.strip())
            
#             if content.startswith("❌"):
#                 st.error(content)
#             else:
#                 st.success("Content extracted successfully!")
                
#                 # Show metrics
#                 col1, col2, col3 = st.columns(3)
#                 with col1:
#                     st.metric("Characters", f"{len(content):,}")
#                 with col2:
#                     st.metric("Words", f"{len(content.split()):,}")
#                 with col3:
#                     st.metric("Lines", f"{len(content.splitlines()):,}")
                
#                 # Show preview
#                 with st.expander("📄 Content Preview", expanded=False):
#                     preview = content[:2000] + "..." if len(content) > 2000 else content
#                     st.text(preview)
                
#                 # Generate summary
#                 with st.spinner("Generating summary..."):
#                     summary = summarize_text_advanced(content, url_length, url_bullets)
                
#                 st.subheader("📊 Content Summary")
#                 if url_bullets:
#                     st.markdown(summary)
#                 else:
#                     st.write(summary)
                
#                 # Copy and download
#                 col4, col5 = st.columns(2)
#                 with col4:
#                     copy_button(summary, "Copy Summary", key="url_copy_btn")
#                 with col5:
#                     st.download_button(
#                         "💾 Download Summary", 
#                         summary, 
#                         "url_summary.txt",
#                         mime="text/plain",
#                         key="url_download_btn"
#                     )

# # Footer
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; padding: 20px; color: rgba(0, 249, 255, 0.6); font-family: monospace;">
#     🌌 TECHNOVA AI NEXUS v2.0 • Advanced Neural Processing Suite
# </div>
# """, unsafe_allow_html=True)






















# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import re
# import base64
# import ast
# from collections import Counter, defaultdict
# import io

# # PDF extraction (optional)
# try:
#     import PyPDF2
#     PDF_AVAILABLE = True
# except ImportError:
#     PDF_AVAILABLE = False

# # Page config
# st.set_page_config(
#     page_title="Technova AI Nexus", 
#     layout="wide", 
#     initial_sidebar_state="collapsed"
# )

# # Enhanced copy button with better reliability
# def copy_button(text: str, label: str = "Copy", key: str = None):
#     """Reliable copy button with fallback"""
#     if text is None:
#         text = ""
    
#     button_key = f"copy_{key}" if key else f"copy_{abs(hash(text[:100]))}"
    
#     # Create button
#     if st.button(f"⚡ {label}", key=button_key, help="Click to prepare text for copying"):
#         st.session_state[f"text_to_copy_{button_key}"] = text
#         st.success("✅ Ready to copy! Use the text area below:")
        
#     # Show text area if button was clicked
#     if f"text_to_copy_{button_key}" in st.session_state:
#         st.text_area(
#             "📋 Select all text and copy (Ctrl+A, Ctrl+C or Cmd+A, Cmd+C):",
#             value=st.session_state[f"text_to_copy_{button_key}"],
#             height=150,
#             key=f"copy_area_{button_key}",
#             help="Select all text in this box and copy it to your clipboard"
#         )

# # Simplified styling
# def set_tech_styling():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;500&display=swap');
    
#     .stApp {
#         background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
#         color: #00f9ff;
#         font-family: 'Rajdhani', sans-serif;
#     }
    
#     h1, h2, h3, h4, h5, h6 {
#         font-family: 'Orbitron', monospace !important;
#         color: #00f9ff !important;
#         text-shadow: 0 0 10px rgba(0, 249, 255, 0.5);
#     }
    
#     .main-title {
#         font-size: 3rem;
#         text-align: center;
#         background: linear-gradient(45deg, #00f9ff, #0099cc, #66ccff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         margin: 2rem 0;
#     }
    
#     .subtitle {
#         text-align: center;
#         color: rgba(0, 249, 255, 0.8);
#         font-style: italic;
#         margin-bottom: 2rem;
#     }
    
#     .metric-card {
#         background: rgba(0, 20, 40, 0.6);
#         border: 1px solid rgba(0, 249, 255, 0.3);
#         border-radius: 10px;
#         padding: 15px;
#         margin: 10px 0;
#     }
    
#     .stTextArea textarea, .stTextInput input {
#         background: rgba(0, 20, 40, 0.8) !important;
#         border: 1px solid rgba(0, 249, 255, 0.3) !important;
#         color: #00f9ff !important;
#     }
    
#     .stButton > button {
#         background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3)) !important;
#         border: 1px solid rgba(0, 249, 255, 0.5) !important;
#         color: #00f9ff !important;
#         font-weight: bold !important;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         color: #00f9ff !important;
#         font-family: 'Orbitron', monospace !important;
#     }
    
#     .stExpander {
#         border: 1px solid rgba(0, 249, 255, 0.3);
#         border-radius: 10px;
#     }
    
#     .success-metric {
#         color: #00ff00;
#         font-weight: bold;
#     }
    
#     .warning-metric {
#         color: #ffaa00;
#         font-weight: bold;
#     }
    
#     .error-metric {
#         color: #ff4444;
#         font-weight: bold;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Initialize styling
# set_tech_styling()

# # Main title
# st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
# st.markdown('<p class="subtitle">Advanced AI-Powered Analysis Suite v2.1</p>', unsafe_allow_html=True)

# # Stopwords for summarization
# STOPWORDS = set([
#     "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", 
#     "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", 
#     "there", "these", "they", "this", "to", "was", "will", "with", "you", "your", "from", 
#     "our", "we", "he", "she", "his", "her", "its", "were", "been", "being", "than", 
#     "also", "can", "could", "should", "would", "may", "might", "have", "has", "had", 
#     "do", "does", "did", "done", "just", "over", "under", "more", "most", "other", 
#     "some", "any", "each", "many", "few", "those", "them", "which", "who", "whom", 
#     "whose", "where", "when", "why", "how"
# ])

# def safe_sentence_split(text: str):
#     """Split text into sentences safely"""
#     pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
#     return [s.strip() for s in pattern.split(text) if s.strip()]

# def summarize_text_advanced(text: str, max_sentences: int = 5, as_bullets: bool = False) -> str:
#     """Advanced text summarization using frequency analysis"""
#     if not text or not text.strip():
#         return "No content to summarize."
    
#     paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
#     sentences = []
#     for para in paragraphs:
#         sentences.extend(safe_sentence_split(para))
    
#     if not sentences:
#         return text

#     # Word frequency analysis
#     word_freq = Counter()
#     for s in sentences:
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         for w in words:
#             if w not in STOPWORDS and len(w) > 2:
#                 word_freq[w] += 1
    
#     if not word_freq:
#         return " ".join(sentences[:max_sentences])

#     # Normalize frequencies
#     max_freq = max(word_freq.values())
#     for w in list(word_freq.keys()):
#         word_freq[w] /= max_freq

#     # Score sentences
#     scored = []
#     for idx, s in enumerate(sentences):
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         score = sum(word_freq.get(w, 0.0) for w in words)
#         length_penalty = 1.0 + 0.2 * max(0, (len(words) - 20) / 20)
#         position_boost = 1.1 if idx < 3 else 1.0
#         scored.append((score / length_penalty * position_boost, idx, s))

#     # Select top sentences
#     scored.sort(key=lambda x: (-x[0], x[1]))
#     top = sorted(scored[:max_sentences], key=lambda x: x[1])
    
#     if as_bullets:
#         return "\n".join([f"• {s}" for _, _, s in top])
#     return " ".join([s for _, _, s in top])

# def analyze_python_enhanced(code: str):
#     """Comprehensive Python code analysis with enhanced metrics"""
#     report = {
#         "basic_stats": {},
#         "functions": [], 
#         "classes": [], 
#         "imports": [], 
#         "variables": [],
#         "purpose_summary": "", 
#         "errors": [], 
#         "warnings": [], 
#         "fixes": [],
#         "complexity_metrics": {},
#         "code_quality": {},
#         "detailed_counts": {}
#     }

#     if not code or not code.strip():
#         return report

#     lines = code.splitlines()
#     code_lines = [line for line in lines if line.strip() and not line.strip().startswith("#")]
#     comment_lines = [line for line in lines if line.strip().startswith("#")]
#     blank_lines = [line for line in lines if not line.strip()]

#     # Basic statistics
#     report["basic_stats"] = {
#         "total_lines": len(lines),
#         "code_lines": len(code_lines),
#         "comment_lines": len(comment_lines),
#         "blank_lines": len(blank_lines),
#         "characters": len(code),
#         "words": len(code.split())
#     }

#     # Initialize counters
#     function_count = 0
#     class_count = 0
#     import_count = 0
#     print_count = 0
#     if_count = 0
#     for_count = 0
#     while_count = 0
#     try_count = 0
#     with_count = 0
#     def_count = 0
#     lambda_count = 0
#     list_comp_count = 0
#     dict_comp_count = 0

#     # Pattern-based counting
#     for line in code_lines:
#         stripped_line = line.strip()
        
#         # Count various constructs
#         if stripped_line.startswith("def "):
#             def_count += 1
#         if stripped_line.startswith("class "):
#             class_count += 1
#         if stripped_line.startswith(("import ", "from ")):
#             import_count += 1
        
#         # Count control structures and statements
#         print_count += len(re.findall(r'\bprint\s*\(', line))
#         if_count += len(re.findall(r'\bif\b', line))
#         for_count += len(re.findall(r'\bfor\b', line))
#         while_count += len(re.findall(r'\bwhile\b', line))
#         try_count += len(re.findall(r'\btry\b', line))
#         with_count += len(re.findall(r'\bwith\b', line))
#         lambda_count += len(re.findall(r'\blambda\b', line))
#         list_comp_count += len(re.findall(r'\[.*for.*in.*\]', line))
#         dict_comp_count += len(re.findall(r'\{.*for.*in.*\}', line))

#     report["detailed_counts"] = {
#         "functions": def_count,
#         "classes": class_count,
#         "imports": import_count,
#         "print_statements": print_count,
#         "if_statements": if_count,
#         "for_loops": for_count,
#         "while_loops": while_count,
#         "try_blocks": try_count,
#         "with_statements": with_count,
#         "lambda_expressions": lambda_count,
#         "list_comprehensions": list_comp_count,
#         "dict_comprehensions": dict_comp_count
#     }

#     # Calculate complexity metrics
#     total_constructs = sum([if_count, for_count, while_count, try_count, def_count])
#     complexity_score = total_constructs / max(1, len(code_lines)) * 100
    
#     report["complexity_metrics"] = {
#         "cyclomatic_complexity_estimate": total_constructs + 1,
#         "complexity_per_line": round(complexity_score, 2),
#         "nesting_level_estimate": max(0, len(re.findall(r'    ', code)) // len(code_lines) * 10) if code_lines else 0
#     }

#     # Code quality metrics
#     comment_ratio = len(comment_lines) / max(1, len(lines)) * 100
#     avg_line_length = sum(len(line) for line in code_lines) / max(1, len(code_lines))
    
#     report["code_quality"] = {
#         "comment_ratio": round(comment_ratio, 2),
#         "avg_line_length": round(avg_line_length, 2),
#         "code_to_comment_ratio": round(len(code_lines) / max(1, len(comment_lines)), 2)
#     }

#     # Basic parsing for simple analysis
#     for line in code_lines:
#         stripped = line.strip()
#         if stripped.startswith("def "):
#             match = re.match(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)", stripped)
#             if match:
#                 report["functions"].append(match.group(1))
#         elif stripped.startswith("class "):
#             match = re.match(r"class\s+([a-zA-Z_][a-zA-Z0-9_]*)", stripped)
#             if match:
#                 report["classes"].append(match.group(1))
#         elif stripped.startswith(("import ", "from ")):
#             report["imports"].append(stripped)

#     # Generate purpose summary
#     report["purpose_summary"] = summarize_text_advanced(code, max_sentences=3)

#     # AST analysis for deeper insights
#     try:
#         tree = ast.parse(code)
#     except SyntaxError as e:
#         report["errors"].append(f"SyntaxError: {e.msg} at line {e.lineno}")
#         report["fixes"].append("Check syntax: indentation, colons, parentheses, quotes.")
#         return report

#     # Enhanced AST analysis
#     imported_names = set()
#     used_names = set()
#     assigned_names = set()
#     builtin_functions_used = set()
    
#     builtin_funcs = {
#         'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir', 'enumerate', 
#         'filter', 'float', 'format', 'frozenset', 'hash', 'hex', 'id', 'input', 
#         'int', 'isinstance', 'len', 'list', 'map', 'max', 'min', 'next', 'oct', 
#         'open', 'ord', 'pow', 'print', 'range', 'repr', 'reversed', 'round', 
#         'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
#     }

#     class EnhancedCodeAnalyzer(ast.NodeVisitor):
#         def visit_Import(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name.split(".")[0])
#             self.generic_visit(node)

#         def visit_ImportFrom(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name)
#             self.generic_visit(node)

#         def visit_FunctionDef(self, node):
#             assigned_names.add(node.name)
#             # Check for mutable default arguments
#             for default in node.args.defaults:
#                 if isinstance(default, (ast.List, ast.Dict, ast.Set)):
#                     report["warnings"].append(f"Mutable default argument in '{node.name}'")
#                     report["fixes"].append(f"Use None as default in '{node.name}' and create objects inside function")
            
#             # Check for long functions
#             func_lines = len([n for n in ast.walk(node) if hasattr(n, 'lineno')])
#             if func_lines > 50:
#                 report["warnings"].append(f"Function '{node.name}' is very long ({func_lines} lines)")
#                 report["fixes"].append(f"Consider breaking down '{node.name}' into smaller functions")
            
#             self.generic_visit(node)

#         def visit_ClassDef(self, node):
#             assigned_names.add(node.name)
#             self.generic_visit(node)

#         def visit_Name(self, node):
#             if isinstance(node.ctx, ast.Load):
#                 used_names.add(node.id)
#                 if node.id in builtin_funcs:
#                     builtin_functions_used.add(node.id)
#             elif isinstance(node.ctx, ast.Store):
#                 assigned_names.add(node.id)
#                 report["variables"].append(node.id)
#             self.generic_visit(node)

#         def visit_Call(self, node):
#             if isinstance(node.func, ast.Name):
#                 if node.func.id in {"eval", "exec"}:
#                     report["warnings"].append(f"Dangerous {node.func.id} usage detected")
#                     report["fixes"].append(f"Avoid {node.func.id}; use safer alternatives")
#                 elif node.func.id == "print" and len(node.args) == 0:
#                     report["warnings"].append("Empty print() statement found")
#                     report["fixes"].append("Remove empty print() or add meaningful content")
#             self.generic_visit(node)

#     EnhancedCodeAnalyzer().visit(tree)

#     # Add builtin functions used to report
#     report["builtin_functions_used"] = sorted(list(builtin_functions_used))

#     # Check for unused imports
#     unused_imports = []
#     for name in sorted(imported_names):
#         if name not in used_names and name not in {"__future__"}:
#             unused_imports.append(name)
#             report["warnings"].append(f"Possibly unused import: '{name}'")
#             report["fixes"].append(f"Remove unused import '{name}' if not needed")

#     # Check for builtin shadowing
#     builtins_list = [
#         'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir', 'enumerate', 
#         'filter', 'float', 'format', 'frozenset', 'hash', 'hex', 'id', 'input', 
#         'int', 'isinstance', 'len', 'list', 'map', 'max', 'min', 'next', 'oct', 
#         'open', 'ord', 'pow', 'print', 'range', 'repr', 'reversed', 'round', 
#         'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
#     ]
    
#     shadowed_builtins = []
#     for name in assigned_names:
#         if name in builtins_list:
#             shadowed_builtins.append(name)
#             report["warnings"].append(f"Variable '{name}' shadows builtin")
#             report["fixes"].append(f"Rename '{name}' to avoid shadowing builtins")

#     # Code quality analysis
#     if report["code_quality"]["comment_ratio"] < 5:
#         report["warnings"].append("Low comment density - consider adding more documentation")
#         report["fixes"].append("Add docstrings to functions and classes, and inline comments for complex logic")
    
#     if report["code_quality"]["avg_line_length"] > 100:
#         report["warnings"].append("Some lines are very long - consider breaking them up")
#         report["fixes"].append("Break long lines at logical points (after commas, operators, etc.)")

#     # Add general recommendations
#     if not report["errors"]:
#         if not report["warnings"]:
#             report["fixes"].append("🎉 Code looks excellent! Consider adding unit tests and type hints.")
#         else:
#             report["fixes"].append("Review warnings above and apply suggested fixes for better code quality.")

#     # Remove duplicate variables
#     report["variables"] = sorted(list(set(report["variables"])))

#     return report

# def detect_ai_generated_code(code: str) -> dict:
#     """Detect if code might be AI-generated based on patterns"""
#     if not code or not code.strip():
#         return {"score": 0, "label": "❓ No content", "reasons": [], "features": {}}
    
#     lines = code.splitlines()
#     code_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
#     comment_lines = [ln for ln in lines if ln.strip().startswith("#")]
    
#     features = {}
#     total_lines = max(1, len(lines))
    
#     # Comment density
#     features["comment_density"] = len(comment_lines) / total_lines
    
#     # Repeated lines
#     normalized = [re.sub(r"\s+", " ", ln.strip()) for ln in code_lines]
#     counts = Counter(normalized)
#     repeated = sum(c for c in counts.values() if c > 1)
#     features["repeated_line_ratio"] = repeated / max(1, len(code_lines))
    
#     # Generic variable names
#     generic_names = {"data", "result", "temp", "value", "item", "input", "output", "res", "var", "obj"}
#     tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code)
#     generic_count = sum(1 for t in tokens if t in generic_names)
#     features["generic_name_density"] = generic_count / max(1, len(tokens))
    
#     # Perfect formatting (suspicious)
#     perfect_indent = all(len(line) - len(line.lstrip()) % 4 == 0 for line in code_lines if line.strip())
#     features["perfect_formatting"] = 1.0 if perfect_indent and len(code_lines) > 10 else 0.0
    
#     # Calculate score
#     score = (
#         25 * min(1.0, abs(features["comment_density"] - 0.15) / 0.15) +
#         35 * features["repeated_line_ratio"] +
#         20 * min(1.0, features["generic_name_density"] * 20) +
#         20 * features["perfect_formatting"]
#     )
    
#     score = max(0.0, min(100.0, score))
    
#     # Determine label
#     if score >= 70:
#         label = "🚨 Likely AI-generated"
#     elif score >= 45:
#         label = "🤔 Unclear/Mixed"
#     else:
#         label = "✅ Likely human-written"
    
#     # Generate reasons
#     reasons = []
#     if features["repeated_line_ratio"] > 0.1:
#         reasons.append("High repetition of similar code patterns")
#     if features["comment_density"] < 0.02 or features["comment_density"] > 0.4:
#         reasons.append("Unusual comment density")
#     if features["generic_name_density"] > 0.03:
#         reasons.append("Frequent generic variable names")
#     if features["perfect_formatting"] == 1.0:
#         reasons.append("Suspiciously perfect code formatting")
    
#     return {
#         "score": round(score, 1), 
#         "label": label, 
#         "reasons": reasons, 
#         "features": features
#     }

# def fetch_from_url(url: str) -> str:
#     """Fetch and extract text content from URL"""
#     try:
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
#         }
#         resp = requests.get(url, timeout=10, headers=headers)
#         resp.raise_for_status()
        
#         content_type = resp.headers.get("Content-Type", "")
#         if "text/html" in content_type:
#             soup = BeautifulSoup(resp.text, "html.parser")
#             # Remove unwanted elements
#             for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
#                 element.extract()
#             return soup.get_text(separator="\n", strip=True)
#         else:
#             return resp.text
            
#     except requests.exceptions.RequestException as e:
#         return f"❌ Error fetching URL: {str(e)}"
#     except Exception as e:
#         return f"❌ Error processing content: {str(e)}"

# # Create tabs
# tabs = st.tabs([
#     "📄 Document Processor", 
#     "🧠 Code Analyzer", 
#     "🤖 AI Detection", 
#     "🌐 URL Extractor"
# ])

# # Tab 1: Document Processor
# with tabs[0]:
#     st.header("📄 Neural Document Processor")
#     st.write("*Advanced text analysis and summarization*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         doc_text = st.text_area(
#             "Input Text", 
#             height=200, 
#             placeholder="Paste your document content here...",
#             key="doc_text_input"
#         )
    
#     with col2:
#         doc_file = st.file_uploader("Upload Document", type=["txt", "md", "pdf"], key="doc_file_upload")
#         doc_url = st.text_input("Document URL", placeholder="https://...", key="doc_url_input")
#         doc_length = st.slider("Summary Length", 1, 10, 5, key="doc_summary_length")
#         doc_bullets = st.checkbox("Use Bullets", value=False, key="doc_use_bullets")

#     if st.button("🚀 Analyze Document", type="primary", key="doc_analyze_btn"):
#         content = ""
        
#         # Get content from various sources
#         if doc_file:
#             if doc_file.name.lower().endswith(".pdf"):
#                 if not PDF_AVAILABLE:
#                     st.error("PDF processing requires PyPDF2. Install with: pip install PyPDF2")
#                 else:
#                     try:
#                         reader = PyPDF2.PdfReader(io.BytesIO(doc_file.read()))
#                         pages_text = []
#                         for page in reader.pages:
#                             pages_text.append(page.extract_text() or "")
#                         content = "\n".join(pages_text)
#                     except Exception as e:
#                         st.error(f"PDF error: {e}")
#             else:
#                 content = doc_file.read().decode("utf-8", errors="ignore")
#         elif doc_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(doc_url.strip())
#         elif doc_text.strip():
#             content = doc_text

#         if not content:
#             st.warning("Please provide content via text, file, or URL.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Processing..."):
#                 summary = summarize_text_advanced(content, doc_length, doc_bullets)
            
#             st.success("Analysis Complete!")
            
#             # Show document metrics
#             col1, col2, col3, col4 = st.columns(4)
#             with col1:
#                 st.metric("Characters", f"{len(content):,}")
#             with col2:
#                 st.metric("Words", f"{len(content.split()):,}")
#             with col3:
#                 st.metric("Lines", f"{len(content.splitlines()):,}")
#             with col4:
#                 st.metric("Paragraphs", f"{len([p for p in content.split('\\n\\n') if p.strip()]):,}")
            
#             with st.expander("📊 Summary Results", expanded=True):
#                 st.subheader("📋 Generated Summary")
#                 if doc_bullets:
#                     st.markdown(summary)
#                 else:
#                     st.write(summary)
                
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     copy_button(summary, "Copy Summary", key="doc_copy_btn")
#                 with col2:
#                     st.download_button(
#                         "💾 Download", 
#                         summary, 
#                         "summary.txt",
#                         mime="text/plain",
#                         key="doc_download_btn"
#                     )

# # Tab 2: Enhanced Code Analyzer
# with tabs[1]:
#     st.header("🧠 Quantum Code Analyzer")
#     st.write("*Deep code analysis with comprehensive metrics and optimization recommendations*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         code_text = st.text_area(
#             "Python Code", 
#             height=250, 
#             placeholder="Paste your Python code here...",
#             key="code_text_input"
#         )
    
#     with col2:
#         code_file = st.file_uploader("Upload Python File", type=["py"], key="code_file_upload")
#         code_url = st.text_input("Code URL", placeholder="https://...", key="code_url_input")

#     if st.button("🔍 Analyze Code", type="primary", key="code_analyze_btn"):
#         code_content = ""
        
#         if code_file:
#             code_content = code_file.read().decode("utf-8", errors="ignore")
#         elif code_url.strip():
#             with st.spinner("Fetching code..."):
#                 code_content = fetch_from_url(code_url.strip())
#         elif code_text.strip():
#             code_content = code_text

#         if not code_content:
#             st.warning("Please provide code via input, file, or URL.")
#         elif code_content.startswith("❌"):
#             st.error(code_content)
#         else:
#             with st.expander("Code Preview", expanded=False):
#                 st.code(code_content, language="python")

#             with st.spinner("Analyzing code..."):
#                 report = analyze_python_enhanced(code_content)

#             st.success("🎉 Analysis Complete!")

#             # Basic Statistics Section
#             st.subheader("📊 Code Statistics")
#             col1, col2, col3, col4 = st.columns(4)
            
#             with col1:
#                 st.metric("Total Lines", report["basic_stats"].get("total_lines", 0))
#                 st.metric("Functions", report["detailed_counts"].get("functions", 0))
#             with col2:
#                 st.metric("Code Lines", report["basic_stats"].get("code_lines", 0))
#                 st.metric("Classes", report["detailed_counts"].get("classes", 0))
#             with col3:
#                 st.metric("Comments", report["basic_stats"].get("comment_lines", 0))
#                 st.metric("Imports", report["detailed_counts"].get("imports", 0))
#             with col4:
#                 st.metric("Characters", f"{report['basic_stats'].get('characters', 0):,}")
#                 st.metric("Print Statements", report["detailed_counts"].get("print_statements", 0))

#             # Detailed Counts Section
#             st.subheader("🔧 Code Constructs")
#             col1, col2, col3, col4 = st.columns(4)
            
#             with col1:
#                 st.metric("If Statements", report["detailed_counts"].get("if_statements", 0))
#                 st.metric("For Loops", report["detailed_counts"].get("for_loops", 0))
#             with col2:
#                 st.metric("While Loops", report["detailed_counts"].get("while_loops", 0))
#                 st.metric("Try Blocks", report["detailed_counts"].get("try_blocks", 0))
#             with col3:
#                 st.metric("With Statements", report["detailed_counts"].get("with_statements", 0))
#                 st.metric("Lambda Expressions", report["detailed_counts"].get("lambda_expressions", 0))
#             with col4:
#                 st.metric("List Comprehensions", report["detailed_counts"].get("list_comprehensions", 0))
#                 st.metric("Dict Comprehensions", report["detailed_counts"].get("dict_comprehensions", 0))

#             # Code Quality Metrics
#             st.subheader("📈 Quality Metrics")
#             col1, col2, col3 = st.columns(3)
            
#             with col1:
#                 comment_ratio = report["code_quality"].get("comment_ratio", 0)
#                 st.metric("Comment Ratio", f"{comment_ratio:.1f}%")
                
#             with col2:
#                 avg_line_length = report["code_quality"].get("avg_line_length", 0)
#                 st.metric("Avg Line Length", f"{avg_line_length:.1f} chars")
                
#             with col3:
#                 complexity = report["complexity_metrics"].get("cyclomatic_complexity_estimate", 0)
#                 st.metric("Complexity Score", complexity)

#             # Main Analysis Results
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 st.subheader("📋 Code Summary")
#                 st.write(report["purpose_summary"])
                
#                 if report["functions"]:
#                     st.subheader("🔧 Functions Found")
#                     for func in report["functions"][:10]:  # Show first 10
#                         st.write(f"• `{func}()`")
#                     if len(report["functions"]) > 10:
#                         st.write(f"... and {len(report['functions']) - 10} more")
                
#                 if report["classes"]:
#                     st.subheader("🏗️ Classes Found")
#                     for cls in report["classes"]:
#                         st.write(f"• `{cls}`")
                
#                 if report["builtin_functions_used"]:
#                     st.subheader("🐍 Built-in Functions Used")
#                     builtin_display = ", ".join(f"`{func}()`" for func in report["builtin_functions_used"][:15])
#                     st.write(builtin_display)
#                     if len(report["builtin_functions_used"]) > 15:
#                         st.write(f"... and {len(report['builtin_functions_used']) - 15} more")
            
#             with col2:
#                 # Errors Section
#                 st.subheader("❌ Errors")
#                 if report["errors"]:
#                     for error in report["errors"]:
#                         st.error(error)
#                 else:
#                     st.success("✅ No syntax errors found!")
                
#                 # Warnings Section
#                 st.subheader("⚠️ Warnings")
#                 if report["warnings"]:
#                     for warning in report["warnings"][:8]:  # Show first 8 warnings
#                         st.warning(warning)
#                     if len(report["warnings"]) > 8:
#                         st.info(f"... and {len(report['warnings']) - 8} more warnings")
#                 else:
#                     st.success("✅ No warnings!")
                
#                 # Recommendations Section
#                 st.subheader("💡 Recommendations")
#                 for fix in report["fixes"][:6]:  # Show first 6 recommendations
#                     st.info(fix)
#                 if len(report["fixes"]) > 6:
#                     st.info(f"... and {len(report['fixes']) - 6} more recommendations")

#             # Imports and Variables
#             with st.expander("📦 Imports & Variables Details", expanded=False):
#                 col1, col2 = st.columns(2)
                
#                 with col1:
#                     if report["imports"]:
#                         st.subheader("📥 Imports")
#                         for imp in report["imports"]:
#                             st.code(imp, language="python")
#                     else:
#                         st.write("No imports found")
                
#                 with col2:
#                     if report["variables"]:
#                         st.subheader("📝 Variables")
#                         variables_display = ", ".join(f"`{var}`" for var in report["variables"][:20])
#                         st.write(variables_display)
#                         if len(report["variables"]) > 20:
#                             st.write(f"... and {len(report['variables']) - 20} more variables")
#                     else:
#                         st.write("No variables detected")
            
#             # Copy and download options
#             col3, col4 = st.columns(2)
#             with col3:
#                 # Create a formatted report for copying
#                 formatted_report = f"""
# CODE ANALYSIS REPORT
# ==================

# BASIC STATISTICS:
# - Total Lines: {report['basic_stats'].get('total_lines', 0)}
# - Code Lines: {report['basic_stats'].get('code_lines', 0)}
# - Comment Lines: {report['basic_stats'].get('comment_lines', 0)}
# - Characters: {report['basic_stats'].get('characters', 0):,}

# CODE CONSTRUCTS:
# - Functions: {report['detailed_counts'].get('functions', 0)}
# - Classes: {report['detailed_counts'].get('classes', 0)}
# - Imports: {report['detailed_counts'].get('imports', 0)}
# - Print Statements: {report['detailed_counts'].get('print_statements', 0)}
# - If Statements: {report['detailed_counts'].get('if_statements', 0)}
# - For Loops: {report['detailed_counts'].get('for_loops', 0)}
# - While Loops: {report['detailed_counts'].get('while_loops', 0)}

# QUALITY METRICS:
# - Comment Ratio: {report['code_quality'].get('comment_ratio', 0):.1f}%
# - Avg Line Length: {report['code_quality'].get('avg_line_length', 0):.1f} chars
# - Complexity Score: {report['complexity_metrics'].get('cyclomatic_complexity_estimate', 0)}

# SUMMARY: {report['purpose_summary']}

# ERRORS: {len(report['errors'])} found
# WARNINGS: {len(report['warnings'])} found
# RECOMMENDATIONS: {len(report['fixes'])} provided
# """
#                 copy_button(formatted_report, "Copy Report", key="code_copy_btn")
#             with col4:
#                 st.download_button(
#                     "💾 Download Report", 
#                     formatted_report, 
#                     "code_analysis_report.txt",
#                     mime="text/plain",
#                     key="code_download_btn"
#                 )

# # Tab 3: AI Detection
# with tabs[2]:
#     st.header("🤖 AI Detection Matrix")
#     st.write("*Advanced pattern recognition for AI-generated content*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         ai_text = st.text_area(
#             "Content for Analysis", 
#             height=200, 
#             placeholder="Paste text or code to analyze for AI patterns...",
#             key="ai_text_input"
#         )
    
#     with col2:
#         ai_file = st.file_uploader("Upload File", type=["txt", "py", "md"], key="ai_file_upload")
#         ai_url = st.text_input("Content URL", placeholder="https://...", key="ai_url_input")

#     if st.button("🔬 Scan for AI Patterns", type="primary", key="ai_analyze_btn"):
#         content = ""
        
#         if ai_file:
#             content = ai_file.read().decode("utf-8", errors="ignore")
#         elif ai_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(ai_url.strip())
#         elif ai_text.strip():
#             content = ai_text

#         if not content:
#             st.warning("Please provide content for analysis.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Analyzing patterns..."):
#                 result = detect_ai_generated_code(content)
            
#             st.success("🔍 Analysis Complete!")
            
#             # Display results with enhanced visualization
#             score_color = "🟢" if result['score'] < 45 else "🟡" if result['score'] < 65 else "🔴"
            
#             with st.expander(f"{score_color} Detection Results", expanded=True):
#                 # Main score display
#                 col1, col2, col3 = st.columns([1, 2, 1])
                
#                 with col2:
#                     # Create a visual score indicator
#                     score_val = result['score']
#                     if score_val < 45:
#                         color = "success"
#                         interpretation = "Human-like patterns detected"
#                     elif score_val < 65:
#                         color = "warning"
#                         interpretation = "Mixed or uncertain patterns"
#                     else:
#                         color = "error"
#                         interpretation = "AI-like patterns detected"
                    
#                     st.metric(
#                         "🎯 AI Likelihood Score", 
#                         f"{score_val}%",
#                         delta=f"{score_val - 50:+.1f}% vs baseline",
#                         delta_color="inverse"
#                     )
                    
#                     # Progress bar for visual representation
#                     progress_color = "#ff4444" if score_val >= 65 else "#ffaa00" if score_val >= 45 else "#00ff00"
#                     st.markdown(f"""
#                     <div style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 5px; margin: 10px 0;">
#                         <div style="background: {progress_color}; height: 20px; width: {score_val}%; border-radius: 8px; transition: all 0.3s;"></div>
#                     </div>
#                     <p style="text-align: center; color: {progress_color}; font-weight: bold;">{interpretation}</p>
#                     """, unsafe_allow_html=True)
                
#                 st.markdown(f"**🏷️ Assessment:** {result['label']}")
                
#                 # Key indicators
#                 if result["reasons"]:
#                     st.subheader("🔍 Key Indicators Found")
#                     for i, reason in enumerate(result["reasons"], 1):
#                         st.write(f"{i}. {reason}")
#                 else:
#                     st.success("✅ No significant AI patterns detected")
                
#                 # Detailed feature analysis
#                 st.subheader("📊 Detailed Feature Analysis")
                
#                 col1, col2 = st.columns(2)
                
#                 with col1:
#                     st.write("**📈 Pattern Metrics:**")
#                     for feature, value in result["features"].items():
#                         feature_name = feature.replace("_", " ").title()
                        
#                         # Color code based on feature values
#                         if "density" in feature or "ratio" in feature:
#                             if value > 0.3:
#                                 color = "🔴"
#                             elif value > 0.15:
#                                 color = "🟡"
#                             else:
#                                 color = "🟢"
#                         else:
#                             color = "🔵"
                        
#                         st.write(f"{color} **{feature_name}:** `{value:.3f}`")
                
#                 with col2:
#                     st.write("**🎯 Confidence Breakdown:**")
                    
#                     # Create confidence indicators for each feature
#                     features = result["features"]
                    
#                     if "comment_density" in features:
#                         cd_score = abs(features["comment_density"] - 0.15) / 0.15
#                         st.write(f"📝 Comment Pattern: `{cd_score:.2f}` {'⚠️' if cd_score > 0.5 else '✅'}")
                    
#                     if "repeated_line_ratio" in features:
#                         rr_score = features["repeated_line_ratio"]
#                         st.write(f"🔄 Code Repetition: `{rr_score:.2f}` {'⚠️' if rr_score > 0.1 else '✅'}")
                    
#                     if "generic_name_density" in features:
#                         gn_score = features["generic_name_density"]
#                         st.write(f"🏷️ Generic Names: `{gn_score:.2f}` {'⚠️' if gn_score > 0.03 else '✅'}")
                    
#                     if "perfect_formatting" in features:
#                         pf_score = features["perfect_formatting"]
#                         st.write(f"✨ Perfect Format: `{pf_score:.2f}` {'⚠️' if pf_score > 0.5 else '✅'}")
                
#                 # Copy and download
#                 col4, col5 = st.columns(2)
#                 with col4:
#                     detection_report = f"""
# AI DETECTION ANALYSIS REPORT
# ============================

# OVERALL ASSESSMENT: {result['label']}
# CONFIDENCE SCORE: {result['score']}%

# KEY INDICATORS:
# {chr(10).join(f"- {reason}" for reason in result['reasons']) if result['reasons'] else "- No significant patterns detected"}

# FEATURE ANALYSIS:
# {chr(10).join(f"- {k.replace('_', ' ').title()}: {v:.3f}" for k, v in result['features'].items())}

# INTERPRETATION:
# {interpretation}
# """
#                     copy_button(detection_report, "Copy Results", key="ai_copy_btn")
#                 with col5:
#                     st.download_button(
#                         "💾 Download Analysis", 
#                         detection_report, 
#                         "ai_detection_report.txt",
#                         mime="text/plain",
#                         key="ai_download_btn"
#                     )

# # Tab 4: URL Extractor
# with tabs[3]:
#     st.header("🌐 URL Data Extraction Engine")
#     st.write("*Advanced web content extraction and intelligent analysis*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         url_input = st.text_input(
#             "🎯 Target URL", 
#             placeholder="Enter any URL for intelligent content extraction...",
#             key="url_input_field",
#             help="Supports web pages, GitHub files, documentation, articles, and more"
#         )
    
#     with col2:
#         url_length = st.slider("Summary Length", 1, 15, 7, key="url_summary_length")
#         url_bullets = st.checkbox("Use Bullet Points", value=True, key="url_use_bullets")
#         url_show_preview = st.checkbox("Show Content Preview", value=True, key="url_show_preview")

#     if st.button("🚀 Extract & Analyze", type="primary", key="url_analyze_btn"):
#         if not url_input.strip():
#             st.warning("⚠️ Please enter a valid URL to proceed.")
#         else:
#             with st.spinner("🔄 Extracting content from URL..."):
#                 content = fetch_from_url(url_input.strip())
            
#             if content.startswith("❌"):
#                 st.error(content)
#             else:
#                 st.success("✅ Content extracted successfully!")
                
#                 # Enhanced metrics display
#                 words = content.split()
#                 sentences = len(re.findall(r'[.!?]+', content))
#                 paragraphs = len([p for p in content.split('\n\n') if p.strip()])
                
#                 col1, col2, col3, col4, col5 = st.columns(5)
#                 with col1:
#                     st.metric("📄 Characters", f"{len(content):,}")
#                 with col2:
#                     st.metric("📝 Words", f"{len(words):,}")
#                 with col3:
#                     st.metric("📋 Lines", f"{len(content.splitlines()):,}")
#                 with col4:
#                     st.metric("📖 Sentences", f"{sentences:,}")
#                 with col5:
#                     st.metric("📑 Paragraphs", f"{paragraphs:,}")
                
#                 # Reading time estimation
#                 avg_reading_speed = 200  # words per minute
#                 reading_time = max(1, len(words) // avg_reading_speed)
#                 st.info(f"📚 Estimated reading time: ~{reading_time} minute{'s' if reading_time != 1 else ''}")
                
#                 # Content preview with better formatting
#                 if url_show_preview:
#                     with st.expander("📄 Content Preview", expanded=False):
#                         preview_length = 3000
#                         preview = content[:preview_length]
#                         if len(content) > preview_length:
#                             preview += f"\n\n... [Content truncated - showing first {preview_length:,} characters of {len(content):,} total]"
                        
#                         # Try to detect if it's code
#                         if any(keyword in content.lower()[:500] for keyword in ['def ', 'class ', 'import ', 'function', '#include', 'public class']):
#                             st.code(preview, language="python" if "def " in preview or "import " in preview else "text")
#                         else:
#                             st.text(preview)
                
#                 # Generate enhanced summary
#                 with st.spinner("🧠 Generating intelligent summary..."):
#                     summary = summarize_text_advanced(content, url_length, url_bullets)
                
#                 # Display summary with better styling
#                 st.subheader("🎯 Intelligent Content Summary")
                
#                 summary_container = st.container()
#                 with summary_container:
#                     if url_bullets:
#                         st.markdown(summary)
#                     else:
#                         st.write(summary)
                
#                 # Additional analysis
#                 with st.expander("📊 Content Analysis", expanded=False):
#                     col1, col2 = st.columns(2)
                    
#                     with col1:
#                         st.write("**📈 Content Statistics:**")
#                         avg_word_length = sum(len(word) for word in words) / max(len(words), 1)
#                         st.write(f"• Average word length: {avg_word_length:.1f} characters")
                        
#                         if sentences > 0:
#                             avg_sentence_length = len(words) / sentences
#                             st.write(f"• Average sentence length: {avg_sentence_length:.1f} words")
                        
#                         # Most common words (excluding stopwords)
#                         filtered_words = [word.lower().strip('.,!?";()[]') for word in words 
#                                         if len(word) > 3 and word.lower() not in STOPWORDS]
#                         if filtered_words:
#                             common_words = Counter(filtered_words).most_common(5)
#                             st.write("• Most frequent words:")
#                             for word, count in common_words:
#                                 st.write(f"  - **{word}**: {count} times")
                    
#                     with col2:
#                         st.write("**🔍 Content Characteristics:**")
                        
#                         # Detect content type
#                         if any(keyword in content.lower() for keyword in ['function', 'variable', 'method', 'class', 'algorithm']):
#                             st.write("• 💻 **Type**: Technical/Programming content")
#                         elif any(keyword in content.lower() for keyword in ['research', 'study', 'analysis', 'data', 'results']):
#                             st.write("• 🔬 **Type**: Research/Academic content")
#                         elif any(keyword in content.lower() for keyword in ['tutorial', 'how to', 'step', 'guide', 'instructions']):
#                             st.write("• 📚 **Type**: Educational/Tutorial content")
#                         else:
#                             st.write("• 📰 **Type**: General/Article content")
                        
#                         # Complexity estimate
#                         complex_words = [word for word in words if len(word) > 7]
#                         complexity = len(complex_words) / max(len(words), 1) * 100
                        
#                         if complexity > 20:
#                             st.write("• 🎓 **Complexity**: Advanced")
#                         elif complexity > 12:
#                             st.write("• 📖 **Complexity**: Intermediate")
#                         else:
#                             st.write("• 📝 **Complexity**: Beginner-friendly")
                        
#                         st.write(f"• 📊 **Complexity Score**: {complexity:.1f}%")
                
#                 # Enhanced copy and download options
#                 col4, col5, col6 = st.columns(3)
#                 with col4:
#                     copy_button(summary, "Copy Summary", key="url_copy_summary")
#                 with col5:
#                     copy_button(content, "Copy Full Content", key="url_copy_full")
#                 with col6:
#                     # Create comprehensive report
#                     comprehensive_report = f"""
# URL EXTRACTION REPORT
# ====================

# SOURCE URL: {url_input}
# EXTRACTION DATE: {st.session_state.get('current_date', 'Today')}

# CONTENT METRICS:
# - Characters: {len(content):,}
# - Words: {len(words):,}
# - Lines: {len(content.splitlines()):,}
# - Sentences: {sentences:,}
# - Paragraphs: {paragraphs:,}
# - Estimated Reading Time: ~{reading_time} minute(s)

# INTELLIGENT SUMMARY:
# {summary}

# FULL EXTRACTED CONTENT:
# {content}
# """
#                     st.download_button(
#                         "💾 Download Full Report", 
#                         comprehensive_report, 
#                         f"url_analysis_report_{url_input.split('/')[-1][:20]}.txt",
#                         mime="text/plain",
#                         key="url_download_full"
#                     )

# # Enhanced Footer with additional info
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; padding: 30px;">
#     <h3 style="color: rgba(0, 249, 255, 0.8); font-family: 'Orbitron', monospace;">🌌 TECHNOVA AI NEXUS v2.1</h3>
#     <p style="color: rgba(0, 249, 255, 0.6); font-family: monospace; margin: 10px 0;">
#         Advanced Neural Processing Suite • Quantum Code Analysis • AI Pattern Detection
#     </p>
#     <p style="color: rgba(0, 249, 255, 0.4); font-size: 0.9em;">
#         Enhanced with comprehensive metrics, intelligent analysis, and reliable copy functionality
#     </p>
#     <div style="margin-top: 20px; color: rgba(0, 249, 255, 0.3);">
#         🚀 Built for developers, researchers, and AI enthusiasts
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Add session state management for better UX
# if 'analysis_history' not in st.session_state:
#     st.session_state['analysis_history'] = []

# # Optional: Add a sidebar with tips and shortcuts
# with st.sidebar:
#     st.header("⚡ Quick Tips")
#     st.write("""
#     **🔧 Code Analyzer:**
#     • Upload .py files for best results
#     • Supports GitHub raw URLs
#     • Detects 12+ code constructs
    
#     **🤖 AI Detection:**
#     • Analyzes patterns in code/text
#     • Uses multiple indicators
#     • Confidence scoring system
    
#     **🌐 URL Extractor:**
#     • Works with most websites
#     • Intelligent content filtering
#     • Automatic summarization
    
#     **📋 Copy Functionality:**
#     • Click copy button first
#     • Select all text in the box
#     • Use Ctrl+C (or Cmd+C) to copy
#     """)
    
#     if st.button("🗑️ Clear All Data", key="clear_all"):
#         for key in list(st.session_state.keys()):
#             if key.startswith(('text_to_copy_', 'copied_text_')):
#                 del st.session_state[key]
#         st.success("All temporary data cleared!")
#         st.rerun()








































# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import re
# import base64
# import ast
# from collections import Counter, defaultdict
# import io

# # PDF extraction (optional)
# try:
#     import PyPDF2
#     PDF_AVAILABLE = True
# except ImportError:
#     PDF_AVAILABLE = False

# # Page config
# st.set_page_config(
#     page_title="Technova AI Nexus", 
#     layout="wide", 
#     initial_sidebar_state="collapsed"
# )

# # Simple and reliable copy function using streamlit components
# def copy_button(text: str, label: str = "Copy", key: str = None):
#     """Simple copy button using streamlit text area"""
#     if text is None:
#         text = ""
    
#     button_key = f"copy_btn_{key}" if key else f"copy_btn_{abs(hash(text[:50]))}"
#     area_key = f"copy_area_{key}" if key else f"copy_area_{abs(hash(text[:50]))}"
    
#     # Show copy button and text area side by side
#     col1, col2 = st.columns([1, 6])
    
#     with col1:
#         st.button(f"📋 {label}", key=button_key, help="Click to show text for copying")
    
#     with col2:
#         st.text_area(
#             "Select all text below and copy (Ctrl+A, Ctrl+C):",
#             value=text,
#             height=120,
#             key=area_key,
#             help="Select all text and copy to clipboard"
#         )

# # Simplified styling
# def set_tech_styling():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;500&display=swap');
    
#     .stApp {
#         background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
#         color: #00f9ff;
#         font-family: 'Rajdhani', sans-serif;
#     }
    
#     h1, h2, h3, h4, h5, h6 {
#         font-family: 'Orbitron', monospace !important;
#         color: #00f9ff !important;
#         text-shadow: 0 0 10px rgba(0, 249, 255, 0.5);
#     }
    
#     .main-title {
#         font-size: 3rem;
#         text-align: center;
#         background: linear-gradient(45deg, #00f9ff, #0099cc, #66ccff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         margin: 2rem 0;
#     }
    
#     .subtitle {
#         text-align: center;
#         color: rgba(0, 249, 255, 0.8);
#         font-style: italic;
#         margin-bottom: 2rem;
#     }
    
#     .stTextArea textarea, .stTextInput input {
#         background: rgba(0, 20, 40, 0.8) !important;
#         border: 1px solid rgba(0, 249, 255, 0.3) !important;
#         color: #00f9ff !important;
#     }
    
#     .stButton > button {
#         background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3)) !important;
#         border: 1px solid rgba(0, 249, 255, 0.5) !important;
#         color: #00f9ff !important;
#         font-weight: bold !important;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         color: #00f9ff !important;
#         font-family: 'Orbitron', monospace !important;
#     }
    
#     .stExpander {
#         border: 1px solid rgba(0, 249, 255, 0.3);
#         border-radius: 10px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Initialize styling
# set_tech_styling()

# # Main title
# st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
# st.markdown('<p class="subtitle">Advanced AI-Powered Analysis Suite v2.1</p>', unsafe_allow_html=True)

# # Stopwords for summarization
# STOPWORDS = set([
#     "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", 
#     "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", 
#     "there", "these", "they", "this", "to", "was", "will", "with", "you", "your", "from", 
#     "our", "we", "he", "she", "his", "her", "its", "were", "been", "being", "than", 
#     "also", "can", "could", "should", "would", "may", "might", "have", "has", "had", 
#     "do", "does", "did", "done", "just", "over", "under", "more", "most", "other", 
#     "some", "any", "each", "many", "few", "those", "them", "which", "who", "whom", 
#     "whose", "where", "when", "why", "how"
# ])

# def safe_sentence_split(text: str):
#     """Split text into sentences safely"""
#     pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
#     return [s.strip() for s in pattern.split(text) if s.strip()]

# def summarize_text_advanced(text: str, max_sentences: int = 5, as_bullets: bool = False) -> str:
#     """Advanced text summarization using frequency analysis"""
#     if not text or not text.strip():
#         return "No content to summarize."
    
#     paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
#     sentences = []
#     for para in paragraphs:
#         sentences.extend(safe_sentence_split(para))
    
#     if not sentences:
#         return text

#     # Word frequency analysis
#     word_freq = Counter()
#     for s in sentences:
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         for w in words:
#             if w not in STOPWORDS and len(w) > 2:
#                 word_freq[w] += 1
    
#     if not word_freq:
#         return " ".join(sentences[:max_sentences])

#     # Normalize frequencies
#     max_freq = max(word_freq.values())
#     for w in list(word_freq.keys()):
#         word_freq[w] /= max_freq

#     # Score sentences
#     scored = []
#     for idx, s in enumerate(sentences):
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         score = sum(word_freq.get(w, 0.0) for w in words)
#         length_penalty = 1.0 + 0.2 * max(0, (len(words) - 20) / 20)
#         position_boost = 1.1 if idx < 3 else 1.0
#         scored.append((score / length_penalty * position_boost, idx, s))

#     # Select top sentences
#     scored.sort(key=lambda x: (-x[0], x[1]))
#     top = sorted(scored[:max_sentences], key=lambda x: x[1])
    
#     if as_bullets:
#         return "\n".join([f"• {s}" for _, _, s in top])
#     return " ".join([s for _, _, s in top])

# def analyze_python_enhanced(code: str):
#     """Comprehensive Python code analysis with enhanced metrics"""
#     report = {
#         "basic_stats": {},
#         "functions": [], 
#         "classes": [], 
#         "imports": [], 
#         "variables": [],
#         "purpose_summary": "", 
#         "errors": [], 
#         "warnings": [], 
#         "fixes": [],
#         "complexity_metrics": {},
#         "code_quality": {},
#         "detailed_counts": {},
#         "builtin_functions_used": []  # Initialize this key
#     }

#     if not code or not code.strip():
#         return report

#     lines = code.splitlines()
#     code_lines = [line for line in lines if line.strip() and not line.strip().startswith("#")]
#     comment_lines = [line for line in lines if line.strip().startswith("#")]
#     blank_lines = [line for line in lines if not line.strip()]

#     # Basic statistics
#     report["basic_stats"] = {
#         "total_lines": len(lines),
#         "code_lines": len(code_lines),
#         "comment_lines": len(comment_lines),
#         "blank_lines": len(blank_lines),
#         "characters": len(code),
#         "words": len(code.split())
#     }

#     # Initialize counters
#     function_count = 0
#     class_count = 0
#     import_count = 0
#     print_count = 0
#     if_count = 0
#     for_count = 0
#     while_count = 0
#     try_count = 0
#     with_count = 0
#     def_count = 0
#     lambda_count = 0
#     list_comp_count = 0
#     dict_comp_count = 0

#     # Pattern-based counting
#     for line in code_lines:
#         stripped_line = line.strip()
        
#         # Count various constructs
#         if stripped_line.startswith("def "):
#             def_count += 1
#         if stripped_line.startswith("class "):
#             class_count += 1
#         if stripped_line.startswith(("import ", "from ")):
#             import_count += 1
        
#         # Count control structures and statements
#         print_count += len(re.findall(r'\bprint\s*\(', line))
#         if_count += len(re.findall(r'\bif\b', line))
#         for_count += len(re.findall(r'\bfor\b', line))
#         while_count += len(re.findall(r'\bwhile\b', line))
#         try_count += len(re.findall(r'\btry\b', line))
#         with_count += len(re.findall(r'\bwith\b', line))
#         lambda_count += len(re.findall(r'\blambda\b', line))
#         list_comp_count += len(re.findall(r'\[.*for.*in.*\]', line))
#         dict_comp_count += len(re.findall(r'\{.*for.*in.*\}', line))

#     report["detailed_counts"] = {
#         "functions": def_count,
#         "classes": class_count,
#         "imports": import_count,
#         "print_statements": print_count,
#         "if_statements": if_count,
#         "for_loops": for_count,
#         "while_loops": while_count,
#         "try_blocks": try_count,
#         "with_statements": with_count,
#         "lambda_expressions": lambda_count,
#         "list_comprehensions": list_comp_count,
#         "dict_comprehensions": dict_comp_count
#     }

#     # Calculate complexity metrics
#     total_constructs = sum([if_count, for_count, while_count, try_count, def_count])
#     complexity_score = total_constructs / max(1, len(code_lines)) * 100
    
#     report["complexity_metrics"] = {
#         "cyclomatic_complexity_estimate": total_constructs + 1,
#         "complexity_per_line": round(complexity_score, 2),
#         "nesting_level_estimate": max(0, len(re.findall(r'    ', code)) // len(code_lines) * 10) if code_lines else 0
#     }

#     # Code quality metrics
#     comment_ratio = len(comment_lines) / max(1, len(lines)) * 100
#     avg_line_length = sum(len(line) for line in code_lines) / max(1, len(code_lines))
    
#     report["code_quality"] = {
#         "comment_ratio": round(comment_ratio, 2),
#         "avg_line_length": round(avg_line_length, 2),
#         "code_to_comment_ratio": round(len(code_lines) / max(1, len(comment_lines)), 2)
#     }

#     # Basic parsing for simple analysis
#     for line in code_lines:
#         stripped = line.strip()
#         if stripped.startswith("def "):
#             match = re.match(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)", stripped)
#             if match:
#                 report["functions"].append(match.group(1))
#         elif stripped.startswith("class "):
#             match = re.match(r"class\s+([a-zA-Z_][a-zA-Z0-9_]*)", stripped)
#             if match:
#                 report["classes"].append(match.group(1))
#         elif stripped.startswith(("import ", "from ")):
#             report["imports"].append(stripped)

#     # Generate purpose summary
#     report["purpose_summary"] = summarize_text_advanced(code, max_sentences=3)

#     # AST analysis for deeper insights
#     try:
#         tree = ast.parse(code)
#     except SyntaxError as e:
#         report["errors"].append(f"SyntaxError: {e.msg} at line {e.lineno}")
#         report["fixes"].append("Check syntax: indentation, colons, parentheses, quotes.")
#         return report

#     # Enhanced AST analysis
#     imported_names = set()
#     used_names = set()
#     assigned_names = set()
#     builtin_functions_used = set()
    
#     builtin_funcs = {
#         'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir', 'enumerate', 
#         'filter', 'float', 'format', 'frozenset', 'hash', 'hex', 'id', 'input', 
#         'int', 'isinstance', 'len', 'list', 'map', 'max', 'min', 'next', 'oct', 
#         'open', 'ord', 'pow', 'print', 'range', 'repr', 'reversed', 'round', 
#         'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
#     }

#     class EnhancedCodeAnalyzer(ast.NodeVisitor):
#         def visit_Import(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name.split(".")[0])
#             self.generic_visit(node)

#         def visit_ImportFrom(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name)
#             self.generic_visit(node)

#         def visit_FunctionDef(self, node):
#             assigned_names.add(node.name)
#             # Check for mutable default arguments
#             for default in node.args.defaults:
#                 if isinstance(default, (ast.List, ast.Dict, ast.Set)):
#                     report["warnings"].append(f"Mutable default argument in '{node.name}'")
#                     report["fixes"].append(f"Use None as default in '{node.name}' and create objects inside function")
            
#             # Check for long functions
#             func_lines = len([n for n in ast.walk(node) if hasattr(n, 'lineno')])
#             if func_lines > 50:
#                 report["warnings"].append(f"Function '{node.name}' is very long ({func_lines} lines)")
#                 report["fixes"].append(f"Consider breaking down '{node.name}' into smaller functions")
            
#             self.generic_visit(node)

#         def visit_ClassDef(self, node):
#             assigned_names.add(node.name)
#             self.generic_visit(node)

#         def visit_Name(self, node):
#             if isinstance(node.ctx, ast.Load):
#                 used_names.add(node.id)
#                 if node.id in builtin_funcs:
#                     builtin_functions_used.add(node.id)
#             elif isinstance(node.ctx, ast.Store):
#                 assigned_names.add(node.id)
#                 report["variables"].append(node.id)
#             self.generic_visit(node)

#         def visit_Call(self, node):
#             if isinstance(node.func, ast.Name):
#                 if node.func.id in {"eval", "exec"}:
#                     report["warnings"].append(f"Dangerous {node.func.id} usage detected")
#                     report["fixes"].append(f"Avoid {node.func.id}; use safer alternatives")
#                 elif node.func.id == "print" and len(node.args) == 0:
#                     report["warnings"].append("Empty print() statement found")
#                     report["fixes"].append("Remove empty print() or add meaningful content")
#             self.generic_visit(node)

#     EnhancedCodeAnalyzer().visit(tree)

#     # Add builtin functions used to report
#     report["builtin_functions_used"] = sorted(list(builtin_functions_used))

#     # Check for unused imports
#     unused_imports = []
#     for name in sorted(imported_names):
#         if name not in used_names and name not in {"__future__"}:
#             unused_imports.append(name)
#             report["warnings"].append(f"Possibly unused import: '{name}'")
#             report["fixes"].append(f"Remove unused import '{name}' if not needed")

#     # Check for builtin shadowing
#     builtins_list = [
#         'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir', 'enumerate', 
#         'filter', 'float', 'format', 'frozenset', 'hash', 'hex', 'id', 'input', 
#         'int', 'isinstance', 'len', 'list', 'map', 'max', 'min', 'next', 'oct', 
#         'open', 'ord', 'pow', 'print', 'range', 'repr', 'reversed', 'round', 
#         'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
#     ]
    
#     shadowed_builtins = []
#     for name in assigned_names:
#         if name in builtins_list:
#             shadowed_builtins.append(name)
#             report["warnings"].append(f"Variable '{name}' shadows builtin")
#             report["fixes"].append(f"Rename '{name}' to avoid shadowing builtins")

#     # Code quality analysis
#     if report["code_quality"]["comment_ratio"] < 5:
#         report["warnings"].append("Low comment density - consider adding more documentation")
#         report["fixes"].append("Add docstrings to functions and classes, and inline comments for complex logic")
    
#     if report["code_quality"]["avg_line_length"] > 100:
#         report["warnings"].append("Some lines are very long - consider breaking them up")
#         report["fixes"].append("Break long lines at logical points (after commas, operators, etc.)")

#     # Add general recommendations
#     if not report["errors"]:
#         if not report["warnings"]:
#             report["fixes"].append("🎉 Code looks excellent! Consider adding unit tests and type hints.")
#         else:
#             report["fixes"].append("Review warnings above and apply suggested fixes for better code quality.")

#     # Remove duplicate variables
#     report["variables"] = sorted(list(set(report["variables"])))

#     return report

# def detect_ai_generated_code(code: str) -> dict:
#     """Detect if code might be AI-generated based on patterns"""
#     if not code or not code.strip():
#         return {"score": 0, "label": "❓ No content", "reasons": [], "features": {}}
    
#     lines = code.splitlines()
#     code_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
#     comment_lines = [ln for ln in lines if ln.strip().startswith("#")]
    
#     features = {}
#     total_lines = max(1, len(lines))
    
#     # Comment density
#     features["comment_density"] = len(comment_lines) / total_lines
    
#     # Repeated lines
#     normalized = [re.sub(r"\s+", " ", ln.strip()) for ln in code_lines]
#     counts = Counter(normalized)
#     repeated = sum(c for c in counts.values() if c > 1)
#     features["repeated_line_ratio"] = repeated / max(1, len(code_lines))
    
#     # Generic variable names
#     generic_names = {"data", "result", "temp", "value", "item", "input", "output", "res", "var", "obj"}
#     tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code)
#     generic_count = sum(1 for t in tokens if t in generic_names)
#     features["generic_name_density"] = generic_count / max(1, len(tokens))
    
#     # Perfect formatting (suspicious)
#     perfect_indent = all(len(line) - len(line.lstrip()) % 4 == 0 for line in code_lines if line.strip())
#     features["perfect_formatting"] = 1.0 if perfect_indent and len(code_lines) > 10 else 0.0
    
#     # Calculate score
#     score = (
#         25 * min(1.0, abs(features["comment_density"] - 0.15) / 0.15) +
#         35 * features["repeated_line_ratio"] +
#         20 * min(1.0, features["generic_name_density"] * 20) +
#         20 * features["perfect_formatting"]
#     )
    
#     score = max(0.0, min(100.0, score))
    
#     # Determine label
#     if score >= 70:
#         label = "🚨 Likely AI-generated"
#     elif score >= 45:
#         label = "🤔 Unclear/Mixed"
#     else:
#         label = "✅ Likely human-written"
    
#     # Generate reasons
#     reasons = []
#     if features["repeated_line_ratio"] > 0.1:
#         reasons.append("High repetition of similar code patterns")
#     if features["comment_density"] < 0.02 or features["comment_density"] > 0.4:
#         reasons.append("Unusual comment density")
#     if features["generic_name_density"] > 0.03:
#         reasons.append("Frequent generic variable names")
#     if features["perfect_formatting"] == 1.0:
#         reasons.append("Suspiciously perfect code formatting")
    
#     return {
#         "score": round(score, 1), 
#         "label": label, 
#         "reasons": reasons, 
#         "features": features
#     }

# def fetch_from_url(url: str) -> str:
#     """Fetch and extract text content from URL"""
#     try:
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
#         }
#         resp = requests.get(url, timeout=10, headers=headers)
#         resp.raise_for_status()
        
#         content_type = resp.headers.get("Content-Type", "")
#         if "text/html" in content_type:
#             soup = BeautifulSoup(resp.text, "html.parser")
#             # Remove unwanted elements
#             for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
#                 element.extract()
#             return soup.get_text(separator="\n", strip=True)
#         else:
#             return resp.text
            
#     except requests.exceptions.RequestException as e:
#         return f"❌ Error fetching URL: {str(e)}"
#     except Exception as e:
#         return f"❌ Error processing content: {str(e)}"

# # Create tabs
# tabs = st.tabs([
#     "📄 Document Processor", 
#     "🧠 Code Analyzer", 
#     "🤖 AI Detection", 
#     "🌐 URL Extractor"
# ])

# # Tab 1: Document Processor
# with tabs[0]:
#     st.header("📄 Neural Document Processor")
#     st.write("*Advanced text analysis and summarization*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         doc_text = st.text_area(
#             "Input Text", 
#             height=200, 
#             placeholder="Paste your document content here...",
#             key="doc_text_input"
#         )
    
#     with col2:
#         doc_file = st.file_uploader("Upload Document", type=["txt", "md", "pdf"], key="doc_file_upload")
#         doc_url = st.text_input("Document URL", placeholder="https://...", key="doc_url_input")
#         doc_length = st.slider("Summary Length", 1, 10, 5, key="doc_summary_length")
#         doc_bullets = st.checkbox("Use Bullets", value=False, key="doc_use_bullets")

#     if st.button("🚀 Analyze Document", type="primary", key="doc_analyze_btn"):
#         content = ""
        
#         # Get content from various sources
#         if doc_file:
#             if doc_file.name.lower().endswith(".pdf"):
#                 if not PDF_AVAILABLE:
#                     st.error("PDF processing requires PyPDF2. Install with: pip install PyPDF2")
#                 else:
#                     try:
#                         reader = PyPDF2.PdfReader(io.BytesIO(doc_file.read()))
#                         pages_text = []
#                         for page in reader.pages:
#                             pages_text.append(page.extract_text() or "")
#                         content = "\n".join(pages_text)
#                     except Exception as e:
#                         st.error(f"PDF error: {e}")
#             else:
#                 content = doc_file.read().decode("utf-8", errors="ignore")
#         elif doc_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(doc_url.strip())
#         elif doc_text.strip():
#             content = doc_text

#         if not content:
#             st.warning("Please provide content via text, file, or URL.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Processing..."):
#                 summary = summarize_text_advanced(content, doc_length, doc_bullets)
            
#             st.success("Analysis Complete!")
            
#             # Show summary FIRST (most important)
#             st.subheader("📋 Generated Summary")
#             if doc_bullets:
#                 st.markdown(summary)
#             else:
#                 st.write(summary)
            
#             # Copy functionality for summary
#             st.subheader("📋 Copy Summary")
#             copy_button(summary, "Copy Summary", key="doc_summary")
            
#             # Then show document metrics
#             st.subheader("📊 Document Statistics")
#             col1, col2, col3, col4 = st.columns(4)
#             with col1:
#                 st.metric("Characters", f"{len(content):,}")
#             with col2:
#                 st.metric("Words", f"{len(content.split()):,}")
#             with col3:
#                 st.metric("Lines", f"{len(content.splitlines()):,}")
#             with col4:
#                 st.metric("Paragraphs", f"{len([p for p in content.split('\\n\\n') if p.strip()]):,}")
            
#             # Download option
#             st.download_button(
#                 "💾 Download Summary", 
#                 summary, 
#                 "summary.txt",
#                 mime="text/plain",
#                 key="doc_download_btn"
#             )

# # Tab 2: Enhanced Code Analyzer with reordered sections
# with tabs[1]:
#     st.header("🧠 Quantum Code Analyzer")
#     st.write("*Deep code analysis with comprehensive metrics and optimization recommendations*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         code_text = st.text_area(
#             "Python Code", 
#             height=250, 
#             placeholder="Paste your Python code here...",
#             key="code_text_input"
#         )
    
#     with col2:
#         code_file = st.file_uploader("Upload Python File", type=["py"], key="code_file_upload")
#         code_url = st.text_input("Code URL", placeholder="https://...", key="code_url_input")

#     if st.button("🔍 Analyze Code", type="primary", key="code_analyze_btn"):
#         code_content = ""
        
#         if code_file:
#             code_content = code_file.read().decode("utf-8", errors="ignore")
#         elif code_url.strip():
#             with st.spinner("Fetching code..."):
#                 code_content = fetch_from_url(code_url.strip())
#         elif code_text.strip():
#             code_content = code_text

#         if not code_content:
#             st.warning("Please provide code via input, file, or URL.")
#         elif code_content.startswith("❌"):
#             st.error(code_content)
#         else:
#             with st.expander("Code Preview", expanded=False):
#                 st.code(code_content, language="python")

#             with st.spinner("Analyzing code..."):
#                 report = analyze_python_enhanced(code_content)

#             st.success("🎉 Analysis Complete!")

#             # PRIORITY SECTION 1: ERRORS (Most Important)
#             st.header("❌ Errors")
#             if report["errors"]:
#                 for error in report["errors"]:
#                     st.error(error)
#             else:
#                 st.success("✅ No syntax errors found!")
            
#             # PRIORITY SECTION 2: WARNINGS
#             st.header("⚠️ Warnings")
#             if report["warnings"]:
#                 for warning in report["warnings"]:
#                     st.warning(warning)
#             else:
#                 st.success("✅ No warnings!")
            
#             # PRIORITY SECTION 3: SUGGESTIONS/RECOMMENDATIONS
#             st.header("💡 Suggestions & Recommendations")
#             for fix in report["fixes"]:
#                 st.info(fix)
            
#             # PRIORITY SECTION 4: CODE SUMMARY
#             st.header("📋 Code Summary")
#             st.write(report["purpose_summary"])
            
#             # Copy functionality for main analysis
#             st.header("📋 Copy Analysis Report")
#             formatted_report = f"""
# CODE ANALYSIS REPORT
# ==================

# ERRORS ({len(report['errors'])} found):
# {chr(10).join(f"- {error}" for error in report['errors']) if report['errors'] else "✅ No errors"}

# WARNINGS ({len(report['warnings'])} found):
# {chr(10).join(f"- {warning}" for warning in report['warnings']) if report['warnings'] else "✅ No warnings"}

# RECOMMENDATIONS:
# {chr(10).join(f"- {fix}" for fix in report['fixes'])}

# CODE SUMMARY:
# {report['purpose_summary']}

# FUNCTIONS FOUND ({len(report['functions'])}):
# {', '.join(report['functions']) if report['functions'] else "None"}

# CLASSES FOUND ({len(report['classes'])}):
# {', '.join(report['classes']) if report['classes'] else "None"}

# DETAILED STATISTICS:
# - Total Lines: {report['basic_stats'].get('total_lines', 0)}
# - Code Lines: {report['basic_stats'].get('code_lines', 0)}
# - Comment Lines: {report['basic_stats'].get('comment_lines', 0)}
# - Functions: {report['detailed_counts'].get('functions', 0)}
# - Classes: {report['detailed_counts'].get('classes', 0)}
# - Imports: {report['detailed_counts'].get('imports', 0)}
# - Print Statements: {report['detailed_counts'].get('print_statements', 0)}
# - If Statements: {report['detailed_counts'].get('if_statements', 0)}
# - For Loops: {report['detailed_counts'].get('for_loops', 0)}
# - While Loops: {report['detailed_counts'].get('while_loops', 0)}
# """
#             copy_button(formatted_report, "Copy Full Report", key="code_report")
            
#             # NOW SHOW DETAILED METRICS (Lower Priority)
#             st.header("📊 Detailed Code Metrics")
            
#             # Functions and Classes Found
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 if report["functions"]:
#                     st.subheader("🔧 Functions Found")
#                     for func in report["functions"][:10]:  # Show first 10
#                         st.write(f"• `{func}()`")
#                     if len(report["functions"]) > 10:
#                         st.write(f"... and {len(report['functions']) - 10} more")
                
#                 # SAFE ACCESS TO builtin_functions_used - FIXED LINE
#                 builtin_functions = report.get("builtin_functions_used", [])
#                 if builtin_functions:
#                     st.subheader("🐍 Built-in Functions Used")
#                     builtin_display = ", ".join(f"`{func}()`" for func in builtin_functions[:15])
#                     st.write(builtin_display)
#                     if len(builtin_functions) > 15:
#                         st.write(f"... and {len(builtin_functions) - 15} more")
            
#             with col2:
#                 if report["classes"]:
#                     st.subheader("🏗️ Classes Found")
#                     for cls in report["classes"]:
#                         st.write(f"• `{cls}`")
                
#                 if report["variables"]:
#                     st.subheader("📝 Variables")
#                     variables_display = ", ".join(f"`{var}`" for var in report["variables"][:20])
#                     st.write(variables_display)
#                     if len(report["variables"]) > 20:
#                         st.write(f"... and {len(report['variables']) - 20} more variables")

#             # Basic Statistics Section
#             st.subheader("📈 Line Statistics")
#             col1, col2, col3, col4 = st.columns(4)
            
#             with col1:
#                 st.metric("Total Lines", report["basic_stats"].get("total_lines", 0))
#                 st.metric("Functions", report["detailed_counts"].get("functions", 0))
#             with col2:
#                 st.metric("Code Lines", report["basic_stats"].get("code_lines", 0))
#                 st.metric("Classes", report["detailed_counts"].get("classes", 0))
#             with col3:
#                 st.metric("Comments", report["basic_stats"].get("comment_lines", 0))
#                 st.metric("Imports", report["detailed_counts"].get("imports", 0))
#             with col4:
#                 st.metric("Characters", f"{report['basic_stats'].get('characters', 0):,}")
#                 st.metric("Print Statements", report["detailed_counts"].get("print_statements", 0))

#             # Detailed Counts Section
#             st.subheader("🔧 Code Constructs")
#             col1, col2, col3, col4 = st.columns(4)
            
#             with col1:
#                 st.metric("If Statements", report["detailed_counts"].get("if_statements", 0))
#                 st.metric("For Loops", report["detailed_counts"].get("for_loops", 0))
#             with col2:
#                 st.metric("While Loops", report["detailed_counts"].get("while_loops", 0))
#                 st.metric("Try Blocks", report["detailed_counts"].get("try_blocks", 0))
#             with col3:
#                 st.metric("With Statements", report["detailed_counts"].get("with_statements", 0))
#                 st.metric("Lambda Expressions", report["detailed_counts"].get("lambda_expressions", 0))
#             with col4:
#                 st.metric("List Comprehensions", report["detailed_counts"].get("list_comprehensions", 0))
#                 st.metric("Dict Comprehensions", report["detailed_counts"].get("dict_comprehensions", 0))

#             # Code Quality Metrics
#             st.subheader("📊 Quality Metrics")
#             col1, col2, col3 = st.columns(3)
            
#             with col1:
#                 comment_ratio = report["code_quality"].get("comment_ratio", 0)
#                 st.metric("Comment Ratio", f"{comment_ratio:.1f}%")
                
#             with col2:
#                 avg_line_length = report["code_quality"].get("avg_line_length", 0)
#                 st.metric("Avg Line Length", f"{avg_line_length:.1f} chars")
                
#             with col3:
#                 complexity = report["complexity_metrics"].get("cyclomatic_complexity_estimate", 0)
#                 st.metric("Complexity Score", complexity)

#             # Imports and Variables Details
#             with st.expander("📦 Imports & Variables Details", expanded=False):
#                 col1, col2 = st.columns(2)
                
#                 with col1:
#                     if report["imports"]:
#                         st.subheader("📥 Imports")
#                         for imp in report["imports"]:
#                             st.code(imp, language="python")
#                     else:
#                         st.write("No imports found")
                
#                 with col2:
#                     if report["variables"]:
#                         st.subheader("📝 All Variables")
#                         variables_display = ", ".join(f"`{var}`" for var in report["variables"])
#                         st.write(variables_display)
#                     else:
#                         st.write("No variables detected")
            
#             # Download option
#             st.download_button(
#                 "💾 Download Full Report", 
#                 formatted_report, 
#                 "code_analysis_report.txt",
#                 mime="text/plain",
#                 key="code_download_btn"
#             )

# # Tab 3: AI Detection with reordered sections
# with tabs[2]:
#     st.header("🤖 AI Detection Matrix")
#     st.write("*Advanced pattern recognition for AI-generated content*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         ai_text = st.text_area(
#             "Content for Analysis", 
#             height=200, 
#             placeholder="Paste text or code to analyze for AI patterns...",
#             key="ai_text_input"
#         )
    
#     with col2:
#         ai_file = st.file_uploader("Upload File", type=["txt", "py", "md"], key="ai_file_upload")
#         ai_url = st.text_input("Content URL", placeholder="https://...", key="ai_url_input")

#     if st.button("🔬 Scan for AI Patterns", type="primary", key="ai_analyze_btn"):
#         content = ""
        
#         if ai_file:
#             content = ai_file.read().decode("utf-8", errors="ignore")
#         elif ai_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(ai_url.strip())
#         elif ai_text.strip():
#             content = ai_text

#         if not content:
#             st.warning("Please provide content for analysis.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Analyzing patterns..."):
#                 result = detect_ai_generated_code(content)
            
#             st.success("🔍 Analysis Complete!")
            
#             # PRIORITY 1: MAIN ASSESSMENT (Most Important)
#             score_val = result['score']
#             if score_val < 45:
#                 color = "#00ff00"
#                 interpretation = "Human-like patterns detected"
#             elif score_val < 65:
#                 color = "#ffaa00"
#                 interpretation = "Mixed or uncertain patterns"
#             else:
#                 color = "#ff4444"
#                 interpretation = "AI-like patterns detected"
            
#             st.header(f"🎯 AI Detection Result: {result['label']}")
            
#             # Visual score indicator
#             col1, col2, col3 = st.columns([1, 2, 1])
#             with col2:
#                 st.metric(
#                     "AI Likelihood Score", 
#                     f"{score_val}%",
#                     delta=f"{score_val - 50:+.1f}% vs baseline",
#                     delta_color="inverse"
#                 )
                
#                 # Progress bar for visual representation
#                 st.markdown(f"""
#                 <div style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 5px; margin: 10px 0;">
#                     <div style="background: {color}; height: 20px; width: {score_val}%; border-radius: 8px; transition: all 0.3s;"></div>
#                 </div>
#                 <p style="text-align: center; color: {color}; font-weight: bold;">{interpretation}</p>
#                 """, unsafe_allow_html=True)
            
#             # PRIORITY 2: KEY INDICATORS
#             st.header("🔍 Key Indicators")
#             if result["reasons"]:
#                 for i, reason in enumerate(result["reasons"], 1):
#                     st.warning(f"{i}. {reason}")
#             else:
#                 st.success("✅ No significant AI patterns detected")
            
#             # PRIORITY 3: COPY FUNCTIONALITY
#             st.header("📋 Copy Detection Report")
#             detection_report = f"""
# AI DETECTION ANALYSIS REPORT
# ============================

# OVERALL ASSESSMENT: {result['label']}
# CONFIDENCE SCORE: {result['score']}%
# INTERPRETATION: {interpretation}

# KEY INDICATORS:
# {chr(10).join(f"- {reason}" for reason in result['reasons']) if result['reasons'] else "- No significant patterns detected"}

# DETAILED FEATURE ANALYSIS:
# {chr(10).join(f"- {k.replace('_', ' ').title()}: {v:.3f}" for k, v in result['features'].items())}

# CONFIDENCE BREAKDOWN:
# - Comment Pattern Score: {abs(result['features'].get('comment_density', 0) - 0.15) / 0.15:.2f}
# - Code Repetition Score: {result['features'].get('repeated_line_ratio', 0):.2f}
# - Generic Names Score: {result['features'].get('generic_name_density', 0):.2f}
# - Perfect Format Score: {result['features'].get('perfect_formatting', 0):.2f}
# """
#             copy_button(detection_report, "Copy Detection Report", key="ai_report")
            
#             # LOWER PRIORITY: DETAILED METRICS
#             st.header("📊 Detailed Feature Analysis")
            
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 st.write("**📈 Pattern Metrics:**")
#                 for feature, value in result["features"].items():
#                     feature_name = feature.replace("_", " ").title()
                    
#                     # Color code based on feature values
#                     if "density" in feature or "ratio" in feature:
#                         if value > 0.3:
#                             color_indicator = "🔴"
#                         elif value > 0.15:
#                             color_indicator = "🟡"
#                         else:
#                             color_indicator = "🟢"
#                     else:
#                         color_indicator = "🔵"
                    
#                     st.write(f"{color_indicator} **{feature_name}:** `{value:.3f}`")
            
#             with col2:
#                 st.write("**🎯 Confidence Breakdown:**")
                
#                 # Create confidence indicators for each feature
#                 features = result["features"]
                
#                 if "comment_density" in features:
#                     cd_score = abs(features["comment_density"] - 0.15) / 0.15
#                     st.write(f"📝 Comment Pattern: `{cd_score:.2f}` {'⚠️' if cd_score > 0.5 else '✅'}")
                
#                 if "repeated_line_ratio" in features:
#                     rr_score = features["repeated_line_ratio"]
#                     st.write(f"🔄 Code Repetition: `{rr_score:.2f}` {'⚠️' if rr_score > 0.1 else '✅'}")
                
#                 if "generic_name_density" in features:
#                     gn_score = features["generic_name_density"]
#                     st.write(f"🏷️ Generic Names: `{gn_score:.2f}` {'⚠️' if gn_score > 0.03 else '✅'}")
                
#                 if "perfect_formatting" in features:
#                     pf_score = features["perfect_formatting"]
#                     st.write(f"✨ Perfect Format: `{pf_score:.2f}` {'⚠️' if pf_score > 0.5 else '✅'}")
            
#             # Download option
#             st.download_button(
#                 "💾 Download Analysis", 
#                 detection_report, 
#                 "ai_detection_report.txt",
#                 mime="text/plain",
#                 key="ai_download_btn"
#             )

# # Tab 4: URL Extractor with reordered sections
# with tabs[3]:
#     st.header("🌐 URL Data Extraction Engine")
#     st.write("*Advanced web content extraction and intelligent analysis*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         url_input = st.text_input(
#             "🎯 Target URL", 
#             placeholder="Enter any URL for intelligent content extraction...",
#             key="url_input_field",
#             help="Supports web pages, GitHub files, documentation, articles, and more"
#         )
    
#     with col2:
#         url_length = st.slider("Summary Length", 1, 15, 7, key="url_summary_length")
#         url_bullets = st.checkbox("Use Bullet Points", value=True, key="url_use_bullets")
#         url_show_preview = st.checkbox("Show Content Preview", value=True, key="url_show_preview")

#     if st.button("🚀 Extract & Analyze", type="primary", key="url_analyze_btn"):
#         if not url_input.strip():
#             st.warning("⚠️ Please enter a valid URL to proceed.")
#         else:
#             with st.spinner("🔄 Extracting content from URL..."):
#                 content = fetch_from_url(url_input.strip())
            
#             if content.startswith("❌"):
#                 st.error(content)
#             else:
#                 st.success("✅ Content extracted successfully!")
                
#                 # Generate enhanced summary
#                 with st.spinner("🧠 Generating intelligent summary..."):
#                     summary = summarize_text_advanced(content, url_length, url_bullets)
                
#                 # PRIORITY 1: SUMMARY (Most Important)
#                 st.header("🎯 Intelligent Content Summary")
#                 if url_bullets:
#                     st.markdown(summary)
#                 else:
#                     st.write(summary)
                
#                 # PRIORITY 2: COPY FUNCTIONALITY
#                 st.header("📋 Copy Summary")
#                 copy_button(summary, "Copy Summary", key="url_summary")
                
#                 # Enhanced metrics display (LOWER PRIORITY)
#                 words = content.split()
#                 sentences = len(re.findall(r'[.!?]+', content))
#                 paragraphs = len([p for p in content.split('\n\n') if p.strip()])
                
#                 # Reading time estimation
#                 avg_reading_speed = 200  # words per minute
#                 reading_time = max(1, len(words) // avg_reading_speed)
#                 st.info(f"📚 Estimated reading time: ~{reading_time} minute{'s' if reading_time != 1 else ''}")
                
#                 st.header("📊 Content Statistics")
#                 col1, col2, col3, col4, col5 = st.columns(5)
#                 with col1:
#                     st.metric("📄 Characters", f"{len(content):,}")
#                 with col2:
#                     st.metric("📝 Words", f"{len(words):,}")
#                 with col3:
#                     st.metric("📋 Lines", f"{len(content.splitlines()):,}")
#                 with col4:
#                     st.metric("📖 Sentences", f"{sentences:,}")
#                 with col5:
#                     st.metric("📑 Paragraphs", f"{paragraphs:,}")
                
#                 # Content preview with better formatting
#                 if url_show_preview:
#                     with st.expander("📄 Content Preview", expanded=False):
#                         preview_length = 3000
#                         preview = content[:preview_length]
#                         if len(content) > preview_length:
#                             preview += f"\n\n... [Content truncated - showing first {preview_length:,} characters of {len(content):,} total]"
                        
#                         # Try to detect if it's code
#                         if any(keyword in content.lower()[:500] for keyword in ['def ', 'class ', 'import ', 'function', '#include', 'public class']):
#                             st.code(preview, language="python" if "def " in preview or "import " in preview else "text")
#                         else:
#                             st.text(preview)
                
#                 # Additional analysis
#                 with st.expander("📊 Content Analysis", expanded=False):
#                     col1, col2 = st.columns(2)
                    
#                     with col1:
#                         st.write("**📈 Content Statistics:**")
#                         avg_word_length = sum(len(word) for word in words) / max(len(words), 1)
#                         st.write(f"• Average word length: {avg_word_length:.1f} characters")
                        
#                         if sentences > 0:
#                             avg_sentence_length = len(words) / sentences
#                             st.write(f"• Average sentence length: {avg_sentence_length:.1f} words")
                        
#                         # Most common words (excluding stopwords)
#                         filtered_words = [word.lower().strip('.,!?";()[]') for word in words 
#                                         if len(word) > 3 and word.lower() not in STOPWORDS]
#                         if filtered_words:
#                             common_words = Counter(filtered_words).most_common(5)
#                             st.write("• Most frequent words:")
#                             for word, count in common_words:
#                                 st.write(f"  - **{word}**: {count} times")
                    
#                     with col2:
#                         st.write("**🔍 Content Characteristics:**")
                        
#                         # Detect content type
#                         if any(keyword in content.lower() for keyword in ['function', 'variable', 'method', 'class', 'algorithm']):
#                             st.write("• 💻 **Type**: Technical/Programming content")
#                         elif any(keyword in content.lower() for keyword in ['research', 'study', 'analysis', 'data', 'results']):
#                             st.write("• 🔬 **Type**: Research/Academic content")
#                         elif any(keyword in content.lower() for keyword in ['tutorial', 'how to', 'step', 'guide', 'instructions']):
#                             st.write("• 📚 **Type**: Educational/Tutorial content")
#                         else:
#                             st.write("• 📰 **Type**: General/Article content")
                        
#                         # Complexity estimate
#                         complex_words = [word for word in words if len(word) > 7]
#                         complexity = len(complex_words) / max(len(words), 1) * 100
                        
#                         if complexity > 20:
#                             st.write("• 🎓 **Complexity**: Advanced")
#                         elif complexity > 12:
#                             st.write("• 📖 **Complexity**: Intermediate")
#                         else:
#                             st.write("• 📝 **Complexity**: Beginner-friendly")
                        
#                         st.write(f"• 📊 **Complexity Score**: {complexity:.1f}%")
                
#                 # Enhanced copy and download options
#                 col4, col5, col6 = st.columns(3)
#                 with col4:
#                     copy_button(content, "Copy Full Content", key="url_full")
#                 with col5:
#                     st.download_button(
#                         "💾 Download Summary", 
#                         summary, 
#                         "url_summary.txt",
#                         mime="text/plain",
#                         key="url_download_summary"
#                     )
#                 with col6:
#                     # Create comprehensive report
#                     comprehensive_report = f"""
# URL EXTRACTION REPORT
# ====================

# SOURCE URL: {url_input}
# EXTRACTION DATE: Today

# CONTENT SUMMARY:
# {summary}

# CONTENT METRICS:
# - Characters: {len(content):,}
# - Words: {len(words):,}
# - Lines: {len(content.splitlines()):,}
# - Sentences: {sentences:,}
# - Paragraphs: {paragraphs:,}
# - Estimated Reading Time: ~{reading_time} minute(s)

# FULL EXTRACTED CONTENT:
# {content}
# """
#                     st.download_button(
#                         "💾 Download Full Report", 
#                         comprehensive_report, 
#                         f"url_analysis_report.txt",
#                         mime="text/plain",
#                         key="url_download_full"
#                     )

# # Enhanced Footer
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; padding: 30px;">
#     <h3 style="color: rgba(0, 249, 255, 0.8); font-family: 'Orbitron', monospace;">🌌 TECHNOVA AI NEXUS v2.1</h3>
#     <p style="color: rgba(0, 249, 255, 0.6); font-family: monospace; margin: 10px 0;">
#         Advanced Neural Processing Suite • Quantum Code Analysis • AI Pattern Detection
#     </p>
#     <p style="color: rgba(0, 249, 255, 0.4); font-size: 0.9em;">
#         Priority-ordered analysis with reliable copy functionality
#     </p>
#     <div style="margin-top: 20px; color: rgba(0, 249, 255, 0.3);">
#         🚀 Built for developers, researchers, and AI enthusiasts
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Add session state management for better UX
# if 'analysis_history' not in st.session_state:
#     st.session_state['analysis_history'] = []

# # Optional: Add a sidebar with tips and shortcuts
# with st.sidebar:
#     st.header("⚡ Quick Tips")
#     st.write("""
#     **🔧 Code Analyzer:**
#     • Shows errors & warnings first
#     • Upload .py files for best results
#     • Supports GitHub raw URLs
#     • Detects 12+ code constructs
    
#     **🤖 AI Detection:**
#     • Assessment result shown first
#     • Analyzes patterns in code/text
#     • Uses multiple indicators
#     • Confidence scoring system
    
#     **🌐 URL Extractor:**
#     • Summary appears first
#     • Works with most websites
#     • Intelligent content filtering
#     • Automatic summarization
    
#     **📋 Copy Functionality:**
#     • Click copy button
#     • Text area appears below
#     • Select all text (Ctrl+A)
#     • Copy to clipboard (Ctrl+C)
#     """)
    
#     if st.button("🗑️ Clear All Data", key="clear_all"):
#         keys_to_remove = []
#         for key in st.session_state.keys():
#             if any(prefix in key for prefix in ['text_to_copy_', 'copied_text_', 'copy_btn_', 'copy_area_']):
#                 keys_to_remove.append(key)
        
#         for key in keys_to_remove:
#             del st.session_state[key]
        
#         st.success("All temporary data cleared!")
#         st.rerun()










import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
import re
import base64
import ast
from collections import Counter, defaultdict
import io
import json
from typing import Optional, Dict, List
import sqlite3
import hashlib
import random
import string
from datetime import datetime, timedelta
import os

# Safe imports with error handling
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False

try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="TechNova AI Nexus",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Streamlit Secrets Configuration with better error handling
def load_secrets():
    """Load secrets with proper error handling"""
    try:
        return {
            'OPENAI_API_KEY': st.secrets.get("OPENAI_API_KEY", ""),
            'STRIPE_PUBLISHABLE_KEY': st.secrets.get("STRIPE_PUBLISHABLE_KEY", ""),
            'STRIPE_SECRET_KEY': st.secrets.get("STRIPE_SECRET_KEY", ""),
            'STRIPE_MONTHLY_PRICE_ID': st.secrets.get("STRIPE_MONTHLY_PRICE_ID", ""),
            'STRIPE_ANNUAL_PRICE_ID': st.secrets.get("STRIPE_ANNUAL_PRICE_ID", ""),
            'BASE_URL': st.secrets.get("BASE_URL", "http://localhost:8501")
        }
    except Exception as e:
        return {
            'OPENAI_API_KEY': "",
            'STRIPE_PUBLISHABLE_KEY': "",
            'STRIPE_SECRET_KEY': "",
            'STRIPE_MONTHLY_PRICE_ID': "",
            'STRIPE_ANNUAL_PRICE_ID': "",
            'BASE_URL': "http://localhost:8501"
        }

# Load secrets
SECRETS = load_secrets()

# Initialize OpenAI client if available
openai_client = None
if OPENAI_AVAILABLE and SECRETS['OPENAI_API_KEY']:
    try:
        openai_client = openai.OpenAI(api_key=SECRETS['OPENAI_API_KEY'])
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {e}")

# Initialize Stripe if available
if STRIPE_AVAILABLE and SECRETS['STRIPE_SECRET_KEY']:
    stripe.api_key = SECRETS['STRIPE_SECRET_KEY']

# Database Setup with Migration Support
def get_db_version():
    """Get current database version"""
    try:
        conn = sqlite3.connect('technova.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='db_version'")
        if cursor.fetchone():
            cursor.execute("SELECT version FROM db_version ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()
            version = result[0] if result else 0
        else:
            version = 0
        conn.close()
        return version
    except Exception:
        return 0

def set_db_version(version):
    """Set database version"""
    try:
        conn = sqlite3.connect('technova.db', timeout=10)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS db_version (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version INTEGER NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute("INSERT INTO db_version (version) VALUES (?)", (version,))
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Error setting database version: {e}")

def migrate_database():
    """Handle database migrations"""
    current_version = get_db_version()
    target_version = 2  # Current target version
    
    if current_version >= target_version:
        return  # No migration needed
    
    try:
        conn = sqlite3.connect('technova.db', timeout=10)
        cursor = conn.cursor()
        
        # Migration from version 0 to 1: Add Stripe columns
        if current_version < 1:
            # Check if columns already exist
            cursor.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'stripe_customer_id' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN stripe_customer_id TEXT")
            
            if 'stripe_subscription_id' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN stripe_subscription_id TEXT")
            
            conn.commit()
            set_db_version(1)
        
        # Migration from version 1 to 2: Additional future migrations can go here
        if current_version < 2:
            # Future migrations
            set_db_version(2)
        
        conn.close()
        
    except Exception as e:
        st.error(f"Database migration error: {e}")

def init_database():
    """Initialize the SQLite database with error handling and migration support"""
    try:
        conn = sqlite3.connect('technova.db', timeout=10)
        cursor = conn.cursor()
        
        # Users table (complete schema)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                subscription_type TEXT DEFAULT 'free',
                subscription_expires TIMESTAMP,
                stripe_customer_id TEXT,
                stripe_subscription_id TEXT
            )
        ''')
        
        # Usage tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                tab_name TEXT,
                usage_date DATE,
                usage_count INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, tab_name, usage_date)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Run migrations
        migrate_database()
        
    except Exception as e:
        st.error(f"Database initialization error: {e}")

# Initialize database on startup
init_database()

# Authentication Functions
class AuthManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt or hashlib as fallback"""
        if BCRYPT_AVAILABLE:
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        else:
            # Fallback to hashlib with salt
            salt = os.urandom(32)
            pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            return salt.hex() + pwdhash.hex()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        try:
            if BCRYPT_AVAILABLE and hashed.startswith('$2'):
                return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
            else:
                # Fallback verification
                if len(hashed) < 64:
                    return False
                salt = bytes.fromhex(hashed[:64])
                stored_hash = hashed[64:]
                pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
                return pwdhash.hex() == stored_hash
        except Exception:
            return False
    
    @staticmethod
    def is_valid_username(username: str) -> bool:
        """Check if username is valid (alphanumeric + underscore, 3-20 chars)"""
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def create_user(username: str, password: str) -> tuple[bool, str]:
        """Create a new user account"""
        if not AuthManager.is_valid_username(username):
            return False, "Username must be 3-20 characters long and contain only letters, numbers, and underscores."
        
        try:
            conn = sqlite3.connect('technova.db', timeout=10)
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                conn.close()
                return False, "A user with this username already exists."
            
            # Hash password
            password_hash = AuthManager.hash_password(password)
            
            # Create user with 14-day free trial
            cursor.execute('''
                INSERT INTO users (username, password_hash, subscription_expires, stripe_customer_id, stripe_subscription_id)
                VALUES (?, ?, ?, NULL, NULL)
            ''', (username, password_hash, (datetime.now() + timedelta(days=14)).isoformat()))
            
            conn.commit()
            conn.close()
            
            return True, "Account created successfully! You have a 14-day free trial."
                
        except Exception as e:
            return False, f"Error creating account: {str(e)}"
    
    @staticmethod
    def login_user(username: str, password: str) -> tuple[bool, str, dict]:
        """Login user and return user info"""
        try:
            conn = sqlite3.connect('technova.db', timeout=10)
            cursor = conn.cursor()
            
            # Use safe column access with COALESCE for potentially missing columns
            cursor.execute('''
                SELECT id, password_hash, subscription_type, subscription_expires, 
                       COALESCE(stripe_customer_id, '') as stripe_customer_id,
                       COALESCE(stripe_subscription_id, '') as stripe_subscription_id
                FROM users WHERE username = ?
            ''', (username,))
            
            result = cursor.fetchone()
            if not result:
                conn.close()
                return False, "Invalid username or password.", {}
            
            user_id, password_hash, sub_type, sub_expires, stripe_customer_id, stripe_subscription_id = result
            
            if not AuthManager.verify_password(password, password_hash):
                conn.close()
                return False, "Invalid username or password.", {}
            
            # Check subscription status
            if sub_expires:
                sub_expires_dt = datetime.fromisoformat(sub_expires)
                if datetime.now() > sub_expires_dt and sub_type != 'plus':
                    # Update subscription to expired
                    cursor.execute("UPDATE users SET subscription_type = 'expired' WHERE id = ?", (user_id,))
                    conn.commit()
                    sub_type = 'expired'
            else:
                sub_expires_dt = None
            
            conn.close()
            
            user_info = {
                'id': user_id,
                'username': username,
                'subscription_type': sub_type,
                'subscription_expires': sub_expires_dt,
                'stripe_customer_id': stripe_customer_id or None,
                'stripe_subscription_id': stripe_subscription_id or None
            }
            
            return True, "Login successful!", user_info
            
        except Exception as e:
            return False, f"Login error: {str(e)}", {}

# Payment Functions
class PaymentManager:
    @staticmethod
    def create_stripe_customer(username: str) -> Optional[str]:
        """Create a Stripe customer"""
        if not STRIPE_AVAILABLE or not SECRETS['STRIPE_SECRET_KEY']:
            return None
        
        try:
            customer = stripe.Customer.create(
                metadata={'username': username}
            )
            return customer.id
        except Exception as e:
            st.error(f"Error creating Stripe customer: {e}")
            return None
    
    @staticmethod
    def create_checkout_session(user_id: int, username: str, price_id: str, plan_type: str) -> Optional[str]:
        """Create a Stripe checkout session"""
        if not STRIPE_AVAILABLE or not SECRETS['STRIPE_SECRET_KEY']:
            return None
        
        try:
            # Get or create Stripe customer
            conn = sqlite3.connect('technova.db', timeout=10)
            cursor = conn.cursor()
            cursor.execute("SELECT COALESCE(stripe_customer_id, '') FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            
            customer_id = result[0] if result and result[0] else None
            
            if not customer_id:
                customer_id = PaymentManager.create_stripe_customer(username)
                if customer_id:
                    cursor.execute("UPDATE users SET stripe_customer_id = ? WHERE id = ?", (customer_id, user_id))
                    conn.commit()
            
            conn.close()
            
            if not customer_id:
                return None
            
            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{SECRETS['BASE_URL']}?success=true&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{SECRETS['BASE_URL']}?canceled=true",
                metadata={
                    'user_id': user_id,
                    'plan_type': plan_type
                }
            )
            
            return session.url
        except Exception as e:
            st.error(f"Error creating checkout session: {e}")
            return None
    
    @staticmethod
    def handle_successful_payment(session_id: str):
        """Handle successful payment"""
        if not STRIPE_AVAILABLE or not SECRETS['STRIPE_SECRET_KEY']:
            return
        
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                user_id = int(session.metadata.get('user_id'))
                subscription_id = session.subscription
                
                # Update user subscription
                conn = sqlite3.connect('technova.db', timeout=10)
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users 
                    SET subscription_type = 'plus', 
                        stripe_subscription_id = ?,
                        subscription_expires = NULL
                    WHERE id = ?
                ''', (subscription_id, user_id))
                conn.commit()
                conn.close()
                
                st.success("Payment successful! Your TechNova Plus subscription is now active.")
        except Exception as e:
            st.error(f"Error processing payment: {e}")

# Usage Tracking Functions
class UsageManager:
    @staticmethod
    def can_use_tab(user_id: int, tab_name: str) -> tuple[bool, str]:
        """Check if user can use a specific tab"""
        try:
            conn = sqlite3.connect('technova.db', timeout=10)
            cursor = conn.cursor()
            
            # Check user subscription
            cursor.execute("SELECT subscription_type FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            if not result:
                conn.close()
                return False, "User not found."
            
            sub_type = result[0]
            
            # If TechNova Plus, allow unlimited usage
            if sub_type == 'plus':
                conn.close()
                return True, ""
            
            # If expired, deny access
            if sub_type == 'expired':
                conn.close()
                return False, "Your free trial has expired. Please upgrade to TechNova Plus."
            
            # Check daily usage for free users
            today = datetime.now().date().isoformat()
            cursor.execute('''
                SELECT usage_count FROM usage_logs 
                WHERE user_id = ? AND tab_name = ? AND usage_date = ?
            ''', (user_id, tab_name, today))
            
            result = cursor.fetchone()
            usage_count = result[0] if result else 0
            
            conn.close()
            
            if usage_count >= 4:
                return False, f"Daily limit reached for {tab_name}. You have used 4/4 attempts today."
            
            return True, ""
            
        except Exception as e:
            return False, f"Error checking usage: {str(e)}"
    
    @staticmethod
    def log_usage(user_id: int, tab_name: str):
        """Log tab usage for a user"""
        try:
            conn = sqlite3.connect('technova.db', timeout=10)
            cursor = conn.cursor()
            
            today = datetime.now().date().isoformat()
            cursor.execute('''
                INSERT OR REPLACE INTO usage_logs (user_id, tab_name, usage_date, usage_count)
                VALUES (?, ?, ?, COALESCE((SELECT usage_count FROM usage_logs 
                                         WHERE user_id = ? AND tab_name = ? AND usage_date = ?), 0) + 1)
            ''', (user_id, tab_name, today, user_id, tab_name, today))
            
            conn.commit()
            conn.close()
        except Exception as e:
            st.error(f"Error logging usage: {str(e)}")
    
    @staticmethod
    def get_usage_stats(user_id: int) -> dict:
        """Get usage statistics for a user"""
        try:
            conn = sqlite3.connect('technova.db', timeout=10)
            cursor = conn.cursor()
            
            today = datetime.now().date().isoformat()
            cursor.execute('''
                SELECT tab_name, usage_count FROM usage_logs 
                WHERE user_id = ? AND usage_date = ?
            ''', (user_id, today))
            
            results = cursor.fetchall()
            conn.close()
            return {tab: count for tab, count in results}
            
        except Exception as e:
            return {}

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Handle payment success from URL parameters
query_params = st.query_params
if 'success' in query_params and 'session_id' in query_params:
    PaymentManager.handle_successful_payment(query_params['session_id'])
    # Clear query parameters
    st.query_params.clear()

# Styling
def set_tech_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;500&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #00f9ff;
        font-family: 'Rajdhani', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', monospace !important;
        color: #00f9ff !important;
        text-shadow: 0 0 10px rgba(0, 249, 255, 0.5);
    }
    
    .main-title {
        font-size: 3rem;
        text-align: center;
        background: linear-gradient(45deg, #00f9ff, #0099cc, #66ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 2rem 0;
    }
    
    .auth-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        border: 1px solid rgba(0, 249, 255, 0.3);
        border-radius: 10px;
        background: rgba(0, 20, 40, 0.5);
    }
    
    .usage-warning {
        background: rgba(255, 193, 7, 0.1);
        border: 1px solid #ffc107;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    
    .subscription-info {
        background: rgba(0, 249, 255, 0.1);
        border: 1px solid rgba(0, 249, 255, 0.3);
        border-radius: 5px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .payment-card {
        background: rgba(0, 249, 255, 0.05);
        border: 1px solid rgba(0, 249, 255, 0.2);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
    }
    
    .stTextArea textarea, .stTextInput input {
        background: rgba(0, 20, 40, 0.8) !important;
        border: 1px solid rgba(0, 249, 255, 0.3) !important;
        color: #00f9ff !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3)) !important;
        border: 1px solid rgba(0, 249, 255, 0.5) !important;
        color: #00f9ff !important;
        font-weight: bold !important;
    }
    
    .tab-content {
        background: rgba(0, 20, 40, 0.3);
        border: 1px solid rgba(0, 249, 255, 0.2);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .result-box {
        background: rgba(0, 20, 40, 0.6);
        border: 1px solid rgba(0, 249, 255, 0.3);
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        white-space: pre-wrap;
    }
    </style>
    """, unsafe_allow_html=True)

set_tech_styling()

# Authentication Pages
def login_page():
    st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            st.subheader("🔐 Login")
            
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password")
            
            col_login, col_signup = st.columns(2)
            
            with col_login:
                if st.button("Login", use_container_width=True):
                    if username and password:
                        success, message, user_info = AuthManager.login_user(username, password)
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.user_info = user_info
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("Please enter both username and password.")
            
            with col_signup:
                if st.button("Sign Up", use_container_width=True):
                    st.session_state.page = 'signup'
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

def signup_page():
    st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            st.subheader("📝 Create TechNova Account")
            
            username = st.text_input("Username", placeholder="Choose a username (3-20 characters)")
            st.caption("Username can contain letters, numbers, and underscores only")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            col_create, col_back = st.columns(2)
            
            with col_create:
                if st.button("Create Account", use_container_width=True):
                    if not username or not password or not confirm_password:
                        st.error("Please fill in all fields.")
                    elif password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters long.")
                    else:
                        success, message = AuthManager.create_user(username, password)
                        if success:
                            st.success(message)
                            st.balloons()
                            st.session_state.page = 'login'
                            st.rerun()
                        else:
                            st.error(message)
            
            with col_back:
                if st.button("Back to Login", use_container_width=True):
                    st.session_state.page = 'login'
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

# Subscription Management
def show_subscription_info():
    """Display subscription information and usage stats"""
    user_info = st.session_state.user_info
    sub_type = user_info.get('subscription_type', 'free')
    
    if sub_type == 'free':
        sub_expires = user_info.get('subscription_expires')
        if sub_expires:
            days_left = (sub_expires - datetime.now()).days
            st.markdown(f"""
            <div class="subscription-info">
                <strong>🆓 Free Trial</strong><br>
                Days remaining: <strong>{max(0, days_left)} days</strong><br>
                Daily limit: <strong>4 uses per tab</strong>
            </div>
            """, unsafe_allow_html=True)
    elif sub_type == 'plus':
        st.markdown("""
        <div class="subscription-info">
            <strong>⭐ TechNova Plus</strong><br>
            Status: <strong>Active</strong><br>
            Usage: <strong>Unlimited</strong>
        </div>
        """, unsafe_allow_html=True)
    elif sub_type == 'expired':
        st.markdown("""
        <div class="usage-warning">
            <strong>⚠️ Trial Expired</strong><br>
            Please upgrade to TechNova Plus to continue using the service.
        </div>
        """, unsafe_allow_html=True)
        
        # Show upgrade options
        if STRIPE_AVAILABLE and SECRETS['STRIPE_SECRET_KEY']:
            st.subheader("Upgrade to TechNova Plus")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="payment-card">
                    <h4>Monthly Plan</h4>
                    <h3>$15/month</h3>
                    <p>• Unlimited usage<br>
                    • All features<br>
                    • Cancel anytime</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Subscribe Monthly", key="monthly", use_container_width=True):
                    if SECRETS['STRIPE_MONTHLY_PRICE_ID']:
                        url = PaymentManager.create_checkout_session(
                            user_info['id'], 
                            user_info['username'], 
                            SECRETS['STRIPE_MONTHLY_PRICE_ID'], 
                            'monthly'
                        )
                        if url:
                            st.markdown(f'<meta http-equiv="refresh" content="0;url={url}">', unsafe_allow_html=True)
                    else:
                        st.error("Monthly price ID not configured")
            
            with col2:
                st.markdown("""
                <div class="payment-card">
                    <h4>Annual Plan</h4>
                    <h3>$150/year</h3>
                    <p>• Save 30%<br>
                    • Unlimited usage<br>
                    • All features</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Subscribe Annually", key="annual", use_container_width=True):
                    if SECRETS['STRIPE_ANNUAL_PRICE_ID']:
                        url = PaymentManager.create_checkout_session(
                            user_info['id'], 
                            user_info['username'], 
                            SECRETS['STRIPE_ANNUAL_PRICE_ID'], 
                            'annual'
                        )
                        if url:
                            st.markdown(f'<meta http-equiv="refresh" content="0;url={url}">', unsafe_allow_html=True)
                    else:
                        st.error("Annual price ID not configured")
        else:
            st.info("Payment system not configured. Contact administrator for upgrade options.")
    
    # Show daily usage stats
    usage_stats = UsageManager.get_usage_stats(user_info['id'])
    if usage_stats and sub_type == 'free':
        st.write("**Today's Usage:**")
        for tab, count in usage_stats.items():
            st.write(f"• {tab}: {count}/4 uses")

def check_tab_access(tab_name: str) -> bool:
    """Check if user can access a tab and show appropriate message"""
    user_id = st.session_state.user_info['id']
    can_use, message = UsageManager.can_use_tab(user_id, tab_name)
    
    if not can_use:
        st.error(message)
        return False
    
    return True

def log_tab_usage(tab_name: str):
    """Log usage for a tab"""
    user_id = st.session_state.user_info['id']
    UsageManager.log_usage(user_id, tab_name)

# Utility Functions
def copy_button(text: str, label: str = "Copy", key: str = None):
    """Enhanced copy button with better error handling"""
    if text is None:
        text = ""
    
    import html
    escaped_text = html.escape(str(text))
    button_key = f"copy_btn_{key}" if key else f"copy_btn_{abs(hash(str(text)[:50]))}"
    
    copy_html = f"""
    <div style="margin: 10px 0;">
        <button onclick="copyToClipboard_{button_key}()" 
                style="background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3));
                       border: 1px solid rgba(0, 249, 255, 0.5);
                       color: #00f9ff;
                       padding: 8px 16px;
                       border-radius: 5px;
                       cursor: pointer;
                       font-weight: bold;">
            📋 {label}
        </button>
    </div>
    
    <script>
    function copyToClipboard_{button_key}() {{
        const text = `{escaped_text}`;
        navigator.clipboard.writeText(text).then(function() {{
            console.log('Text copied to clipboard');
        }}).catch(function(err) {{
            console.error('Could not copy text: ', err);
        }});
    }}
    </script>
    """
    
    components.html(copy_html, height=50)

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    if not PDF_AVAILABLE:
        return "PDF processing not available. Please install PyPDF2."
    
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def get_openai_response(prompt: str, system_prompt: str = "") -> str:
    """Get response from OpenAI API using the new client interface"""
    if not OPENAI_AVAILABLE or not openai_client:
        return "OpenAI API not configured. Please add your API key to the secrets."
    
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"

def scrape_website(url: str) -> str:
    """Scrape text content from a website"""
    try:
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:5000]  # Limit to first 5000 characters
        
    except requests.RequestException as e:
        return f"Error scraping website: {str(e)}"
    except Exception as e:
        return f"Error processing website content: {str(e)}"

# AI Tool Functions
def text_summarizer_tab():
    """Text Summarization Tool"""
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.subheader("📄 Text Summarizer")
    st.write("Summarize long texts, articles, or documents into concise summaries.")
    
    # Check access
    if not check_tab_access("Text Summarizer"):
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Input options
    input_method = st.radio("Choose input method:", ["Text Input", "Upload PDF", "Website URL"])
    
    text_to_summarize = ""
    
    if input_method == "Text Input":
        text_to_summarize = st.text_area("Enter text to summarize:", height=200, 
                                       placeholder="Paste your text here...")
    
    elif input_method == "Upload PDF":
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file is not None:
            with st.spinner("Extracting text from PDF..."):
                text_to_summarize = extract_text_from_pdf(uploaded_file)
                if text_to_summarize and not text_to_summarize.startswith("Error"):
                    st.success(f"Extracted {len(text_to_summarize)} characters from PDF")
                else:
                    st.error(text_to_summarize)
    
    elif input_method == "Website URL":
        url = st.text_input("Enter website URL:", placeholder="https://example.com/article")
        if url and st.button("Fetch Content"):
            with st.spinner("Scraping website content..."):
                text_to_summarize = scrape_website(url)
                if text_to_summarize and not text_to_summarize.startswith("Error"):
                    st.success(f"Scraped {len(text_to_summarize)} characters from website")
                    st.text_area("Scraped content preview:", text_to_summarize[:500] + "...", height=100)
                else:
                    st.error(text_to_summarize)
    
    # Summary options
    col1, col2 = st.columns(2)
    with col1:
        summary_length = st.selectbox("Summary length:", ["Short", "Medium", "Long"])
    with col2:
        summary_style = st.selectbox("Summary style:", ["Bullet Points", "Paragraph", "Key Insights"])
    
    if st.button("Generate Summary", use_container_width=True) and text_to_summarize:
        if len(text_to_summarize.strip()) < 100:
            st.error("Please provide more text (at least 100 characters) for summarization.")
        else:
            with st.spinner("Generating summary..."):
                length_map = {"Short": "in 2-3 sentences", "Medium": "in 1-2 paragraphs", "Long": "in 3-4 paragraphs"}
                style_map = {
                    "Bullet Points": "as bullet points highlighting key information",
                    "Paragraph": "in well-structured paragraphs",
                    "Key Insights": "focusing on key insights and main takeaways"
                }
                
                prompt = f"Summarize the following text {length_map[summary_length]} {style_map[summary_style]}:\n\n{text_to_summarize}"
                
                summary = get_openai_response(prompt, "You are a helpful assistant specialized in creating clear, concise summaries.")
                
                if summary:
                    log_tab_usage("Text Summarizer")
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.write("**Summary:**")
                    st.write(summary)
                    st.markdown('</div>', unsafe_allow_html=True)
                    copy_button(summary, "Copy Summary", "summary")
                else:
                    st.error("Failed to generate summary. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def code_generator_tab():
    """Code Generation Tool"""
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.subheader("💻 Code Generator")
    st.write("Generate code snippets in various programming languages based on your requirements.")
    
    if not check_tab_access("Code Generator"):
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        language = st.selectbox("Programming Language:", [
            "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", 
            "PHP", "Ruby", "Swift", "Kotlin", "TypeScript", "HTML/CSS"
        ])
    
    with col2:
        code_type = st.selectbox("Code Type:", [
            "Function", "Class", "Algorithm", "Web Component", "API Endpoint",
            "Database Query", "Script", "Utility", "Data Structure"
        ])
    
    description = st.text_area("Describe what you want the code to do:", 
                              height=150, 
                              placeholder="Example: Create a function that calculates the fibonacci sequence up to n terms")
    
    # Advanced options
    with st.expander("Advanced Options"):
        include_comments = st.checkbox("Include detailed comments", value=True)
        include_examples = st.checkbox("Include usage examples", value=True)
        code_style = st.selectbox("Code Style:", ["Standard", "Clean/Minimal", "Detailed/Verbose"])
    
    if st.button("Generate Code", use_container_width=True) and description:
        with st.spinner("Generating code..."):
            system_prompt = f"""You are an expert programmer. Generate clean, efficient, and well-structured {language} code.
            Always include proper error handling where appropriate.
            Code style preference: {code_style}
            {"Include detailed comments explaining the code." if include_comments else "Include minimal comments."}
            {"Include usage examples after the main code." if include_examples else ""}"""
            
            prompt = f"Generate a {code_type.lower()} in {language} that {description}"
            
            code = get_openai_response(prompt, system_prompt)
            
            if code:
                log_tab_usage("Code Generator")
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.write(f"**Generated {language} Code:**")
                st.code(code, language=language.lower())
                st.markdown('</div>', unsafe_allow_html=True)
                copy_button(code, "Copy Code", "code")
            else:
                st.error("Failed to generate code. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def content_writer_tab():
    """Content Writing Tool"""
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.subheader("✍️ Content Writer")
    st.write("Create engaging content for blogs, social media, marketing, and more.")
    
    if not check_tab_access("Content Writer"):
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    content_type = st.selectbox("Content Type:", [
        "Blog Post", "Social Media Post", "Product Description", "Email Newsletter",
        "Press Release", "Article", "Advertisement Copy", "Website Copy", "Essay"
    ])
    
    col1, col2 = st.columns(2)
    
    with col1:
        tone = st.selectbox("Tone:", [
            "Professional", "Casual", "Friendly", "Formal", "Persuasive",
            "Humorous", "Inspirational", "Technical", "Creative"
        ])
    
    with col2:
        length = st.selectbox("Length:", [
            "Short (100-200 words)", "Medium (300-500 words)", 
            "Long (600-1000 words)", "Extended (1000+ words)"
        ])
    
    topic = st.text_input("Topic/Subject:", placeholder="Enter the main topic or subject")
    
    additional_details = st.text_area("Additional Details/Requirements:", 
                                    height=100,
                                    placeholder="Any specific points to cover, target audience, keywords, etc.")
    
    # Advanced options
    with st.expander("Advanced Options"):
        target_audience = st.text_input("Target Audience:", placeholder="e.g., young professionals, tech enthusiasts")
        keywords = st.text_input("Keywords to Include:", placeholder="Comma-separated keywords")
        call_to_action = st.text_input("Call to Action:", placeholder="What should readers do after reading?")
    
    if st.button("Generate Content", use_container_width=True) and topic:
        with st.spinner("Creating content..."):
            length_map = {
                "Short (100-200 words)": "100-200 words",
                "Medium (300-500 words)": "300-500 words", 
                "Long (600-1000 words)": "600-1000 words",
                "Extended (1000+ words)": "1000+ words"
            }
            
            system_prompt = f"""You are a professional content writer specializing in creating engaging, high-quality content.
            Write in a {tone.lower()} tone and make the content compelling and well-structured.
            Always include proper headings, subheadings, and formatting where appropriate."""
            
            prompt_parts = [
                f"Write a {content_type.lower()} about {topic}",
                f"Length: {length_map[length]}",
                f"Tone: {tone}"
            ]
            
            if additional_details:
                prompt_parts.append(f"Additional requirements: {additional_details}")
            if target_audience:
                prompt_parts.append(f"Target audience: {target_audience}")
            if keywords:
                prompt_parts.append(f"Include these keywords naturally: {keywords}")
            if call_to_action:
                prompt_parts.append(f"Include this call to action: {call_to_action}")
            
            prompt = "\n".join(prompt_parts)
            
            content = get_openai_response(prompt, system_prompt)
            
            if content:
                log_tab_usage("Content Writer")
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.write(f"**Generated {content_type}:**")
                st.markdown(content)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Word count
                word_count = len(content.split())
                st.info(f"Word count: {word_count}")
                
                copy_button(content, "Copy Content", "content")
            else:
                st.error("Failed to generate content. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def data_analyzer_tab():
    """Data Analysis Tool"""
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.subheader("📊 Data Analyzer")
    st.write("Analyze data patterns, generate insights, and create simple visualizations.")
    
    if not check_tab_access("Data Analyzer"):
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    analysis_type = st.selectbox("Analysis Type:", [
        "Statistical Summary", "Pattern Recognition", "Trend Analysis",
        "Comparative Analysis", "Data Interpretation", "Insights Generation"
    ])
    
    # Data input options
    data_input_method = st.radio("Data Input Method:", ["Paste Data", "Upload CSV"])
    
    data_text = ""
    
    if data_input_method == "Paste Data":
        data_text = st.text_area("Paste your data here:", 
                                height=200,
                                placeholder="Enter your data (CSV format, JSON, or any structured format)")
    
    elif data_input_method == "Upload CSV":
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            try:
                df_preview = pd.read_csv(uploaded_file, nrows=5)
                st.write("**Data Preview:**")
                st.dataframe(df_preview)
                
                # Convert to string for analysis
                full_df = pd.read_csv(uploaded_file)
                data_text = full_df.to_string()
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
    
    # Analysis options
    with st.expander("Analysis Options"):
        focus_areas = st.multiselect("Focus Areas:", [
            "Trends", "Outliers", "Correlations", "Distributions", 
            "Missing Data", "Key Metrics", "Comparisons", "Predictions"
        ])
        
        specific_questions = st.text_area("Specific Questions:", 
                                        placeholder="What specific insights are you looking for?")
    
    if st.button("Analyze Data", use_container_width=True) and data_text:
        with st.spinner("Analyzing data..."):
            system_prompt = """You are a data analyst expert. Analyze the provided data and provide clear, 
            actionable insights. Include statistical observations, patterns, and recommendations where appropriate.
            Format your response with clear sections and bullet points for readability."""
            
            prompt_parts = [
                f"Perform a {analysis_type.lower()} on the following data:",
                data_text[:3000],  # Limit data size
            ]
            
            if focus_areas:
                prompt_parts.append(f"Focus particularly on: {', '.join(focus_areas)}")
            
            if specific_questions:
                prompt_parts.append(f"Address these specific questions: {specific_questions}")
            
            prompt_parts.append("Provide actionable insights and recommendations based on your analysis.")
            
            prompt = "\n\n".join(prompt_parts)
            
            analysis = get_openai_response(prompt, system_prompt)
            
            if analysis:
                log_tab_usage("Data Analyzer")
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.write("**Data Analysis Results:**")
                st.markdown(analysis)
                st.markdown('</div>', unsafe_allow_html=True)
                copy_button(analysis, "Copy Analysis", "analysis")
            else:
                st.error("Failed to analyze data. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def language_translator_tab():
    """Language Translation Tool"""
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.subheader("🌍 Language Translator")
    st.write("Translate text between different languages with context awareness.")
    
    if not check_tab_access("Language Translator"):
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    col1, col2 = st.columns(2)
    
    languages = [
        "Spanish", "French", "German", "Italian", "Portuguese", "Russian",
        "Chinese (Simplified)", "Chinese (Traditional)", "Japanese", "Korean",
        "Arabic", "Hindi", "Dutch", "Swedish", "Norwegian", "Danish",
        "Polish", "Turkish", "Greek", "Hebrew", "Thai", "Vietnamese"
    ]
    
    with col1:
        source_lang = st.selectbox("From Language:", ["Auto-detect"] + languages)
    
    with col2:
        target_lang = st.selectbox("To Language:", languages)
    
    text_to_translate = st.text_area("Enter text to translate:", 
                                   height=150,
                                   placeholder="Type or paste the text you want to translate...")
    
    # Translation options
    with st.expander("Translation Options"):
        translation_style = st.selectbox("Translation Style:", [
            "Standard", "Formal", "Casual", "Technical", "Literary"
        ])
        
        preserve_formatting = st.checkbox("Preserve formatting", value=True)
        include_pronunciation = st.checkbox("Include pronunciation guide (where applicable)")
    
    if st.button("Translate", use_container_width=True) and text_to_translate and target_lang:
        with st.spinner("Translating..."):
            system_prompt = f"""You are a professional translator with expertise in multiple languages.
            Provide accurate, contextually appropriate translations.
            Translation style: {translation_style}
            {'Preserve original formatting and structure.' if preserve_formatting else 'Focus on natural flow in target language.'}
            Always maintain the original meaning and tone."""
            
            source_lang_text = source_lang if source_lang != "Auto-detect" else "the source language (auto-detect)"
            
            prompt_parts = [
                f"Translate the following text from {source_lang_text} to {target_lang}:",
                text_to_translate
            ]
            
            if include_pronunciation and target_lang in ["Chinese (Simplified)", "Chinese (Traditional)", "Japanese", "Korean", "Russian", "Arabic", "Hindi", "Thai"]:
                prompt_parts.append(f"Also include pronunciation guide in Latin characters.")
            
            prompt = "\n\n".join(prompt_parts)
            
            translation = get_openai_response(prompt, system_prompt)
            
            if translation:
                log_tab_usage("Language Translator")
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.write(f"**Translation ({target_lang}):**")
                st.write(translation)
                st.markdown('</div>', unsafe_allow_html=True)
                
                copy_button(translation, "Copy Translation", "translation")
                
                # Character count info
                char_count = len(text_to_translate)
                st.info(f"Translated {char_count} characters")
            else:
                st.error("Failed to translate text. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def email_generator_tab():
    """Email Generation Tool"""
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.subheader("📧 Email Generator")
    st.write("Generate professional emails for various purposes and situations.")
    
    if not check_tab_access("Email Generator"):
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    email_type = st.selectbox("Email Type:", [
        "Business Inquiry", "Follow-up", "Thank You", "Apology", "Request",
        "Introduction", "Resignation", "Complaint", "Invitation", "Newsletter",
        "Sales Pitch", "Meeting Request", "Feedback Request", "Custom"
    ])
    
    col1, col2 = st.columns(2)
    
    with col1:
        tone = st.selectbox("Tone:", [
            "Professional", "Formal", "Friendly", "Casual", "Persuasive",
            "Apologetic", "Enthusiastic", "Diplomatic"
        ])
    
    with col2:
        urgency = st.selectbox("Urgency Level:", [
            "Low", "Normal", "High", "Urgent"
        ])
    
    # Email details
    recipient = st.text_input("Recipient Name:", placeholder="John Smith")
    subject_hint = st.text_input("Subject Line Hint:", placeholder="What is the email about?")
    
    main_purpose = st.text_area("Main Purpose/Content:", 
                               height=120,
                               placeholder="Describe the main purpose of the email and key points to cover...")
    
    # Additional options
    with st.expander("Additional Options"):
        sender_name = st.text_input("Your Name:", placeholder="Your name for signature")
        company = st.text_input("Company/Organization:", placeholder="Optional")
        include_call_to_action = st.checkbox("Include call to action", value=True)
        email_length = st.selectbox("Email Length:", ["Short", "Medium", "Long"])
    
    if st.button("Generate Email", use_container_width=True) and main_purpose:
        with st.spinner("Generating email..."):
            system_prompt = f"""You are a professional email writing assistant. Generate well-structured, 
            appropriate emails with proper formatting, subject lines, and signatures.
            Tone: {tone}
            Urgency: {urgency}
            Always include a subject line, greeting, body, and professional closing."""
            
            prompt_parts = [
                f"Generate a {email_type.lower()} email with the following details:",
                f"Purpose: {main_purpose}"
            ]
            
            if recipient:
                prompt_parts.append(f"Recipient: {recipient}")
            if subject_hint:
                prompt_parts.append(f"Subject should relate to: {subject_hint}")
            if sender_name:
                prompt_parts.append(f"Sender name: {sender_name}")
            if company:
                prompt_parts.append(f"Company/Organization: {company}")
            
            length_instructions = {
                "Short": "Keep it concise and to the point",
                "Medium": "Provide adequate detail and context", 
                "Long": "Include comprehensive details and background"
            }
            prompt_parts.append(length_instructions[email_length])
            
            if include_call_to_action:
                prompt_parts.append("Include an appropriate call to action")
            
            prompt = "\n".join(prompt_parts)
            
            email = get_openai_response(prompt, system_prompt)
            
            if email:
                log_tab_usage("Email Generator")
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.write("**Generated Email:**")
                st.text(email)
                st.markdown('</div>', unsafe_allow_html=True)
                copy_button(email, "Copy Email", "email")
            else:
                st.error("Failed to generate email. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main Application Logic
def main_app():
    """Main application with tabs"""
    st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
    
    # User info and logout
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write(f"**Welcome, {st.session_state.user_info['username']}!**")
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_info = {}
            st.rerun()
    
    # Subscription info
    show_subscription_info()
    
    # Main tabs
    tabs = st.tabs([
        "📄 Text Summarizer",
        "💻 Code Generator", 
        "✍️ Content Writer",
        "📊 Data Analyzer",
        "🌍 Language Translator",
        "📧 Email Generator"
    ])
    
    with tabs[0]:
        text_summarizer_tab()
    
    with tabs[1]:
        code_generator_tab()
    
    with tabs[2]:
        content_writer_tab()
    
    with tabs[3]:
        data_analyzer_tab()
    
    with tabs[4]:
        language_translator_tab()
    
    with tabs[5]:
        email_generator_tab()

# Application Router
def main():
    """Main application router"""
    
    # Authentication check
    if not st.session_state.authenticated:
        if st.session_state.page == 'signup':
            signup_page()
        else:
            login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
