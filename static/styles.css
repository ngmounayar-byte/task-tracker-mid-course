:root {
  font-family: Inter, system-ui, sans-serif;
  color: #172033;
  background: #f5f7fb;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  min-height: 100vh;
}

button, input, select, textarea {
  font: inherit;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem clamp(1rem, 4vw, 4rem);
  background: white;
  border-bottom: 1px solid #dfe5ef;
  gap: 1rem;
}

h1, h2, p { margin-top: 0; }

.eyebrow {
  margin-bottom: .3rem;
  text-transform: uppercase;
  letter-spacing: .12em;
  font-size: .75rem;
  font-weight: 700;
}

.subtitle {
  margin-bottom: 0;
  color: #667085;
}

main {
  padding: 1.5rem clamp(1rem, 4vw, 4rem) 3rem;
}

.toolbar {
  display: flex;
  align-items: end;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1.25rem;
}

label {
  display: grid;
  gap: .4rem;
  font-weight: 600;
}

input, select, textarea {
  width: 100%;
  border: 1px solid #cbd5e1;
  border-radius: .65rem;
  padding: .7rem .8rem;
  background: white;
}

.toolbar input, .toolbar select {
  min-width: 180px;
}

button {
  border: 0;
  border-radius: .65rem;
  padding: .72rem 1rem;
  cursor: pointer;
  font-weight: 700;
}

.primary {
  background: #1f5eff;
  color: white;
}

.secondary {
  background: #e9eef8;
  color: #27364d;
}

.danger {
  background: #fee2e2;
  color: #b42318;
}

.board {
  display: grid;
  grid-template-columns: repeat(3, minmax(240px, 1fr));
  gap: 1rem;
}

.column {
  background: #edf1f7;
  border-radius: 1rem;
  padding: 1rem;
  min-height: 360px;
}

.column h2 {
  font-size: 1rem;
  display: flex;
  justify-content: space-between;
}

.card {
  background: white;
  border: 1px solid #dfe5ef;
  border-radius: .85rem;
  padding: .9rem;
  margin-bottom: .8rem;
  box-shadow: 0 2px 8px rgba(31, 41, 55, .05);
  cursor: pointer;
}

.card h3 {
  margin: 0 0 .4rem;
  font-size: 1rem;
}

.card p {
  color: #667085;
  font-size: .9rem;
  margin-bottom: .7rem;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: .4rem;
  font-size: .78rem;
}

.badge, .tag {
  border-radius: 999px;
  padding: .25rem .5rem;
  background: #eef2ff;
}

.overdue {
  background: #fee2e2;
  color: #b42318;
  font-weight: 700;
}

dialog {
  width: min(680px, calc(100% - 2rem));
  border: 0;
  border-radius: 1rem;
  padding: 0;
}

dialog::backdrop {
  background: rgba(17, 24, 39, .55);
}

form {
  padding: 1.25rem;
  display: grid;
  gap: 1rem;
}

.dialog-header, .dialog-actions {
  display: flex;
  align-items: center;
  gap: .75rem;
}

.dialog-header {
  justify-content: space-between;
}

.icon-button {
  background: transparent;
  font-size: 1.6rem;
  padding: .2rem .5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.spacer { flex: 1; }

.hidden { display: none; }

.error {
  color: #b42318;
  min-height: 1.2rem;
  margin-bottom: 0;
}

small {
  color: #667085;
  font-weight: 400;
}

.empty {
  color: #667085;
  text-align: center;
  padding: 2rem .5rem;
}

@media (max-width: 850px) {
  .board { grid-template-columns: 1fr; }
}

@media (max-width: 560px) {
  .app-header {
    align-items: flex-start;
    flex-direction: column;
  }
  .form-grid { grid-template-columns: 1fr; }
}
